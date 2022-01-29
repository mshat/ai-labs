from tree.visual_tree import VisualNode
from tree.tree_tools import calc_distance_between_nodes
from tree.tree_loader import load_tree_dict, create_tree_from_json


if __name__ == '__main__':
    tree = create_tree_from_json('genres.json')
    # tree.render_tree()
    # VisualNode.show_tree(tree)
    print(calc_distance_between_nodes(tree, 'Rapcore', 'Emo'))
    print(calc_distance_between_nodes(tree, 'RapRock', 'Emo'))
    print(calc_distance_between_nodes(tree, 'Classic', 'Emo'))
