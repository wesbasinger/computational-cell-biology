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


def mean_squared_displacement_by_step(result: SimulationResult) -> tuple[float, ...]:
    """Return the ensemble MSD from each particle's initial position at every step."""
    if not result.trajectories:
        raise ValueError("Cannot calculate displacement without trajectories.")

    trajectories = tuple(result.trajectories.values())
    step_count = len(trajectories[0])
    if step_count == 0:
        raise ValueError("Each trajectory must contain an initial position.")
    if any(len(trajectory) != step_count for trajectory in trajectories):
        raise ValueError("All trajectories must contain the same number of positions.")

    return tuple(
        fmean(
            (x - trajectory[0][0]) ** 2 + (y - trajectory[0][1]) ** 2
            for trajectory in trajectories
            for x, y in (trajectory[step],)
        )
        for step in range(step_count)
    )