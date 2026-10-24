
from genetic_algorithm import GeneticAlgorithm
from fitness import calculate_fitness, get_line_cells
from random_search import run_random_search
from visualization import (
    plot_fitness,
    plot_uav_route,
    plot_coverage_heatmap
)
from sensitive_analysis import run_sensitivity_analysis


def create_grid():
    # Grid size: 10 x 10
    grid = [[0 for _ in range(10)] for _ in range(10)]

    # No-fly zones
    no_fly_zones = [
        (3, 2), (3, 3), (3, 4),
        (4, 4), (5, 4)
    ]

    # Hazard zones
    hazard_zones = [
        (6, 2), (6, 3), (7, 3)
    ]

    # Priority zones
    priority_zones = [
        (7, 1), (8, 1), (8, 2),
        (2, 7), (3, 7)
    ]

    # Mark zones on grid using grid[y][x]
    for x, y in no_fly_zones:
        grid[y][x] = 1

    for x, y in hazard_zones:
        grid[y][x] = 2

    for x, y in priority_zones:
        grid[y][x] = 3

    return grid, no_fly_zones, hazard_zones, priority_zones


def validate_route(solution, no_fly_zones):
    """Check route cells using the project's line-sampling method."""
    no_fly_set = set(no_fly_zones)
    route_cells = set()

    for i in range(len(solution.waypoints) - 1):
        cells = get_line_cells(
            solution.waypoints[i],
            solution.waypoints[i + 1]
        )
        route_cells.update(cells)

    hits = route_cells.intersection(no_fly_set)

    print("\n===== ROUTE VALIDATION =====")

    if hits:
        print("Route Validation: FAIL")
        print("No-fly zone intersections:", sorted(hits))
    else:
        print("Route Validation: PASS")
        print("No sampled route cells intersect no-fly zones.")

    return len(hits) == 0


def main():
    print("==========================================")
    print(" UAV DISASTER MANAGEMENT STRATEGY ENGINE")
    print(" Genetic Algorithm vs Random Search")
    print("==========================================")

    # Step 1: Create hazard grid
    grid, no_fly_zones, hazard_zones, priority_zones = create_grid()

    print("\nGrid created successfully.")
    print("Grid size: 10 x 10")
    print("Start position: (0, 0)")
    print("Destination: (9, 9)")
    print("No-fly zones:", no_fly_zones)
    print("Hazard zones:", hazard_zones)
    print("Priority zones:", priority_zones)

    # Step 2: Run Genetic Algorithm
    print("\n===== STARTING GENETIC ALGORITHM =====")

    ga = GeneticAlgorithm(
        grid=grid,
        population_size=20,
        generations=30,
        mutation_rate=0.2,
        tournament_size=3
    )

    best_solution, best_history, average_history = ga.run()

    # Step 3: Validate the best route
    validate_route(best_solution, no_fly_zones)

    # Step 4: Show fitness details
    print("\n===== BEST SOLUTION FITNESS DETAILS =====")
    calculate_fitness(best_solution, grid, show_details=True)

    # Step 5: Plot GA convergence
    print("\nDisplaying fitness convergence graph...")
    plot_fitness(best_history, average_history)

    # Step 6: Plot UAV route
    print("\nDisplaying UAV route...")
    plot_uav_route(
        best_solution,
        grid,
        no_fly_zones,
        hazard_zones,
        priority_zones
    )

    # Step 7: Plot coverage heatmap
    print("\nDisplaying route and coverage heatmap...")
    plot_coverage_heatmap(
        best_solution,
        grid,
        no_fly_zones,
        hazard_zones,
        priority_zones
    )

    # Step 8: Run Random Search for comparison
    print("\n===== STARTING RANDOM SEARCH COMPARISON =====")

    random_solution, random_history = run_random_search(
        grid=grid,
        no_fly_zones=no_fly_zones,
        attempts=600
    )

    # Step 9: Compare results
    print("\n==========================================")
    print("       GA VS RANDOM SEARCH")
    print("==========================================")

    print(f"Genetic Algorithm Fitness: {best_solution.fitness:.2f}")
    print(f"Random Search Fitness:     {random_solution.fitness:.2f}")

    if best_solution.fitness > random_solution.fitness:
        print("GA found a higher-fitness solution in this run.")
    elif best_solution.fitness < random_solution.fitness:
        print("Random Search found a higher-fitness solution in this run.")
    else:
        print("Both methods found the same fitness in this run.")

    print("\nGA generations:", len(best_history))
    print("Random Search attempts:", len(random_history))

    # Step 10: Sensitivity analysis
    print("\n===== STARTING SENSITIVITY ANALYSIS =====")

    run_sensitivity_analysis(
        grid=grid,
        no_fly_zones=no_fly_zones
    )

    print("\n==========================================")
    print("       SIMULATION COMPLETED")
    print("==========================================")


if __name__ == "__main__":
    main()