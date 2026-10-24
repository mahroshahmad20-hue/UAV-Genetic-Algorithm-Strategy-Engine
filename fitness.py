
import math


def get_line_cells(point1, point2):
    """Return grid cells crossed by a line between two points."""

    x1, y1 = point1
    x2, y2 = point2

    cells = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    steps = max(dx, dy, 1)

    for i in range(steps + 1):
        x = round(x1 + (x2 - x1) * i / steps)
        y = round(y1 + (y2 - y1) * i / steps)

        cell = (x, y)

        if cell not in cells:
            cells.append(cell)

    return cells


def calculate_fitness(chromosome, grid, show_details=False):

    waypoints = chromosome.waypoints
    speeds = chromosome.speeds
    sensor_power = chromosome.sensor_power

    # Step 1: Find priority cells
    priority_cells = set()

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 3:
                priority_cells.add((x, y))

    # Step 2: Calculate priority coverage
    visited_priority = set()

    for x, y in waypoints:
        if grid[y][x] == 3:
            visited_priority.add((x, y))

    if priority_cells:
        coverage = len(visited_priority) / len(priority_cells)
    else:
        coverage = 0.0

    # Step 3: Calculate sensor detection score
    if sensor_power:
        detection = sum(sensor_power) / len(sensor_power)
    else:
        detection = 0.0

    # Step 4: Calculate distance and flight time
    distance = 0.0
    flight_time = 0.0
    energy_raw = 0.0

    for i in range(len(waypoints) - 1):

        segment_distance = math.dist(
            waypoints[i],
            waypoints[i + 1]
        )

        distance += segment_distance

        speed = speeds[i]

        if speed > 0:
            flight_time += segment_distance / speed

        energy_raw += segment_distance * (speed ** 2)

    energy_raw += sum(sensor_power) * 2

    energy = min(energy_raw / 200, 1.0)
    time_cost = min(flight_time / 30, 1.0)

    # Step 5: Count hazard waypoints
    hazard_count = 0

    for x, y in waypoints:
        if grid[y][x] == 2:
            hazard_count += 1

    risk = min(hazard_count / 3, 1.0)

    # Step 6: Check every route segment for no-fly cells
    no_fly_hits = set()

    for i in range(len(waypoints) - 1):

        segment_cells = get_line_cells(
            waypoints[i],
            waypoints[i + 1]
        )

        for x, y in segment_cells:
            if grid[y][x] == 1:
                no_fly_hits.add((x, y))

    # Step 7: Calculate final fitness
    fitness = (
        40 * coverage
        + 20 * detection
        - 15 * energy
        - 15 * time_cost
        - 10 * risk
        - 100 * len(no_fly_hits)
    )

    chromosome.fitness = fitness

    # Step 8: Display results when requested
    if show_details:
        print("\n--- FITNESS RESULTS ---")
        print("Priority Coverage:", round(coverage, 2))
        print("Target Detection:", round(detection, 2))
        print("Total Distance:", round(distance, 2))
        print("Energy Cost:", round(energy, 2))
        print("Flight Time Cost:", round(time_cost, 2))
        print("Hazard Risk:", round(risk, 2))
        print("No-Fly Cells Crossed:", len(no_fly_hits))
        print("No-Fly Cells:", sorted(no_fly_hits))
        print("Final Fitness:", round(fitness, 2))

    return fitness
