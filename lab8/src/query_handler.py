from typing import List, Callable
from query import Query
from tag_condition import PatternMatcher, AndMultiTagCondition, OrMultiTagCondition, AndTagCondition, OrTagCondition
from config import SHOW_QUERY_PATTERNS, DEBUG

QUERY_PATTERN_STRINGS = set()


def log_query_pattern_strings():
    with open('query_pattern_strings.txt', 'w', encoding='utf-8') as f:
        for line in sorted(QUERY_PATTERN_STRINGS, key=lambda s: s[:55]):
            f.write(f'{line}\n')


class QueryPattern:
    def __init__(
            self,
            conditions: List[AndTagCondition | OrTagCondition | AndMultiTagCondition | OrMultiTagCondition],
            required_argument_type: str = None
    ):
        self.pattern_matcher = PatternMatcher(conditions)
        self.conditions = conditions
        self.required_argument_type = required_argument_type

    def match_pattern(self, query: Query):
        query_tag_structure = query.query_tag_structure
        res = None

        if self.required_argument_type:
            res = self.required_argument_type in query.arguments

        if res is None:
            res = self.pattern_matcher.match_pattern(query_tag_structure)
        else:
            res *= self.pattern_matcher.match_pattern(query_tag_structure)
        return res

    def __str__(self):
        conditions = ', '.join([str(cond) for cond in self.conditions])
        return f'Необходимый аргумент: {self.required_argument_type} | Условия: {conditions}'


class QueryHandler:
    pattern: QueryPattern
    handle: Callable

    def __init__(self, pattern: QueryPattern, handle_func: Callable, debug_msg: str = ''):
        self.pattern = pattern
        self.handle = handle_func
        self.debug_msg = debug_msg

        if SHOW_QUERY_PATTERNS:
            QUERY_PATTERN_STRINGS.add(self.__str__())
            print(self.__str__())

    def match_pattern(self, query: Query):
        if self.pattern.match_pattern(query):
            if DEBUG:
                print(f'Запрос: {self.debug_msg}')

            return self.handle(query)

    def __str__(self):
        return f'Запрос: {self.debug_msg.ljust(46)} | Паттерн: {self.pattern}'