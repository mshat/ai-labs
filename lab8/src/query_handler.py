from typing import List, Callable, Tuple, Dict
from lab8.src.query import Query, Word, Argument
from lab8.src.tag_condition import PatternMatcher, AndMultiTagCondition, OrMultiTagCondition, AndTagCondition, OrTagCondition
from lab8.src.config import SHOW_QUERY_PATTERNS, DEBUG

QUERY_PATTERN_STRINGS = []

ALL = -1


def log_query_pattern_strings():
    with open('query_pattern_strings.txt', 'w', encoding='utf-8') as f:
        # for line in sorted(QUERY_PATTERN_STRINGS, key=lambda s: s[:55]):
        for line in QUERY_PATTERN_STRINGS:
            f.write(f'{line}\n')


class QueryPattern:
    def __init__(
            self,
            conditions: List[AndTagCondition | OrTagCondition | AndMultiTagCondition | OrMultiTagCondition],
            required_argument_type: str = None,
            required_arguments: Dict[str, int] = None,
    ):
        self.pattern_matcher = PatternMatcher(conditions)
        self.conditions = conditions
        self.required_argument_type = required_argument_type
        self.required_arguments = required_arguments
        assert not (required_argument_type and required_arguments)

    def match(self, query: Query) -> Tuple[bool, List[Word], List[Argument]]:
        query_tag_structure = query.query_tag_structure
        res = None
        all_used_words = []
        used_args = []

        if self.required_argument_type:
            if self.required_argument_type in query.arguments:
                res = True
                used_args = query.arguments[self.required_argument_type][:1]
            else:
                res = False

        if self.required_arguments:
            for arg_type, num in self.required_arguments.items():
                if arg_type in query.arguments:
                    required_arguments_num = len(query.arguments[arg_type])
                    if num == ALL and required_arguments_num > 0:
                        res = True
                        used_args = query.arguments[arg_type]
                    elif required_arguments_num >= num:
                        res = True
                        used_args = query.arguments[arg_type][:num]
                    else:
                        res = False
                else:
                    res = False

        match_res, used_words = self.pattern_matcher.match_pattern(query_tag_structure)
        if match_res:
            all_used_words += used_words
        if res is None:
            res = match_res
        else:
            res *= match_res
        return res, all_used_words, used_args

    def __str__(self):
        conditions = ' '.join([str(cond) for cond in self.conditions])
        conditions_without_first_word = conditions.split()[1:]
        conditions = ' '.join(conditions_without_first_word)
        if self.required_argument_type:
            arguments = f'{self.required_argument_type}: 1'
        elif self.required_arguments:
            arguments = ' '.join([f'{argument}: {num if num != ALL else "ALL"}'
                                  for argument, num in self.required_arguments.items()])
        else:
            arguments = ''

        return f'Аргументы: {arguments.ljust(20)} | Условие: {conditions}'


class QueryHandler:
    pattern: QueryPattern
    handle: Callable

    def __init__(self, pattern: QueryPattern, handle_func: Callable, debug_msg: str = '', debug_res: str = ''):
        self.pattern = pattern
        self.handle = handle_func
        self.debug_msg = debug_msg
        self.debug_res = debug_res

        self.used_keywords = []
        self.used_args = []

        QUERY_PATTERN_STRINGS.append(self.__str__())
        if SHOW_QUERY_PATTERNS:
            print(self.__str__())

    def match_pattern(self, query: Query):
        res, self.used_keywords, self.used_args = self.pattern.match(query)
        if res:
            if DEBUG:
                print(f'Запрос: {self.debug_msg}')
        return res

    def remove_used_keywords_and_args(self, query: Query):
        # print(f'!!!!!!!! BEFOIRE {query}')
        for word in self.used_keywords:
            query.remove_word(word)
        for arg in self.used_args:
            query.remove_argument(arg)
        # print(f'!!!!!!!!!! AFTER {query}')

    def __str__(self):
        return f'Запрос: {self.debug_msg.ljust(46)} | Паттерн: {self.pattern}'