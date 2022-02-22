from typing import List
from lab8.src.query_handler import Query, QueryPattern, QueryHandler
from lab8.src.tag_condition import (AndMultiTagCondition as AndMulti, OrMultiTagCondition as OrMulti,
                                    AndTagCondition as And, OrTagCondition as Or, AndNotTagCondition as AndNot,
                                    OrNotTagCondition as OrNot)
from lab8.src.dialog_state import DialogState
from lab8.src.query_handler import log_query_pattern_strings, ALL
from lab8.src.tools import debug_print
from lab8.src.query import ArtistArgument, NumArgument, SexArgument, GenreArgument
from lab8.src.user import User
from lab8.src.recommender_system import filter
from lab8.src.recommender_system import interface
from lab8.src.config import DEBUG
from lab8.src.const import SexFilter


def filter_search_result(user: User):
    if user.search_result:
        user.search_result = filter.filter_recommendations(
            user.search_result,
            group_type=user.group_type_filter.value,
            sex=user.sex_filter.value,
            younger=user.younger_filter,
            older=user.older_filter,
        )
    return user.search_result


def show_recommendations(user: User):
    if user.str_filters != '':
        print(f'Установлены фильтры: {user.str_filters}')
    if user.dislikes:
        print(f'Список дизлайков: {", ".join(user.dislikes)}')
    artists = filter_search_result(user)
    interface.print_recommendations(artists, output_len=user.output_len, debug=DEBUG)


def get_arguments_by_type(query: Query, argument_type: str) \
        -> List[ArtistArgument | NumArgument | SexArgument | GenreArgument]:
    return [argument for type_, arguments in query.arguments.items() for argument in arguments if type_ == argument_type]


def restart(query: Query, user: User):
    return DialogState.start


def like(query: Query, user: User):
    liked_artists = get_arguments_by_type(query, 'ArtistArgument')
    liked_artists = [artist.value for artist in liked_artists]
    for artist in liked_artists:
        user.add_like(artist)
    print(f'Поставлен лайк: {", ".join(liked_artists)}')
    return DialogState.like


def dislike(query: Query, user: User):
    disliked_artists = get_arguments_by_type(query, 'ArtistArgument')
    disliked_artists = [artist.value for artist in disliked_artists]
    for artist in disliked_artists:
        user.add_dislike(artist)
    print(f'Поставлен дизлайк: {", ".join(disliked_artists)}')
    return DialogState.dislike


def show_all_artists(query: Query, user: User):
    artists = interface.get_all_artists()
    interface.print_artists(artists)
    return DialogState.search


def search_by_artist(query: Query, user: User):
    artist = get_arguments_by_type(query, 'ArtistArgument')[0]
    artists = interface.recommend_by_seed(artist.value, disliked_artists=user.dislikes)
    user.search_result = artists
    return DialogState.search


def search_by_genre(query: Query, user: User):
    genre = get_arguments_by_type(query, 'GenreArgument')[0]
    artists = interface.get_artists_by_genre(genre.value)
    interface.print_artists(artists, debug=DEBUG)
    return DialogState.search


def search_by_sex(query: Query, user: User):
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    artists = interface.get_all_artists()
    artists = filter.filter_artists(artists, sex=sex.value.value)
    interface.print_artists(artists)
    return DialogState.search


def search_by_age_range(query: Query, user: User):
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) >= 2:
        from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
        debug_print(f'количество артистов от {from_age} до {to_age} лет')

        artists = interface.get_all_artists()
        artists = filter.filter_artists(artists, older=from_age, younger=to_age)
        interface.print_artists(artists)
        user.search_result = artists
    else:
        return
    return DialogState.search


def search_by_age(query: Query, user: User):
    age = get_arguments_by_type(query, 'NumArgument')[0]
    age = int(age.value)

    artists = interface.get_all_artists()

    if 'younger' in query.query_tag_structure:
        debug_print(f'фильтр до {age} лет')
        artists = filter.filter_artists(artists, younger=age)
    elif 'older' in query.query_tag_structure:
        debug_print(f'фильтр от {age} лет')
        artists = filter.filter_artists(artists, older=age)

    interface.print_artists(artists)
    user.search_result = artists
    return DialogState.search


def info(query: Query, user: User):
    artist_arg = get_arguments_by_type(query, 'ArtistArgument')[0]
    artist = interface.get_artist_by_name(artist_arg.value)
    if not artist:
        print('Артист не найден :(')
    else:
        sex = "мужской" if artist.male_or_female == 1 else "женский"
        if artist.group_members_number == 1:
            print(f'Артист {artist.name}')
        elif artist.group_members_number == 2:
            print(f'Дуэт {artist.name}')
        else:
            print(f'Группа {artist.name}')
        if artist.group_members_number > 1:
            print(f'Возраст фронтмэна: {artist.age}')
            print(f'Пол фронтмэна: {sex}')
            print(f'Количество участников: {artist.group_members_number}')
        else:
            print(f'Возраст: {artist.age}')
            print(f'Пол: {sex}')

    return DialogState.info


def number(query: Query, user: User):
    artists = interface.get_all_artists()
    print(f'В базе {len(artists)} исполнителя')
    return DialogState.number


def number_with_sex(query: Query, user: User):
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    artists = interface.get_all_artists()
    artists = filter.filter_artists(artists, sex=sex.value.value)
    if sex.value == SexFilter.male:
        print(f'В базе {len(artists)} исполнителя мужского пола')
    else:
        print(f'В базе {len(artists)} исполнитель женского пола')
    return DialogState.number


def number_with_age_range(query: Query, user: User):
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) >= 2:
        from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
        debug_print(f'количество артистов от {from_age} до {to_age} лет')

        artists = interface.get_all_artists()
        artists = filter.filter_artists(artists, older=from_age, younger=to_age)

        print(f'Количество исполнителей от {from_age} до {to_age} лет: {len(artists)}')
    else:
        return
    return DialogState.number


def number_with_age(query: Query, user: User):
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) >= 2:
        age = age[0]

    if 'younger' in query.query_tag_structure:
        debug_print(f'количество артистов до {age} лет')
    elif 'older' in query.query_tag_structure:
        debug_print(f'количество артистов от {age} лет')
    return DialogState.number


def set_output_len(query: Query, user: User):
    output_len = get_arguments_by_type(query, 'NumArgument')[-1]
    user.output_len = output_len
    debug_print(f'Ограничение вывода: {output_len} строк')
    return DialogState.count_filter


def filter_by_sex_include(query: Query, user: User):
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    debug_print(f'Убрать всех, кроме {sex.value.value} пола')

    user.add_sex_filter(sex.value)

    filter_search_result(user)
    show_recommendations(user)
    return DialogState.filter


def filter_by_sex_exclude(query: Query, user: User):
    sex_arg = get_arguments_by_type(query, 'SexArgument')[0]
    debug_print(f'Убрать артистов {sex_arg.value} пола')

    sex = SexFilter.male if sex_arg.value == SexFilter.female else SexFilter.female
    user.add_sex_filter(sex)

    filter_search_result(user)
    show_recommendations(user)

    return DialogState.filter


def filter_by_age_range(query: Query, user: User):
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) >= 2:
        from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
        debug_print(f'фильтр от {from_age} до {to_age} лет')
    else:
        return
    return DialogState.filter


def filter_by_age_include(query: Query, user: User):
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) > 1:
        age = age[0]
    if 'younger' in query.query_tag_structure:
        debug_print(f'фильтр до {age} лет')
    elif 'older' in query.query_tag_structure:
        debug_print(f'фильтр от {age} лет')
    return DialogState.filter


def filter_by_age_exclude(query: Query, user: User):
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) > 1:
        age = age[0]
    if 'younger' in query.query_tag_structure:
        debug_print(f'фильтр от {age} лет')
    elif 'older' in query.query_tag_structure:
        debug_print(f'фильтр до {age} лет')
    return DialogState.filter


def filter_by_members_count(query: Query, user: User):
    tags = query.query_tag_structure
    if 'group' in tags:
        members_count_type = 'group'
    elif 'solo' in tags:
        members_count_type = 'solo'
    elif 'duet' in tags:
        members_count_type = 'duet'
    debug_print(f'оставить {members_count_type}')
    return DialogState.filter


def remove_result_len_filter(query: Query, user: User):
    return DialogState.filter


def remove_filters(query: Query, user: User):
    return DialogState.filter


restart_handler = QueryHandler(
    QueryPattern([And('restart')]),
    restart, 'Рестарт')

filter_by_sex_include_handler = QueryHandler(
    # QueryPattern([Or('include'), OrMulti([And('exclude'), And('except')])], 'SexArgument'),
    QueryPattern([], 'SexArgument'),
    filter_by_sex_include, 'Фильтр по полу "включить"')

filter_by_sex_exclude_handler = QueryHandler(
    QueryPattern([Or('exclude'), AndNot('except')], 'SexArgument'),
    # QueryPattern([Or('exclude')], 'SexArgument'),
    filter_by_sex_exclude, 'Фильтр по полу "исключить"')

filter_by_age_range_handler = QueryHandler(
    QueryPattern([Or('range'), OrMulti([And('older'), And('younger')])], required_arguments={'NumArgument': 2}),
    filter_by_age_range, 'Фильтр по возрасту в диапазоне')

filter_by_age_include_handler = QueryHandler(
    QueryPattern([AndMulti([Or('older'), Or('younger')])], 'NumArgument'),
    filter_by_age_include, 'Фильтр по возрасту')

filter_by_age_exclude_handler = QueryHandler(
    QueryPattern([And('exclude'), AndMulti([Or('older'), Or('younger')])], 'NumArgument'),
    filter_by_age_exclude, 'Фильтр по возрасту')

set_output_len_handler = QueryHandler(
    QueryPattern([Or('show'), OrMulti([And('po'), AndMulti([Or('result'), Or('artist')])])], 'NumArgument'),
    set_output_len, 'Изменить количество выводимых результатов')

filter_by_members_count_handler = QueryHandler(
    QueryPattern([Or('group'), Or('solo'), Or('duet')]),
    filter_by_members_count, 'Фильтр по количеству участников коллектива')

remove_filters_handler = QueryHandler(
    QueryPattern([And('exclude'), And('all'), And('filter')]),
    remove_filters, 'Удалить все фильтры')

remove_result_len_filter_handler = QueryHandler(
    QueryPattern([
        OrMulti([And('exclude'), And('number')]),
        OrMulti([AndMulti([Or('show'), Or('include')]), And('all')])
    ]),
    remove_result_len_filter, 'Удалить ограничение количества выводимых строк')

exclude_dislike_handler = QueryHandler(
    QueryPattern([And('dislike'), And('exclude')], required_arguments={'ArtistArgument': ALL}),
    like, 'Лайк')

exclude_like_handler = QueryHandler(
    QueryPattern([And('like'), And('exclude')], required_arguments={'ArtistArgument': ALL}),
    dislike, 'Дизлайк')

like_handler = QueryHandler(
    QueryPattern([And('like')], required_arguments={'ArtistArgument': ALL}),
    like, 'Лайк')

dislike_handler = QueryHandler(
    QueryPattern([And('dislike')], required_arguments={'ArtistArgument': ALL}),
    dislike, 'Дизлайк')

number_with_sex_handler = QueryHandler(
    QueryPattern([Or('number'), Or('how many')], 'SexArgument'),
    number_with_sex, 'Количество артистов указанного пола в базе')

number_with_age_range_handler = QueryHandler(
    QueryPattern(
        [AndMulti([Or('number'), Or('how many')]), AndMulti([Or('range'), OrMulti([And('older'), And('younger')])])],
        required_arguments={'NumArgument': 2}
    ),
    number_with_age_range, 'Количество артистов от X до Y лет в базе')

number_with_age_handler = QueryHandler(
    QueryPattern(
        [AndMulti([Or('number'), Or('how many')]), AndMulti([Or('older'), Or('younger')])],
        'NumArgument'
    ),
    number_with_age, 'Количество артистов указанного возраста в базе')

number_handler = QueryHandler(
    QueryPattern([Or('number'), Or('how many')]),
    number, 'Количество артистов в базе')

search_by_sex_handler = QueryHandler(
    QueryPattern([Or('artist'), Or('recommend'), Or('show')], 'SexArgument'),
    search_by_sex, 'Вывести исполнителей указанного пола')

search_by_age_range_handler = QueryHandler(
    QueryPattern(
        [AndMulti([Or('artist'), Or('recommend'), Or('show')]), AndMulti([Or('range'), OrMulti([And('older'), And('younger')])])],
        required_arguments={'NumArgument': 2}),
    search_by_age_range, 'Вывести исполнителей в диапазоне возраста')

search_by_age_handler = QueryHandler(
    QueryPattern([AndMulti([Or('artist'), Or('recommend'), Or('show')]), AndMulti([Or('older'), Or('younger')])], 'NumArgument'),
    search_by_age, 'Вывести исполнителей в указанном возрасте')

search_by_genre_handler = QueryHandler(
    QueryPattern([Or('genre'), Or('recommend'), Or('show')], 'GenreArgument'),
    search_by_genre, 'Вывести артистов в определённом жанре')

search_by_artist_handler = QueryHandler(
    QueryPattern([Or('search'), Or('recommend'), Or('show')], 'ArtistArgument'),
    search_by_artist, 'Рекомендация по артисту')

show_all_handler = QueryHandler(
    QueryPattern([And('all'), AndMulti([Or('include'), Or('artist'), Or('show')])]),
    show_all_artists, 'Вывести всех артистов в базе')

info_handler = QueryHandler(
    QueryPattern([Or('talk about'), Or('about'), Or('info')], 'ArtistArgument'),
    info, 'Информация об артисте')


if __name__ == "__main__":
    log_query_pattern_strings()