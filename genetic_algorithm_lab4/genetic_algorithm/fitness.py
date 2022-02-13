from typing import List


def calc_one_max_fitness(chromosome) -> int:
    return sum(chromosome.gene_values)


# def calc_assignment_fitness(chromosome, cost_matrix: List[int]) -> int:
#     data = chromosome.gene_values
#     assert len(cost_matrix) == len(data)
#
#     res = 0
#     for i, cost in enumerate(cost_matrix):
#         res += cost * data[i]
#
#     return res