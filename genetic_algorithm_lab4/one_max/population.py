from __future__ import annotations
import random
from typing import List
from .fitness import calc_one_max_fitness

FITNESS_FUNCTION = calc_one_max_fitness


class Population:
    def __init__(
            self,
            chromosomes: List[Chromosome] = None,
            members: List[Individual] = None,
            size: int = None,
            chromosome_len: int = None
    ):
        assert bool(chromosomes) + bool(members) + bool(size and chromosome_len) == 1
        if chromosomes:
            self.members: List[Individual] = [Individual(chromosome=chromosome) for chromosome in chromosomes]
        elif members:
            self.members: List[Individual] = members
        elif size and chromosome_len:
            self.members: List[Individual] = [Individual(chromosome_len=chromosome_len) for i in range(size)]

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