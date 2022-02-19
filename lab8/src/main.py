from parsers import SentenceParser
from query_solver import QuerySolver
from query_handler import log_query_pattern_strings


if __name__ == '__main__':
    query_solver = QuerySolver()

    sentence = "мне нравится кровосток"
    query = SentenceParser(sentence).parse(query_solver.state)
    print(query)
    # print(query.words)
    res = query_solver.solve(query)
    print(res)
    log_query_pattern_strings()
    exit()

    # while True:
    #     sentence = input('-> ')
    #     query = SentenceParser(sentence).parse(query_solver.state)
    #     query_solver.solve(query)