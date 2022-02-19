from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict
from data import keywords


class PatternMatcher:  # TODO как-то вынести в отдельный модуль, разрешив циклический импорт
    def __init__(
            self,
            conditions: List[AndTagCondition | OrTagCondition | AndMultiTagCondition, OrMultiTagCondition],
    ):
        self.conditions = conditions

    def match_pattern(self, query_tag_structure: dict) -> bool:
        res = None

        for condition in self.conditions:
            if isinstance(condition, AndTagCondition) or isinstance(condition, AndMultiTagCondition):
                if res is None:
                    res = condition.solve(query_tag_structure)
                else:
                    res *= condition.solve(query_tag_structure)
            elif isinstance(condition, OrTagCondition) or isinstance(condition, OrMultiTagCondition):
                if res is None:
                    res = condition.solve(query_tag_structure)
                else:
                    res += condition.solve(query_tag_structure)
        return res


class BaseTagCondition(ABC):
    @abstractmethod
    def solve(self, query_tag_structure: Dict) -> bool:
        pass


class TagCondition(BaseTagCondition):
    """
    Условие - составная часть паттерна запроса.
    Инициализируется тэгом, который должен быть найден в запросе, чтобы паттерн подошел к запросу
    """

    def __init__(self, tag: str):
        assert tag in keywords
        self.tag = tag

    def solve(self, query_tag_structure: Dict):
        if self.tag in query_tag_structure:
            return True
        else:
            return False


class AndTagCondition(TagCondition):
    """
    Условие "И"
    Такое условие должно обязательно выполняться для запроса, чтобы паттерн подошел к нему
    """
    def __str__(self):
        return f'AND {self.tag}'

    def __repr__(self):
        return self.__str__()


class OrTagCondition(TagCondition):
    """
    Условие "ИЛИ"
    Результат проверки такого условия будет учитываться как логическое СЛОЖЕНИЕ при сопоставлении паттерна с запросом
    """
    def __str__(self):
        return f'OR {self.tag}'

    def __repr__(self):
        return self.__str__()


class MultiTagCondition(BaseTagCondition):
    """
    Составное условие - составная часть паттерна запроса.
    """

    def __init__(self, conditions: List[AndTagCondition | OrTagCondition]):
        self.pattern_matcher = PatternMatcher(conditions)
        self.conditions = conditions

    def solve(self, query_tag_structure: Dict) -> bool:
        res = self.pattern_matcher.match_pattern(query_tag_structure)
        return res if res else False


class AndMultiTagCondition(MultiTagCondition):
    """
    Мультиусловиеусловие "И"
    Такое условие должно обязательно выполняться для запроса, чтобы паттерн подошел к нему
    """
    def __str__(self):
        conditions = ' '.join([str(condition) for condition in self.conditions])
        conditions_without_first_word = conditions.split()[1:]
        conditions = ' '.join(conditions_without_first_word)
        return f'AND ({conditions})'

    def __repr__(self):
        return self.__str__()


class OrMultiTagCondition(MultiTagCondition):
    """
    Мультиусловие "ИЛИ"
    Результат проверки такого условия будет учитываться как логическое СЛОЖЕНИЕ при сопоставлении паттерна с запросом
    """
    def __str__(self):
        conditions = ' '.join([str(condition) for condition in self.conditions])
        conditions_without_first_word = conditions.split()[1:]
        conditions = ' '.join(conditions_without_first_word)
        return f'OR ({conditions})'

    def __repr__(self):
        return self.__str__()