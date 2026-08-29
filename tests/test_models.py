"""Tests for the simulation data model."""

import pytest

from cell_sim.models import Particle, SimulationMetadata, SimulationResult


def test_particle_retains_identity_and_position() -> None:
    particle = Particle(id=7, x=1.25, y=3.5)

    assert particle.id == 7
    assert particle.x == 1.25
    assert particle.y == 3.5


def test_particle_position_can_be_updated() -> None:
    particle = Particle(id=7, x=1.25, y=3.5)

    particle.x = 2.0
    particle.y = 4.0

    assert (particle.x, particle.y) == (2.0, 4.0)


def test_simulation_result_retains_trajectories_and_metadata() -> None:
    metadata = SimulationMetadata(
        width=10.0,
        height=5.0,
        timestep=0.1,
        steps=2,
        noise_scale=0.5,
        random_seed=42,
        boundary_policy="reflecting",
    )
    trajectories = {0: ((1.0, 1.0), (1.1, 0.9), (1.3, 1.0))}

    result = SimulationResult(trajectories=trajectories, metadata=metadata)

    assert result.trajectories[0] == ((1.0, 1.0), (1.1, 0.9), (1.3, 1.0))
    assert result.metadata.random_seed == 42
    assert result.metadata.steps == 2


def test_simulation_result_copies_trajectories_into_an_immutable_snapshot() -> None:
    metadata = SimulationMetadata(
        width=10.0,
        height=5.0,
        timestep=0.1,
        steps=1,
        noise_scale=0.5,
        random_seed=42,
        boundary_policy="reflecting",
    )
    trajectories = {0: [(1.0, 1.0), (1.1, 0.9)]}

    result = SimulationResult(trajectories=trajectories, metadata=metadata)
    trajectories[0].append((1.3, 1.0))

    assert result.trajectories[0] == ((1.0, 1.0), (1.1, 0.9))
    with pytest.raises(TypeError):
        result.trajectories[1] = ((2.0, 2.0),)  # type: ignore[index]