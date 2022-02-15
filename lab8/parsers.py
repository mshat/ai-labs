from typing import List
from morph_nalyzer import MorphAnalyzer
from sentence import Word, Sentence
from string_cleaner import StrCleaner
from query import (ArtistParameterError, GenreParameterError, ParameterError, ArtistParameter, GenreParameter,
                   StrParameter, NumParameter, ARTISTS, GENRES)


class SentenceParsingError(Exception): pass


class SentenceParser:
    def __init__(self, sentence: str):
        if sentence == "":
            raise SentenceParsingError('Empty input')
        self._sentence = sentence
        # self._clear_sentence()
        self._is_question = self._check_is_it_question()
        self._sentence = self._sentence.replace('?', '')
        self._raw_words = self._sentence.split()

    def _clear_sentence(self):
        pass

    def _check_is_it_question(self):
        if self._sentence[-1] == '?':
            return True
        else:
            return False

    def get_artists(self):
        pass

    def get_genres(self):
        pass

    def parse(self) -> Sentence:
        parsed_words: List[Word] = []
        for word in self._raw_words:
            word_parser = WordParser(word)
            parsed_words.append(word_parser.parse())
        return Sentence(words=parsed_words, is_question=self._is_question)


class WordParsingError(Exception): pass


class WordParser:
    def __init__(self, word: str):
        if word == '':
            raise WordParsingError('Empty input')
        self._word = word

    def parse(self) -> Word:
        parsed_word = MorphAnalyzer.parse(self._word)[0]  # TODO не обязательно первый вариант правильный
        return Word(
            word=self._word,
            normal_word=parsed_word.normal_form,
            speech_part=parsed_word.tag.POS
        )

