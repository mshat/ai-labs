import random
import time
from typing import List
from .fitness import calc_one_max_fitness
from .population import Population, Individual
from .selecting import tournament_selector
from .crossing import one_point_crossing
from .mutating import invert_bit_mutation

FITNESS_FUNCTION = calc_one_max_fitness


def crossover(population: Population, crossover_probability: float = 0.9) -> Population:
    crossovered_members: List[Individual] = []

    for parent1, parent2 in zip(population.members[::2], population.members[1::2]):
        if random.random() < crossover_probability:
            child1, child2 = one_point_crossing(parent1, parent2)
        else:
            child1, child2 = parent1, parent2
        crossovered_members.append(child1)
        crossovered_members.append(child2)
    return Population(members=crossovered_members)


def mutate(population: Population, mutation_probability: float = 0.1) -> None:
    for member in population.members:
        if random.random() < mutation_probability:
            invert_bit_mutation(member, gene_mutation_probability=1.0 / len(member.chromosome))


def save_data_for_plot(
        max_fitness_values: List[float],
        avg_fitness_values: List[float],
        filename='genetic_fitness_data.txt'):
    data = {"max_fitness_values": max_fitness_values, "avg_fitness_values": avg_fitness_values}
    with open(filename, 'w') as f:
        f.write(str(data))


def solve_with_genetic_algorithm(
        max_generations: int,
        population_size: int,
        chromosome_len: int,
        crossover_probability: float,
        mutation_probability: float,
        debug=False
) -> (List[float], List[float]):
    time_start = time.time()
    population = Population(size=population_size, chromosome_len=chromosome_len)

    max_fitness_values = []
    avg_fitness_values = []
    best_fitness = 0

    generation_counter = 0
    while generation_counter < max_generations:
        generation_counter += 1
        population = tournament_selector(population)

        population = crossover(population, crossover_probability)

        mutate(population, mutation_probability)

        fitness_values = [member.fitness for member in population.members]

        max_fitness = max(fitness_values)
        avg_fitness = sum(fitness_values) / len(fitness_values)
        max_fitness_values.append(max_fitness)
        avg_fitness_values.append(avg_fitness)
        if debug:
            print(f"Поколение {generation_counter}: Макс приспособ. = {max_fitness}, Средняя приспособ.= {avg_fitness}")

        best_individual_index = fitness_values.index(max(fitness_values))
        if debug:
            print("Лучший индивидуум = ", population.members[best_individual_index], "\n")

        if max_fitness > best_fitness:
            best_fitness = max_fitness
    print(f'{best_fitness=}')
    time_finish = time.time()
    print(f'Время выполнения {time_finish - time_start}')
    return max_fitness_values, avg_fitness_values


def time_test(test_num=10, *args, **kwargs):
    time_sum = 0
    num = test_num
    for i in range(num):
        t1 = time.time()
        solve_with_genetic_algorithm(*args, **kwargs)
        t2 = time.time()
        time_sum += t2 - t1
    print(time_sum / num)

