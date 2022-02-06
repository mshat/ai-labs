import random
from .population import Individual, Chromosome


def one_point_crossing(parent1: Individual, parent2: Individual) -> (Individual, Individual):
    """
    Одноточечное скрещивание. Выбирается случайный индекс хромосомы, по которому она делится на 2 половины.
    Затем первый потомок получает гены первого родителя до индекса s и гены второго родителя начиная с индекса s, а
    второй потомок получает гены второго родитля до индекса s и гены первого родителя начиная с индекса s
    """
    s = random.randint(2, len(parent1)-3)  # TODO почему с 2, а не с 1?
    parent1_chromosome = parent1.chromosome
    parent2_chromosome = parent2.chromosome
    parent1.chromosome = Chromosome(parent1_chromosome.genes[:s] + parent2_chromosome.genes[s:])
    parent2.chromosome = Chromosome(parent2_chromosome.genes[:s] + parent1_chromosome.genes[s:])
    return parent1, parent2
