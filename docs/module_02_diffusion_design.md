# Module 2: Diffusion Design

## Objective

Extend the Module 1 random walk into a two-dimensional, idealized diffusion model. The aim is to connect random individual motion to measurable population spreading without claiming to simulate the full physical behavior of molecules in a cell.

## Biological Background

Molecules in a fluid undergo continual thermal motion and collisions. When many molecules begin concentrated in one region, their aggregate distribution tends to spread over time. Diffusion is the population-level description of that spreading.

This module models freely diffusing, noninteracting particles in a uniform two-dimensional environment. It does not model molecular dynamics, solvent molecules, molecular shape, crowding, active transport, chemical reactions, or a particular cellular medium.

## Mathematical Abstraction

For free, isotropic diffusion in two dimensions, the expected mean squared displacement is

$$
\mathbb{E}[r^2(t)] = 4Dt,
$$

where $D$ is the diffusion coefficient, $t$ is elapsed time, and $r^2 = (x-x_0)^2 + (y-y_0)^2$.

The discrete-time model will sample independent coordinate displacements:

$$
\Delta x, \Delta y \sim \mathcal{N}(0, \sqrt{2D\Delta t}).
$$

With this choice, one step has expected squared displacement $4D\Delta t$. This relationship applies to the idealized, unbounded model. Reflecting boundaries eventually constrain the particle distribution and invalidate a simple indefinitely linear MSD expectation.

## Software Design

Keep the existing `Simulation` class and Module 1 `noise_scale` behavior unchanged. Add a clearly named diffusion constructor or factory that accepts `diffusion_coefficient` and derives the Gaussian coordinate noise scale from $D$ and `timestep`.

The initial implementation should add:

- `Simulation.for_diffusion(...)`, with the same domain, particle, seed, initial-position, and boundary configuration as `Simulation`.
- Validation that `diffusion_coefficient >= 0`.
- Diffusion metadata that records `diffusion_coefficient` alongside the derived `noise_scale`.
- `mean_squared_displacement_by_step(result)`, returning MSD at every recorded timestep.
- A diffusion experiment that plots MSD against elapsed time and compares it with the theoretical line $4Dt` for an unbounded run.

The existing trajectory visualization remains independent from simulation execution. New MSD plotting should similarly consume only a `SimulationResult`.

## Testing Strategy

Test deterministic properties, not one particular random trajectory:

1. The derived coordinate noise scale equals $\sqrt{2D\Delta t}$.
2. Zero diffusion coefficient produces stationary particles.
3. Identical parameters, initial positions, and seed reproduce trajectories.
4. MSD-by-step has one value for every recorded position, including step zero.
5. An unbounded, sufficiently large ensemble has MSD close to $4Dt$ within a documented statistical tolerance.
6. Reflecting boundaries retain particles in the domain but are not tested against unbounded $4Dt$ behavior at long times.

## Experiments

Run these comparisons with explicit commands, seeds, and outputs recorded:

1. **MSD growth:** Use many particles, `--boundary-policy none`, and plot MSD versus elapsed time. Compare the observed trend with $4Dt$.
2. **Diffusion coefficient:** Repeat with several $D$ values while holding timestep and run duration fixed. Higher $D$ should produce faster early-time MSD growth.
3. **Timestep refinement:** Hold total elapsed time and $D$ fixed while changing timestep and step count together. Compare aggregate MSD behavior, not individual trajectories.
4. **Bounded domain:** Repeat an otherwise matching run with reflecting boundaries. Observe how finite boundaries alter long-time spreading.

### Reproducible Commands

All commands below use seed `42` and write a distinct figure under `data/module_02/`.

```powershell
python experiments/module_02/run_diffusion_experiment.py --particles 10000 --steps 500 --width 1000 --height 1000 --timestep 0.1 --diffusion-coefficient 1.0 --boundary-policy none --seed 42 --output data/module_02/msd_growth.png
python experiments/module_02/run_diffusion_experiment.py --particles 10000 --steps 500 --width 1000 --height 1000 --timestep 0.1 --diffusion-coefficient 0.25 --boundary-policy none --seed 42 --output data/module_02/msd_d025.png
python experiments/module_02/run_diffusion_experiment.py --particles 10000 --steps 500 --width 1000 --height 1000 --timestep 0.1 --diffusion-coefficient 2.0 --boundary-policy none --seed 42 --output data/module_02/msd_d2.png
python experiments/module_02/run_diffusion_experiment.py --particles 10000 --steps 250 --width 1000 --height 1000 --timestep 0.2 --diffusion-coefficient 1.0 --boundary-policy none --seed 42 --output data/module_02/msd_timestep_02.png
python experiments/module_02/run_diffusion_experiment.py --particles 10000 --steps 500 --width 1000 --height 1000 --timestep 0.1 --diffusion-coefficient 1.0 --boundary-policy reflecting --seed 42 --output data/module_02/msd_reflecting.png
```

The reported relative error compares one finite random ensemble with the unbounded $4Dt$ expectation; it is not an error estimate for a physical cell. Compare the theory line only for `--boundary-policy none`. Reflecting boundaries keep particles in the domain, so their long-time MSD is expected to fall below the unbounded line.

## Acceptance Criteria

- [ ] A diffusion-configured simulation derives its motion scale from $D$ and $\Delta t$.
- [ ] Seeded diffusion runs are reproducible.
- [ ] MSD can be computed for every simulated timepoint.
- [ ] An unbounded ensemble exhibits approximately linear early-time MSD growth.
- [ ] Diffusion visualization works without simulation-engine imports.
- [ ] The experiment distinguishes the theoretical idealization from observed finite-sample results.
- [ ] Assumptions and limitations are documented.

## Sources

- Howard C. Berg, *Random Walks in Biology*, Princeton University Press, 1993.
- Samuel A. Safran, *Statistical Thermodynamics of Surfaces, Interfaces, and Membranes*, Westview Press, 2003, diffusion fundamentals.
- Philip Nelson, *Biological Physics: Energy, Information, Life*, W. H. Freeman, 2014, chapters on diffusion and random walks.

## Scope Boundary

This module does not implement concentration fields, Fick's second-law solvers, molecular encounters, binding, reactions, or cellular transport mechanisms. Those are future extensions after the particle-level diffusion behavior is tested and understood.