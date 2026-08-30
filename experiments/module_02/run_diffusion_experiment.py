"""Run a reproducible idealized two-dimensional diffusion experiment."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cell_sim.analysis import mean_squared_displacement, mean_squared_displacement_by_step
from cell_sim.simulation import Simulation
from cell_sim.visualization import plot_mean_squared_displacement

FIGURE_SIZE = (8.0, 6.0)
OUTPUT_DPI = 200


def parse_arguments() -> argparse.Namespace:
    """Parse command-line parameters for an idealized diffusion experiment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--particles", type=int, default=10_000)
    parser.add_argument("--steps", type=int, default=500)
    parser.add_argument("--width", type=float, default=1_000.0)
    parser.add_argument("--height", type=float, default=1_000.0)
    parser.add_argument("--timestep", type=float, default=0.1)
    parser.add_argument("--diffusion-coefficient", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--boundary-policy", choices=("none", "reflecting"), default="none"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/module_02/msd_comparison.png"),
        help="Path for the generated MSD plot.",
    )
    return parser.parse_args()


def main() -> None:
    """Run, plot, and report a finite-sample diffusion measurement."""
    arguments = parse_arguments()
    simulation = Simulation.for_diffusion(
        width=arguments.width,
        height=arguments.height,
        particle_count=arguments.particles,
        timestep=arguments.timestep,
        diffusion_coefficient=arguments.diffusion_coefficient,
        random_seed=arguments.seed,
        boundary_policy=arguments.boundary_policy,
    )
    simulation.run(arguments.steps)
    result = simulation.result()

    axes = plot_mean_squared_displacement(result)
    axes.figure.set_size_inches(FIGURE_SIZE)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    axes.figure.savefig(arguments.output, dpi=OUTPUT_DPI, bbox_inches="tight")
    plt.close(axes.figure)

    elapsed_time = result.metadata.steps * result.metadata.timestep
    theoretical_msd = 4 * arguments.diffusion_coefficient * elapsed_time
    observed_msd = mean_squared_displacement(result)
    relative_error = (observed_msd - theoretical_msd) / theoretical_msd if theoretical_msd else 0.0

    print(f"Random seed: {result.metadata.random_seed}")
    print(f"Boundary policy: {result.metadata.boundary_policy}")
    print(f"Particles: {len(result.trajectories)}")
    print(f"Elapsed time: {elapsed_time:.6f}")
    print(f"Observed final MSD: {observed_msd:.6f}")
    print(f"Unbounded theory (4Dt): {theoretical_msd:.6f}")
    print(f"Relative final MSD error: {relative_error:.2%}")
    print(f"Recorded MSD timepoints: {len(mean_squared_displacement_by_step(result))}")
    print(f"MSD plot: {arguments.output}")


if __name__ == "__main__":
    main()