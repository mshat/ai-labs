from typing import List
from word import Word, Placeholder
from data import ARTISTS, GENRES, GENDERS


class ArgumentError(Exception): pass
class ArtistArgumentError(ArgumentError): pass
class GenreArgumentError(ArgumentError): pass


class Argument:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'Argument: {self.value}'

    def __repr__(self):
        return self.__str__()


class NumArgument(Argument):
    def __init__(self, value: str):
        super().__init__(value)
        if not value.isdigit():
            raise ArgumentError('Wrong value type')


class StrArgument(Argument):
    def __init__(self, value: str):
        super().__init__(value)
        if not isinstance(value, str):
            raise ArgumentError('Wrong value type')


class SexArgument(StrArgument):
    def __init__(self, value: str):
        super().__init__(value)
        if self.value.lower() not in GENDERS.values():
            raise ArtistArgumentError('This sex is not found ')


class ArtistArgument(StrArgument):
    def __init__(self, value: str):
        super().__init__(value)
        if self.value.lower() not in ARTISTS:
            raise ArtistArgumentError('This artist is not found ')


class GenreArgument(StrArgument):
    def __init__(self, value: str):
        super().__init__(value)
        if self.value.lower() not in GENRES:
            raise GenreArgumentError('This genre is not found ')


class Query:
    _raw_sentence: str
    _words: List[Word]
    _arguments: List[Argument]
    is_question: bool

    def __init__(self, raw_sentence: str, words: List[Word], arguments: List[Argument] = None, is_question=True):
        self._raw_sentence = raw_sentence
        self._words = words
        self._arguments = [] if arguments is None else arguments
        self.is_question = is_question

    def remove_word(self, word: Word):
        self._words.remove(word)

    def remove_argument(self, arg: Argument):
        self._arguments.remove(arg)

    @property
    def keywords(self):
        return [word for word in self._words if isinstance(word, Placeholder) or word.tag]

    @property
    def words(self):
        return self._words

    @property
    def arguments(self) -> dict:
        arguments = {}
        for arg in self._arguments:
            key = type(arg).__name__
            if key not in arguments:
                arguments[key] = [arg]
            else:
                arguments[key].append(arg)
        return arguments

    @property
    def query_tag_structure(self) -> dict:
        query_structure = {}
        for keyword in self.keywords:
            if not isinstance(keyword, Placeholder):
                if keyword.tag not in query_structure:
                    query_structure[keyword.tag] = [keyword]
                else:
                    query_structure[keyword.tag].append(keyword)
        return query_structure

    def __str__(self):
        res = 'Предложение:\n' if not self.is_question else 'Вопросительное предложение:\n'
        res += f"\tRaw: {self._raw_sentence}\n"
        res += "\tParsed: "
        if len(self._words) > 30:
            res += f"cодержит {len(self.keywords)} ключевых слов"
        else:
            res += ' '.join([str(word) for word in self.keywords])
        res += f"\n\tArguments: {self._arguments}"
        return res