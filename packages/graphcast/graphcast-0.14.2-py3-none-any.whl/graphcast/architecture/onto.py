"""Core ontology and data structures for graph database operations.

This module defines the fundamental data structures and types used throughout the graphcast
package for working with graph databases. It provides:

- Core data types for vertices and edges
- Database index configurations
- Graph container implementations
- Edge mapping and casting utilities
- Action context for graph transformations

The module is designed to be database-agnostic, supporting both ArangoDB and Neo4j through
the DBFlavor enum. It provides a unified interface for working with graph data structures
while allowing for database-specific optimizations and features.

Key Components:
    - EdgeMapping: Defines how edges are mapped between vertices
    - IndexType: Supported database index types
    - EdgeType: Types of edge handling in the graph database
    - GraphContainer: Main container for graph data
    - ActionContext: Context for graph transformation operations

Example:
    >>> container = GraphContainer(vertices={}, edges={}, linear=[])
    >>> index = Index(fields=["name", "age"], type=IndexType.PERSISTENT)
    >>> context = ActionContext()
"""

from __future__ import annotations

import dataclasses
import logging
from abc import ABCMeta
from collections import defaultdict
from typing import Any, Optional, Union

from graphcast.onto import BaseDataclass, BaseEnum, DBFlavor
from graphcast.util.transform import pick_unique_dict

SOURCE_AUX = "__source"
TARGET_AUX = "__target"
DISCRIMINANT_KEY = "__discriminant_key"

# type for vertex or edge name (index)
EdgeId = tuple[str, str, Optional[str]]
GraphEntity = Union[str, EdgeId]

logger = logging.getLogger(__name__)


class EdgeMapping(BaseEnum):
    """Defines how edges are mapped between vertices.

    ALL: Maps all vertices to all vertices
    ONE_N: Maps one vertex to many vertices
    """

    ALL = "all"
    ONE_N = "1-n"


class EncodingType(BaseEnum):
    """Supported character encodings for data input/output."""

    ISO_8859 = "ISO-8859-1"
    UTF_8 = "utf-8"


class IndexType(BaseEnum):
    """Types of database indexes supported.

    PERSISTENT: Standard persistent index
    HASH: Hash-based index for fast lookups
    SKIPLIST: Sorted index using skip list data structure
    FULLTEXT: Index optimized for text search
    """

    PERSISTENT = "persistent"
    HASH = "hash"
    SKIPLIST = "skiplist"
    FULLTEXT = "fulltext"


class EdgeType(BaseEnum):
    """Defines how edges are handled in the graph database.

    INDIRECT: Defined as a collection with indexes, may be used after data ingestion
    DIRECT: In addition to indexes, these edges are generated during ingestion
    """

    INDIRECT = "indirect"
    DIRECT = "direct"


@dataclasses.dataclass
class ABCFields(BaseDataclass, metaclass=ABCMeta):
    """Abstract base class for entities that have fields.

    Attributes:
        name: Optional name of the entity
        fields: List of field names
    """

    name: Optional[str] = None
    fields: list[str] = dataclasses.field(default_factory=list)

    def cfield(self, x: str) -> str:
        """Creates a composite field name by combining the entity name with a field name.

        Args:
            x: Field name to combine with entity name

        Returns:
            Composite field name in format "entity@field"
        """
        return f"{self.name}@{x}"


@dataclasses.dataclass
class Weight(ABCFields):
    """Defines weight configuration for edges.

    Attributes:
        discriminant: Optional field used to discriminate between weights
        map: Dictionary mapping field values to weights
        filter: Dictionary of filter conditions for weights
    """

    discriminant: Optional[str] = None
    map: dict = dataclasses.field(default_factory=dict)
    filter: dict = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class Index(BaseDataclass):
    """Configuration for database indexes.

    Attributes:
        name: Optional name of the index
        fields: List of fields to index
        unique: Whether the index enforces uniqueness
        type: Type of index to create
        deduplicate: Whether to deduplicate index entries
        sparse: Whether to create a sparse index
        exclude_edge_endpoints: Whether to exclude edge endpoints from index
    """

    name: str | None = None
    fields: list[str] = dataclasses.field(default_factory=list)
    unique: bool = True
    type: IndexType = IndexType.PERSISTENT
    deduplicate: bool = True
    sparse: bool = False
    exclude_edge_endpoints: bool = False

    def __iter__(self):
        """Iterate over the indexed fields."""
        return iter(self.fields)

    def db_form(self, db_type: DBFlavor) -> dict:
        """Convert index configuration to database-specific format.

        Args:
            db_type: Type of database (ARANGO or NEO4J)

        Returns:
            Dictionary of index configuration in database-specific format

        Raises:
            ValueError: If db_type is not supported
        """
        r = self.to_dict()
        if db_type == DBFlavor.ARANGO:
            _ = r.pop("name")
            _ = r.pop("exclude_edge_endpoints")
        elif db_type == DBFlavor.NEO4J:
            pass
        else:
            raise ValueError(f"Unknown db_type {db_type}")

        return r


class ItemsView:
    """View class for iterating over vertices and edges in a GraphContainer."""

    def __init__(self, gc: GraphContainer):
        self._dictlike = gc

    def __iter__(self):
        """Iterate over vertices and edges in the container."""
        for key in self._dictlike.vertices:
            yield key, self._dictlike.vertices[key]
        for key in self._dictlike.edges:
            yield key, self._dictlike.edges[key]


@dataclasses.dataclass
class GraphContainer(BaseDataclass):
    """Container for graph data including vertices and edges.

    Attributes:
        vertices: Dictionary mapping vertex names to lists of vertex data
        edges: Dictionary mapping edge IDs to lists of edge data
        linear: List of default dictionaries containing linear data
    """

    vertices: dict[str, list]
    edges: dict[tuple[str, str, str | None], list]
    linear: list[defaultdict[str | tuple[str, str, str | None], list[Any]]]

    def __post_init__(self):
        pass

    def items(self):
        """Get an ItemsView of the container's contents."""
        return ItemsView(self)

    def pick_unique(self):
        """Remove duplicate entries from vertices and edges."""
        for k, v in self.vertices.items():
            self.vertices[k] = pick_unique_dict(v)
        for k, v in self.edges.items():
            self.edges[k] = pick_unique_dict(v)

    def loop_over_relations(self, edge_def: tuple[str, str, str | None]):
        """Iterate over edges matching the given edge definition.

        Args:
            edge_def: Tuple of (source, target, optional_purpose)

        Returns:
            Generator yielding matching edge IDs
        """
        source, target, _ = edge_def
        return (ed for ed in self.edges if source == ed[0] and target == ed[1])

    @classmethod
    def from_docs_list(
        cls, list_default_dicts: list[defaultdict[GraphEntity, list]]
    ) -> GraphContainer:
        """Create a GraphContainer from a list of default dictionaries.

        Args:
            list_default_dicts: List of default dictionaries containing vertex and edge data

        Returns:
            New GraphContainer instance

        Raises:
            AssertionError: If edge IDs are not properly formatted
        """
        vdict: defaultdict[str, list] = defaultdict(list)
        edict: defaultdict[tuple[str, str, str | None], list] = defaultdict(list)

        for d in list_default_dicts:
            for k, v in d.items():
                if isinstance(k, str):
                    vdict[k].extend(v)
                elif isinstance(k, tuple):
                    assert (
                        len(k) == 3
                        and all(isinstance(item, str) for item in k[:-1])
                        and isinstance(k[-1], (str, type(None)))
                    )
                    edict[k].extend(v)
        return GraphContainer(
            vertices=dict(vdict.items()),
            edges=dict(edict.items()),
            linear=list_default_dicts,
        )


class EdgeCastingType(BaseEnum):
    """Types of edge casting supported.

    PAIR_LIKE: Edges are cast as pairs of vertices
    PRODUCT_LIKE: Edges are cast as products of vertex sets
    """

    PAIR_LIKE = "pair"
    PRODUCT_LIKE = "product"


def inner_factory_vertex() -> defaultdict[Optional[str], list]:
    """Create a default dictionary for vertex data."""
    return defaultdict(list)


def outer_factory() -> defaultdict[str, defaultdict[Optional[str], list]]:
    """Create a nested default dictionary for vertex data."""
    return defaultdict(inner_factory_vertex)


def dd_factory() -> defaultdict[GraphEntity, list]:
    """Create a default dictionary for graph entity data."""
    return defaultdict(list)


@dataclasses.dataclass(kw_only=True)
class ActionContext(BaseDataclass):
    """Context for graph transformation actions.

    Attributes:
        acc_v_local: Local accumulation of vertices
        acc_vertex: Global accumulation of vertices
        acc_global: Global accumulation of graph entities
        buffer_vertex: Buffer for vertex data
        cdoc: Current document being processed
    """

    acc_v_local: defaultdict[str, defaultdict[Optional[str], list]] = dataclasses.field(
        default_factory=outer_factory
    )
    acc_vertex: defaultdict[str, defaultdict[Optional[str], list]] = dataclasses.field(
        default_factory=outer_factory
    )
    acc_global: defaultdict[GraphEntity, list] = dataclasses.field(
        default_factory=dd_factory
    )
    buffer_vertex: defaultdict[GraphEntity, dict] = dataclasses.field(
        default_factory=lambda: defaultdict(dict)
    )
    cdoc: dict = dataclasses.field(default_factory=dict)
