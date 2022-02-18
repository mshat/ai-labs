import enum
from query import Query


DEBUG = True


def debug_print(msg: str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if DEBUG:
                print(f'[DEBUG] {msg}')
            function(*args, **kwargs)

        return wrapper
    return decorator


class DialogState(enum.Enum):
    start = 1
    search = 2
    filter = 3
    count_filter = 4
    number = 5
    like = 6
    dislike = 7
    info = 8


class QuerySolver:
    def __init__(self):
        self._state = DialogState.start
        # self.state = DialogState.search
        self.response = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val

    def _get_arguments_by_type(self, query: Query, argument_type: str):
        return [argument for argument_type, arguments in query.arguments.items() for argument in arguments if argument_type == argument_type]

    @debug_print('Рестарт')
    def restart(self):
        self.state = DialogState.start
        self.response = None

    @debug_print('Поставить лайк')
    def like(self, query: Query):
        self.state = DialogState.like
        allowed_states = (DialogState.search, DialogState.start)
        artists = self._get_arguments_by_type(query, 'ArtistArgument')

    @debug_print('Поставить дизлайк')
    def dislike(self, query: Query):
        self.state = DialogState.dislike
        allowed_states = (DialogState.search, DialogState.start)
        artists = self._get_arguments_by_type(query, 'ArtistArgument')

    @debug_print('Вывести всех артистов в базе')
    def show_all_artists(self, query: Query):
        self.state = DialogState.search
        allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)

    @debug_print('Рекомендация по артисту')
    def search_by_artist(self, query: Query):
        self.state = DialogState.search
        allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
        artists = self._get_arguments_by_type(query, 'ArtistArgument')

    @debug_print('Вывести артистов в определённом жанре')
    def search_by_genre(self, query: Query):
        self.state = DialogState.search
        allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
        genres = self._get_arguments_by_type(query, 'GenreArgument')

    @debug_print('Вывести исполнителей указанного пола')
    def search_by_sex(self, query: Query):
        self.state = DialogState.search
        allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
        sex = self._get_arguments_by_type(query, 'SexArgument')[0]

    @debug_print('Информация об артисте')
    def info(self, query: Query):
        self.state = DialogState.info
        allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
        artists = self._get_arguments_by_type(query, 'ArtistArgument')

    @debug_print('Количество артистов в базе')
    def number(self, query: Query):
        self.state = DialogState.number
        allowed_states = (DialogState.number, DialogState.search, DialogState.start)
        print(query.arguments.items())

    @debug_print('Количество артистов указанного пола в базе')
    def number_with_sex(self, query: Query):
        self.state = DialogState.number
        allowed_states = (DialogState.number, DialogState.search, DialogState.start)
        sex = self._get_arguments_by_type(query, 'SexArgument')[0]

    @debug_print('Количество артистов указанного пола в базе')
    def number_with_age(self, query: Query):
        self.state = DialogState.number
        allowed_states = (DialogState.number, DialogState.search, DialogState.start)
        age = self._get_arguments_by_type(query, 'NumArgument')
        # if len(age) == 2:
        #     from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
        #     print(f'количество артистов от {from_age} до {to_age} лет')
        # else:
        #     if 'younger' in query.tags_query_structure:
        #         print(f'количество артистов до {age} лет')
        #     elif 'older' in query.tags_query_structure:
        #         print(f'количество артистов от {age} лет')

    @debug_print('Изменить количество выводимых результатов')
    def set_result_len(self, query: Query):
        self.state = DialogState.count_filter
        allowed_states = (DialogState.filter, DialogState.start)
        result_len = self._get_arguments_by_type(query, 'NumArgument')

    @debug_print('Фильтр по полу')
    def filter_by_sex(self, query: Query):
        self.state = DialogState.filter
        allowed_states = (DialogState.filter, DialogState.start)
        sex = self._get_arguments_by_type(query, 'SexArgument')[0]

    @debug_print('Фильтр по возрасту')
    def filter_by_age_include(self, query: Query):
        self.state = DialogState.filter
        allowed_states = (DialogState.filter, DialogState.start)
        age = self._get_arguments_by_type(query, 'NumArgument')
        if len(age) == 2:
            from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
            print(f'фильтр от {from_age} до {to_age} лет')
        else:
            if 'younger' in query.tags_query_structure:
                print(f'фильтр до {age} лет')
            elif 'older' in query.tags_query_structure:
                print(f'фильтр от {age} лет')

    @debug_print('Фильтр по возрасту')
    def filter_by_age_exclude(self, query: Query):
        self.state = DialogState.filter
        allowed_states = (DialogState.filter, DialogState.start)
        age = self._get_arguments_by_type(query, 'NumArgument')
        if len(age) == 2:
            from_age, to_age = sorted(age)
            print(f'фильтр от {from_age} до {to_age} лет')
        else:
            if 'younger' in query.tags_query_structure:
                print(f'фильтр от {age} лет')
            elif 'older' in query.tags_query_structure:
                print(f'фильтр до {age} лет')

    @debug_print('Фильтр по количеству участников коллектива')
    def filter_by_members_count(self, query: Query):
        self.state = DialogState.filter
        allowed_states = (DialogState.filter, DialogState.start)
        tags = query.tags_query_structure
        if 'group' in tags:
            members_count_type = 'group'
        elif 'solo' in tags:
            members_count_type = 'solo'
        elif 'duet' in tags:
            members_count_type = 'duet'
        print(f'оставить {members_count_type}')

    @debug_print('Удалить ограничение количества выводимых строк')
    def remove_result_len_filter(self, query):
        self.state = DialogState.filter
        allowed_states = (DialogState.filter, DialogState.start)

    @debug_print('Удалить все фильтры')
    def remove_filters(self, query: Query):
        self.state = DialogState.filter
        allowed_states = (DialogState.filter, DialogState.start)

    def unknown(self):
        print('Я не понял вопрос')

    ##
    def find_like_dislike_patterns(self, query: Query):
        tags = query.tags_query_structure
        if 'dislike' in tags and 'exclude' in tags:
            self.like(query)
            return 'like'
        if 'dislike' in tags:
            self.dislike(query)
            return 'dislike'
        if 'like' in tags and 'exclude' in tags:
            self.dislike(query)
            return 'dislike'
        if 'like' in tags:
            self.like(query)
            return 'like'

    def find_number_query_patterns(self, query: Query):
        tags = query.tags_query_structure
        arguments = query.arguments
        if ('number' in tags or 'how many' in tags) and 'SexArgument' in arguments:
            self.number_with_sex(query)
            return 'number_with_sex'
        if ('number' in tags or 'how many' in tags) and ('NumArgument' in arguments or 'older' in tags or 'younger' in tags):
            self.number_with_age(query)
            return 'number_with_age'
        if 'number' in tags or 'how many' in tags:
            self.number(query)
            return 'number'

    def find_search_patterns(self, query: Query):
        tags = query.tags_query_structure
        arguments = query.arguments
        if 'SexArgument' in arguments and ('filter' in tags or 'artist' in tags):
            self.search_by_sex(query)
            return 'search_by_sex'
        if 'genre' in tags and 'GenreArgument' in arguments:
            self.search_by_genre(query)
            return 'search_by_genre'
        if 'search' in tags and 'ArtistArgument' in arguments:
            self.search_by_artist(query)
            return 'search_by_artist'
        if 'all' in tags and ('include' in tags or 'artist' in tags):
            self.show_all_artists(query)
            return 'show_all_artists'

    def find_info_patterns(self, query: Query):
        tags = query.tags_query_structure
        arguments = query.arguments
        if 'ArtistArgument' in arguments and ('show' in tags or 'about' in tags or 'info' in tags):
            self.info(query)
            return 'info'

    def find_filter_patterns(self, query: Query):
        tags = query.tags_query_structure
        arguments = query.arguments
        if 'SexArgument' in arguments and ('filter' in tags or 'artist' in tags):
            self.filter_by_sex(query)
            return 'filter_by_sex'
        if ('older' in tags or 'younger' in tags) and 'include' in tags:
            self.filter_by_age_include(query)
            return 'filter_by_age_include'
        if ('older' in tags or 'younger' in tags) and 'exclude' in tags:
            self.filter_by_age_exclude(query)
            return 'filter_by_age_exclude'
        if 'include' in tags and 'NumArgument' in arguments:
            self.set_result_len(query)
            return 'set_result_len'
        if 'group' in tags or 'solo' in tags or 'duet' in tags:
            self.filter_by_members_count(query)
            return 'filter_by_members_count'
        if 'exclude' in tags and 'all' in tags:
            self.remove_filters(query)
            return 'remove_filters'
        if ('exclude' in tags or 'include' in tags) and ('all' in tags or 'number' in tags):
            self.remove_result_len_filter(query)
            return 'remove_result_len_filter'

    def solve(self, query: Query):
        tags = query.tags_query_structure
        if 'restart' in tags:
            self.restart()
            return 'restart'
        if self.state in (DialogState.search, DialogState.filter, DialogState.count_filter):
            res = self.find_filter_patterns(query)
            if res:
                return res
            else:
                self.state = DialogState.start

        if self.state in (DialogState.start, DialogState.number, DialogState.like, DialogState.dislike, DialogState.info):
            res = self.find_like_dislike_patterns(query)
            if res: return res

            res = self.find_number_query_patterns(query)
            if res: return res

            res = self.find_search_patterns(query)
            if res: return res

            res = self.find_info_patterns(query)
            if res: return res

        self.unknown()





