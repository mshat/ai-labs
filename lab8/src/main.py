from parsers import SentenceParser
from query_solver import QuerySolver
from dialog_state import DialogState


if __name__ == '__main__':
    query_solver = QuerySolver()
    # query_solver.state = DialogState.search

    sentence = "порекомендуй соло исполнителей мужского пола, в возрасте от 20 лет похожих на касту и выводи по 10 результатов"
    # sentence = "покажи исполнителей мужчин и до 10 лет и от 20 до 40"
    query = SentenceParser(sentence).parse(query_solver.state)
    print(f'Вход: {query.raw_sentence}')
    # print(query.words)
    # res = query_solver.multi_solve(query)
    res = query_solver.solve(query)
    print(res)
    exit()

    # while True:
    #     sentence = input('-> ')
    #     query = SentenceParser(sentence).parse(query_solver.state)
    #     query_solver.solve(query)