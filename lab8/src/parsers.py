import re
from typing import List, Dict, ClassVar, Union
from morph_nalyzer import MorphAnalyzer
from word import BaseWord, Placeholder, Word
from string_cleaner import StrCleaner
from query import (ArtistArgumentError, GenreArgumentError, ArgumentError, Argument, ArtistArgument, SexArgument,
                   GenreArgument, StrArgument, NumArgument, ARTISTS, GENRES, Query)
from word_classifier import WORD_CLASSIFIER
from data import GENDERS

PLACEHOLDERS = {'artist': '*ARTISTNAME*', 'genre': '*GENRENAME*', 'gender': '*GENDER*', 'number': '*NUMBER*'}


class SentenceParsingError(Exception): pass


class SentenceParser:
    def __init__(self, sentence: str):
        if sentence == "":
            raise SentenceParsingError('Empty input')
        self._raw_sentence = sentence
        self._sentence = sentence
        # self._clear_sentence()
        self._is_question = self._check_is_it_question()
        self._sentence = self._sentence.replace('?', '')

    def _clear_sentence(self):
        pass

    def _check_is_it_question(self):
        if self._sentence[-1] == '?':
            return True
        else:
            return False

    def find_arguments(self, possible_arguments: Dict, placeholder='') -> List[str]:
        """ Находит в предложении все вхождения ключей словаря possible_arguments и
        возвращает список соответствующих этим ключам значений словаря.
        Найденные ключевые слова заменяются на placeholder в исходном предложении"""
        possible_keys = list(possible_arguments.keys())
        found_args = re.findall('|'.join(possible_keys), self._sentence)
        arguments = []
        for arg in found_args:
            arguments.append(possible_arguments[arg])
            self._sentence = self._sentence.replace(arg, placeholder)
        return arguments

    def find_number_arguments(self, placeholder=''):
        words = self._sentence.split()
        arguments = []
        for word in words:
            if word.isdigit():
                arguments.append(word)
                self._sentence = self._sentence.replace(word, placeholder)
        return arguments

    def _split(self) -> List[str]:
        words = self._sentence.split()
        i = 0
        while i < len(words):
            if words[i] == 'не' and i < len(words) - 1:
                words[i + 1] = words[i] + ' ' + words[i + 1]
                words.pop(i)
            i += 1
        return words

    def parse(self, dialog_state) -> Query:
        artist_arguments = [ArtistArgument(arg) for arg in self.find_arguments(ARTISTS, PLACEHOLDERS['artist'])]
        genre_arguments = [GenreArgument(arg) for arg in self.find_arguments(GENRES, PLACEHOLDERS['genre'])]
        gender_arguments = [SexArgument(arg) for arg in self.find_arguments(GENDERS, PLACEHOLDERS['gender'])]
        number_arguments = [NumArgument(arg) for arg in self.find_number_arguments(PLACEHOLDERS['number'])]
        arguments = [*artist_arguments, *genre_arguments, *gender_arguments, *number_arguments]

        # raw_words = self._sentence.split()
        raw_words = self._split()

        parsed_words: List[Union[BaseWord, Word]] = []
        for word in raw_words:
            if word not in PLACEHOLDERS.values():
                word_parser = WordParser(word)
                parsed_words.append(word_parser.parse(dialog_state))
            else:
                parsed_words.append(Placeholder(word))
        return Query(
            raw_sentence=self._raw_sentence,
            words=parsed_words,
            arguments=arguments,
            is_question=self._is_question
        )


class WordParsingError(Exception): pass


class WordParser:
    _tag: str

    def __init__(self, word: str):
        if word == '':
            raise WordParsingError('Empty input')
        self._word = word

    def parse(self, dialog_state) -> Word:
        parsed_word = MorphAnalyzer.parse(self._word)[0]  # TODO не обязательно первый вариант правильный
        return Word(
            word=self._word,
            normal_word=parsed_word.normal_form,
            morph_speech_part=parsed_word.tag.POS,
            tag=WORD_CLASSIFIER.assign_tags(parsed_word.normal_form, dialog_state),
        )
