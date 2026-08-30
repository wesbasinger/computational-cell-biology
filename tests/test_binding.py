"""Tests for molecular encounters and reversible binding."""

import pytest

from cell_sim.binding import BindingSimulation
from cell_sim.models import BindingStateCounts


def build_simulation(**parameters: object) -> BindingSimulation:
    defaults: dict[str, object] = {
        "width": 10.0,
        "height": 10.0,
        "a_count": 1,
        "b_count": 1,
        "timestep": 0.1,
        "a_diffusion_coefficient": 0.0,
        "b_diffusion_coefficient": 0.0,
        "complex_diffusion_coefficient": 0.0,
        "encounter_radius": 1.0,
        "binding_probability": 1.0,
        "dissociation_probability": 0.0,
        "initial_a_positions": ((1.0, 1.0),),
        "initial_b_positions": ((1.5, 1.0),),
    }
    return BindingSimulation(**(defaults | parameters))  # type: ignore[arg-type]


def test_particles_outside_the_encounter_radius_cannot_bind() -> None:
    simulation = build_simulation(initial_b_positions=((3.0, 1.0),))

    simulation.step()

    assert simulation.result().state_counts[-1] == BindingStateCounts(1, 1, 0)


def test_encountering_particles_bind_with_probability_one() -> None:
    simulation = build_simulation()

    simulation.step()

    assert simulation.result().state_counts == (
        BindingStateCounts(1, 1, 0),
        BindingStateCounts(0, 0, 1),
    )
    assert simulation.trajectories[0][-1] == simulation.trajectories[1][-1]


def test_complex_dissociates_with_probability_one() -> None:
    simulation = build_simulation(dissociation_probability=1.0)
    simulation.step()
    simulation.binding_probability = 0.0

    simulation.step()

    assert simulation.result().state_counts[-1] == BindingStateCounts(1, 1, 0)


def test_particle_can_participate_in_at_most_one_binding_event_per_step() -> None:
    simulation = build_simulation(
        a_count=2,
        initial_a_positions=((1.0, 1.0), (1.25, 1.0)),
    )

    simulation.step()

    assert simulation.result().state_counts[-1] == BindingStateCounts(1, 0, 1)


def test_matching_configuration_and_seed_reproduce_results() -> None:
    parameters = {
        "a_diffusion_coefficient": 1.0,
        "b_diffusion_coefficient": 0.8,
        "complex_diffusion_coefficient": 0.5,
        "binding_probability": 0.3,
        "dissociation_probability": 0.2,
        "random_seed": 42,
    }
    first_simulation = build_simulation(**parameters)
    second_simulation = build_simulation(**parameters)

    first_simulation.run(10)
    second_simulation.run(10)

    assert first_simulation.result() == second_simulation.result()


def test_state_counts_conserve_molecules() -> None:
    simulation = build_simulation(a_count=2, b_count=3, initial_a_positions=None, initial_b_positions=None)

    simulation.run(5)

    assert all(
        counts.free_a + counts.bound_complexes == 2
        and counts.free_b + counts.bound_complexes == 3
        for counts in simulation.result().state_counts
    )


def test_reflecting_boundaries_keep_all_molecules_in_the_domain() -> None:
    simulation = build_simulation(
        width=1.0,
        height=1.0,
        a_diffusion_coefficient=100.0,
        b_diffusion_coefficient=100.0,
        complex_diffusion_coefficient=100.0,
        initial_a_positions=((0.5, 0.5),),
        initial_b_positions=((0.5, 0.5),),
        random_seed=42,
    )

    simulation.run(20)

    assert all(
        0 <= coordinate <= 1
        for trajectory in simulation.result().trajectories.values()
        for position in trajectory
        for coordinate in position
    )


@pytest.mark.parametrize(
    ("parameters", "message"),
    [
        ({"encounter_radius": -0.1}, "Encounter radius"),
        ({"binding_probability": 1.1}, "Binding probabilities"),
        ({"dissociation_probability": -0.1}, "Binding probabilities"),
        ({"a_diffusion_coefficient": -0.1}, "Diffusion coefficients"),
    ],
)
def test_binding_simulation_rejects_invalid_configuration(
    parameters: dict[str, object], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        build_simulation(**parameters)