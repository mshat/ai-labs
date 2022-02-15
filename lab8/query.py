from typing import List
from sentence import Word
from data import ARTISTS, GENRES


class ParameterError(Exception): pass
class ArtistParameterError(ParameterError): pass
class GenreParameterError(ParameterError): pass


class Parameter:
    def __init__(self, parameter):
        self._parameter = parameter


class NumParameter(Parameter):
    def __init__(self, parameter: str):
        super().__init__(parameter)
        if not isinstance(parameter, int) or not isinstance(parameter, float):
            raise ParameterError('Wrong parameter type')


class StrParameter(Parameter):
    def __init__(self, parameter: str):
        super().__init__(parameter)
        if not isinstance(parameter, str):
            raise ParameterError('Wrong parameter type')


class ArtistParameter(StrParameter):
    def __init__(self, parameter: str):
        super().__init__(parameter)
        if self._parameter.lower() not in ARTISTS:
            raise ArtistParameterError('This artist is not found ')


class GenreParameter(StrParameter):
    def __init__(self, parameter: str):
        super().__init__(parameter)
        if self._parameter.lower() not in ARTISTS:
            raise GenreParameterError('This genre is not found ')


class Query:
    _verb: Word
    _params: List[Parameter]
    _allowed_verbs: List[str]

    def __init__(self, verb: Word, params: List[Parameter]):
        self._verb = verb
        self._params = params


class SearchQuery(Query):
    pass