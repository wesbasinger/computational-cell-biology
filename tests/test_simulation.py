"""Tests for simulation construction and initial state."""

from math import sqrt

import pytest

from cell_sim.analysis import mean_squared_displacement
from cell_sim.simulation import Simulation


def test_simulation_creates_configured_number_of_centered_particles() -> None:
    simulation = Simulation(
        width=10.0,
        height=6.0,
        particle_count=3,
        timestep=0.1,
        noise_scale=0.5,
        random_seed=42,
    )

    assert [(particle.id, particle.x, particle.y) for particle in simulation.particles] == [
        (0, 5.0, 3.0),
        (1, 5.0, 3.0),
        (2, 5.0, 3.0),
    ]
    assert simulation.trajectories == {
        0: [(5.0, 3.0)],
        1: [(5.0, 3.0)],
        2: [(5.0, 3.0)],
    }


def test_simulation_uses_explicit_initial_positions() -> None:
    simulation = Simulation(
        width=10.0,
        height=6.0,
        particle_count=2,
        timestep=0.1,
        noise_scale=0.5,
        initial_positions=((0.0, 0.0), (10.0, 6.0)),
    )

    assert [(particle.x, particle.y) for particle in simulation.particles] == [
        (0.0, 0.0),
        (10.0, 6.0),
    ]
    assert simulation.trajectories == {0: [(0.0, 0.0)], 1: [(10.0, 6.0)]}


def test_step_moves_particles_and_records_their_new_positions() -> None:
    simulation = Simulation(
        width=10.0,
        height=6.0,
        particle_count=2,
        timestep=0.1,
        noise_scale=0.5,
        random_seed=42,
    )

    simulation.step()

    assert len(simulation.trajectories[0]) == 2
    assert len(simulation.trajectories[1]) == 2
    assert simulation.trajectories[0][-1] == (
        simulation.particles[0].x,
        simulation.particles[0].y,
    )
    assert simulation.trajectories[1][-1] == (
        simulation.particles[1].x,
        simulation.particles[1].y,
    )
    assert simulation.trajectories[0][-1] != simulation.trajectories[0][0]


def test_zero_noise_step_preserves_particle_positions() -> None:
    simulation = Simulation(
        width=10.0,
        height=6.0,
        particle_count=1,
        timestep=0.1,
        noise_scale=0.0,
        random_seed=42,
    )

    simulation.step()

    assert simulation.trajectories[0] == [(5.0, 3.0), (5.0, 3.0)]


def test_diffusion_factory_derives_coordinate_noise_scale_and_metadata() -> None:
    simulation = Simulation.for_diffusion(
        width=10.0,
        height=6.0,
        particle_count=2,
        timestep=0.25,
        diffusion_coefficient=0.8,
        random_seed=42,
        boundary_policy="none",
    )

    assert simulation.noise_scale == sqrt(2 * 0.8 * 0.25)
    assert simulation.result().metadata.diffusion_coefficient == 0.8


def test_diffusion_factory_rejects_negative_diffusion_coefficient() -> None:
    with pytest.raises(ValueError, match="Diffusion coefficient"):
        Simulation.for_diffusion(
            width=10.0,
            height=6.0,
            particle_count=1,
            timestep=0.1,
            diffusion_coefficient=-0.1,
        )


def test_zero_diffusion_coefficient_produces_stationary_particles() -> None:
    simulation = Simulation.for_diffusion(
        width=10.0,
        height=6.0,
        particle_count=2,
        timestep=0.1,
        diffusion_coefficient=0.0,
        random_seed=42,
    )

    simulation.run(5)

    assert all(
        trajectory == [(5.0, 3.0)] * 6
        for trajectory in simulation.trajectories.values()
    )


def test_matching_seed_and_initial_state_reproduce_diffusion_trajectories() -> None:
    parameters = {
        "width": 10.0,
        "height": 6.0,
        "particle_count": 2,
        "timestep": 0.1,
        "diffusion_coefficient": 0.8,
        "random_seed": 42,
        "initial_positions": ((1.0, 1.0), (2.0, 2.0)),
        "boundary_policy": "none",
    }
    first_simulation = Simulation.for_diffusion(**parameters)
    second_simulation = Simulation.for_diffusion(**parameters)

    first_simulation.run(5)
    second_simulation.run(5)

    assert first_simulation.trajectories == second_simulation.trajectories


def test_unbounded_diffusion_ensemble_msd_matches_theoretical_value() -> None:
    diffusion_coefficient = 0.8
    timestep = 0.1
    steps = 200
    simulation = Simulation.for_diffusion(
        width=1_000.0,
        height=1_000.0,
        particle_count=10_000,
        timestep=timestep,
        diffusion_coefficient=diffusion_coefficient,
        random_seed=42,
        boundary_policy="none",
    )

    simulation.run(steps)

    expected_msd = 4 * diffusion_coefficient * timestep * steps
    assert mean_squared_displacement(simulation.result()) == pytest.approx(
        expected_msd, rel=0.05
    )


def test_reflecting_boundary_keeps_particles_inside_the_domain() -> None:
    simulation = Simulation(
        width=1.0,
        height=1.0,
        particle_count=2,
        timestep=0.1,
        noise_scale=10.0,
        random_seed=42,
    )

    simulation.run(100)

    assert all(
        0.0 <= x <= simulation.width and 0.0 <= y <= simulation.height
        for trajectory in simulation.trajectories.values()
        for x, y in trajectory
    )


def test_none_boundary_allows_particles_to_leave_the_domain() -> None:
    simulation = Simulation(
        width=1.0,
        height=1.0,
        particle_count=1,
        timestep=0.1,
        noise_scale=10.0,
        random_seed=42,
        boundary_policy="none",
    )

    simulation.run(100)

    assert any(
        x < 0.0 or x > simulation.width or y < 0.0 or y > simulation.height
        for x, y in simulation.trajectories[0]
    )


def test_matching_seed_and_initial_state_produce_matching_step() -> None:
    parameters = {
        "width": 10.0,
        "height": 6.0,
        "particle_count": 2,
        "timestep": 0.1,
        "noise_scale": 0.5,
        "random_seed": 42,
        "initial_positions": ((1.0, 1.0), (2.0, 2.0)),
    }
    first_simulation = Simulation(**parameters)
    second_simulation = Simulation(**parameters)

    first_simulation.step()
    second_simulation.step()

    assert first_simulation.trajectories == second_simulation.trajectories


def test_run_records_one_position_per_particle_for_each_step() -> None:
    simulation = Simulation(
        width=10.0,
        height=6.0,
        particle_count=2,
        timestep=0.1,
        noise_scale=0.5,
        random_seed=42,
    )

    simulation.run(5)

    assert all(len(trajectory) == 6 for trajectory in simulation.trajectories.values())


def test_different_seeds_produce_different_run_trajectories() -> None:
    parameters = {
        "width": 10.0,
        "height": 6.0,
        "particle_count": 2,
        "timestep": 0.1,
        "noise_scale": 0.5,
        "initial_positions": ((1.0, 1.0), (2.0, 2.0)),
    }
    first_simulation = Simulation(**parameters, random_seed=42)
    second_simulation = Simulation(**parameters, random_seed=43)

    first_simulation.run(5)
    second_simulation.run(5)

    assert first_simulation.trajectories != second_simulation.trajectories


def test_run_rejects_negative_step_counts() -> None:
    simulation = Simulation(
        width=10.0,
        height=6.0,
        particle_count=1,
        timestep=0.1,
        noise_scale=0.5,
    )

    with pytest.raises(ValueError, match="Step count"):
        simulation.run(-1)


def test_result_returns_immutable_snapshot_with_reproducibility_metadata() -> None:
    simulation = Simulation(
        width=10.0,
        height=6.0,
        particle_count=1,
        timestep=0.1,
        noise_scale=0.5,
        random_seed=42,
        boundary_policy="none",
    )
    simulation.run(2)

    result = simulation.result()
    simulation.step()

    assert result.metadata.steps == 2
    assert result.metadata.boundary_policy == "none"
    assert len(result.trajectories[0]) == 3
    assert len(simulation.trajectories[0]) == 4


@pytest.mark.parametrize(
    ("parameters", "message"),
    [
        ({"width": 0.0}, "Simulation dimensions"),
        ({"particle_count": -1}, "Particle count"),
        ({"timestep": 0.0}, "Timestep"),
        ({"noise_scale": -0.1}, "Noise scale"),
        ({"boundary_policy": "invalid"}, "Boundary policy"),
        ({"initial_positions": ((1.0, 1.0),)}, "Initial position count"),
        ({"initial_positions": ((11.0, 1.0), (2.0, 2.0))}, "inside"),
    ],
)
def test_simulation_rejects_invalid_configuration(
    parameters: dict[str, object], message: str
) -> None:
    base_parameters: dict[str, object] = {
        "width": 10.0,
        "height": 6.0,
        "particle_count": 2,
        "timestep": 0.1,
        "noise_scale": 0.5,
    }

    with pytest.raises(ValueError, match=message):
        Simulation(**(base_parameters | parameters))  # type: ignore[arg-type]