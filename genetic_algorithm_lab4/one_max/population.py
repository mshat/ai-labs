from __future__ import annotations
import random
from typing import List
from .fitness import calc_one_max_fitness

FITNESS_FUNCTION = calc_one_max_fitness


class Population:
    def __init__(
            self,
            selection_function,
            crossing_function,
            mutation_function,
            chromosomes: List[Chromosome] = None,
            members: List[Individual] = None,
            size: int = None,
            chromosome_len: int = None,

    ):
        self.selection_function = selection_function
        self.crossing_function = crossing_function
        self.mutation_function = mutation_function
        assert bool(chromosomes) + bool(members) + bool(size and chromosome_len) == 1
        if chromosomes:
            self.members: List[Individual] = [Individual(chromosome=chromosome) for chromosome in chromosomes]
        elif members:
            self.members: List[Individual] = members
        elif size and chromosome_len:
            self.members: List[Individual] = [Individual(chromosome_len=chromosome_len) for i in range(size)]

    def select(self):
        self.members = self.selection_function(self, n=3)

    def mutate(self, mutation_probability: float = 0.1) -> None:
        for member in self.members:
            if random.random() < mutation_probability:
                self.mutation_function(member, gene_mutation_probability=1.0 / len(member.chromosome))

    def crossover(self, crossover_probability: float = 0.9):
        crossovered_members: List[Individual] = []

        for parent1, parent2 in zip(self.members[::2], self.members[1::2]):
            if random.random() < crossover_probability:
                child1, child2 = self.crossing_function(parent1, parent2)
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
    def __init__(self, other: Individual = None, chromosome: Chromosome = None, chromosome_len: int = None):
        assert bool(other) + bool(chromosome) + bool(chromosome_len) == 1
        if other:
            self.chromosome: Chromosome = other.chromosome
        elif chromosome_len:
            self.chromosome: Chromosome = Chromosome([Gene(random.randint(0, 1)) for i in range(chromosome_len)])
        elif chromosome:
            self.chromosome: Chromosome = chromosome
        self.fitness_calculator = FITNESS_FUNCTION
        if isinstance(self.chromosome, Individual):
            print('Я охуел, да')

    @property
    def fitness(self) -> int:
        return self.fitness_calculator(self.chromosome)

    def __len__(self):
        return len(self.chromosome)

    def __str__(self):
        if len(self.chromosome) <= 10:
            return f'{self.chromosome} fitness: {self.fitness}'
        else:
            return f'Индивид с хромосомой длиной {len(self.chromosome)} fitness: {self.fitness}'