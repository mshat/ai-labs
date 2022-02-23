from typing import List
from lab8.src.query_handling import handlers
from lab8.src.sentence_analyzer.query import Query
from lab8.src.query_solving.dialog_state import DialogState
from lab8.src.config import DEBUG
from lab8.src.query_handling.query_handler import QueryHandler
from lab8.src.query_solving.user import User
import lab8.src.query_handling.handling_functions as handling_functions


class QuerySolver:
    def __init__(self, user: User):
        self._state = DialogState.start
        self._user = user
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

    def match_patterns(self, handlers_: List[QueryHandler], query: Query, show=True) -> str | None:
        for handler in handlers_:
            if handler.match_pattern(query):
                self.state = handler.handle(query, self._user, show)
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
        search_handler = handlers.search_by_artist_handler
        if search_handler.match_pattern(query):
            self.state = search_handler.handle(query, self._user)
            search_handler.remove_used_keywords_and_args(query)
            used_filter = self.solve_multi_filters(query)
            handling_functions.show_recommendations(self._user)
            return search_handler.handle.__name__

        search_handlers = [
            handlers.recommendation_handler,
            handlers.search_by_sex_handler,
            handlers.search_by_age_range_handler,
            handlers.search_by_age_handler,
            handlers.search_by_genre_handler,
            handlers.show_all_handler,
        ]
        return self.match_patterns(search_handlers, query)

    def match_info_patterns(self, query: Query):
        info_handlers = [
            handlers.info_handler,
            handlers.info_about_bot_algorithm_handler,
            handlers.info_about_bot_handler,
            handlers.info_about_bot_opportunities_handler,
        ]
        return self.match_patterns(info_handlers, query)

    def match_filter_patterns(self, query: Query, show=True) -> str | None:
        filter_handlers = [
            handlers.filter_by_sex_exclude_handler,
            handlers.filter_by_sex_include_handler,
            handlers.filter_by_age_range_handler,
            handlers.filter_by_age_exclude_handler,
            handlers.filter_by_age_include_handler,
            handlers.filter_by_members_count_handler,
            handlers.filter_output_len_handler,
            handlers.remove_filters_handler,
            handlers.remove_result_len_filter_handler,
        ]
        return self.match_patterns(filter_handlers, query, show=show)

    def solve_multi_filters(self, query: Query):
        last_res = None
        while True:
            res = self.match_filter_patterns(query, show=False)
            if res is None:
                break
            else:
                last_res = res

        return last_res

    def solve(self, query: Query):
        # restart
        res = self.match_restart_patterns(query)
        if res: return res

        # set output len
        res = self.match_patterns([handlers.set_output_len_handler], query)
        if res: return res

        # filters
        if self.state in (DialogState.search, DialogState.filter, DialogState.count_filter):
            res = self.match_filter_patterns(query)
            if res:
                return res
            else:
                self.state = DialogState.start

        # like/dislike, number query, search, info
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





