from query_handler import (Query, QueryPattern, QueryHandler, AndTagCondition as AndCond, OrTagCondition as OrCond,
                           AndMultiTagCondition as AndMulCond, OrMultiTagCondition as OrMulCond)
from dialog_state import DialogState


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
    print(query.arguments.items())
    return DialogState.number


def number_with_sex(query: Query):
    allowed_states = (DialogState.number, DialogState.search, DialogState.start)
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    return DialogState.number


def number_with_age(query: Query):
    allowed_states = (DialogState.number, DialogState.search, DialogState.start)
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) == 2:
        from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
        print(f'количество артистов от {from_age} до {to_age} лет')
    else:
        if 'younger' in query.query_tag_structure:
            print(f'количество артистов до {age} лет')
        elif 'older' in query.query_tag_structure:
            print(f'количество артистов от {age} лет')
    return DialogState.number


def set_result_len(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    result_len = get_arguments_by_type(query, 'NumArgument')
    return DialogState.count_filter


def filter_by_sex_include(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    print(f'Убрать всех, кроме {sex} пола')
    return DialogState.filter


def filter_by_sex_exclude(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    print(f'Убрать артистов {sex} пола')
    return DialogState.filter


def filter_by_age_include(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) == 2:
        from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
        print(f'фильтр от {from_age} до {to_age} лет')
    else:
        if 'younger' in query.query_tag_structure:
            print(f'фильтр до {age} лет')
        elif 'older' in query.query_tag_structure:
            print(f'фильтр от {age} лет')
    return DialogState.filter


def filter_by_age_exclude(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    age = get_arguments_by_type(query, 'NumArgument')
    if len(age) == 2:
        from_age, to_age = sorted(age)
        print(f'фильтр от {from_age} до {to_age} лет')
    else:
        if 'younger' in query.query_tag_structure:
            print(f'фильтр от {age} лет')
        elif 'older' in query.query_tag_structure:
            print(f'фильтр до {age} лет')
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
    print(f'оставить {members_count_type}')
    return DialogState.filter


def remove_result_len_filter(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    return DialogState.filter


def remove_filters(query: Query):
    allowed_states = (DialogState.filter, DialogState.start)
    return DialogState.filter


restart_handler = QueryHandler(QueryPattern([AndCond('restart')]), restart, 'Рестарт')

exclude_dislike_handler = QueryHandler(
    QueryPattern([AndCond('dislike'), AndCond('exclude')]),
    like, 'Лайк')

like_handler = QueryHandler(QueryPattern([AndCond('like')]), like, 'Лайк')

exclude_like_handler = QueryHandler(
    QueryPattern([AndCond('like'), AndCond('exclude')]),
    dislike, 'Дизлайк')

dislike_handler = QueryHandler(QueryPattern([AndCond('dislike')]), dislike, 'Дизлайк')


show_all_handler = QueryHandler(QueryPattern([AndCond('all'), AndMulCond([OrCond('include'), OrCond('artist')])]), show_all_artists, 'Вывести всех артистов в базе')

search_by_artist_handler = QueryHandler(QueryPattern([OrCond('search'), OrCond('recommend')], 'ArtistArgument'), search_by_artist, 'Рекомендация по артисту')

search_by_genre_handler = QueryHandler(QueryPattern([OrCond('genre'), OrCond('recommend')], 'GenreArgument'), search_by_genre, 'Вывести артистов в определённом жанре')

search_by_sex_handler = QueryHandler(QueryPattern([OrCond('artist'), OrCond('recommend')], 'SexArgument'), search_by_sex, 'Вывести исполнителей указанного пола')

info_handler = QueryHandler(QueryPattern([OrCond('talk about'), OrCond('about'), OrCond('info')], 'ArtistArgument'), info, 'Информация об артисте')

number_handler = QueryHandler(QueryPattern([OrCond('number'), OrCond('how many')]), number, 'Количество артистов в базе')

number_with_age_handler = QueryHandler(QueryPattern([AndMulCond([OrCond('number'), OrCond('how many')]), AndMulCond([OrCond('older'), OrCond('younger')])], 'NumArgument'), number_with_age, 'Количество артистов указанного пола в базе')

number_with_sex_handler = QueryHandler(QueryPattern([OrCond('number'), OrCond('how many')], 'SexArgument'), number_with_sex, 'Количество артистов указанного пола в базе')

set_result_len_handler = QueryHandler(QueryPattern([AndCond('show')], 'NumArgument'), set_result_len, 'Изменить количество выводимых результатов')

filter_by_sex_include_handler = QueryHandler(QueryPattern([OrCond('include'), OrCond('artist')], 'SexArgument'), filter_by_sex_include, 'Фильтр по полу')

filter_by_sex_exclude_handler = QueryHandler(QueryPattern([OrCond('exclude'), OrCond('artist')], 'SexArgument'), filter_by_sex_exclude, 'Фильтр по полу')

filter_by_age_include_handler = QueryHandler(QueryPattern([AndCond('include'), AndMulCond([OrCond('older'), OrCond('younger')])]), filter_by_age_include, 'Фильтр по возрасту')

filter_by_age_exclude_handler = QueryHandler(QueryPattern([AndCond('exclude'), AndMulCond([OrCond('older'), OrCond('younger')])]), filter_by_age_exclude, 'Фильтр по возрасту')

filter_by_members_count_handler = QueryHandler(QueryPattern([OrCond('group'), OrCond('solo'), OrCond('duet')]), filter_by_members_count, 'Фильтр по количеству участников коллектива')

remove_filters_handler = QueryHandler(QueryPattern([AndCond('exclude'), AndCond('all')]), remove_filters, 'Удалить все фильтры')

remove_result_len_filter_handler = QueryHandler(QueryPattern([AndMulCond([OrCond('show'), OrCond('exclude'), OrCond('include')]), AndMulCond([OrCond('all'), OrCond('number')])]), remove_result_len_filter, 'Удалить ограничение количества выводимых строк')

