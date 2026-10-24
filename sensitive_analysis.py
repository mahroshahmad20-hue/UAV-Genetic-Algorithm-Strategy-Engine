
import matplotlib.pyplot as plt

from genetic_algorithm import GeneticAlgorithm


def run_sensitivity_analysis(grid, no_fly_zones):

    print("\n======================================")
    print("       SENSITIVITY ANALYSIS")
    print("======================================")

    population_results = {}
    mutation_results = {}
    tournament_results = {}

    # ======================================
    # TEST 1: POPULATION SIZE
    # ======================================

    print("\n--- TEST 1: POPULATION SIZE ---")

    population_sizes = [10, 20, 40]

    for size in population_sizes:

        print(f"\nTesting population size: {size}")

        ga = GeneticAlgorithm(
            grid=grid,
            population_size=size,
            generations=20,
            mutation_rate=0.2,
            tournament_size=3
        )

        best_solution, _, _ = ga.run()

        population_results[size] = best_solution.fitness

        print(
            f"Population = {size}, "
            f"Best Fitness = {best_solution.fitness:.2f}"
        )

    # ======================================
    # TEST 2: MUTATION RATE
    # ======================================

    print("\n--- TEST 2: MUTATION RATE ---")

    mutation_rates = [0.1, 0.2, 0.4]

    for rate in mutation_rates:

        print(f"\nTesting mutation rate: {rate}")

        ga = GeneticAlgorithm(
            grid=grid,
            population_size=20,
            generations=20,
            mutation_rate=rate,
            tournament_size=3
        )

        best_solution, _, _ = ga.run()

        mutation_results[rate] = best_solution.fitness

        print(
            f"Mutation Rate = {rate}, "
            f"Best Fitness = {best_solution.fitness:.2f}"
        )

    # ======================================
    # TEST 3: SELECTION PRESSURE
    # ======================================

    print("\n--- TEST 3: SELECTION PRESSURE ---")

    tournament_sizes = [2, 3, 5]

    for size in tournament_sizes:

        print(f"\nTesting tournament size: {size}")

        ga = GeneticAlgorithm(
            grid=grid,
            population_size=20,
            generations=20,
            mutation_rate=0.2,
            tournament_size=size
        )

        best_solution, _, _ = ga.run()

        tournament_results[size] = best_solution.fitness

        print(
            f"Tournament Size = {size}, "
            f"Best Fitness = {best_solution.fitness:.2f}"
        )

    # ======================================
    # DISPLAY RESULTS
    # ======================================

    print("\n======================================")
    print("     SENSITIVITY RESULTS SUMMARY")
    print("======================================")

    print("\nPopulation Size:")
    for setting, score in population_results.items():
        print(f"{setting}: {score:.2f}")

    print("\nMutation Rate:")
    for setting, score in mutation_results.items():
        print(f"{setting}: {score:.2f}")

    print("\nTournament Size:")
    for setting, score in tournament_results.items():
        print(f"{setting}: {score:.2f}")

    # ======================================
    # PLOT SENSITIVITY GRAPHS
    # ======================================

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Graph 1: Population size
    axes[0].plot(
        list(population_results.keys()),
        list(population_results.values()),
        marker="o"
    )

    axes[0].set_title("Population Size")
    axes[0].set_xlabel("Population Size")
    axes[0].set_ylabel("Best Fitness")
    axes[0].grid(True)

    # Graph 2: Mutation rate
    axes[1].plot(
        list(mutation_results.keys()),
        list(mutation_results.values()),
        marker="o"
    )

    axes[1].set_title("Mutation Rate")
    axes[1].set_xlabel("Mutation Rate")
    axes[1].set_ylabel("Best Fitness")
    axes[1].grid(True)

    # Graph 3: Tournament size
    axes[2].plot(
        list(tournament_results.keys()),
        list(tournament_results.values()),
        marker="o"
    )

    axes[2].set_title("Selection Pressure")
    axes[2].set_xlabel("Tournament Size")
    axes[2].set_ylabel("Best Fitness")
    axes[2].grid(True)

    fig.suptitle("Genetic Algorithm Sensitivity Analysis")
    fig.tight_layout()
    plt.show()

    print("\nSensitivity analysis completed successfully.")

    return (
        population_results,
        mutation_results,
        tournament_results
    )
