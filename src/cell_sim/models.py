"""Data structures shared by simulation, analysis, and visualization code."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Sequence


@dataclass
class Particle:
    """A particle with a stable identifier and two-dimensional position."""

    id: int
    x: float
    y: float


@dataclass(frozen=True)
class SimulationMetadata:
    """Parameters needed to describe and reproduce a simulation run."""

    width: float
    height: float
    timestep: float
    steps: int
    noise_scale: float
    random_seed: int | None
    boundary_policy: str
    diffusion_coefficient: float | None = None


@dataclass(frozen=True)
class SimulationResult:
    """Recorded particle trajectories and the parameters that produced them."""

    trajectories: Mapping[int, tuple[tuple[float, float], ...]]
    metadata: SimulationMetadata

    def __post_init__(self) -> None:
        trajectories = {
            particle_id: tuple(positions)
            for particle_id, positions in self.trajectories.items()
        }
        object.__setattr__(self, "trajectories", MappingProxyType(trajectories))