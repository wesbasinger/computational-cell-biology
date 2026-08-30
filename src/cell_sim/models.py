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


@dataclass
class Molecule:
    """A mutable molecule with a species label and two-dimensional position."""

    id: int
    species: str
    x: float
    y: float


@dataclass
class BoundComplex:
    """A mutable one-to-one complex that moves as a single particle."""

    a_id: int
    b_id: int
    x: float
    y: float


@dataclass(frozen=True)
class BindingStateCounts:
    """Counts of free molecules and bound complexes at one recorded timepoint."""

    free_a: int
    free_b: int
    bound_complexes: int


@dataclass(frozen=True)
class BindingMetadata:
    """Parameters needed to reproduce an encounter-and-binding simulation run."""

    width: float
    height: float
    timestep: float
    steps: int
    a_diffusion_coefficient: float
    b_diffusion_coefficient: float
    complex_diffusion_coefficient: float
    encounter_radius: float
    binding_probability: float
    dissociation_probability: float
    random_seed: int | None
    boundary_policy: str
    a_count: int
    b_count: int


@dataclass(frozen=True)
class BindingResult:
    """Recorded molecular trajectories, state counts, and binding configuration."""

    trajectories: Mapping[int, tuple[tuple[float, float], ...]]
    state_counts: tuple[BindingStateCounts, ...]
    metadata: BindingMetadata

    def __post_init__(self) -> None:
        trajectories = {
            molecule_id: tuple(positions)
            for molecule_id, positions in self.trajectories.items()
        }
        object.__setattr__(self, "trajectories", MappingProxyType(trajectories))
        object.__setattr__(self, "state_counts", tuple(self.state_counts))