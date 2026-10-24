
import random

from chromosome import create_random_chromosome
from fitness import calculate_fitness


def run_random_search(
    grid,
    no_fly_zones,
    attempts=600
):
    print("\n===== STARTING RANDOM SEARCH =====")

    best_solution = None
    best_fitness = float("-inf")

    fitness_history = []

    # Generate and test random solutions
    for attempt in range(attempts):

        chromosome = create_random_chromosome(
            no_fly_zones
        )

        fitness = calculate_fitness(
            chromosome,
            grid
        )

        fitness_history.append(fitness)

        # Keep the best solution found so far
        if fitness > best_fitness:
            best_fitness = fitness
            best_solution = chromosome

        if (attempt + 1) % 100 == 0:
            print(
                f"Attempt {attempt + 1}: "
                f"Best Fitness = {best_fitness:.2f}"
            )

    print("\n===== RANDOM SEARCH RESULT =====")
    print("Total Attempts:", attempts)
    print("Best Fitness:", round(best_fitness, 2))

    best_solution.display()

    return best_solution, fitness_history
