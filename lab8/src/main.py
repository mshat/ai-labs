from parsers import SentenceParser
from query_solver import QuerySolver
from dialog_state import DialogState


if __name__ == '__main__':
    query_solver = QuerySolver()
    query_solver.state = DialogState.search

    sentence = "убери всех исполнителей кроме женского пола"
    query = SentenceParser(sentence).parse(query_solver.state)
    print(query)
    # print(query.words)
    res = query_solver.solve(query)
    print(res)
    exit()

    # while True:
    #     sentence = input('-> ')
    #     query = SentenceParser(sentence).parse(query_solver.state)
    #     query_solver.solve(query)