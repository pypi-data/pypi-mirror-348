from collections import defaultdict
from typing import Any

from cognite.client.data_classes.data_modeling import (
    Edge,
    EdgeConnection,
    MappedProperty,
    Node,
    View,
)
from cognite.client.data_classes.data_modeling.query import (
    QueryResult,
)
from cognite.client.data_classes.data_modeling.views import (
    MultiReverseDirectRelation,
    SingleReverseDirectRelation,
)

from capybara_orm.constants import EDGE_DIRECTION, EDGE_MARKER, NESTED_SEP

from .view_mapper import ViewMapper


class QueryResultMapper:
    def __init__(self, view_mapper: ViewMapper):
        self._view_mapper = view_mapper

    def map_nodes(
        self, root_node: str, query_result: QueryResult
    ) -> tuple[list[dict[str, Any]], str | None]:
        if root_node not in query_result:
            raise ValueError(
                f"{root_node} is not available in the query result"
            )

        root_view = self._view_mapper.get_view(root_node)

        values = self._map_node_property(root_node, root_view, query_result)
        if not values:
            return [], None

        data = [
            node
            for nodes in values.values()
            for node in self._nodes_to_dict(nodes)
        ]

        return data, query_result.cursors.get(root_node)

    def _map_node_property(
        self,
        key: str,
        view: View,
        query_result: QueryResult,
        result_property_key: str | None = None,
    ) -> dict[tuple[str, str], list[Node]] | None:
        if key not in query_result:
            return None

        mappings = self._get_property_mappings(key, view, query_result)

        view_id = view.as_id()

        nodes = (
            node
            for node in query_result.get_nodes(key)
            if isinstance(node, Node)
        )

        def get_node_id(node: Node) -> tuple[str, str]:
            if not result_property_key:
                return (node.space, node.external_id)

            entry = properties.get(result_property_key)
            if not isinstance(entry, dict):
                raise ValueError(
                    f"Invalid result property key {result_property_key}"
                )

            return entry.get("space", ""), entry.get("externalId", "")

        result: defaultdict[tuple[str, str], list[Node]] = defaultdict(list)
        for node in nodes:
            properties = node.properties.get(view_id, {})
            node_id = get_node_id(node)
            for mapping_key, (values, is_list) in mappings.items():
                element = properties.get(mapping_key)

                element_key: tuple[str, str] = (
                    (element.get("space", ""), element.get("externalId", ""))
                    if isinstance(element, dict)
                    else node_id
                )

                entries = values.get(element_key)
                if not entries:
                    continue

                entry_data = self._nodes_to_dict(entries)
                properties[mapping_key] = (
                    entry_data if is_list else entry_data[0]
                )

            node.properties[view_id] = properties

            result[node_id].append(node)

        return dict(result)

    def _get_property_mappings(
        self, key: str, view: View, query_result: QueryResult
    ) -> dict[str, tuple[dict[tuple[str, str], list[Node]], bool]]:
        mappings: dict[
            str, tuple[dict[tuple[str, str], list[Node]], bool]
        ] = {}

        for property_name, property in view.properties.items():
            property_key = f"{key}{NESTED_SEP}{property_name}"

            entry: dict[tuple[str, str], list[Node]] | None = None
            is_list = False

            if isinstance(property, MappedProperty) and property.source:
                entry = self._map_node_property(
                    property_key,
                    self._view_mapper.get_view(property.source.external_id),
                    query_result,
                )
                is_list = False
            elif (
                isinstance(property, SingleReverseDirectRelation)
                and property.source
            ):
                entry = self._map_node_property(
                    property_key,
                    self._view_mapper.get_view(property.source.external_id),
                    query_result,
                    property.through.property,
                )
                is_list = False
            elif (
                isinstance(property, MultiReverseDirectRelation)
                and property.source
            ):
                entry = self._map_node_property(
                    property_key,
                    self._view_mapper.get_view(property.source.external_id),
                    query_result,
                    property.through.property,
                )
                is_list = True

            elif isinstance(property, EdgeConnection) and property.source:
                entry = self._map_edge_property(
                    property_key,
                    self._view_mapper.get_view(property.source.external_id),
                    query_result,
                    property.direction,
                )
                is_list = True

            if entry:
                mappings[property_name] = entry, is_list

        return mappings

    def _map_edge_property(
        self,
        key: str,
        view: View,
        query_result: QueryResult,
        edge_direction: EDGE_DIRECTION,
    ) -> dict[tuple[str, str], list[Node]] | None:
        edge_key = f"{key}{NESTED_SEP}{EDGE_MARKER}"
        if key not in query_result or edge_key not in query_result:
            return None

        nodes = self._map_node_property(key, view, query_result)
        if not nodes:
            return None

        result: defaultdict[tuple[str, str], list[Node]] = defaultdict(list)

        edges = (
            edge
            for edge in query_result.get_edges(edge_key)
            if isinstance(edge, Edge)
        )
        for edge in edges:
            entry_key, node_key = (
                (
                    edge.end_node.as_tuple(),
                    edge.start_node.as_tuple(),
                )
                if edge_direction == "inwards"
                else (edge.start_node.as_tuple(), edge.end_node.as_tuple())
            )

            if node_item := nodes.get(node_key):
                result[entry_key].extend(node_item)

        return dict(result)

    def _nodes_to_dict(self, nodes: list[Node]) -> list[dict[str, Any]]:
        return [self._node_to_dict(node) for node in nodes]

    def _node_to_dict(self, node: Node) -> dict[str, Any]:
        entry = node.dump()
        properties: dict[str, dict[str, dict[str, Any]]] = (
            entry.pop("properties") or {}
        )
        for space_mapping in properties.values():
            for view_mapping in space_mapping.values():
                entry.update(view_mapping)

        return entry
