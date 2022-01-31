from tree.visual_node import VisualNode, Node
from tree.tree_tools import calc_distance_between_nodes
from tree.tree_loader import load_tree_dict, create_tree_from_json, get_artists
from tree.genre_node import GenreVisualNode
from pow_distance import pow_distance


def euclidean(leaf_1, leaf_2):
    print(leaf_1, leaf_2)
    return pow_distance(leaf_1, leaf_2, 2)


def manhattan(leaf_1, leaf_2):
    return pow_distance(leaf_1, leaf_2, 1)


if __name__ == '__main__':
    tree = create_tree_from_json('genres.json')

    # мера близости по длине пути по дереву
    # print(calc_distance_between_nodes(tree, 'лсп', 'мукка'))

    # ноды для мер близости
    atl = Node.get_child_by_name(tree, 'atl')
    marlow = Node.get_child_by_name(tree, 'slava marlow')
    max_korj = Node.get_child_by_name(tree, 'макс корж')
    lsp = Node.get_child_by_name(tree, 'лсп')
    mukka = Node.get_child_by_name(tree, 'мукка')
    krovostok = Node.get_child_by_name(tree, 'кровосток')

    # мера близости euclidean
    print(euclidean(marlow, max_korj))

    # print(euclidean(lsp, marlow))
    # print(euclidean(lsp, max_korj))
    # print(euclidean(lsp, atl))
    #
    # print(euclidean(lsp, mukka))
    # print(euclidean(lsp, krovostok))
    # print(euclidean(krovostok, mukka))

    # мера близости manhattan
    # lsp = Node.get_child_by_name(tree, 'лсп')
    # mukka = Node.get_child_by_name(tree, 'мукка')
    # euclidean_coeff = manhattan(lsp, mukka)
    # print(euclidean_coeff)

    #tree.render_tree()
    #VisualNode.show_tree(tree)


