from __future__ import annotations

from collections.abc import Iterable
from typing import Optional, Union

from pandas import DataFrame

from .node import Node
from .relationship import Relationship
from .visualization_graph import VisualizationGraph

DFS_TYPE = Union[DataFrame, Iterable[DataFrame]]


def _from_dfs(
    node_dfs: DFS_TYPE,
    rel_dfs: DFS_TYPE,
    node_radius_min_max: Optional[tuple[float, float]] = (3, 60),
    rename_properties: Optional[dict[str, str]] = None,
) -> VisualizationGraph:
    if isinstance(node_dfs, DataFrame):
        node_dfs_iter: Iterable[DataFrame] = [node_dfs]
    else:
        node_dfs_iter = node_dfs

    has_size = True
    nodes = []
    for node_df in node_dfs_iter:
        has_size &= "size" in node_df.columns
        for _, row in node_df.iterrows():
            top_level = {}
            properties = {}
            for key, value in row.to_dict().items():
                if key in Node.model_fields.keys():
                    top_level[key] = value
                else:
                    if rename_properties and key in rename_properties:
                        key = rename_properties[key]
                    properties[key] = value

            nodes.append(Node(**top_level, properties=properties))

    if isinstance(rel_dfs, DataFrame):
        rel_dfs_iter: Iterable[DataFrame] = [rel_dfs]
    else:
        rel_dfs_iter = rel_dfs

    relationships = []
    for rel_df in rel_dfs_iter:
        for _, row in rel_df.iterrows():
            top_level = {}
            properties = {}
            for key, value in row.to_dict().items():
                if key in Relationship.model_fields.keys():
                    top_level[key] = value
                else:
                    if rename_properties and key in rename_properties:
                        key = rename_properties[key]
                    properties[key] = value

            relationships.append(Relationship(**top_level, properties=properties))

    VG = VisualizationGraph(nodes=nodes, relationships=relationships)

    if node_radius_min_max is not None and has_size:
        VG.resize_nodes(node_radius_min_max=node_radius_min_max)

    return VG


def from_dfs(
    node_dfs: DFS_TYPE,
    rel_dfs: DFS_TYPE,
    node_radius_min_max: Optional[tuple[float, float]] = (3, 60),
) -> VisualizationGraph:
    """
    Create a VisualizationGraph from pandas DataFrames representing a graph.

    All columns will be included in the visualization graph.
    If the columns are named as the fields of the `Node` or `Relationship` classes, they will be included as
    top level fields of the respective objects. Otherwise, they will be included in the `properties` dictionary.

    Parameters
    ----------
    node_dfs: Union[DataFrame, Iterable[DataFrame]]
        DataFrame or iterable of DataFrames containing node data.
    rel_dfs: Union[DataFrame, Iterable[DataFrame]]
        DataFrame or iterable of DataFrames containing relationship data.
    node_radius_min_max : tuple[float, float], optional
        Minimum and maximum node radius.
        To avoid tiny or huge nodes in the visualization, the node sizes are scaled to fit in the given range.
    """

    return _from_dfs(node_dfs, rel_dfs, node_radius_min_max)
