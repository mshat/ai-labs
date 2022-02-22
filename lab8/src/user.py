from typing import List, Dict
from lab8.src.const import SexFilter, GroupTypeFilter


class User:
    _name: str
    _likes: List[str]
    _dislikes: List[str]
    _group_type_filter: GroupTypeFilter
    _younger_filter: int | None
    _older_filter: int | None
    _sex_filter: SexFilter

    def __init__(self, name: str = None):
        self._name = name
        self._likes = []
        self._dislikes = []
        self._group_type_filter = GroupTypeFilter.any
        self._younger_filter = None
        self._older_filter = None
        self._sex_filter = SexFilter.any

    @property
    def name(self) -> str:
        return self._name

    @property
    def likes(self) -> List[str]:
        return self._likes

    @property
    def dislikes(self) -> List[str]:
        return self._dislikes

    @property
    def group_type_filter(self) -> GroupTypeFilter:
        return self._group_type_filter

    @property
    def younger_filter(self) -> int | None:
        return self.younger_filter

    @younger_filter.setter
    def younger_filter(self, val: int):
        self._younger_filter = val

    @property
    def older_filter(self) -> int | None:
        return self.older_filter

    @older_filter.setter
    def older_filter(self, val: int):
        self._older_filter = val

    @property
    def sex_filter(self) -> SexFilter | None:
        return self._sex_filter

    def add_group_type_filter(self, filter_: GroupTypeFilter):
        self._group_type_filter = filter_

    def add_sex_filter(self, sex: SexFilter):
        self._sex_filter = sex

    def add_like(self, artist_name: str):
        if artist_name in self._dislikes:
            self._dislikes.remove(artist_name)
        else:
            if artist_name not in self._likes:
                self._likes.append(artist_name)

    def add_dislike(self, artist_name: str):
        if artist_name in self._likes:
            self._likes.remove(artist_name)
        else:
            if artist_name not in self._dislikes:
                self._dislikes.append(artist_name)

    def __str__(self):
        return f'User {self.name} likes: {self._likes}, dislikes: {self._dislikes}'