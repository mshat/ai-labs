from pow_distance import calc_distance_in_pow
from tree.genre_node import GenreVisualNode
from tree.node import Node
from tree.tree_tools import calc_distance_between_nodes, get_leafs, calc_max_distance_between_nodes
from tree.tree_tools import calc_distance_between_all_nodes


def calc_euclidean_measure(leaf_1: GenreVisualNode, leaf_2: GenreVisualNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items() if name not in ('name', 'theme')]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items() if name not in ('name', 'theme')]
    #print(leaf_1.name, leaf_2.name, attributes1, attributes2)
    return calc_distance_in_pow(attributes1, attributes2, 2)


def calc_manhattan_measure(leaf_1: GenreVisualNode, leaf_2: GenreVisualNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items() if name in ('name', 'theme')]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items() if name in ('name', 'theme')]
    # attributes1 = [val for name, val in leaf_1.countable_attributes.items()]
    # attributes2 = [val for name, val in leaf_2.countable_attributes.items()]
    return calc_distance_in_pow(attributes1, attributes2, 1)


def calc_tree_distance_measure(
        tree: Node,
        leaf_1: GenreVisualNode,
        leaf_2: GenreVisualNode,
        max_distance_between_nodes: int
):
    return calc_distance_between_nodes(tree, leaf_1.name, leaf_2.name) / max_distance_between_nodes


def generalizing_proximity_measure(
        tree: Node,
        leaf_1: GenreVisualNode,
        leaf_2: GenreVisualNode,
        max_distance_between_nodes: int) -> float:
    euclidean_proximity = calc_euclidean_measure(leaf_1, leaf_2)
    manhattan_proximity = calc_manhattan_measure(leaf_1, leaf_2)
    tree_distance = calc_tree_distance_measure(tree, leaf_1, leaf_2, max_distance_between_nodes)
    generalizing_proximity = euclidean_proximity + manhattan_proximity / 10 + tree_distance
    return generalizing_proximity


def calc_generalizing_proximity_measure_for_all_leafs(tree) -> dict:
    leafs = []
    get_leafs(tree, leafs)

    distances_between_nodes = calc_distance_between_all_nodes(tree, leafs)
    max_distance_between_nodes = calc_max_distance_between_nodes(distances_between_nodes)

    artist_pairs_proximity = {}
    i = 0
    for leaf1 in leafs:
        for leaf2 in leafs:
            if leaf1 != leaf2:
                proximity = generalizing_proximity_measure(tree, leaf1, leaf2, max_distance_between_nodes)
                artist_pairs_proximity.update(
                    {leaf1.name: {'artist2': leaf2.name, 'proximity': proximity}})
                i += 1
    return artist_pairs_proximity