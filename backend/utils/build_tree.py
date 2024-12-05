from typing import Any, Sequence

from common.enums import BuildTreeType
from utils.serializers import RowData, select_list_serialize


def get_tree_nodes(row: Sequence[RowData]) -> list[dict[str, Any]]:
    tree_nodes = select_list_serialize(row)
    tree_nodes.sort(key=lambda x: x["sort"])
    return tree_nodes


def traversal_to_tree(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tree = []
    node_dict = {node["id"]: node for node in nodes}

    for node in nodes:
        parent_id = node["parent_id"]
        if parent_id is None:
            tree.append(node)
        else:
            parent_node = node_dict.get(parent_id)
            if parent_node is not None:
                if "children" not in parent_node:
                    parent_node["children"] = []
                if node not in parent_node["children"]:
                    parent_node["children"].append(node)
            else:
                if node not in tree:
                    tree.append(node)

    return tree


def recursive_to_tree(
    nodes: list[dict[str, Any]], *, parent_id: int | None = None
) -> list[dict[str, Any]]:
    tree = []
    for node in nodes:
        if node["parent_id"] == parent_id:
            child_node = recursive_to_tree(nodes, parent_id=node["id"])
            if child_node:
                node["children"] = child_node
            tree.append(node)
    return tree


def get_tree_data(
    row: Sequence[RowData],
    build_type: BuildTreeType = BuildTreeType.traversal,
    *,
    parent_id: int | None = None,
) -> list[dict[str, Any]]:
    nodes = get_tree_nodes(row)
    match build_type:
        case BuildTreeType.traversal:
            tree = traversal_to_tree(nodes)
        case BuildTreeType.recursive:
            tree = recursive_to_tree(nodes, parent_id=parent_id)
        case _:
            raise ValueError(f"Недопустимый тип: {build_type}")
    return tree
