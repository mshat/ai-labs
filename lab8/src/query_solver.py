import handlers
from query import Query
from dialog_state import DialogState
from config import DEBUG


class QuerySolver:
    def __init__(self):
        self._state = DialogState.start
        self.response = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val

    def unknown(self, query: Query):
        print('Я не понял вопрос')
        if DEBUG:
            print(f'[DEBUG KEYWORDS] {query.arguments} {query.keywords} {query.words}')

    def find_like_dislike_patterns(self, query: Query):
        next_state = handlers.exclude_dislike_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'like'

        next_state = handlers.exclude_like_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'dislike'

        next_state = handlers.like_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'like'

        next_state = handlers.dislike_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'dislike'

    def find_number_query_patterns(self, query: Query):
        next_state = handlers.number_with_sex_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'number_with_sex'

        next_state = handlers.number_with_age_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'number_with_age'

        next_state = handlers.number_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'number'

    def find_search_patterns(self, query: Query):
        next_state = handlers.search_by_sex_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'search_by_sex'

        next_state = handlers.search_by_genre_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'search_by_genre'

        next_state = handlers.search_by_artist_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'search_by_artist'

        next_state = handlers.show_all_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'show_all_artists'

    def find_info_patterns(self, query: Query):
        next_state = handlers.info_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'info'

    def find_filter_patterns(self, query: Query):
        next_state = handlers.filter_by_sex_include_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'filter_by_sex'

        next_state = handlers.filter_by_sex_exclude_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'filter_by_sex'

        next_state = handlers.filter_by_age_include_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'filter_by_age_include'

        next_state = handlers.filter_by_age_exclude_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'filter_by_age_exclude'

        next_state = handlers.set_result_len_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'set_result_len'

        next_state = handlers.filter_by_members_count_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'filter_by_members_count'

        next_state = handlers.remove_filters_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'remove_filters'

        next_state = handlers.remove_result_len_filter_handler.match_pattern(query)
        if next_state:
            self.state = next_state
            return 'remove_result_len_filter'

    def solve(self, query: Query):
        next_state = handlers.restart_handler.match_pattern(query)
        if next_state:
            self.state = next_state
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

        self.unknown(query)





