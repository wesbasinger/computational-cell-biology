"""Run a reproducible two-species diffusion and reversible-binding experiment."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cell_sim.analysis import bound_fraction_by_step
from cell_sim.binding import BindingSimulation
from cell_sim.visualization import plot_molecular_state_counts

FIGURE_SIZE = (8.0, 6.0)
OUTPUT_DPI = 200


def parse_arguments() -> argparse.Namespace:
    """Parse the parameters for a two-species encounter-and-binding experiment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a-count", type=int, default=100)
    parser.add_argument("--b-count", type=int, default=100)
    parser.add_argument("--steps", type=int, default=500)
    parser.add_argument("--width", type=float, default=20.0)
    parser.add_argument("--height", type=float, default=20.0)
    parser.add_argument("--timestep", type=float, default=0.1)
    parser.add_argument("--a-diffusion-coefficient", type=float, default=1.0)
    parser.add_argument("--b-diffusion-coefficient", type=float, default=1.0)
    parser.add_argument("--complex-diffusion-coefficient", type=float, default=0.5)
    parser.add_argument("--encounter-radius", type=float, default=0.5)
    parser.add_argument("--binding-probability", type=float, default=0.2)
    parser.add_argument("--dissociation-probability", type=float, default=0.02)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--boundary-policy", choices=("none", "reflecting"), default="reflecting"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/module_03/binding_states.png"),
        help="Path for the generated state-count plot.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the experiment, save state populations, and report final binding."""
    arguments = parse_arguments()
    simulation = BindingSimulation(
        width=arguments.width,
        height=arguments.height,
        a_count=arguments.a_count,
        b_count=arguments.b_count,
        timestep=arguments.timestep,
        a_diffusion_coefficient=arguments.a_diffusion_coefficient,
        b_diffusion_coefficient=arguments.b_diffusion_coefficient,
        complex_diffusion_coefficient=arguments.complex_diffusion_coefficient,
        encounter_radius=arguments.encounter_radius,
        binding_probability=arguments.binding_probability,
        dissociation_probability=arguments.dissociation_probability,
        random_seed=arguments.seed,
        boundary_policy=arguments.boundary_policy,
    )
    simulation.run(arguments.steps)
    result = simulation.result()

    axes = plot_molecular_state_counts(result)
    axes.figure.set_size_inches(FIGURE_SIZE)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    axes.figure.savefig(arguments.output, dpi=OUTPUT_DPI, bbox_inches="tight")
    plt.close(axes.figure)

    final_counts = result.state_counts[-1]
    print(f"Random seed: {result.metadata.random_seed}")
    print(f"Boundary policy: {result.metadata.boundary_policy}")
    print(f"Elapsed time: {result.metadata.steps * result.metadata.timestep:.6f}")
    print(f"Final free A: {final_counts.free_a}")
    print(f"Final free B: {final_counts.free_b}")
    print(f"Final bound AB: {final_counts.bound_complexes}")
    print(f"Final bound fraction: {bound_fraction_by_step(result)[-1]:.2%}")
    print(f"State plot: {arguments.output}")


if __name__ == "__main__":
    main()