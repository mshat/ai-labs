from __future__ import annotations
import random
from typing import List
from .fitness import calc_one_max_fitness

FITNESS_FUNCTION = calc_one_max_fitness


class Population:
    def __init__(
            self,
            fitness_function,
            selection_function,
            crossing_function,
            mutation_function,
            chromosomes: List[Chromosome] = None,
            members: List[Individual] = None,
            size: int = None,
            chromosome_len: int = None,

    ):
        self._fitness_function = fitness_function
        self._selection_function = selection_function
        self._crossing_function = crossing_function
        self._mutation_function = mutation_function

        assert bool(chromosomes) + bool(members) + bool(size and chromosome_len) == 1
        if chromosomes:
            self.members: List[Individual] = \
                [Individual(self._fitness_function, chromosome=chromosome) for chromosome in chromosomes]
        elif members:
            self.members: List[Individual] = members
        elif size and chromosome_len:
            self.members: List[Individual] = \
                [Individual(self._fitness_function, chromosome_len=chromosome_len) for i in range(size)]

    def select(self):
        self.members = self._selection_function(self, n=3)

    def mutate(self, mutation_probability: float = 0.1) -> None:
        for member in self.members:
            if random.random() < mutation_probability:
                self._mutation_function(member, gene_mutation_probability=1.0 / len(member._chromosome))

    def crossover(self, crossover_probability: float = 0.9):
        crossovered_members: List[Individual] = []

        for parent1, parent2 in zip(self.members[::2], self.members[1::2]):
            if random.random() < crossover_probability:
                child1, child2 = self._crossing_function(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            crossovered_members.append(child1)
            crossovered_members.append(child2)
        self.members = crossovered_members

    def __len__(self):
        return len(self.members)

    def __str__(self):
        res = f'Population: members number {len(self.members)} '
        if len(self.members) < 10:
            res += '\nMembers:\n'
            for member in self.members:
                res += f'{member}\n'
        else:
            res += '\nThere are too many members to display\n'
        return res


class Gene:
    def __init__(self, value):
        self.value = value


class Chromosome:
    def __init__(self, genes: List[Gene]):
        self.genes: List[Gene] = genes

    @property
    def gene_values(self) -> List:
        return [gene.value for gene in self.genes]

    def __len__(self):
        return len(self.genes)


class Individual:
    def __init__(self, fitness_function, other: Individual = None, chromosome: Chromosome = None, chromosome_len: int = None):
        assert bool(other) + bool(chromosome) + bool(chromosome_len) == 1
        if other:
            self._chromosome: Chromosome = other._chromosome
        elif chromosome_len:
            self._chromosome: Chromosome = Chromosome([Gene(random.randint(0, 1)) for i in range(chromosome_len)])
        elif chromosome:
            self._chromosome: Chromosome = chromosome
        self.fitness_calculator = fitness_function

    @property
    def chromosome(self):
        return self._chromosome

    @chromosome.setter
    def chromosome(self, val: Chromosome):
        assert isinstance(val, Chromosome)
        self._chromosome = val

    @property
    def fitness(self) -> int:
        return self.fitness_calculator(self._chromosome)

    def __len__(self):
        return len(self._chromosome)

    def __str__(self):
        if len(self._chromosome) <= 10:
            return f'{self._chromosome} fitness: {self.fitness}'
        else:
            return f'Индивид с хромосомой длиной {len(self._chromosome)} fitness: {self.fitness}'