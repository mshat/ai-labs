import json
from tree.visual_node import VisualNode, Node
from tree.tree_tools import calc_distance_between_nodes, get_leafs, find_path_to_node, calc_max_distance_between_nodes, calc_distance_between_all_nodes
from tree.tree_loader import load_tree_dict, create_tree_from_json, get_artists
from tree.genre_node import GenreVisualNode
from proximity_measures import calc_euclidean_measure, calc_manhattan_measure, generalizing_proximity_measure, calc_tree_distance_measure
from proximity_measures import calc_generalizing_proximity_measure_for_all_leafs
from tools import format_print
from compare_measures import compare_measures


def create_artist_pairs_proximity_json(tree):
    artist_pairs_proximity = calc_generalizing_proximity_measure_for_all_leafs(tree)

    with open('data/artist_pairs_proximity.json', 'w') as file:
        json.dump(artist_pairs_proximity, file)


def load_artist_pairs_proximity_json(filename: str = 'data/artist_pairs_proximity.json') -> dict:
    with open(filename, 'r') as file:
        return json.load(file)


def print_all_artist_pairs_proximity(artist_pairs_proximity: dict):
    for pair_num, pair_data in artist_pairs_proximity.items():
        print(f'{pair_num} {pair_data["artist1"]} - {pair_data["artist2"]} = {pair_data["proximity"]}')


def get_recommendation_list(seed_object: GenreVisualNode, artist_pairs_proximity: dict) -> list[GenreVisualNode]:
    pass


def main():
    tree = create_tree_from_json('data/genres.json')
    artist_pairs_proximity = load_artist_pairs_proximity_json()

    ## ноды для мер близости
    atl = Node.get_child_by_name(tree, 'atl')
    marlow = Node.get_child_by_name(tree, 'slava marlow')
    max_korj = Node.get_child_by_name(tree, 'макс корж')
    lsp = Node.get_child_by_name(tree, 'лсп')
    mukka = Node.get_child_by_name(tree, 'мукка')
    krovostok = Node.get_child_by_name(tree, 'кровосток')
    liga = Node.get_child_by_name(tree, 'лигалайз')
    jah = Node.get_child_by_name(tree, 'jah khalib')

    ## сравнение
    # artist_pairs = [(marlow, max_korj), (lsp, marlow), (lsp, max_korj), (lsp, atl), (lsp, mukka), (lsp, krovostok),
    #                 (krovostok, mukka), (liga, jah)]
    # compare_measures(tree, artist_pairs)


if __name__ == '__main__':
    main()