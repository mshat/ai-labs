from __future__ import annotations
from typing import List


class BaseWord:
    word: str

    def __init__(self, word: str):
        self.word = word

    def __str__(self):
        return f'{self.word}'


class Placeholder(BaseWord): pass


class Word(BaseWord):
    word: str
    normal: str
    morph_speech_part: str
    speech_part: str
    query_type: str

    def __init__(self, word: str, normal_word: str, morph_speech_part: str, speech_part: str, query_type: str):
        super().__init__(word)
        self.normal = normal_word
        self.morph_speech_part = morph_speech_part
        self.speech_part = speech_part
        self.query_type = query_type

    def __str__(self):
        return f'{self.normal}[{self.speech_part} {self.morph_speech_part} {self.query_type}]'

    def __repr__(self):
        return self.__str__()


