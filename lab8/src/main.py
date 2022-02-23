from lab8.src.sentence_analyzer.sentence_parser import SentenceParser
from lab8.src.query_solving.query_solver import QuerySolver
from lab8.src.query_solving.user import User
from lab8.src.query_solving.dialog import DialogState
from lab8.src.config import DEBUG


def test(sentences: [str]):
    user = User()
    query_solver = QuerySolver(user)
    for sentence_ in sentences:
        query_ = SentenceParser(sentence_).parse(query_solver.state)
        print(f'Вход: {query_.raw_sentence}')
        # print(query_.keywords)
        res_ = query_solver.solve(query_)
        # print(user)
        print(res_)
        print()


def main():
    user = User()
    query_solver = QuerySolver(user)

    print('Вас приветствует бот-помощник по миру русского хипхопа.\n'
          'Вы можете узнать о моих возможностях, спросив меня об этом')
    while True:
        if query_solver.state in (DialogState.search, DialogState.filter):
            input_prompt = 'ФИЛЬТР -> '
        else:
            input_prompt = 'ЗАПРОС -> '
        sentence = input(input_prompt)
        if sentence == '': continue
        query = SentenceParser(sentence).parse(query_solver.state)
        query_solver.solve(query)
        if DEBUG: print('[CURRENT STATE]', query_solver.state)
        print()


if __name__ == '__main__':
    main()
    # sentence = "порекомендуй соло исполнителей мужского пола, в возрасте от 20 лет похожих на касту и выводи по 10 результатов"
    # sentence = "порекомендуй похожих на оксимирона, женского пола"
    # sentence = "порекомендуй группы похожие на касту"
    # sentence = "порекомендуй похожих на касту"
    # sentence = "показывай по 10 артистов"
    # sentences = [sentence]

    rec_sent = [
        'мне нравится каста, гуф, нойз',
        "ограничь вывод 5 артистами",
        # 'мне понравится',
        # 'порекомендуй по лайкам',
        # 'артисты по моим интересам',
        # 'порекомендуй по интересам',
        'порекомендуй по интересам',
        # 'начать с начала',
        "порекомендуй соло исполнителей мужского пола, в возрасте от 20 лет похожих на касту и выводи по 10 результатов",
        "порекомендуй соло исполнителей мужского пола похожих на касту и выводи по 10 результатов"
    ]

    # sentences = [
    #     "не люблю многоточие и крека",
    #     # "люблю кровосток и нойза",
    #     # "порекомендуй похожих на оксимирона и убери исполнителей мужского пола",
    #     # "порекомендуй похожих на оксимирона убери младше 35 лет",
    #     # "порекомендуй группы, похожие на оксимирона убери младше 35 лет и выводи по 5 артистов",
    #     # "порекомендуй артистов, похожих на оксимирона и выводи по 5 артистов",
    #     # "порекомендуй соло исполнителей мужского пола, в возрасте от 20 лет похожих на касту и выводи по 10 результатов"
    #     "порекомендуй соло исполнителей мужского пола, в возрасте от 20 лет и выводи по 10 результатов"
    # ]
    # test(['Что ты можешь?'])

