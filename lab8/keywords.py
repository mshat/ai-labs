import enum
from data import keywords as raw_keywords


class Keyword:
    def __init__(self, keyword: str, query_type, speech_part):
        self.keyword = keyword
        self.query_type = query_type
        self.speech_part = speech_part

    def __str__(self):
        return f'Keyword: {self.keyword} [{self.query_type} {self.speech_part}]'

    def __repr__(self):
        return self.__str__()


def load_keywords(keywords_dict):
    res = []
    for query_type, speech_type_keywords in keywords_dict.items():
        for speech_part, keywords in speech_type_keywords.items():
            for keyword in keywords:
                res.append(Keyword(keyword, query_type, speech_part))
    return res


KEYWORDS = load_keywords(raw_keywords)

