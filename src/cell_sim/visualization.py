"""Matplotlib visualizations for completed simulation results."""

from matplotlib.axes import Axes
import matplotlib.pyplot as plt

from cell_sim.analysis import (
    mean_squared_displacement_by_step,
    molecular_state_counts_by_step,
)
from cell_sim.models import BindingResult, SimulationResult


def plot_trajectories(result: SimulationResult, *, axes: Axes | None = None) -> Axes:
    """Plot each particle trajectory and return the axes containing the plot."""
    if axes is None:
        _, axes = plt.subplots()

    for particle_id, trajectory in result.trajectories.items():
        x_coordinates, y_coordinates = zip(*trajectory)
        axes.plot(x_coordinates, y_coordinates, label=f"Particle {particle_id}")

    axes.set_xlim(0.0, result.metadata.width)
    axes.set_ylim(0.0, result.metadata.height)
    axes.set_aspect("equal", adjustable="box")
    axes.set_xlabel("x position")
    axes.set_ylabel("y position")
    axes.set_title("Particle trajectories")
    return axes


def plot_mean_squared_displacement(
    result: SimulationResult, *, axes: Axes | None = None
) -> Axes:
    """Plot observed MSD and, for diffusion results, its unbounded $4Dt$ reference."""
    if axes is None:
        _, axes = plt.subplots()

    elapsed_times = tuple(
        step * result.metadata.timestep
        for step in range(len(mean_squared_displacement_by_step(result)))
    )
    axes.plot(elapsed_times, mean_squared_displacement_by_step(result), label="Observed")

    diffusion_coefficient = result.metadata.diffusion_coefficient
    if diffusion_coefficient is not None:
        axes.plot(
            elapsed_times,
            [4 * diffusion_coefficient * time for time in elapsed_times],
            linestyle="--",
            label="Theory: 4Dt",
        )

    axes.set_xlabel("Elapsed time")
    axes.set_ylabel("Mean squared displacement")
    axes.set_title("Mean squared displacement")
    axes.legend()
    return axes


def plot_molecular_state_counts(
    result: BindingResult, *, axes: Axes | None = None
) -> Axes:
    """Plot free molecule and bound-complex populations across elapsed time."""
    if axes is None:
        _, axes = plt.subplots()

    state_counts = molecular_state_counts_by_step(result)
    elapsed_times = tuple(step * result.metadata.timestep for step in range(len(state_counts)))
    axes.plot(elapsed_times, [counts.free_a for counts in state_counts], label="_nolegend_")
    axes.plot(elapsed_times, [counts.free_b for counts in state_counts], label="Free B")
    axes.plot(
        elapsed_times,
        [counts.bound_complexes for counts in state_counts],
        label="Bound AB",
    )
    axes.set_xlabel("Elapsed time")
    axes.set_ylabel("Molecule count")
    axes.set_title("Molecular binding states")
    axes.legend()
    return axes