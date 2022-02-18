from parsers import SentenceParser
from query_solver import QuerySolver


if __name__ == '__main__':
    query_solver = QuerySolver()

    # sentence = "начать заново"
    # query = SentenceParser(sentence).parse(query_solver.state)
    # print(query)
    # print(query.words)
    # res = query_solver.solve(query)
    # print(res)
    # exit()

    while True:
        sentence = input('-> ')
        query = SentenceParser(sentence).parse(query_solver.state)
        query_solver.solve(query)