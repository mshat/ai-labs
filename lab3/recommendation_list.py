import json
from collections import OrderedDict
from tree.visual_node import VisualNode, Node
from tree.tree_tools import calc_distance_between_nodes, get_leafs, find_path_to_node, calc_max_distance_between_nodes, calc_distance_between_all_nodes
from tree.tree_loader import load_tree_dict, create_tree_from_json, get_artists
from tree.genre_node import GenreVisualNode
from proximity_measures import calc_euclidean_measure, calc_manhattan_measure, generalizing_proximity_measure, calc_tree_distance_measure
from proximity_measures import calc_generalizing_proximity_measure_for_all_leafs, calc_max_general_proximity, normalize_proximities
from tools import format_print
from compare_measures import compare_measures


def create_artist_pairs_proximity_json(tree):
    artist_pairs_proximity = calc_generalizing_proximity_measure_for_all_leafs(tree)

    with open('data/artist_pairs_proximity.json', 'w') as file:
        json.dump(artist_pairs_proximity, file)


def load_artist_pairs_proximity_json(filename: str = 'data/ARTIST_PAIRS_PROXIMITY.json') -> dict:
    with open(filename, 'r') as file:
        return json.load(file)


def print_all_artist_pairs_proximity(artist_pairs_proximity: dict):
    for artist1_name, pair_artists in artist_pairs_proximity.items():
        for pair_name, pair_proximity in pair_artists.items():
            print(f'{artist1_name} - {pair_name} = {pair_proximity}')


def get_recommendations(
        seed_object: GenreVisualNode,
        artist_pairs_proximity: dict,
        max_len: int = None) -> OrderedDict:
    artist_pairs = artist_pairs_proximity[seed_object.name]
    recommendations = OrderedDict(sorted(artist_pairs.items(), key=lambda item: item[1]))
    if max_len:
        limited_recommendations = OrderedDict()
        i = 0
        for key, val in recommendations.items():
            if i > max_len:
                break
            i += 1
            limited_recommendations.update({key: val})
        return limited_recommendations
    return recommendations


def show_recommendations(
        seed_object: GenreVisualNode,
        artist_pairs_proximity: dict,
        max_len: int = None,
        show_proximity=False) -> None:
    recommendations = get_recommendations(seed_object, artist_pairs_proximity, max_len)
    # print(f'seed_object: {seed_object.name}')
    for recommendation_name, proximity in recommendations.items():
        if show_proximity:
            format_print([recommendation_name, proximity], [20, 5])
        else:
            print(recommendation_name)


def main():
    tree = create_tree_from_json('data/genres.json')
    # create_artist_pairs_proximity_json(tree)
    artist_pairs_proximity = load_artist_pairs_proximity_json()
    max_general_proximity = calc_max_general_proximity(artist_pairs_proximity)
    normalize_proximities(artist_pairs_proximity, max_general_proximity)

    # print_all_artist_pairs_proximity(ARTIST_PAIRS_PROXIMITY)

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
    # compare_measures(tree, artist_pairs, max_general_proximity)

    show_recommendations(atl, artist_pairs_proximity, show_proximity=True)


if __name__ == '__main__':
    main()