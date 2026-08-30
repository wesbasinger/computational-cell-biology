"""Tests for final-displacement statistics."""

import pytest

from cell_sim.analysis import (
    bound_fraction_by_step,
    displacement_variance,
    final_displacements,
    mean_displacement,
    mean_squared_displacement,
    mean_squared_displacement_by_step,
    molecular_state_counts_by_step,
)
from cell_sim.models import (
    BindingMetadata,
    BindingResult,
    BindingStateCounts,
    SimulationMetadata,
    SimulationResult,
)


@pytest.fixture
def result() -> SimulationResult:
    metadata = SimulationMetadata(
        width=10.0,
        height=10.0,
        timestep=0.1,
        steps=1,
        noise_scale=0.5,
        random_seed=42,
        boundary_policy="reflecting",
    )
    return SimulationResult(
        trajectories={
            0: ((0.0, 0.0), (3.0, 4.0)),
            1: ((0.0, 0.0), (0.0, 0.0)),
        },
        metadata=metadata,
    )


def test_final_displacements_are_measured_from_initial_to_final_position(
    result: SimulationResult,
) -> None:
    assert final_displacements(result) == (5.0, 0.0)


def test_mean_displacement(result: SimulationResult) -> None:
    assert mean_displacement(result) == 2.5


def test_displacement_variance(result: SimulationResult) -> None:
    assert displacement_variance(result) == 6.25


def test_mean_squared_displacement(result: SimulationResult) -> None:
    assert mean_squared_displacement(result) == 12.5


def test_mean_squared_displacement_by_step_includes_the_initial_timepoint(
    result: SimulationResult,
) -> None:
    assert mean_squared_displacement_by_step(result) == (0.0, 12.5)


def test_analysis_rejects_results_without_trajectories() -> None:
    metadata = SimulationMetadata(
        width=10.0,
        height=10.0,
        timestep=0.1,
        steps=0,
        noise_scale=0.5,
        random_seed=42,
        boundary_policy="reflecting",
    )
    result = SimulationResult(trajectories={}, metadata=metadata)

    with pytest.raises(ValueError, match="without trajectories"):
        final_displacements(result)


def test_msd_by_step_rejects_uneven_trajectories() -> None:
    metadata = SimulationMetadata(
        width=10.0,
        height=10.0,
        timestep=0.1,
        steps=1,
        noise_scale=0.5,
        random_seed=42,
        boundary_policy="reflecting",
    )
    result = SimulationResult(
        trajectories={0: ((0.0, 0.0),), 1: ((0.0, 0.0), (1.0, 1.0))},
        metadata=metadata,
    )

    with pytest.raises(ValueError, match="same number"):
        mean_squared_displacement_by_step(result)


@pytest.fixture
def binding_result() -> BindingResult:
    metadata = BindingMetadata(
        width=10.0,
        height=10.0,
        timestep=0.5,
        steps=2,
        a_diffusion_coefficient=1.0,
        b_diffusion_coefficient=1.0,
        complex_diffusion_coefficient=0.5,
        encounter_radius=1.0,
        binding_probability=0.5,
        dissociation_probability=0.1,
        random_seed=42,
        boundary_policy="none",
        a_count=4,
        b_count=2,
    )
    return BindingResult(
        trajectories={},
        state_counts=(
            BindingStateCounts(4, 2, 0),
            BindingStateCounts(3, 1, 1),
            BindingStateCounts(2, 0, 2),
        ),
        metadata=metadata,
    )


def test_binding_state_analysis_returns_counts_and_bound_fraction(
    binding_result: BindingResult,
) -> None:
    assert molecular_state_counts_by_step(binding_result) == binding_result.state_counts
    assert bound_fraction_by_step(binding_result) == (0.0, 0.5, 1.0)