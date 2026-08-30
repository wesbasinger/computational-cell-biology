# Module 3: Molecular Encounters and Binding Design

## Objective

Extend the diffusion model with a minimal, explicit model of molecular encounters and reversible binding. The module connects random motion to encounter frequency and shows how a bound-complex population can emerge from specified association and dissociation rules.

## Biological Background

Molecules that diffuse through the same cellular region may encounter one another. Some encounters lead to a temporary bound complex, while others do not. Whether binding occurs depends on molecular structure, orientation, local environment, and chemistry; a particle model cannot infer those mechanisms from distance alone.

This module represents two molecule species, $A$ and $B$, as points with assigned interaction radii. An eligible encounter can produce a single $AB$ complex with a configured probability. Complexes can dissociate with a configured probability. These rules are a learning model of reversible binding, not a molecular-dynamics or chemical-kinetics simulation.

## Mathematical Abstraction

Two unbound particles are considered to encounter when their center-to-center distance satisfies

$$
\sqrt{(x_A-x_B)^2 + (y_A-y_B)^2} \leq r_{\mathrm{encounter}}.
$$

At each eligible encounter, binding is sampled as a Bernoulli event:

$$
P(A+B\rightarrow AB \mid \mathrm{encounter}) = p_{\mathrm{bind}}.
$$

For each existing complex at a timestep, dissociation is also sampled as a Bernoulli event:

$$
P(AB\rightarrow A+B \mid \Delta t) = p_{\mathrm{dissociate}}.
$$

The probabilities are discrete-time model parameters. They are not association or dissociation rate constants and must not be interpreted as calibrated measurements without a separate rate-conversion and validation step.

## First Implementation Scope

Build a separate encounter-and-binding simulation rather than modifying the existing `Simulation` class. Preserve Modules 1 and 2 as diffusion-only baselines.

The initial implementation should add:

- `BindingSimulation`, configured with domain dimensions, timestep, species counts, diffusion coefficients, encounter radius, binding probability, dissociation probability, seed, initial positions, and boundary policy.
- Explicit particle states for unbound $A$, unbound $B$, and bound $AB$ complexes.
- Independent Gaussian diffusion for unbound particles, using each species' configured diffusion coefficient.
- Deterministic encounter-pair selection: a particle can participate in at most one binding event per timestep.
- Complex motion using a separately configured complex diffusion coefficient.
- Dissociation before new encounter processing. On dissociation, both particles resume at the complex position.
- Immutable results that record positions, state counts at every timestep, and all reproducibility parameters.
- Analysis functions for bound fraction and per-step molecular state counts.
- A result-only plot of $A$, $B$, and $AB$ counts against elapsed time.
- A reproducible experiment comparing no binding, high binding, and reversible binding conditions.

## Update Order

For each timestep:

1. Diffuse every unbound molecule and existing complex.
2. Apply the selected boundary policy to each moved position.
3. Sample dissociation for every complex.
4. Find eligible unbound $A$-$B$ encounter pairs.
5. In ascending particle-ID order, sample binding for each eligible pair whose particles have not already been selected at that timestep.
6. Record positions and state counts.

The explicit order is part of the model. It prevents a molecule from binding twice in one timestep and makes seeded runs reproducible.

## Testing Strategy

Test deterministic model properties rather than a particular random history:

1. Invalid radii and probabilities outside $[0, 1]$ are rejected.
2. Particles farther apart than the encounter radius cannot bind.
3. Particles within the encounter radius bind when `binding_probability=1`.
4. A complex dissociates when `dissociation_probability=1`.
5. Zero diffusion preserves positions except for state transitions.
6. An individual molecule participates in at most one binding event per timestep.
7. Matching parameters, initial state, and seed reproduce trajectories and state counts.
8. State counts are conserved: $A_{\mathrm{total}} = A_{\mathrm{free}} + AB$ and $B_{\mathrm{total}} = B_{\mathrm{free}} + AB$.
9. Reflecting boundaries retain all positions in the configured domain.

## Experiments

Run each comparison with an explicit seed and saved output:

1. **No binding:** Set `binding_probability=0` to establish the diffusion-only control.
2. **Irreversible binding:** Set a nonzero binding probability and `dissociation_probability=0`; observe accumulation of $AB$ complexes.
3. **Reversible binding:** Use nonzero binding and dissociation probabilities; observe fluctuating free and bound populations.
4. **Encounter radius:** Hold all other values fixed while varying encounter radius; larger radii should generally create more eligible encounters in this model.
5. **Diffusion coefficient:** Hold interaction rules fixed while varying diffusion; compare aggregate binding outcomes across repeated seeds rather than relying on a single trajectory.

### Reproducible Commands

All commands below use seed `42` and save their state-count plot under `data/module_03/`.

```powershell
python experiments/module_03/run_binding_experiment.py --binding-probability 0 --dissociation-probability 0 --seed 42 --output data/module_03/no_binding.png
python experiments/module_03/run_binding_experiment.py --binding-probability 0.2 --dissociation-probability 0 --seed 42 --output data/module_03/irreversible_binding.png
python experiments/module_03/run_binding_experiment.py --binding-probability 0.2 --dissociation-probability 0.02 --seed 42 --output data/module_03/reversible_binding.png
python experiments/module_03/run_binding_experiment.py --encounter-radius 0.25 --seed 42 --output data/module_03/radius_025.png
python experiments/module_03/run_binding_experiment.py --encounter-radius 1.0 --seed 42 --output data/module_03/radius_10.png
python experiments/module_03/run_binding_experiment.py --a-diffusion-coefficient 2.0 --b-diffusion-coefficient 2.0 --complex-diffusion-coefficient 1.0 --seed 42 --output data/module_03/higher_diffusion.png
```

The plots show outcomes from one seeded stochastic realization. Treat changes in binding behavior as model observations rather than proof of a general trend. Repeat conditions using several `--seed` values before drawing a conclusion about encounter radius or diffusivity.

## Assumptions and Limitations

- Molecules are point particles and do not exclude volume.
- A distance threshold replaces molecular orientation, force fields, and chemical specificity.
- Binding and dissociation use timestep-dependent probabilities, not calibrated reaction rates.
- Complex formation does not conserve momentum, energy, or molecular geometry.
- A uniform domain omits cellular crowding, compartments, membrane surfaces, and active transport.
- Pairwise binding is restricted to one $A$ and one $B$ molecule; multivalent complexes and reactions are outside this module.

## Scope Boundary

This module does not implement reaction-rate calibration, collision mechanics, steric exclusion, concentration-field solvers, many-body interactions, enzyme catalysis, or reaction networks. Those belong to later modules after the encounter and reversible-binding rules are tested and interpreted.