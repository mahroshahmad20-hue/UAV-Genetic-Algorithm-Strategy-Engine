
import random

from chromosome import create_random_chromosome, Chromosome
from fitness import calculate_fitness


class GeneticAlgorithm:

    def __init__(
        self,
        grid,
        population_size=20,
        generations=30,
        mutation_rate=0.2,
        tournament_size=3
    ):
        self.grid = grid
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size

        # Find no-fly zone coordinates
        self.no_fly_zones = {
            (x, y)
            for y, row in enumerate(grid)
            for x, cell in enumerate(row)
            if cell == 1
        }

        # Create initial population
        self.population = [
            create_random_chromosome(self.no_fly_zones)
            for _ in range(population_size)
        ]

    # ------------------------------------------
    # STEP 1: EVALUATE POPULATION
    # ------------------------------------------

    def evaluate_population(self):
        for chromosome in self.population:
            calculate_fitness(chromosome, self.grid)

    # ------------------------------------------
    # STEP 2: TOURNAMENT SELECTION
    # ------------------------------------------

    def select_parent(self):

        contestants = random.sample(
            self.population,
            min(self.tournament_size, len(self.population))
        )

        return max(
            contestants,
            key=lambda chromosome: chromosome.fitness
        )

    # ------------------------------------------
    # STEP 3: CROSSOVER
    # ------------------------------------------

    def crossover(self, parent1, parent2):

        # Combine waypoints
        cut = random.randint(
            1,
            len(parent1.waypoints) - 2
        )

        child_waypoints = (
            parent1.waypoints[:cut]
            + parent2.waypoints[cut:-1]
            + [parent1.waypoints[-1]]
        )

        # Combine speeds
        speed_cut = random.randint(
            1,
            len(parent1.speeds) - 1
        )

        child_speeds = (
            parent1.speeds[:speed_cut]
            + parent2.speeds[speed_cut:]
        )

        # Combine sensor power
        sensor_cut = random.randint(
            1,
            len(parent1.sensor_power) - 1
        )

        child_sensor = (
            parent1.sensor_power[:sensor_cut]
            + parent2.sensor_power[sensor_cut:]
        )

        return Chromosome(
            child_waypoints,
            child_speeds,
            child_sensor
        )

    # ------------------------------------------
    # STEP 4: MUTATION
    # ------------------------------------------

    def mutate(self, chromosome):

        # Mutate intermediate waypoints
        for i in range(1, len(chromosome.waypoints) - 1):

            if random.random() < self.mutation_rate:

                for _ in range(100):

                    x = random.randint(1, 8)
                    y = random.randint(1, 8)

                    if (x, y) not in self.no_fly_zones:
                        chromosome.waypoints[i] = (x, y)
                        break

        # Mutate speeds
        for i in range(len(chromosome.speeds)):

            if random.random() < self.mutation_rate:

                chromosome.speeds[i] = random.randint(1, 3)

        # Mutate sensor power
        for i in range(len(chromosome.sensor_power)):

            if random.random() < self.mutation_rate:

                chromosome.sensor_power[i] = round(
                    random.uniform(0.2, 1.0),
                    2
                )

    # ------------------------------------------
    # STEP 5: RUN GENETIC ALGORITHM
    # ------------------------------------------

    def run(self):

        best_history = []
        average_history = []

        for generation in range(self.generations):

            # Evaluate current population
            self.evaluate_population()

            # Find best chromosome
            best = max(
                self.population,
                key=lambda chromosome: chromosome.fitness
            )

            # Calculate average fitness
            average_fitness = sum(
                chromosome.fitness
                for chromosome in self.population
            ) / len(self.population)

            best_history.append(best.fitness)
            average_history.append(average_fitness)

            print(
                f"Generation {generation + 1}: "
                f"Best Fitness = {best.fitness:.2f}, "
                f"Average Fitness = {average_fitness:.2f}"
            )

            # Elitism: preserve the best solution
            next_population = [
                Chromosome(
                    best.waypoints.copy(),
                    best.speeds.copy(),
                    best.sensor_power.copy()
                )
            ]

            # Generate new population
            while len(next_population) < self.population_size:

                parent1 = self.select_parent()
                parent2 = self.select_parent()

                child = self.crossover(
                    parent1,
                    parent2
                )

                self.mutate(child)

                next_population.append(child)

            # Replace old population
            self.population = next_population

        # Evaluate final population
        self.evaluate_population()

        best_solution = max(
            self.population,
            key=lambda chromosome: chromosome.fitness
        )

        print("\n===== BEST UAV SOLUTION =====")
        best_solution.display()

        return (
            best_solution,
            best_history,
            average_history
        )
