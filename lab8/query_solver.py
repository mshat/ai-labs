import enum
from query import Query


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
        self.state = DialogState.start
        # self.state = DialogState.search
        self.response = None

    def _get_arguments_by_type(self, query: Query, argument_type: str):
        return [argument for argument_type, arguments in query.arguments.items() for argument in arguments if argument_type == argument_type]

    def restart(self):
        self.state = DialogState.start
        self.response = None
        print('рестарт')

    def like(self, query: Query):
        allowed_states = (DialogState.search, DialogState.start)
        artists = self._get_arguments_by_type(query, 'ArtistArgument')
        print(f'лайк: {artists}')

    def dislike(self, query: Query):
        allowed_states = (DialogState.search, DialogState.start)
        artists = self._get_arguments_by_type(query, 'ArtistArgument')
        print(f'дизлайк: {artists}')

    def show_all_artists(self, query: Query):
        allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
        print(f'вывести всех артистов в базе')

    def search_by_artist(self, query: Query):
        allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
        artists = self._get_arguments_by_type(query, 'ArtistArgument')
        print(f'поиск по артисту: {artists}')

    def search_by_genre(self, query: Query):
        allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
        genres = self._get_arguments_by_type(query, 'GenreArgument')
        print(f'поиск по жанру: {genres}')

    def search_by_sex(self, query: Query):
        allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
        sex = self._get_arguments_by_type(query, 'SexArgument')[0]
        print(f'вывести исполнителей {sex} пола')

    def info(self, query: Query):
        allowed_states = (DialogState.filter, DialogState.count_filter, DialogState.start)
        artists = self._get_arguments_by_type(query, 'ArtistArgument')
        print(f'информация об артисте: {artists}')

    def number(self, query: Query):
        allowed_states = (DialogState.number, DialogState.search, DialogState.start)
        print(query.arguments.items())
        print('количество артистов в базе')

    def number_with_sex(self, query: Query):
        allowed_states = (DialogState.number, DialogState.search, DialogState.start)
        sex = self._get_arguments_by_type(query, 'SexArgument')[0]
        print(f'количество артистов {sex} пола в базе')

    def number_with_age(self, query: Query):
        allowed_states = (DialogState.number, DialogState.search, DialogState.start)
        age = self._get_arguments_by_type(query, 'NumArgument')
        if len(age) == 2:
            from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
            print(f'количество артистов от {from_age} до {to_age} лет')
        else:
            if 'younger' in query.tags_query_structure:
                print(f'количество артистов до {age} лет')
            elif 'older' in query.tags_query_structure:
                print(f'количество артистов от {age} лет')

    def set_result_len(self, query: Query):
        allowed_states = (DialogState.filter, DialogState.start)
        result_len = self._get_arguments_by_type(query, 'NumArgument')
        print(f'размер выборки: {result_len}')

    def filter_by_sex(self, query: Query):
        allowed_states = (DialogState.filter, DialogState.start)
        sex = self._get_arguments_by_type(query, 'SexArgument')[0]
        print(f'фильтр по полу: {sex}')

    def filter_by_age_include(self, query: Query):
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

    def filter_by_age_exclude(self, query: Query):
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

    def filter_by_members_count(self, query: Query):
        allowed_states = (DialogState.filter, DialogState.start)
        tags = query.tags_query_structure
        if 'group' in tags:
            members_count_type = 'group'
        elif 'solo' in tags:
            members_count_type = 'solo'
        elif 'duet' in tags:
            members_count_type = 'duet'
        print(f'оставить {members_count_type}')

    def remove_result_len_filter(self, query):
        allowed_states = (DialogState.filter, DialogState.start)
        print('выводить всю выборку без ограничения на количество')

    def remove_age_filter(self, query):
        allowed_states = (DialogState.filter, DialogState.start)
        print('удалить фильтр возраста')

    def remove_sex_filter(self, query):
        allowed_states = (DialogState.filter, DialogState.start)
        print('удалить фильтр пола')

    def remove_members_count_filter(self, query):
        allowed_states = (DialogState.filter, DialogState.start)
        print('удалить фильтр количества артистов')

    def remove_filters(self, query: Query):
        allowed_states = (DialogState.filter, DialogState.start)
        print('удалить все фильтры')

    def count_filter(self, query: Query):
        allowed_states = (DialogState.filter, DialogState.start)
        print(query.arguments.items())
        print('количественный фильтр')

    def unknown(self):
        print('Я не понял вопрос')

    def solve(self, query: Query):
        query_structure = query.query_structure
        tags = query.tags_query_structure
        arguments = query.arguments
        if 'restart' in query_structure:
            self.restart()
            return 'restart'
        if self.state == DialogState.start:
            if 'dislike' in query_structure and 'exclude' in tags:
                self.like(query)
                return 'like'
            if 'dislike' in query_structure:
                self.dislike(query)
                return 'dislike'
            if 'like' in query_structure and 'exclude' in tags:
                self.dislike(query)
                return 'dislike'
            if 'like' in query_structure:
                self.like(query)
                return 'like'
            if 'number' in query_structure and 'SexArgument' in arguments:
                self.number_with_sex(query)
                return 'number_with_sex'
            if 'number' in query_structure and ('NumArgument' in arguments or 'older' in tags or 'younger' in tags):
                self.number_with_age(query)
                return 'number_with_age'
            if 'number' in query_structure:
                self.number(query)
                return 'number'
            if 'SexArgument' in arguments and ('filter' in query_structure or 'artist' in tags):
                self.search_by_sex(query)
                return 'search_by_sex'
            if 'search' in query_structure and 'GenreArgument' in arguments:
                self.search_by_genre(query)
                return 'search_by_genre'
            if 'search' in query_structure and 'ArtistArgument' in arguments:
                self.search_by_artist(query)
                return 'search_by_artist'
            if 'search' in query_structure and 'all' in tags:
                self.show_all_artists(query)
                return 'show_all_artists'
            if 'info' in query_structure:
                self.info(query)
                return 'info'
            else:
                self.unknown()
        elif self.state == DialogState.search or self.state == DialogState.filter:
            if 'SexArgument' in arguments and ('filter' in query_structure or 'artist' in tags):
                self.filter_by_sex(query)
                return 'filter_by_sex'
            if 'filter' in query_structure and ('older' in tags or 'younger' in tags) and 'include' in tags:
                self.filter_by_age_include(query)
                return 'filter_by_age_include'
            if 'filter' in query_structure and ('older' in tags or 'younger' in tags) and 'exclude' in tags:
                self.filter_by_age_exclude(query)
                return 'filter_by_age_exclude'
            if 'filter' in query_structure and 'NumArgument' in arguments:
                self.set_result_len(query)
                return 'set_result_len'
            if 'filter' in query_structure and ('group' in tags or 'solo' in tags or 'duet' in tags):
                self.filter_by_members_count(query)
                return 'filter_by_members_count'
            if 'filter' in query_structure and 'exclude' in tags and 'all' in tags:
                self.remove_filters(query)
                return 'remove_filters'
            if 'filter' in query_structure and ('all' in tags or 'exclude' in tags or 'number' in tags):
                self.remove_result_len_filter(query)
                return 'remove_result_len_filter'
            if 'count_filter' in query_structure:
                self.count_filter(query)
                return 'count_filter'
            else:
                self.unknown()



