import random
from .population import Individual


def invert_bit_mutation(individual: Individual, gene_mutation_probability=0.01) -> None:
    for i in range(len(individual)):
        if random.random() < gene_mutation_probability:
            individual._chromosome.gene_values[i] = 0 if individual._chromosome.gene_values[i] == 1 else 1