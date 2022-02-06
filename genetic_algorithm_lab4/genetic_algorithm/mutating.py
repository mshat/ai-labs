import random
from .population import Individual


def invert_bit_mutation(individual: Individual, gene_mutation_probability=0.01) -> None:
    mutated_gen_index = random.randint(0, len(individual.chromosome.gene_values) - 1)
    individual.chromosome.genes[mutated_gen_index].invert_value()
    # for i in range(len(individual)):
    #     if random.random() < gene_mutation_probability:
    #         mutated = 1
    #         individual.chromosome.gene_values[i] = 0 if individual.chromosome.gene_values[i] == 1 else 1