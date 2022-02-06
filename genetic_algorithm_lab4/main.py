from one_max.one_max import solve_with_genetic_algorithm, save_data_for_plot
#from plot_fitness_data import plot


if __name__ == "__main__":
    max_fitness_values, avg_fitness_values = solve_with_genetic_algorithm(100, 100, 100, 0, 0.99)
    save_data_for_plot(max_fitness_values, avg_fitness_values)
    #plot()