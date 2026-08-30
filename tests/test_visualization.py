"""Tests for trajectory visualization."""

import matplotlib

matplotlib.use("Agg")

from cell_sim.models import (
    BindingMetadata,
    BindingResult,
    BindingStateCounts,
    SimulationMetadata,
    SimulationResult,
)
from cell_sim.visualization import (
    plot_mean_squared_displacement,
    plot_molecular_state_counts,
    plot_trajectories,
)


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


def test_plot_mean_squared_displacement_draws_observed_and_theoretical_lines() -> None:
    metadata = SimulationMetadata(
        width=10.0,
        height=5.0,
        timestep=0.5,
        steps=2,
        noise_scale=1.0,
        random_seed=42,
        boundary_policy="none",
        diffusion_coefficient=1.0,
    )
    result = SimulationResult(
        trajectories={0: ((0.0, 0.0), (1.0, 0.0), (2.0, 0.0))},
        metadata=metadata,
    )

    axes = plot_mean_squared_displacement(result)

    assert len(axes.lines) == 2
    assert list(axes.lines[0].get_xdata()) == [0.0, 0.5, 1.0]
    assert list(axes.lines[0].get_ydata()) == [0.0, 1.0, 4.0]
    assert list(axes.lines[1].get_ydata()) == [0.0, 2.0, 4.0]
    assert axes.get_xlabel() == "Elapsed time"
    assert axes.get_ylabel() == "Mean squared displacement"


def test_plot_molecular_state_counts_draws_one_line_per_state() -> None:
    result = BindingResult(
        trajectories={},
        state_counts=(
            BindingStateCounts(2, 2, 0),
            BindingStateCounts(1, 1, 1),
        ),
        metadata=BindingMetadata(
            width=10.0,
            height=5.0,
            timestep=0.5,
            steps=1,
            a_diffusion_coefficient=1.0,
            b_diffusion_coefficient=1.0,
            complex_diffusion_coefficient=0.5,
            encounter_radius=1.0,
            binding_probability=0.5,
            dissociation_probability=0.1,
            random_seed=42,
            boundary_policy="none",
            a_count=2,
            b_count=2,
        ),
    )

    axes = plot_molecular_state_counts(result)

    assert len(axes.lines) == 3
    assert list(axes.lines[0].get_xdata()) == [0.0, 0.5]
    assert list(axes.lines[2].get_ydata()) == [0, 1]
    assert [text.get_text() for text in axes.get_legend().get_texts()] == [
        "Free B",
        "Bound AB",
    ]
    assert axes.get_xlabel() == "Elapsed time"
    assert axes.get_ylabel() == "Molecule count"