import time
from typing import List
from genetic_algorithm.fitness import calc_one_max_fitness
from genetic_algorithm.population import Population, Individual
from genetic_algorithm.selecting import tournament_selector
from genetic_algorithm.crossing import one_point_crossing
from genetic_algorithm.mutating import invert_bit_mutation

FITNESS_FUNCTION = calc_one_max_fitness


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
    population = Population(
        selection_function=tournament_selector,
        crossing_function=one_point_crossing,
        mutation_function=invert_bit_mutation,
        size=population_size,
        chromosome_len=chromosome_len
    )

    max_fitness_values = []
    avg_fitness_values = []
    best_fitness = 0

    generation_counter = 0
    while generation_counter < max_generations:
        generation_counter += 1

        population.select()

        population.crossover(crossover_probability)

        population.mutate(mutation_probability)

        fitness_values = [member.fitness for member in population.members]

        max_fitness = max(fitness_values)
        avg_fitness = sum(fitness_values) / len(fitness_values)
        max_fitness_values.append(max_fitness)
        avg_fitness_values.append(avg_fitness)
        if debug:
            print(population)
            print(f"Поколение {generation_counter}: Макс приспособ. = {max_fitness}, Средняя приспособ.= {avg_fitness}")

        best_individual_index = fitness_values.index(max(fitness_values))
        # if debug:
        #     print("Лучший индивидуум = ", population.members[best_individual_index], "\n")

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

