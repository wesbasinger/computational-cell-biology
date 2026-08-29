"""Run a reproducible Brownian-like random-walk experiment for Module 1."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from cell_sim.analysis import (
    displacement_variance,
    mean_displacement,
    mean_squared_displacement,
)
from cell_sim.simulation import Simulation
from cell_sim.visualization import plot_trajectories

FIGURE_SIZE = (8.0, 6.0)
OUTPUT_DPI = 200


def parse_arguments() -> argparse.Namespace:
    """Parse command-line parameters for a single random-walk experiment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--particles", type=int, default=100)
    parser.add_argument("--steps", type=int, default=500)
    parser.add_argument("--width", type=float, default=100.0)
    parser.add_argument("--height", type=float, default=100.0)
    parser.add_argument("--timestep", type=float, default=0.1)
    parser.add_argument("--noise-scale", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--boundary-policy", choices=("none", "reflecting"), default="reflecting"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/module_01/trajectories.png"),
        help="Path for the generated trajectory plot.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the configured experiment, save its plot, and print summary statistics."""
    arguments = parse_arguments()
    simulation = Simulation(
        width=arguments.width,
        height=arguments.height,
        particle_count=arguments.particles,
        timestep=arguments.timestep,
        noise_scale=arguments.noise_scale,
        random_seed=arguments.seed,
        boundary_policy=arguments.boundary_policy,
    )
    simulation.run(arguments.steps)
    result = simulation.result()

    axes = plot_trajectories(result)
    axes.figure.set_size_inches(FIGURE_SIZE)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    axes.figure.savefig(arguments.output, dpi=OUTPUT_DPI, bbox_inches="tight")
    plt.close(axes.figure)

    print(f"Random seed: {result.metadata.random_seed}")
    print(f"Particles: {len(result.trajectories)}")
    print(f"Steps: {result.metadata.steps}")
    print(f"Mean displacement: {mean_displacement(result):.6f}")
    print(f"Displacement variance: {displacement_variance(result):.6f}")
    print(f"Mean squared displacement: {mean_squared_displacement(result):.6f}")
    print(f"Trajectory plot: {arguments.output}")


if __name__ == "__main__":
    main()