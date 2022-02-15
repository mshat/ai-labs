from __future__ import annotations
from typing import List


class Sentence:
    _words: List[Word]
    is_question: bool

    def __init__(self, words: List[Word], is_question=True):
        self._words = words
        self.is_question = is_question

    def __str__(self):
        res = 'Предложение:\n' if not self.is_question else 'Вопросительное предложение:\n'
        res += f"\tRaw: {' '.join([f'{word.word}' for word in self._words])}\n"
        res += "\tParsed: "
        if len(self._words) > 20:
            res += f"cодержит {len(self._words)} слов"
        else:
            res += ' '.join([f"{word.normal} [{word.speech_part}]" for word in self._words])
        return res


class Word:
    word: str
    normal: str
    speech_part: str

    def __init__(self, word: str, normal_word: str, speech_part: str):
        self.word = word
        self.normal = normal_word
        self.speech_part = speech_part

    def __str__(self):
        return f'{self.word} [{self.speech_part}]'


