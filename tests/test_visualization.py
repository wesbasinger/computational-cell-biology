"""Tests for trajectory visualization."""

import matplotlib

matplotlib.use("Agg")

from cell_sim.models import SimulationMetadata, SimulationResult
from cell_sim.visualization import plot_trajectories


def test_plot_trajectories_draws_one_line_per_particle() -> None:
    metadata = SimulationMetadata(
        width=10.0,
        height=5.0,
        timestep=0.1,
        steps=2,
        noise_scale=0.5,
        random_seed=42,
        boundary_policy="reflecting",
    )
    result = SimulationResult(
        trajectories={
            0: ((1.0, 1.0), (2.0, 2.0), (3.0, 2.0)),
            1: ((5.0, 4.0), (4.0, 3.0), (3.0, 3.0)),
        },
        metadata=metadata,
    )

    axes = plot_trajectories(result)

    assert len(axes.lines) == 2
    assert axes.get_xlim() == (0.0, 10.0)
    assert axes.get_ylim() == (0.0, 5.0)
    assert axes.get_xlabel() == "x position"
    assert axes.get_ylabel() == "y position"
    assert axes.get_legend() is None