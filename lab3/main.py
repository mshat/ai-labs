from recommendation_list import show_recommendations
from recommendation_list import (
    Node, create_tree_from_json, load_artist_pairs_proximity_json, calc_max_general_proximity, normalize_proximities)


class ParsingError(Exception): pass


def parse_command(command: str) -> dict:
    command_dict = {'command': '', 'params': {}, 'arg': ''}

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
        if command_dict['arg']:
            raise ParsingError('Parsing error')
        command_dict['arg'] = item
    return command_dict


def interface(tree):
    print('Контент-ориентированная рекомендательная система')
    print('Доступные команды: '
          'similar'
          )
    available_commands = ['similar', 'exit']
    while True:
        command = input('Введите команду: ')
        command = command.lower()
        try:
            command_dict = parse_command(command)
        except ParsingError:
            print('Не могу разобрать команду')
            continue
        if command_dict['command'] not in available_commands:
            print('Unknown command')
            continue

        if command_dict['command'] == 'exit':
            break
        elif command_dict['command'] == 'similar':
            seed = Node.get_child_by_name(tree, command_dict['arg'])
            show_recommendations(seed, ARTIST_PAIRS_PROXIMITY, max_len=5)


if __name__ == "__main__":
    TREE = create_tree_from_json('data/genres.json')
    ARTIST_PAIRS_PROXIMITY = load_artist_pairs_proximity_json()

    max_general_proximity = calc_max_general_proximity(ARTIST_PAIRS_PROXIMITY)
    normalize_proximities(ARTIST_PAIRS_PROXIMITY, max_general_proximity)

    interface(TREE)