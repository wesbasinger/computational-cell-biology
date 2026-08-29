"""Statistical analysis functions for completed simulation runs."""

from math import hypot
from statistics import fmean, pvariance

from cell_sim.models import SimulationResult


def final_displacements(result: SimulationResult) -> tuple[float, ...]:
    """Return each particle's Euclidean displacement from start to finish."""
    if not result.trajectories:
        raise ValueError("Cannot calculate displacement without trajectories.")

    displacements = []
    for trajectory in result.trajectories.values():
        if not trajectory:
            raise ValueError("Each trajectory must contain an initial position.")
        start_x, start_y = trajectory[0]
        final_x, final_y = trajectory[-1]
        displacements.append(hypot(final_x - start_x, final_y - start_y))
    return tuple(displacements)


def mean_displacement(result: SimulationResult) -> float:
    """Return the mean final displacement across all particles."""
    return fmean(final_displacements(result))


def displacement_variance(result: SimulationResult) -> float:
    """Return the population variance of final particle displacements."""
    return pvariance(final_displacements(result))


def mean_squared_displacement(result: SimulationResult) -> float:
    """Return the mean of squared final particle displacements."""
    return fmean(displacement**2 for displacement in final_displacements(result))