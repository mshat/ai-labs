from recommendation_list import show_recommendations, get_recommendations
from recommendation_list import (
    Node, create_tree_from_json, load_artist_pairs_proximity_json, calc_max_general_proximity, normalize_proximities)
import gui


class ParsingError(Exception): pass


def parse_command(command: str) -> dict:
    command_dict = {'command': '', 'params': {}, 'args': []}

    command = command.split()
    command_dict['command'] = command[0]
    command = command[1:]
    for i in range(len(command)):
        item = command[i]
        if item[0] == '-':
            command_dict['params'].update({item[1:]: command[i + 1]})
            i += 1
            continue
        if item[:2] == '--':
            command_dict['params'].update({item[2:]: command[i + 1]})
            i += 1
            continue
        command_dict['args'].append(item.replace(',', ''))
    return command_dict


def interface(tree):
    print('Контент-ориентированная рекомендательная система')
    print('Доступные команды: '
          'similar'
          )
    available_commands = ['similar', 'exit', 'like_list', 's', 'l']
    while True:
        command = input('Введите команду: ')
        command = command.lower()
        try:
            command_dict = parse_command(command)
        except Exception:
            print('Не могу разобрать команду')
            continue
        if command_dict['command'] not in available_commands:
            print('Unknown command')
            continue

        print(command_dict)
        if command_dict['command'] == 'exit':
            break
        elif command_dict['command'] in ('similar', 's'):
            seed = Node.get_child_by_name(tree, command_dict['args'][0])
            show_recommendations(seed, ARTIST_PAIRS_PROXIMITY, max_len=5)
        elif command_dict['command'] in ('like_list', 'l'):  # l noize mc guf
            liked_artists = [Node.get_child_by_name(tree, artist) for artist in command_dict['args']]
            artist_recommendations = {}
            for artist in liked_artists:
                artist_recommendations[artist] = get_recommendations(artist, ARTIST_PAIRS_PROXIMITY, max_len=5)
            print(artist_recommendations)
            # seed = Node.get_child_by_name(tree, command_dict['arg'])
            # show_recommendations(seed, ARTIST_PAIRS_PROXIMITY, max_len=5)


if __name__ == "__main__":
    gui.show()
    TREE = create_tree_from_json('data/genres.json')
    ARTIST_PAIRS_PROXIMITY = load_artist_pairs_proximity_json()
    # seed = Node.get_child_by_name(TREE, '123')
    # show_recommendations(seed, ARTIST_PAIRS_PROXIMITY, max_len=5)
    #
    # max_general_proximity = calc_max_general_proximity(ARTIST_PAIRS_PROXIMITY)
    # normalize_proximities(ARTIST_PAIRS_PROXIMITY, max_general_proximity)
    #
    # interface(TREE)

    # самые непохожие: noize mc лигалайз, alyona alyona каста, noize mc guf, noize mc баста, noize mc лигалайз
    # самые похожие: ram sid, баста guf, krec многоточие