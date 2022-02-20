from typing import Tuple, List
import handlers
from query import Query
from dialog_state import DialogState
from config import DEBUG
from query_handler import QueryHandler


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
            print(f'[UNRECOGNIZED SENTENCE] {query.arguments} {query.keywords} {query.words}')

    def match_patterns(self, handlers_: List[QueryHandler], query: Query) -> str | None:
        for handler in handlers_:
            if handler.match_pattern(query):
                self.state = handler.handle(query)
                handler.remove_used_keywords_and_args(query)
                return handler.handle.__name__

    def match_restart_patterns(self, query: Query):
        restart_handler = handlers.restart_handler
        return self.match_patterns([restart_handler], query)

    def match_like_dislike_patterns(self, query: Query):
        like_dislike_handlers = [
            handlers.exclude_dislike_handler,
            handlers.exclude_like_handler,
            handlers.like_handler,
            handlers.dislike_handler
        ]
        return self.match_patterns(like_dislike_handlers, query)

    def match_number_query_patterns(self, query: Query):
        number_query_handlers = [
            handlers.number_with_sex_handler,
            handlers.number_with_age_range_handler,
            handlers.number_with_age_handler,
            handlers.number_handler,
        ]
        return self.match_patterns(number_query_handlers, query)

    def match_search_patterns(self, query: Query):
        search_handlers = [
            handlers.search_by_artist_handler,
            handlers.search_by_sex_handler,
            handlers.search_by_genre_handler,
            handlers.show_all_handler,
        ]
        res = self.match_patterns(search_handlers, query)
        if res:
            if query.query_tag_structure:
                self.solve_multi_filters(query)
        return res

    def match_info_patterns(self, query: Query):
        info_handlers = [
            handlers.info_handler,
        ]
        return self.match_patterns(info_handlers, query)

    def match_filter_patterns(self, query: Query) -> str | None:
        filter_handlers = [
            handlers.filter_by_sex_include_handler,
            handlers.filter_by_sex_exclude_handler,
            handlers.filter_by_age_range_handler,
            handlers.filter_by_age_exclude_handler,
            handlers.filter_by_age_include_handler,

            handlers.set_result_len_handler,
            handlers.filter_by_members_count_handler,
            handlers.remove_filters_handler,
            handlers.remove_result_len_filter_handler,
        ]
        return self.match_patterns(filter_handlers, query)

    def solve_multi_filters(self, query: Query):
        last_res = None
        while True:
            res = self.match_filter_patterns(query)
            if res is None:
                break
            else:
                last_res = res

        return last_res

    def solve(self, query: Query):
        res = self.match_restart_patterns(query)
        if res: return res

        if self.state in (DialogState.search, DialogState.filter, DialogState.count_filter):
            res = self.match_filter_patterns(query)
            if res:
                return res
            else:
                self.state = DialogState.start

        if self.state in (DialogState.start, DialogState.number, DialogState.like, DialogState.dislike, DialogState.info):
            res = self.match_like_dislike_patterns(query)
            if res: return res

            res = self.match_number_query_patterns(query)
            if res: return res

            res = self.match_search_patterns(query)
            if res: return res

            res = self.match_info_patterns(query)
            if res: return res

        self.unknown(query)





