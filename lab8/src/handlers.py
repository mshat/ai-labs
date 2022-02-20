from query_handler import (Query, QueryPattern, QueryHandler, AndTagCondition as And, OrTagCondition as Or,
                           AndMultiTagCondition as AndMulti, OrMultiTagCondition as OrMulti)
from dialog_state import DialogState
from query_handler import log_query_pattern_strings
from tools import debug_print


def get_arguments_by_type(query: Query, argument_type: str):
    return [argument for type_, arguments in query.arguments.items() for argument in arguments if type_ == argument_type]


def restart(query: Query):
    return DialogState.start


def like(query: Query):
    allowed_states = (DialogState.search, DialogState.start)
    artists = get_arguments_by_type(query, 'ArtistArgument')
    return DialogState.like


def dislike(query: Query):
    allowed_states = (DialogState.search, DialogState.start)
    artists = get_arguments_by_type(query, 'ArtistArgument')
    return DialogState.dislike


def show_all_artists(query: Query):
    allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
    return DialogState.search


def search_by_artist(query: Query):
    allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
    artists = get_arguments_by_type(query, 'ArtistArgument')
    return DialogState.search


def search_by_genre(query: Query):
    allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
    genres = get_arguments_by_type(query, 'GenreArgument')
    return DialogState.search


def search_by_sex(query: Query):
    allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    return DialogState.search


def info(query: Query):
    allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
    artists = get_arguments_by_type(query, 'ArtistArgument')
    return DialogState.info


def number(query: Query):
    allowed_states = (DialogState.number, DialogState.search, DialogState.start)
    debug_print(query.arguments.items())
    return DialogState.number


def number_with_sex(query: Query):
    allowed_states = (DialogState.number, DialogState.search, DialogState.start)
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    return DialogState.number


def number_with_age_range(query: Query):
    allowed_states = (DialogState.number, DialogState.search, DialogState.start)
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) >= 2:
        from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
        debug_print(f'количество артистов от {from_age} до {to_age} лет')
    else:
        return
    return DialogState.number


def number_with_age(query: Query):
    allowed_states = (DialogState.number, DialogState.search, DialogState.start)
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) >= 2:
        age = age[0]

    if 'younger' in query.query_tag_structure:
        debug_print(f'количество артистов до {age} лет')
    elif 'older' in query.query_tag_structure:
        debug_print(f'количество артистов от {age} лет')
    return DialogState.number


def set_result_len(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    result_len = get_arguments_by_type(query, 'NumArgument')[-1]
    debug_print(f'Выводить по {result_len} строк')
    return DialogState.count_filter


def filter_by_sex_include(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    # debug_debug_print(f'Убрать всех, кроме {sex} пола')
    return DialogState.filter


def filter_by_sex_exclude(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    debug_print(f'Убрать артистов {sex} пола')
    return DialogState.filter


def filter_by_age_range(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) >= 2:
        from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
        debug_print(f'фильтр от {from_age} до {to_age} лет')
    else:
        return
    return DialogState.filter


def filter_by_age_include(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) > 1:
        age = age[0]
    if 'younger' in query.query_tag_structure:
        debug_print(f'фильтр до {age} лет')
    elif 'older' in query.query_tag_structure:
        debug_print(f'фильтр от {age} лет')
    return DialogState.filter


def filter_by_age_exclude(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) > 1:
        age = age[0]
    if 'younger' in query.query_tag_structure:
        debug_print(f'фильтр от {age} лет')
    elif 'older' in query.query_tag_structure:
        debug_print(f'фильтр до {age} лет')
    return DialogState.filter


def filter_by_members_count(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    tags = query.query_tag_structure
    if 'group' in tags:
        members_count_type = 'group'
    elif 'solo' in tags:
        members_count_type = 'solo'
    elif 'duet' in tags:
        members_count_type = 'duet'
    debug_print(f'оставить {members_count_type}')
    return DialogState.filter


def remove_result_len_filter(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    return DialogState.filter


def remove_filters(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    return DialogState.filter


restart_handler = QueryHandler(
    QueryPattern([And('restart')]),
    restart, 'Рестарт')

filter_by_sex_include_handler = QueryHandler(
    QueryPattern([Or('include'), Or('artist')], 'SexArgument'),
    filter_by_sex_include, 'Фильтр по полу')

filter_by_sex_exclude_handler = QueryHandler(
    QueryPattern([Or('exclude'), Or('artist')], 'SexArgument'),
    filter_by_sex_exclude, 'Фильтр по полу')

# filter_by_age_include_handler = QueryHandler(QueryPattern([And('include'), AndMulti([Or('older'), Or('younger')])]), filter_by_age_include, 'Фильтр по возрасту')

filter_by_age_range_handler = QueryHandler(
    QueryPattern([Or('range'), OrMulti([And('older'), And('younger')])], required_arguments={'NumArgument': 2}),
    filter_by_age_range, 'Фильтр по возрасту в диапазоне')

filter_by_age_include_handler = QueryHandler(
    QueryPattern([AndMulti([Or('older'), Or('younger')])], 'NumArgument'),
    filter_by_age_include, 'Фильтр по возрасту')

filter_by_age_exclude_handler = QueryHandler(
    QueryPattern([And('exclude'), AndMulti([Or('older'), Or('younger')])], 'NumArgument'),
    filter_by_age_exclude, 'Фильтр по возрасту')

set_result_len_handler = QueryHandler(
    QueryPattern([And('show')], 'NumArgument'),
    set_result_len, 'Изменить количество выводимых результатов')

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
    QueryPattern([And('dislike'), And('exclude')]),
    like, 'Лайк')

exclude_like_handler = QueryHandler(
    QueryPattern([And('like'), And('exclude')]),
    dislike, 'Дизлайк')

like_handler = QueryHandler(
    QueryPattern([And('like')]),
    like, 'Лайк')

dislike_handler = QueryHandler(
    QueryPattern([And('dislike')]),
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

search_by_genre_handler = QueryHandler(
    QueryPattern([Or('genre'), Or('recommend'), Or('show')], 'GenreArgument'),
    search_by_genre, 'Вывести артистов в определённом жанре')

search_by_artist_handler = QueryHandler(
    QueryPattern([Or('search'), Or('recommend'), Or('show')], 'ArtistArgument'),
    search_by_artist, 'Рекомендация по артисту')

show_all_handler = QueryHandler(
    QueryPattern([And('all'), AndMulti([Or('include'), Or('artist')])]),
    show_all_artists, 'Вывести всех артистов в базе')

info_handler = QueryHandler(
    QueryPattern([Or('talk about'), Or('about'), Or('info')], 'ArtistArgument'),
    info, 'Информация об артисте')


if __name__ == "__main__":
    log_query_pattern_strings()