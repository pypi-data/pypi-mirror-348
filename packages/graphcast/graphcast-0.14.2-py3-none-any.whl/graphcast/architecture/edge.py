"""Edge configuration and management for graph databases.

This module provides classes and utilities for managing edges in graph databases.
It handles edge configuration, weight management, indexing, and relationship operations.
The module supports both ArangoDB and Neo4j through the DBFlavor enum.

Key Components:
    - Edge: Represents an edge with its source, target, and configuration
    - EdgeConfig: Manages collections of edges and their configurations
    - WeightConfig: Configuration for edge weights and relationships

Example:
    >>> edge = Edge(source="user", target="post")
    >>> config = EdgeConfig(edges=[edge])
    >>> edge.finish_init(vertex_config=vertex_config)
"""

import dataclasses
from typing import Optional

from graphcast.architecture.onto import (
    BaseDataclass,
    EdgeCastingType,
    EdgeId,
    EdgeType,
    Index,
    Weight,
)
from graphcast.architecture.vertex import VertexConfig
from graphcast.onto import DBFlavor


@dataclasses.dataclass
class WeightConfig(BaseDataclass):
    """Configuration for edge weights and relationships.

    This class manages the configuration of weights and relationships for edges,
    including source and target field mappings.

    Attributes:
        source_fields: List of source vertex fields
        target_fields: List of target vertex fields
        vertices: List of weight configurations
        direct: List of direct field mappings
    """

    source_fields: list[str] = dataclasses.field(default_factory=list)
    target_fields: list[str] = dataclasses.field(default_factory=list)
    vertices: list[Weight] = dataclasses.field(default_factory=list)
    direct: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Edge(BaseDataclass):
    """Represents an edge in the graph database.

    An edge connects two vertices and can have various configurations for
    indexing, weights, and relationship types.

    Attributes:
        source: Source vertex name
        target: Target vertex name
        indexes: List of indexes for the edge
        weights: Optional weight configuration
        non_exclusive: List of non-exclusive fields
        relation: Optional relation name (for Neo4j)
        purpose: Optional purpose for utility collections
        source_discriminant: Optional source discriminant field
        target_discriminant: Optional target discriminant field
        source_relation_field: Optional source relation field
        target_relation_field: Optional target relation field
        type: Edge type (DIRECT or INDIRECT)
        aux: Whether this is an auxiliary edge
        casting_type: Type of edge casting
        by: Optional vertex name for indirect edges
        source_collection: Optional source collection name
        target_collection: Optional target collection name
        graph_name: Optional graph name
        collection_name: Optional collection name
        db_flavor: Database flavor (ARANGO or NEO4J)
    """

    source: str
    target: str
    indexes: list[Index] = dataclasses.field(default_factory=list)
    weights: Optional[WeightConfig] = None

    non_exclusive: list[str] = dataclasses.field(default_factory=list)

    # used for specifies an index (neo4j)
    relation: Optional[str] = None

    # used to create extra utility collections between the same type of vertices (A, B)
    purpose: Optional[str] = None

    source_discriminant: Optional[str] = None
    target_discriminant: Optional[str] = None

    source_relation_field: Optional[str] = None
    target_relation_field: Optional[str] = None

    type: EdgeType = EdgeType.DIRECT

    aux: bool = (
        False  # aux=True edges are init in the db but not considered by graphcast
    )

    casting_type: EdgeCastingType = EdgeCastingType.PAIR_LIKE
    by: Optional[str] = None
    source_collection: Optional[str] = None
    target_collection: Optional[str] = None
    graph_name: Optional[str] = None
    collection_name: Optional[str] = None
    db_flavor: DBFlavor = DBFlavor.ARANGO

    def __post_init__(self):
        """Initialize the edge after dataclass initialization.

        Validates that source and target relation fields are not both set.

        Raises:
            ValueError: If both source and target relation fields are set
        """
        if (
            self.source_relation_field is not None
            and self.target_relation_field is not None
        ):
            raise ValueError(
                f"Both source_relation_field and target_relation_field are set for edge ({self.source}, {self.target})"
            )

    def finish_init(self, vertex_config: VertexConfig):
        """Complete edge initialization with vertex configuration.

        Sets up edge collections, graph names, and initializes indices based on
        the vertex configuration.

        Args:
            vertex_config: Configuration for vertices

        Note:
            Discriminant is used to pin documents among a collection of documents
            of the same vertex type.
        """
        if self.type == EdgeType.INDIRECT and self.by is not None:
            self.by = vertex_config.vertex_dbname(self.by)

        if self.source_discriminant is None and self.target_discriminant is None:
            self.casting_type = EdgeCastingType.PAIR_LIKE
        else:
            self.casting_type = EdgeCastingType.PRODUCT_LIKE

        if self.weights is not None:
            if self.weights.source_fields:
                vertex_config[self.source] = vertex_config[
                    self.source
                ].update_aux_fields(self.weights.source_fields)
            if self.weights.target_fields:
                vertex_config[self.target] = vertex_config[
                    self.target
                ].update_aux_fields(self.weights.target_fields)

        self.source_collection = vertex_config.vertex_dbname(self.source)
        self.target_collection = vertex_config.vertex_dbname(self.target)
        graph_name = [
            vertex_config.vertex_dbname(self.source),
            vertex_config.vertex_dbname(self.target),
        ]
        if self.purpose is not None:
            graph_name += [self.purpose]
        self.graph_name = "_".join(graph_name + ["graph"])
        self.collection_name = "_".join(graph_name + ["edges"])
        self.db_flavor = vertex_config.db_flavor
        self._init_indices(vertex_config)

    def _init_indices(self, vc: VertexConfig):
        """Initialize indices for the edge.

        Args:
            vc: Vertex configuration
        """
        self.indexes = [self._init_index(index, vc) for index in self.indexes]

    def _init_index(self, index: Index, vc: VertexConfig) -> Index:
        """Initialize a single index for the edge.

        Args:
            index: Index to initialize
            vc: Vertex configuration

        Returns:
            Index: Initialized index

        Note:
            Default behavior for edge indices: adds ["_from", "_to"] for uniqueness
            in ArangoDB.
        """
        index_fields = []

        # "@" is reserved : quick hack - do not reinit the index twice
        if any("@" in f for f in index.fields):
            return index
        if index.name is None:
            index_fields += index.fields
        else:
            # add index over a vertex of index.name
            if index.fields:
                fields = index.fields
            else:
                fields = vc.index(index.name).fields
            index_fields += [f"{index.name}@{x}" for x in fields]

        if not index.exclude_edge_endpoints and self.db_flavor == DBFlavor.ARANGO:
            if all([item not in index_fields for item in ["_from", "_to"]]):
                index_fields = ["_from", "_to"] + index_fields

        index.fields = index_fields
        return index

    @property
    def edge_name_dyad(self):
        """Get the edge name as a dyad (source, target).

        Returns:
            tuple[str, str]: Source and target vertex names
        """
        return self.source, self.target

    @property
    def edge_id(self) -> EdgeId:
        """Get the edge ID.

        Returns:
            EdgeId: Tuple of (source, target, purpose)
        """
        return self.source, self.target, self.purpose


@dataclasses.dataclass
class EdgeConfig(BaseDataclass):
    """Configuration for managing collections of edges.

    This class manages a collection of edges, providing methods for accessing
    and manipulating edge configurations.

    Attributes:
        edges: List of edge configurations
    """

    edges: list[Edge] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        """Initialize the edge configuration.

        Creates internal mapping of edge IDs to edge configurations.
        """
        self._edges_map: dict[EdgeId, Edge] = {e.edge_id: e for e in self.edges}

    def finish_init(self, vc: VertexConfig):
        """Complete initialization of all edges with vertex configuration.

        Args:
            vc: Vertex configuration
        """
        for k, e in self._edges_map.items():
            e.finish_init(vc)

    def _reset_edges(self):
        """Reset edges list from internal mapping."""
        self.edges = list(self._edges_map.values())

    def edges_list(self, include_aux=False):
        """Get list of edges.

        Args:
            include_aux: Whether to include auxiliary edges

        Returns:
            generator: Generator yielding edge configurations
        """
        return (e for e in self._edges_map.values() if include_aux or not e.aux)

    def edges_items(self, include_aux=False):
        """Get items of edges.

        Args:
            include_aux: Whether to include auxiliary edges

        Returns:
            generator: Generator yielding (edge_id, edge) tuples
        """
        return (
            (eid, e) for eid, e in self._edges_map.items() if include_aux or not e.aux
        )

    def __contains__(self, item: EdgeId | Edge):
        """Check if edge exists in configuration.

        Args:
            item: Edge ID or Edge instance to check

        Returns:
            bool: True if edge exists, False otherwise
        """
        if isinstance(item, Edge):
            eid = item.edge_id
        else:
            eid = item

        if eid in self._edges_map:
            return True
        else:
            return False

    def update_edges(self, edge: Edge, vertex_config: VertexConfig):
        """Update edge configuration.

        Args:
            edge: Edge configuration to update
            vertex_config: Vertex configuration
        """
        if edge.edge_id in self._edges_map:
            self._edges_map[edge.edge_id].update(edge)
        else:
            self._edges_map[edge.edge_id] = edge
        self._edges_map[edge.edge_id].finish_init(vertex_config=vertex_config)

    @property
    def vertices(self):
        """Get set of vertex names involved in edges.

        Returns:
            set[str]: Set of vertex names
        """
        return {e.source for e in self.edges} | {e.target for e in self.edges}

    # def __getitem__(self, key: EdgeId):
    #     if key in self._reset_edges():
    #         return self._edges_map[key]
    #     else:
    #         raise KeyError(f"Vertex {key} absent")
    #
    # def __setitem__(self, key: EdgeId, value: Edge):
    #     self._edges_map[key] = value
