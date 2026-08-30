"""Encounter-based, reversible binding simulations for Module 3."""

from collections.abc import Sequence
from math import hypot, sqrt
import random
from typing import Literal

from cell_sim.models import (
    BindingMetadata,
    BindingResult,
    BindingStateCounts,
    BoundComplex,
    Molecule,
)

BoundaryPolicy = Literal["none", "reflecting"]


class BindingSimulation:
    """A two-species diffusion model with one-to-one reversible binding."""

    def __init__(
        self,
        *,
        width: float,
        height: float,
        a_count: int,
        b_count: int,
        timestep: float,
        a_diffusion_coefficient: float,
        b_diffusion_coefficient: float,
        complex_diffusion_coefficient: float,
        encounter_radius: float,
        binding_probability: float,
        dissociation_probability: float,
        random_seed: int | None = None,
        initial_a_positions: Sequence[tuple[float, float]] | None = None,
        initial_b_positions: Sequence[tuple[float, float]] | None = None,
        boundary_policy: BoundaryPolicy = "reflecting",
    ) -> None:
        self._validate_configuration(
            width=width,
            height=height,
            a_count=a_count,
            b_count=b_count,
            timestep=timestep,
            diffusion_coefficients=(
                a_diffusion_coefficient,
                b_diffusion_coefficient,
                complex_diffusion_coefficient,
            ),
            encounter_radius=encounter_radius,
            probabilities=(binding_probability, dissociation_probability),
            initial_a_positions=initial_a_positions,
            initial_b_positions=initial_b_positions,
            boundary_policy=boundary_policy,
        )
        self.width = width
        self.height = height
        self.timestep = timestep
        self.a_diffusion_coefficient = a_diffusion_coefficient
        self.b_diffusion_coefficient = b_diffusion_coefficient
        self.complex_diffusion_coefficient = complex_diffusion_coefficient
        self.encounter_radius = encounter_radius
        self.binding_probability = binding_probability
        self.dissociation_probability = dissociation_probability
        self.random_seed = random_seed
        self.boundary_policy = boundary_policy
        self._random = random.Random(random_seed)
        center = (width / 2, height / 2)
        a_positions = initial_a_positions or [center] * a_count
        b_positions = initial_b_positions or [center] * b_count
        self.molecules = {
            molecule_id: Molecule(molecule_id, "A", x, y)
            for molecule_id, (x, y) in enumerate(a_positions)
        }
        self.molecules.update(
            {
                a_count + molecule_id: Molecule(a_count + molecule_id, "B", x, y)
                for molecule_id, (x, y) in enumerate(b_positions)
            }
        )
        self.complexes: list[BoundComplex] = []
        self.trajectories = {
            molecule.id: [(molecule.x, molecule.y)]
            for molecule in self.molecules.values()
        }
        self.state_counts = [BindingStateCounts(a_count, b_count, 0)]
        self.steps = 0

    def step(self) -> None:
        """Diffuse, dissociate, bind eligible pairs, and record one timepoint."""
        self._move_free_molecules()
        self._move_complexes()
        self._dissociate_complexes()
        self._bind_encountering_pairs()
        self._record_timepoint()
        self.steps += 1

    def run(self, steps: int) -> None:
        """Advance the simulation by the requested number of timesteps."""
        if steps < 0:
            raise ValueError("Step count cannot be negative.")
        for _ in range(steps):
            self.step()

    def result(self) -> BindingResult:
        """Return an immutable snapshot of the current molecular state history."""
        return BindingResult(
            trajectories=self.trajectories,
            state_counts=tuple(self.state_counts),
            metadata=BindingMetadata(
                width=self.width,
                height=self.height,
                timestep=self.timestep,
                steps=self.steps,
                a_diffusion_coefficient=self.a_diffusion_coefficient,
                b_diffusion_coefficient=self.b_diffusion_coefficient,
                complex_diffusion_coefficient=self.complex_diffusion_coefficient,
                encounter_radius=self.encounter_radius,
                binding_probability=self.binding_probability,
                dissociation_probability=self.dissociation_probability,
                random_seed=self.random_seed,
                boundary_policy=self.boundary_policy,
                a_count=sum(molecule.species == "A" for molecule in self.molecules.values()),
                b_count=sum(molecule.species == "B" for molecule in self.molecules.values()),
            ),
        )

    def _move_free_molecules(self) -> None:
        bound_ids = {complex_.a_id for complex_ in self.complexes} | {
            complex_.b_id for complex_ in self.complexes
        }
        for molecule in self.molecules.values():
            if molecule.id not in bound_ids:
                coefficient = (
                    self.a_diffusion_coefficient
                    if molecule.species == "A"
                    else self.b_diffusion_coefficient
                )
                molecule.x, molecule.y = self._move_position(
                    molecule.x, molecule.y, coefficient
                )

    def _move_complexes(self) -> None:
        for complex_ in self.complexes:
            complex_.x, complex_.y = self._move_position(
                complex_.x, complex_.y, self.complex_diffusion_coefficient
            )

    def _move_position(self, x: float, y: float, coefficient: float) -> tuple[float, float]:
        noise_scale = sqrt(2 * coefficient * self.timestep)
        x += self._random.gauss(0.0, noise_scale)
        y += self._random.gauss(0.0, noise_scale)
        if self.boundary_policy == "reflecting":
            x = self._reflect_coordinate(x, self.width)
            y = self._reflect_coordinate(y, self.height)
        return x, y

    def _dissociate_complexes(self) -> None:
        remaining_complexes = []
        for complex_ in self.complexes:
            if self._random.random() < self.dissociation_probability:
                for molecule_id in (complex_.a_id, complex_.b_id):
                    molecule = self.molecules[molecule_id]
                    molecule.x, molecule.y = complex_.x, complex_.y
            else:
                remaining_complexes.append(complex_)
        self.complexes = remaining_complexes

    def _bind_encountering_pairs(self) -> None:
        bound_ids = {complex_.a_id for complex_ in self.complexes} | {
            complex_.b_id for complex_ in self.complexes
        }
        free_a = sorted(
            (molecule for molecule in self.molecules.values() if molecule.species == "A" and molecule.id not in bound_ids),
            key=lambda molecule: molecule.id,
        )
        free_b = sorted(
            (molecule for molecule in self.molecules.values() if molecule.species == "B" and molecule.id not in bound_ids),
            key=lambda molecule: molecule.id,
        )
        selected_ids: set[int] = set()
        for a_molecule in free_a:
            for b_molecule in free_b:
                if b_molecule.id in selected_ids or not self._are_encountering(a_molecule, b_molecule):
                    continue
                if self._random.random() < self.binding_probability:
                    self.complexes.append(
                        BoundComplex(
                            a_id=a_molecule.id,
                            b_id=b_molecule.id,
                            x=(a_molecule.x + b_molecule.x) / 2,
                            y=(a_molecule.y + b_molecule.y) / 2,
                        )
                    )
                    selected_ids.update((a_molecule.id, b_molecule.id))
                    break

    def _record_timepoint(self) -> None:
        complex_by_molecule_id = {
            molecule_id: complex_
            for complex_ in self.complexes
            for molecule_id in (complex_.a_id, complex_.b_id)
        }
        for molecule in self.molecules.values():
            complex_ = complex_by_molecule_id.get(molecule.id)
            position = (complex_.x, complex_.y) if complex_ else (molecule.x, molecule.y)
            self.trajectories[molecule.id].append(position)
        bound_count = len(self.complexes)
        self.state_counts.append(
            BindingStateCounts(
                free_a=sum(
                    molecule.species == "A" and molecule.id not in complex_by_molecule_id
                    for molecule in self.molecules.values()
                ),
                free_b=sum(
                    molecule.species == "B" and molecule.id not in complex_by_molecule_id
                    for molecule in self.molecules.values()
                ),
                bound_complexes=bound_count,
            )
        )

    def _are_encountering(self, a_molecule: Molecule, b_molecule: Molecule) -> bool:
        return hypot(a_molecule.x - b_molecule.x, a_molecule.y - b_molecule.y) <= self.encounter_radius

    @staticmethod
    def _reflect_coordinate(coordinate: float, limit: float) -> float:
        reflected_coordinate = coordinate % (2 * limit)
        return 2 * limit - reflected_coordinate if reflected_coordinate > limit else reflected_coordinate

    @staticmethod
    def _validate_configuration(
        *,
        width: float,
        height: float,
        a_count: int,
        b_count: int,
        timestep: float,
        diffusion_coefficients: tuple[float, float, float],
        encounter_radius: float,
        probabilities: tuple[float, float],
        initial_a_positions: Sequence[tuple[float, float]] | None,
        initial_b_positions: Sequence[tuple[float, float]] | None,
        boundary_policy: str,
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Simulation dimensions must be positive.")
        if a_count < 0 or b_count < 0:
            raise ValueError("Species counts cannot be negative.")
        if timestep <= 0:
            raise ValueError("Timestep must be positive.")
        if any(coefficient < 0 for coefficient in diffusion_coefficients):
            raise ValueError("Diffusion coefficients cannot be negative.")
        if encounter_radius < 0:
            raise ValueError("Encounter radius cannot be negative.")
        if any(not 0 <= probability <= 1 for probability in probabilities):
            raise ValueError("Binding probabilities must be between 0 and 1.")
        if boundary_policy not in {"none", "reflecting"}:
            raise ValueError("Boundary policy must be 'none' or 'reflecting'.")
        BindingSimulation._validate_positions(initial_a_positions, a_count, width, height)
        BindingSimulation._validate_positions(initial_b_positions, b_count, width, height)

    @staticmethod
    def _validate_positions(
        positions: Sequence[tuple[float, float]] | None,
        expected_count: int,
        width: float,
        height: float,
    ) -> None:
        if positions is None:
            return
        if len(positions) != expected_count:
            raise ValueError("Initial position count must equal species count.")
        if any(not 0 <= x <= width or not 0 <= y <= height for x, y in positions):
            raise ValueError("Initial positions must be inside the simulation domain.")