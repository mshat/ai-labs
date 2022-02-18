import unittest
from query_solver import QuerySolver, DialogState
from parsers import SentenceParser


class DataForTests:
    search_by_name = {
        "найди похожих исполнителей на крека": 'search_by_artist',
        "найди похожих на моргенштерна": 'search_by_artist',
        "похожие на басту": 'search_by_artist',
    }
    search_by_genre = {
        "найди исполнителей в жанре грайм": 'search_by_genre',
        "исполнители в жанре поп": 'search_by_genre',
    }
    search_by_sex = {
        "покажи исполнителей мужчин": 'search_by_sex',
        "артисты мужчины": 'search_by_sex',
        "покажи исполнителей женщин": 'search_by_sex',
        "артисты женщины": 'search_by_sex',
        "покажи исполнителей мужского пола": 'search_by_sex',
        "исполнители женского пола": 'search_by_sex',
    }
    search_show_all = {
        "покажи всех исполнителей": 'show_all_artists',
        "все артисты": 'show_all_artists',
    }
    test_filter = {
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
    like_dislike = {
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
    number_queries = {
        'какое количество исполнителей в базе?': 'number',
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
    }
    test_info = {
        'расскажи про кровосток': 'info',
        'информация про кизару': 'info',
        'информация о касте': 'info',
        'хочу узнать о многоточии': 'info',
    }


class TestIntegrationStates(unittest.TestCase):
    def check_next_states(self, state, allowed_sentences: dict, disallowed_sentences: dict):
        query_solver = QuerySolver()

        sentences = {
            'allowed': allowed_sentences,
            'disallowed': disallowed_sentences,
        }

        for allowed_disallowed, sentences in sentences.items():
            for expected_res, sentence in sentences.items():
                with self.subTest(i=expected_res):
                    query_solver.state = state
                    query = SentenceParser(sentence).parse(query_solver.state)
                    res = query_solver.solve(query)

                    if allowed_disallowed == 'allowed':
                        self.assertEqual(res, expected_res)
                    else:
                        self.assertNotEqual(res, expected_res)

    def test_next_states_start(self):
        """ Проверяет в какие состояния можно перейти из состояния start"""
        allowed = {
            'search_by_artist': "найди похожих исполнителей на крека",
            'like': "убери моргенштерна из списка дизлайков",
            'number': "сколько исполнителей в базе?",
            'info': "информация о касте"
        }
        disallowed = {
            'filter_by_sex': "оставь исполнителей мужского пола",
        }

        self.check_next_states(DialogState.start, allowed, disallowed)

    def test_next_states_search(self):
        """ Проверяет в какие состояния можно перейти из состояния search"""
        allowed = {
            'filter_by_sex': "оставь исполнителей мужского пола",
            'like': "убери моргенштерна из списка дизлайков",
            'number': "сколько исполнителей в базе?",
            'info': "информация о касте"
        }
        disallowed = {
            'search_by_artist': "артисты мужчины",
        }

        self.check_next_states(DialogState.search, allowed, disallowed)

    def test_next_states_filter(self):
        """ Проверяет в какие состояния можно перейти из состояния filter"""
        allowed = {
            'filter_by_sex': "оставь исполнителей мужского пола",
            'like': "убери моргенштерна из списка дизлайков",
            'number': "сколько исполнителей в базе?",
            'info': "информация о касте"
        }
        disallowed = {
            'search_by_artist': "артисты мужчины",
        }

        self.check_next_states(DialogState.filter, allowed, disallowed)

    def test_next_states_like(self):
        """ Проверяет в какие состояния можно перейти из состояния like"""
        allowed = {
            'search_by_artist': "найди похожих исполнителей на крека",
            'like': "убери моргенштерна из списка дизлайков",
            'number': "сколько исполнителей в базе?",
            'info': "информация о касте"
        }
        disallowed = {
            'filter_by_sex': "оставь исполнителей мужского пола",
        }

        self.check_next_states(DialogState.like, allowed, disallowed)

    def test_next_states_dislike(self):
        """ Проверяет в какие состояния можно перейти из состояния dislike"""
        allowed = {
            'search_by_artist': "найди похожих исполнителей на крека",
            'like': "убери моргенштерна из списка дизлайков",
            'number': "сколько исполнителей в базе?",
            'info': "информация о касте"
        }
        disallowed = {
            'filter_by_sex': "оставь исполнителей мужского пола",
        }

        self.check_next_states(DialogState.dislike, allowed, disallowed)

    def test_next_states_number(self):
        """ Проверяет в какие состояния можно перейти из состояния number"""
        allowed = {
            'search_by_artist': "найди похожих исполнителей на крека",
            'like': "убери моргенштерна из списка дизлайков",
            'number': "сколько исполнителей в базе?",
            'info': "информация о касте"
        }
        disallowed = {
            'filter_by_sex': "оставь исполнителей мужского пола",
        }

        self.check_next_states(DialogState.number, allowed, disallowed)

    def test_next_states_info(self):
        """ Проверяет в какие состояния можно перейти из состояния info"""
        allowed = {
            'search_by_artist': "найди похожих исполнителей на крека",
            'like': "убери моргенштерна из списка дизлайков",
            'number': "сколько исполнителей в базе?",
            'info': "информация о касте"
        }
        disallowed = {
            'filter_by_sex': "оставь исполнителей мужского пола",
        }

        self.check_next_states(DialogState.info, allowed, disallowed)

    def test_repeat_states(self):
        """ Проверяет, что можно делать подряд несколько запросов для одного состояния"""
        query_solver = QuerySolver()

        sentences = {
            'search_by_artist': "найди похожих исполнителей на крека",
            'search_by_genre': "найди исполнителей в жанре грайм",

            'filter_by_sex': "оставь исполнителей мужского пола",
            'filter_by_members_count': "оставь только соло исполнителей",

            'like': "убери моргенштерна из списка дизлайков",
            'dislike': "добавь моргенштерна в список дизлайков",

            'number_with_sex': "сколько исполнителей мужчин ты знаешь?",
            'number': "сколько исполнителей в базе?",

            'info': "информация о касте",
        }

        for expected_res, sentence in sentences.items():
            with self.subTest(i=expected_res):
                query = SentenceParser(sentence).parse(query_solver.state)
                res = query_solver.solve(query)
                self.assertEqual(res, expected_res)

    def test_states_integration(self):
        """
        Проверяет корректную обработку запросов для разных состояний
        QuerySolver принимает по порядку следующие состояния:
        поиск, фильтрация, лайк, дизлайк, количественный запрос, информационный запрос
        """
        query_solver = QuerySolver()

        sentences = {
            'search_by_artist': "найди похожих исполнителей на крека",

            'filter_by_sex': "оставь исполнителей мужского пола",

            'like': "убери моргенштерна из списка дизлайков",

            'dislike': "добавь моргенштерна в список дизлайков",

            'number': "сколько исполнителей в базе?",

            'info': "информация о касте",
        }

        for expected_res, sentence in sentences.items():
            with self.subTest(i=expected_res):
                query = SentenceParser(sentence).parse(query_solver.state)
                res = query_solver.solve(query)
                self.assertEqual(res, expected_res)


class TestQueries(unittest.TestCase):
    def test_search_by_name(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.start

        search_sentences = DataForTests.search_by_name

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                res = query_solver.solve(query)

                self.assertEqual(res, search_sentences[key])

    def test_search_by_genre(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.start

        search_sentences = DataForTests.search_by_genre

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                res = query_solver.solve(query)

                self.assertEqual(res, search_sentences[key])

    def test_search_by_sex(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.start

        search_sentences = DataForTests.search_by_sex

        restart_query = 'в начало'

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query_solver.solve(SentenceParser(restart_query).parse(query_solver.state))

                query = SentenceParser(key).parse(query_solver.state)
                res = query_solver.solve(query)

                self.assertEqual(res, search_sentences[key])

    def test_search_show_all(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.start

        search_sentences = DataForTests.search_show_all

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                res = query_solver.solve(query)

                self.assertEqual(res, search_sentences[key])

    def test_filter(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.search

        search_sentences = DataForTests.test_filter

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                res = query_solver.solve(query)

                self.assertEqual(res, search_sentences[key])

    def test_like_dislike(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.start

        search_sentences = DataForTests.like_dislike

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                res = query_solver.solve(query)

                self.assertEqual(res, search_sentences[key])

    def test_number_queries(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.start

        search_sentences = DataForTests.number_queries

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                res = query_solver.solve(query)

                self.assertEqual(res, search_sentences[key])

    def test_info(self):
        query_solver = QuerySolver()
        query_solver.state = DialogState.start

        search_sentences = DataForTests.test_info

        for key in search_sentences.keys():
            with self.subTest(i=key):
                query = SentenceParser(key).parse(query_solver.state)
                res = query_solver.solve(query)

                self.assertEqual(res, search_sentences[key])
