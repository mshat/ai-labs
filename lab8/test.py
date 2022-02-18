import unittest
from query_solver import QuerySolver, DialogState
from parsers import SentenceParser


class TestQueries(unittest.TestCase):
    def test_search(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.start

        search_sentences = {
            "найди похожих исполнителей на крека": 'search_by_artist',
            "найди похожих на моргенштерна": 'search_by_artist',
            "похожие на басту": 'search_by_artist',
            "найди исполнителей в жанре грайм": 'search_by_genre',
            "исполнители в жанре поп": 'search_by_genre',
            "покажи исполнителей мужчин": 'search_by_sex',
            "артисты мужчины": 'search_by_sex',
            "покажи исполнителей женщин": 'search_by_sex',
            "артисты женщины": 'search_by_sex',
            "покажи исполнителей мужского пола": 'search_by_sex',
            "исполнители женского пола": 'search_by_sex',
        }

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                # print(query)
                res = query_solver.solve(query)
                self.assertEqual(res, search_sentences[key])

    def test_filter(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.search

        search_sentences = {
            "оставь исполнителей мужского пола": 'filter_by_sex',
            "убери всех исполнителей кроме женского пола": 'filter_by_sex',
            "оставь только соло исполнителей": 'filter_by_members_count',
            "убери всех кроме соло исполнителей": 'filter_by_members_count',
            "оставь только дуэты": 'filter_by_members_count',
            "убери всех кроме дуэтов": 'filter_by_members_count',
            "оставь только группы": 'filter_by_members_count',
            "убери всех кроме групп": 'filter_by_members_count',
            "убери исполнителей младше чем 20": 'filter_by_age_exclude',
            "оставь исполнителей старше чем 22": 'filter_by_age_include',
            "убери исполнителей старше чем 30": 'filter_by_age_exclude',
            "оставь исполнителей младше чем 11": 'filter_by_age_include',
            "оставь исполнителей в возрасте от 32 до 43": 'filter_by_age_include',
            "показывай по 10 артистов": 'set_result_len',
            "выводи по 5 артистов": 'set_result_len',
            "удалить все фильтры": 'remove_filters',
            "убери ограничение на количество артистов": 'remove_result_len_filter',
            "выводи всех": 'remove_result_len_filter',
        }

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                # print(query)
                res = query_solver.solve(query)
                self.assertEqual(res, search_sentences[key])

    def test_like_dislike(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.start

        search_sentences = {
            "убери многоточие из списка лайков": 'dislike',
            "мне не нравится егор крид": 'dislike',
            "поставь дизлайк тимати": 'dislike',
            "добавь моргенштерна в список дизлайков": 'dislike',
            "убери моргенштерна из списка дизлайков": 'like',
            "мне нравится кровосток": 'like',
            'люблю нойза': 'like',
            'не люблю биг бейби тейпа': 'dislike',
            "мне нравится исполнитель кровосток": 'like',
            "добавь касту в список любимых": 'like',
            "поставь лайк касте": 'like',
            "мне больше не нравится тимати": 'dislike',
        }

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                # print(query)
                res = query_solver.solve(query)
                self.assertEqual(res, search_sentences[key])

    def test_general_queries(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.start

        search_sentences = {
            "сколько исполнителей в базе?": 'number',
            "сколько исполнителей ты знаешь?": 'number',
            "сколько мужчин в базе?": 'number_with_sex',
            "сколько исполнителей мужчин ты знаешь?": 'number_with_sex',
            "сколько женщин в базе?": 'number_with_sex',
            "сколько исполнителей женщин ты знаешь?": 'number_with_sex',
            "сколько ты знаешь исполнителей старше 26 лет?": 'number_with_age',
            "сколько исполнителей старше 11 лет?": 'number_with_age',
            "сколько ты знаешь исполнителей младше 333 лет?": 'number_with_age',
            "сколько исполнителей младше 0 лет?": 'number_with_age',
            "вернись в начало": 'restart',
            "в начало": 'restart',
            "покажи всех исполнителей": 'show_all_artists',
            "все артисты": 'show_all_artists',
        }

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                # print(query)
                res = query_solver.solve(query)
                self.assertEqual(res, search_sentences[key])

    def test_info(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.start

        search_sentences = {
            'расскажи про кровосток': 'info',
            'информация про кизару': 'info',
            'информация о касте': 'info',
            'хочу узнать о многоточии': 'info',
        }

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                # print(query)
                res = query_solver.solve(query)
                self.assertEqual(res, search_sentences[key])