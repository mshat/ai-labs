from typing import List, Callable, Tuple
from query import Query, Word, Argument
from tag_condition import PatternMatcher, AndMultiTagCondition, OrMultiTagCondition, AndTagCondition, OrTagCondition
from config import SHOW_QUERY_PATTERNS, DEBUG

QUERY_PATTERN_STRINGS = []


def log_query_pattern_strings():
    with open('query_pattern_strings.txt', 'w', encoding='utf-8') as f:
        # for line in sorted(QUERY_PATTERN_STRINGS, key=lambda s: s[:55]):
        for line in QUERY_PATTERN_STRINGS:
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

    def match(self, query: Query) -> Tuple[bool, List[Word], Argument]:
        query_tag_structure = query.query_tag_structure
        res = None
        all_used_words = []
        used_arg = None

        if self.required_argument_type:
            if self.required_argument_type in query.arguments:
                res = True
                used_arg = query.arguments[self.required_argument_type]
            else:
                res = False

        match_res, used_words = self.pattern_matcher.match_pattern(query_tag_structure)
        if match_res:
            all_used_words += used_words
        if res is None:
            res = match_res
        else:
            res *= match_res
        return res, all_used_words, used_arg

    def __str__(self):
        conditions = ' '.join([str(cond) for cond in self.conditions])
        conditions_without_first_word = conditions.split()[1:]
        conditions = ' '.join(conditions_without_first_word)

        return f'Необходимый аргумент: {str(self.required_argument_type).ljust(14)} | Условие: {conditions}'


class QueryHandler:
    pattern: QueryPattern
    handle: Callable

    def __init__(self, pattern: QueryPattern, handle_func: Callable, debug_msg: str = '', debug_res: str = ''):
        self.pattern = pattern
        self.handle = handle_func
        self.debug_msg = debug_msg
        self.debug_res = debug_res

        QUERY_PATTERN_STRINGS.append(self.__str__())
        if SHOW_QUERY_PATTERNS:
            print(self.__str__())

    def match_pattern(self, query: Query):
        res, used_words, used_arg = self.pattern.match(query)
        if res:
            if DEBUG:
                print(f'Запрос: {self.debug_msg}')
        return res

            #return self.handle(query)  # TODO вернуть used_words

    def __str__(self):
        return f'Запрос: {self.debug_msg.ljust(46)} | Паттерн: {self.pattern}'