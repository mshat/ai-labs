from typing import List
from keywords import KEYWORDS
from query_solver import DialogState


class WordClassifier:
    def __init__(self):
        self._keywords = KEYWORDS

    @property
    def keywords(self):
        return {keyword.keyword: keyword for keyword in self._keywords}

    def _exclude_keywords_by_query_type(self, excluded_query_types: List[str]):
        return {keyword.keyword: keyword for keyword in self._keywords if
                keyword.query_type not in excluded_query_types}

    def _get_keywords_by_dialog_state(self, dialog_state):
        if dialog_state == DialogState.search:
            return self._exclude_keywords_by_query_type(['search', 'info', 'like', 'dislike', 'number'])
        else:
            return self._exclude_keywords_by_query_type(['filter'])

    def classify_speech_part(self, word: str, dialog_state):
        keywords = self._get_keywords_by_dialog_state(dialog_state)
        if word not in keywords:
            return None
        return keywords[word].speech_part

    def classify_query_type(self, word: str, dialog_state):
        keywords = self._get_keywords_by_dialog_state(dialog_state)
        if word not in keywords:
            return None
        return keywords[word].query_type


WORD_CLASSIFIER = WordClassifier()
