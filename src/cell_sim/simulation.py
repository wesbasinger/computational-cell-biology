"""Core construction and state management for particle simulations."""

from collections.abc import Sequence
import random
from typing import Literal

from cell_sim.models import Particle, SimulationMetadata, SimulationResult

BoundaryPolicy = Literal["none", "reflecting"]


class Simulation:
    """A two-dimensional particle simulation with explicitly configured state."""

    def __init__(
        self,
        *,
        width: float,
        height: float,
        particle_count: int,
        timestep: float,
        noise_scale: float,
        random_seed: int | None = None,
        initial_positions: Sequence[tuple[float, float]] | None = None,
        boundary_policy: BoundaryPolicy = "reflecting",
    ) -> None:
        self._validate_configuration(
            width=width,
            height=height,
            particle_count=particle_count,
            timestep=timestep,
            noise_scale=noise_scale,
            initial_positions=initial_positions,
            boundary_policy=boundary_policy,
        )
        self.width = width
        self.height = height
        self.timestep = timestep
        self.noise_scale = noise_scale
        self.random_seed = random_seed
        self.boundary_policy = boundary_policy
        self._random = random.Random(random_seed)
        positions = initial_positions or [(width / 2, height / 2)] * particle_count
        self.particles = [
            Particle(id=particle_id, x=x, y=y)
            for particle_id, (x, y) in enumerate(positions)
        ]
        self.trajectories = {
            particle.id: [(particle.x, particle.y)] for particle in self.particles
        }
        self.steps = 0

    def step(self) -> None:
        """Advance every particle by one independent Gaussian displacement."""
        for particle in self.particles:
            particle.x += self._random.gauss(0.0, self.noise_scale)
            particle.y += self._random.gauss(0.0, self.noise_scale)
            if self.boundary_policy == "reflecting":
                particle.x = self._reflect_coordinate(particle.x, self.width)
                particle.y = self._reflect_coordinate(particle.y, self.height)
            self.trajectories[particle.id].append((particle.x, particle.y))
        self.steps += 1

    def run(self, steps: int) -> None:
        """Advance the simulation by the requested number of steps."""
        if steps < 0:
            raise ValueError("Step count cannot be negative.")
        for _ in range(steps):
            self.step()

    def result(self) -> SimulationResult:
        """Return an immutable snapshot of the simulation's current state."""
        metadata = SimulationMetadata(
            width=self.width,
            height=self.height,
            timestep=self.timestep,
            steps=self.steps,
            noise_scale=self.noise_scale,
            random_seed=self.random_seed,
            boundary_policy=self.boundary_policy,
        )
        return SimulationResult(trajectories=self.trajectories, metadata=metadata)

    @staticmethod
    def _reflect_coordinate(coordinate: float, limit: float) -> float:
        reflected_coordinate = coordinate % (2 * limit)
        if reflected_coordinate > limit:
            return 2 * limit - reflected_coordinate
        return reflected_coordinate

    @staticmethod
    def _validate_configuration(
        *,
        width: float,
        height: float,
        particle_count: int,
        timestep: float,
        noise_scale: float,
        initial_positions: Sequence[tuple[float, float]] | None,
        boundary_policy: str,
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Simulation dimensions must be positive.")
        if particle_count < 0:
            raise ValueError("Particle count cannot be negative.")
        if timestep <= 0:
            raise ValueError("Timestep must be positive.")
        if noise_scale < 0:
            raise ValueError("Noise scale cannot be negative.")
        if boundary_policy not in {"none", "reflecting"}:
            raise ValueError("Boundary policy must be 'none' or 'reflecting'.")
        if initial_positions is not None and len(initial_positions) != particle_count:
            raise ValueError("Initial position count must equal particle count.")
        if initial_positions is not None:
            for x, y in initial_positions:
                if not 0 <= x <= width or not 0 <= y <= height:
                    raise ValueError("Initial positions must be inside the simulation domain.")