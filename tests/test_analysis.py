"""Tests for final-displacement statistics."""

import pytest

from cell_sim.analysis import (
    displacement_variance,
    final_displacements,
    mean_displacement,
    mean_squared_displacement,
)
from cell_sim.models import SimulationMetadata, SimulationResult


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