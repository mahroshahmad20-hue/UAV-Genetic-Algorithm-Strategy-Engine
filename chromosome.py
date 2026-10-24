
import random


class Chromosome:

    def __init__(self, waypoints, speeds, sensor_power):
        self.waypoints = waypoints
        self.speeds = speeds
        self.sensor_power = sensor_power
        self.fitness = 0.0

    def display(self):
        print("\n--- UAV CHROMOSOME ---")

        print("Waypoints:")
        for i, point in enumerate(self.waypoints):
            print(f"  Point {i + 1}: {point}")

        print("\nSpeeds:", self.speeds)
        print("Sensor Power:", self.sensor_power)
        print("Fitness:", round(self.fitness, 2))


def create_random_chromosome(no_fly_zones=None):

    # Step 1: Prepare no-fly zone coordinates
    if no_fly_zones is None:
        no_fly_zones = set()
    else:
        no_fly_zones = set(no_fly_zones)

    # Step 2: Fix the starting and ending points
    start = (0, 0)
    destination = (9, 9)

    waypoints = [start]

    # Step 3: Generate 3 safe intermediate waypoints
    while len(waypoints) < 4:

        x = random.randint(1, 8)
        y = random.randint(1, 8)

        # Do not select a no-fly zone
        if (x, y) not in no_fly_zones:
            waypoints.append((x, y))

    # Step 4: Add the destination
    waypoints.append(destination)

    # Step 5: Assign a speed to each route segment
    speeds = [
        random.randint(1, 3)
        for i in range(len(waypoints) - 1)
    ]

    # Step 6: Assign sensor power to each waypoint
    sensor_power = [
        round(random.uniform(0.2, 1.0), 2)
        for i in range(len(waypoints))
    ]

    # Step 7: Return the chromosome
    return Chromosome(
        waypoints,
        speeds,
        sensor_power
    )
