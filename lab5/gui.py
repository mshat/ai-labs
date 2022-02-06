import PySimpleGUI as sg
import interface
from data.artists import ARTISTS

artists_list = reversed(ARTISTS)
artists_list = [artist.ljust(18) for artist in artists_list]
available_artists1 = '\n'.join(list(artists_list[:30]))
available_artists2 = '\n'.join(list(artists_list[30:]))

EXCLUDE = ['sex', 'group_type', 'older', 'younger']

# самые непохожие: noize mc лигалайз, alyona alyona каста, noize mc guf, noize mc баста, noize mc лигалайз
# самые похожие: ram sid, баста guf, krec многоточие

layout = [
    [
        sg.Text('Рекомендация по затравочному значению', size=(39, 1)),
        sg.Radio(text='', group_id=0, default=True, key='_seed_radio_'),
        sg.InputText(key='_seed_'),
    ],
    [
        sg.Text('Рекомендация по списку лайков (через запятую)', size=(39, 1)),
        sg.Radio(text='', group_id=0, key='_liked_radio_'),
        sg.InputText(key='_liked_', default_text='noize mc, лигалайз, guf')
    ],
    [
        sg.Text('Учитывать дизлайки', size=(39, 1)),
        sg.Checkbox(text='', key='_dislikes_'),
        sg.InputText(key='_disliked_', default_text='jah khalib, t-fest, hammali & navai')
    ],
    [
        sg.Text('Сколько артистов выводить (число или "all"):', size=(33, 1)),
        sg.InputText(default_text='6', key='_max_len_', size=(5, 1))
    ],
    [
        sg.Text('Фильтры: ')
    ],
    [
        sg.Radio(text='male', group_id=1, key='_male_'), sg.Radio(text='female', group_id=1, key='_female_'),
        sg.Radio(text='any_sex', group_id=1, default=True, key='_any_sex_'),
        sg.Text('|'),
        sg.Radio(text='solo', group_id=2, key='_solo_'), sg.Radio(text='duet', group_id=2, key='_duet_'),
        sg.Radio(text='group', group_id=2, key='_group_'),
        sg.Radio(text='any', group_id=2, default=True, key='_any_'),
        sg.Text('|'),
        sg.Text('Старше чем (лет): '), sg.InputText(key='_older_', size=(5, 1)),
        sg.Text('Младше чем (лет): '), sg.InputText(key='_younger_', size=(5, 1)),
    ],
    [sg.Checkbox('Очищать вывод', default=True, key='_clean_output_'), sg.Checkbox('DEBUG', default=True, key='_debug_')],
    [sg.Button('Очистить поля ввода')],
    [
        sg.Output(size=(80, 20), key='_output_'),
        sg.Text(size=(18, 30), key='_artists_', text=available_artists1),
        sg.Text(size=(18, 30), key='_artists_', text=available_artists2)
    ],
    [sg.Submit(button_text='Рекомендовать'), sg.Cancel()]
]


def filter(filters, recommendations, exclude=None):
    exclude = exclude if exclude else []
    filtered_recommendations = []
    group_type = filters['group_type']
    sex = filters['sex']
    older = int(filters['older']) if filters['older'] else None
    younger = int(filters['younger']) if filters['younger'] else None
    for artist_name, proximity in recommendations.items():
        artist = interface.find_artist(artist_name)
        if group_type != 'any' and artist.solo_duet_group != group_type and 'group_type' not in exclude:
            continue
        if sex != 'anysex' and artist.sex != sex and 'sex' not in exclude:
            continue
        if older and artist.age < older and 'older' not in exclude:
            continue
        if younger and artist.age > younger and 'younger' not in exclude:
            continue
        filtered_recommendations.append(artist_name)
    return filtered_recommendations


def parse_filters(values) -> dict:
    filters = {}
    for sex in ['_male_', '_female_', '_any_sex_']:
        if values[sex]:
            filters['sex'] = sex.replace('_', '')
            break

    for group_type in ['_solo_', '_duet_', '_group_', '_any_']:
        if values[group_type]:
            filters['group_type'] = group_type.replace('_', '')
            break

    filters['older'] = values['_older_']
    filters['younger'] = values['_younger_']

    return filters


def print_recommendations(final_recommendation_artists, max_output_len):
    for i, artist_name in enumerate(final_recommendation_artists):
        if i < max_output_len:
            # print(artist_name, final_recommendations[artist_name])
            if show:
                print(artist_name)


def show():
    window = sg.Window('lab3', layout)
    while True:
        event, values = window.read()
        seed = values['_seed_']
        seed_radio = values['_seed_radio_']
        liked = values['_liked_']
        liked_radio = values['_liked_radio_']
        disliked = values['_disliked_']
        use_disliked = values['_dislikes_']
        max_len = 100 if values['_max_len_'].lower() == 'all' else int(values['_max_len_'])
        clean = values['_clean_output_']
        debug = values['_debug_']
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == 'Очистить поля ввода':
            window['_seed_'].Update('')
            window['_liked_'].Update('')
            window['_disliked_'].Update('')
        if event == 'Рекомендовать':
            if seed_radio:
                if clean:
                    window['_output_'].Update('')
                try:
                    recommendations = interface.recommend_by_seed(seed, max_len)
                    filtered_recommendations = filter(parse_filters(values), recommendations)
                    if not filtered_recommendations:
                        print('Не найдено точного соответствия, однако, возможно, Вам понравится:')
                    i = 0
                    exclude = []
                    while not filtered_recommendations and i < len(EXCLUDE):
                        exclude.append(EXCLUDE[i])
                        filtered_recommendations = filter(parse_filters(values), recommendations, exclude=exclude)
                        i += 1
                    print_recommendations(filtered_recommendations, max_len)

                except interface.ParseError as e:
                    print('Не могу разобрать аргументы')
                    print(e)
                except interface.ArgumentError as e:
                    print(e)
                except Exception as e:
                    print(f'Неизвестная ошибка: {e}')
            elif use_disliked:
                if clean:
                    window['_output_'].Update('')
                try:
                    recommendations = interface.recommend_by_disliked(disliked, liked, max_len, debug)
                    filtered_recommendations = filter(parse_filters(values), recommendations)
                    if not filtered_recommendations:
                        print('Не найдено точного соответствия, однако, возможно, Вам понравится:')
                    i = 0
                    exclude = []
                    while not filtered_recommendations and i < len(EXCLUDE):
                        exclude.append(EXCLUDE[i])
                        filtered_recommendations = filter(parse_filters(values), recommendations, exclude=exclude)
                        i += 1
                    print_recommendations(filtered_recommendations, max_len)
                except interface.ParseError:
                    print('Не могу разобрать аргументы')
                except Exception as e:
                    print(f'Неизвестная ошибка: {e}')
            elif liked_radio:
                if clean:
                    window['_output_'].Update('')
                try:
                    recommendations = interface.recommend_by_liked(liked, max_len)
                    filtered_recommendations = filter(parse_filters(values), recommendations)
                    if not filtered_recommendations:
                        print('Не найдено точного соответствия, однако, возможно, Вам понравится:')
                    i = 0
                    exclude = []
                    while not filtered_recommendations and i < len(EXCLUDE):
                        exclude.append(EXCLUDE[i])
                        filtered_recommendations = filter(parse_filters(values), recommendations, exclude=exclude)
                        i += 1
                    print_recommendations(filtered_recommendations, max_len)
                except interface.ParseError:
                    print('Не могу разобрать аргументы')
                except interface.ArgumentError as e:
                    print(e)
                except Exception as e:
                    print(f'Неизвестная ошибка: {e}')


    window.close()
