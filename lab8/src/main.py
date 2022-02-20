from parsers import SentenceParser
from query_solver import QuerySolver
from dialog_state import DialogState


if __name__ == '__main__':
    query_solver = QuerySolver()
    # query_solver.state = DialogState.search

    sentence = "найди исполнителей мужского пола похожих на крека и выводи по 10 артистов"
    sentence = "порекомендуй исполнителей мужского пола, похожих на касту и выводи по 10 результатов"
    # sentence = "выводи всех"
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