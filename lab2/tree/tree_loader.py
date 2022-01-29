import json
from .visual_node import VisualNode, Node
from .genre_node import GenreVisualNode


def load_tree_dict(filename='genres.json'):
    with open(filename, 'r') as file:
        genres = json.load(file)
    return genres


def create_node(node_name, children_dict):
    if not children_dict:  # this node is leaf
        #node = GenreVisualNode()
        print(f'"{node_name}"' + ': {},')
        node = VisualNode(val=node_name)
    else:
        node = VisualNode(val=node_name)
    for child_name in children_dict.keys():
        if children_dict:
            node.add_child(create_node(child_name, children_dict[child_name]))
    return node


def create_tree_from_json(filename='genres.json') -> VisualNode:
    tree_dict = load_tree_dict(filename)
    return create_node('HipHop', tree_dict['HipHop'])
