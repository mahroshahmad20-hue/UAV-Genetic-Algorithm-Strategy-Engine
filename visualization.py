
import matplotlib.pyplot as plt
import numpy as np


def plot_fitness(best_history, average_history):
    generations = range(1, len(best_history) + 1)

    plt.figure(figsize=(9, 5))

    plt.plot(
        generations,
        best_history,
        label="Best Fitness",
        marker="o"
    )

    plt.plot(
        generations,
        average_history,
        label="Average Fitness",
        marker="x"
    )

    plt.title("Genetic Algorithm Fitness Convergence")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_uav_route(
    best_solution,
    grid,
    no_fly_zones,
    hazard_zones,
    priority_zones
):
    plt.figure(figsize=(8, 8))

    grid_size = len(grid)

    plt.xlim(-0.5, grid_size - 0.5)
    plt.ylim(-0.5, grid_size - 0.5)
    plt.xticks(range(grid_size))
    plt.yticks(range(grid_size))
    plt.grid(True)

    for i, (x, y) in enumerate(no_fly_zones):
        plt.scatter(
            x, y, marker="s", s=180,
            label="No-Fly Zone" if i == 0 else None
        )

    for i, (x, y) in enumerate(hazard_zones):
        plt.scatter(
            x, y, marker="^", s=150,
            label="Hazard Zone" if i == 0 else None
        )

    for i, (x, y) in enumerate(priority_zones):
        plt.scatter(
            x, y, marker="*", s=200,
            label="Priority Zone" if i == 0 else None
        )

    xs = [point[0] for point in best_solution.waypoints]
    ys = [point[1] for point in best_solution.waypoints]

    plt.plot(
        xs, ys, marker="o", linewidth=2,
        label="UAV Route"
    )

    plt.scatter(
        xs[0], ys[0], marker="s", s=150,
        label="Start"
    )

    plt.scatter(
        xs[-1], ys[-1], marker="X", s=150,
        label="Destination"
    )

    plt.title("Best UAV Flight Route")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.gca().invert_yaxis()
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
    plt.tight_layout()
    plt.show()


def plot_coverage_heatmap(
    best_solution,
    grid,
    no_fly_zones,
    hazard_zones,
    priority_zones
):
    grid_size = len(grid)

    # Create a matrix to count route visits.
    coverage = np.zeros((grid_size, grid_size))

    # Mark cells crossed by each route segment.
    for i in range(len(best_solution.waypoints) - 1):
        x1, y1 = best_solution.waypoints[i]
        x2, y2 = best_solution.waypoints[i + 1]

        steps = max(abs(x2 - x1), abs(y2 - y1), 1)

        for step in range(steps + 1):
            x = round(x1 + (x2 - x1) * step / steps)
            y = round(y1 + (y2 - y1) * step / steps)

            coverage[y, x] += 1

    fig, ax = plt.subplots(figsize=(9, 8))

    image = ax.imshow(
        coverage,
        cmap="YlGn",
        origin="upper"
    )

    fig.colorbar(image, ax=ax, label="Route Visits")

    # Draw grid lines.
    ax.set_xticks(range(grid_size))
    ax.set_yticks(range(grid_size))
    ax.set_xticks(
        np.arange(-0.5, grid_size, 1), minor=True
    )
    ax.set_yticks(
        np.arange(-0.5, grid_size, 1), minor=True
    )
    ax.grid(which="minor", color="gray", linewidth=0.7)
    ax.tick_params(which="minor", bottom=False, left=False)

    # Outline special zones.
    for x, y in no_fly_zones:
        ax.scatter(
            x, y, marker="s", s=150,
            facecolors="none", edgecolors="red",
            linewidths=2
        )

    for x, y in hazard_zones:
        ax.scatter(
            x, y, marker="^", s=130,
            facecolors="none", edgecolors="orange",
            linewidths=2
        )

    for x, y in priority_zones:
        ax.scatter(
            x, y, marker="*", s=180,
            facecolors="none", edgecolors="blue",
            linewidths=2
        )

    # Mark start, destination and waypoints.
    xs = [point[0] for point in best_solution.waypoints]
    ys = [point[1] for point in best_solution.waypoints]

    ax.plot(xs, ys, "k-o", linewidth=1.5, markersize=4)
    ax.scatter(xs[0], ys[0], marker="s", s=130, label="Start")
    ax.scatter(
        xs[-1], ys[-1], marker="X", s=130,
        label="Destination"
    )

    ax.set_title("UAV Route Coverage Heatmap")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.legend(loc="upper left", bbox_to_anchor=(1.15, 1))

    plt.tight_layout()
    plt.show()
