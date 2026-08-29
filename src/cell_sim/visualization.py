"""Matplotlib visualizations for completed simulation results."""

from matplotlib.axes import Axes
import matplotlib.pyplot as plt

from cell_sim.models import SimulationResult


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