# Computational Cell Biology Through Code
## A Model-Agnostic, Agent-Assisted Learning and Simulation Curriculum

**Version:** 0.1  
**Status:** Foundation document + Module 1  
**Primary language:** Python  
**Intended coding agents:** Gemini, GitHub Copilot, Claude Code, Codex, or similar agentic coding systems

---

# 1. Project Vision

The goal of this project is to learn computational cell biology by **building a progressively more sophisticated cell simulation from scratch**.

The project is deliberately interdisciplinary:

- **Computer programming:** architecture, testing, visualization, simulation engines
- **Probability and statistics:** stochastic processes, distributions, noise, sampling
- **Physics:** diffusion, Brownian motion, thermodynamics, transport
- **Chemistry:** molecular interactions, reaction kinetics, equilibrium
- **Cell biology:** membranes, metabolism, gene expression, signaling
- **Systems biology:** feedback, regulation, networks, emergent behavior
- **Scientific reasoning:** distinguishing observations, assumptions, models, and interpretations

The simulator should grow underneath the learner's feet. Each module should add a real capability while preserving and testing everything that came before it.

This is **not** intended to be a scientifically complete simulation of a human cell. A real cell is vastly too complicated for that. The purpose is to build increasingly useful models that illuminate particular biological mechanisms.

A central rule of the project is:

> **Never confuse a model with the biological system it represents.**

Every module must explicitly distinguish:

1. What is known experimentally.
2. What is being modeled.
3. What is being simplified.
4. What is unknown or disputed.
5. What the simulation actually demonstrates.

---

# 2. Learning Philosophy

The project should be treated as a computational laboratory rather than a conventional programming course.

For every major concept:

1. Learn the biological phenomenon.
2. Express it mathematically or algorithmically.
3. Implement the simplest useful model.
4. Run experiments.
5. Compare simulation behavior with theoretical expectations.
6. Identify the model's assumptions and limitations.
7. Extend the model.
8. Record what was learned.

The coding agent is a **technical collaborator**, not an authority.

The human learner remains responsible for understanding what the program means.

---

# 3. Long-Term Curriculum Roadmap

The exact order can evolve, but the intended progression is:

## Module 1 — Brownian Motion

Build the basic stochastic simulation engine.

Topics:

- Random walks
- Brownian motion
- Position and velocity
- Time steps
- Boundary conditions
- Random-number generation
- Reproducible experiments
- Visualization
- Basic statistics

Core question:

> How can random molecular motion produce predictable statistical behavior?

---

## Module 2 — Diffusion

Extend Brownian motion into molecular diffusion.

Topics:

- Concentration gradients
- Mean squared displacement
- Fick's laws
- Diffusion coefficients
- Spatial concentration fields
- One-dimensional and two-dimensional diffusion

Core question:

> How does random molecular motion produce directional movement at the population level?

---

## Module 3 — Molecular Encounters and Binding

Introduce interacting particles.

Topics:

- Collision detection
- Molecular radii
- Binding probability
- Dissociation
- Association rates
- Local concentration
- Search problems

Core question:

> How do molecules find one another in the noisy environment of a cell?

---

## Module 4 — Stochastic Chemical Reactions

Move from particle-level simulation toward reaction-system modeling.

Topics:

- Reaction rates
- Molecular counts
- Poisson processes
- Exponential waiting times
- Reaction propensities
- Gillespie's stochastic simulation algorithm

Example:

A + B -> C

Core question:

> What changes when chemical reactions involve only tens, hundreds, or thousands of molecules rather than macroscopic quantities?

---

## Module 5 — Enzymes

Model catalytic reactions.

Topics:

- Enzyme/substrate binding
- Catalysis
- Michaelis-Menten kinetics
- Stochastic enzyme behavior
- Saturation
- Competing reactions

Core question:

> How can molecular-level randomness produce stable reaction rates?

---

## Module 6 — Membranes and Compartments

Introduce a cell boundary.

Topics:

- Lipid bilayers
- Compartments
- Selective permeability
- Transport
- Membrane-bound molecules
- Concentration differences

Core question:

> What changes when chemistry occurs inside a bounded compartment?

---

## Module 7 — Gene Expression Noise

Build a simplified gene-expression system.

Topics:

- DNA
- Transcription
- mRNA
- Translation
- Protein production
- Degradation
- Promoter states
- Bursting
- Intrinsic noise

Core question:

> Why can genetically identical cells behave differently?

---

## Module 8 — Gene Regulatory Networks

Introduce feedback and control.

Topics:

- Activation
- Repression
- Positive feedback
- Negative feedback
- Toggle switches
- Oscillators
- Bistability

Core question:

> How can simple molecular interactions generate robust cellular states?

---

## Module 9 — Cellular Energy and Metabolism

Introduce energy-dependent processes.

Topics:

- ATP
- Energy budgets
- Reaction coupling
- Proton gradients
- Simplified metabolic pathways

Core question:

> How does a cell maintain organized processes despite constant molecular noise?

---

## Module 10 — Signaling Networks

Model communication inside and between cells.

Topics:

- Receptors
- Second messengers
- Kinase cascades
- Signal amplification
- Noise filtering
- Thresholds

---

## Module 11 — A Minimal Synthetic Cell

Combine previous components into a small artificial cellular environment.

Potential components:

- Membrane
- Diffusing molecules
- Reactions
- Energy currency
- Information molecule
- Gene-expression system
- Regulatory network

The goal is not to claim that this is how the first cell formed.

The goal is to investigate what kinds of behavior can emerge from explicitly specified rules.

---

## Module 12 — Experimental and Origin-of-Life Models

Only after the simulator is mature should the project begin exploring origin-of-life questions.

Potential topics:

- Prebiotic chemistry
- Autocatalytic networks
- Compartment formation
- Template replication
- Chemical selection
- Protocells
- Information vs. chemistry
- Error thresholds
- Competing hypotheses

Every model in this section must clearly identify which assumptions are experimentally established and which are speculative.

---

# 4. Coding-Agent Constitution

Every coding agent working on this repository should follow these rules.

## Rule 1 — Preserve the existing system

Do not rewrite functioning components merely because a different implementation is preferred.

Before changing architecture, explain:

- Why the change is necessary.
- What existing behavior could break.
- How the change will be tested.

## Rule 2 — Small increments

Implement one coherent capability at a time.

Do not create an enormous code dump covering multiple lessons.

## Rule 3 — Tests before confidence

Every significant behavior must have automated tests.

A simulation that produces attractive graphics but cannot be tested is not considered complete.

## Rule 4 — Reproducibility

Random simulations must support deterministic seeds.

Every experiment should be reproducible when given the same:

- seed
- parameters
- simulation version

## Rule 5 — Separate model from visualization

The scientific simulation engine must not depend on the graphical interface.

The same simulation should be runnable:

- headless
- from tests
- from notebooks
- from a GUI

## Rule 6 — Make assumptions explicit

Whenever biology is simplified, document the simplification.

For example:

> Real molecules do not behave as perfectly hard disks. This simulation approximates them as circular particles because the purpose of this experiment is to study encounter statistics.

## Rule 7 — Do not manufacture biological facts

If a biological parameter is unknown, disputed, context-dependent, or unavailable, say so.

Do not invent precision.

## Rule 8 — Explain before extending

Before implementing a new biological mechanism, briefly explain:

- the biological phenomenon
- the mathematical abstraction
- the proposed software abstraction
- the limitations

## Rule 9 — Scientific claims require sources

When a module makes substantive biological claims, identify appropriate primary literature, textbooks, or authoritative sources.

## Rule 10 — The learner must be able to inspect everything

Prefer understandable code over clever code.

The purpose is learning, not merely obtaining a working application.

---

# 5. Suggested Repository Architecture

The exact architecture may evolve, but a reasonable starting point is:

```text
cell-simulator/
├── README.md
├── pyproject.toml
├── docs/
│   ├── curriculum.md
│   ├── research-notes/
│   └── design/
├── src/
│   └── cell_sim/
│       ├── __init__.py
│       ├── simulation.py
│       ├── particles.py
│       ├── random_processes.py
│       └── visualization.py
├── tests/
│   ├── test_simulation.py
│   ├── test_particles.py
│   └── test_random_processes.py
├── experiments/
│   └── module_01/
├── notebooks/
└── data/
```

Do not treat this structure as sacred. The coding agent may propose improvements, but changes should be justified.

---

# 6. Module Format

Every future module should contain:

1. Scientific objective
2. Biology background
3. Mathematical background
4. Programming objective
5. Architecture changes
6. Agent prompt
7. Implementation milestones
8. Acceptance tests
9. Experiments
10. Expected observations
11. Biological interpretation
12. Model limitations
13. Extension challenges
14. Research notebook questions
15. Exit criteria

---

# 7. MODULE 1 — Brownian Motion

## 7.1 Scientific Objective

Build an interactive computational model of Brownian-like particle motion and use it to investigate how random microscopic motion produces measurable statistical patterns.

The learner should finish this module understanding:

- What a stochastic process is.
- What a random walk is.
- Why individual molecular trajectories are unpredictable.
- Why populations of trajectories can exhibit predictable statistics.
- How random sampling works computationally.
- Why reproducibility matters in simulations.

---

# 8. Biology Background

Inside a cell, molecules are constantly moving.

At microscopic scales, molecules collide with surrounding molecules and exchange momentum. The resulting motion is often modeled statistically.

The first simulator does **not** attempt to reproduce molecular dynamics.

Instead, it uses a deliberately simplified model:

> A particle receives random changes in position at discrete time intervals.

This is a random-walk approximation.

The important conceptual distinction is:

**Individual trajectory:** unpredictable.

**Population statistics:** often highly predictable.

That distinction will become fundamental later when modeling chemical reactions and gene expression.

---

# 9. Mathematical Model

For a simple two-dimensional random walk:

```text
x(t + dt) = x(t) + Δx
y(t + dt) = y(t) + Δy
```

where the increments are drawn from a specified probability distribution.

A basic model can use:

```text
Δx ~ Normal(0, σ)
Δy ~ Normal(0, σ)
```

The exact physical relationship between `σ`, time step, temperature, viscosity, and diffusion coefficient will be introduced in Module 2.

For Module 1, the purpose is to understand stochastic motion rather than construct a fully physical diffusion model.

---

# 10. Software Objective

Create a reusable simulation engine capable of:

- Creating particles.
- Updating particle positions.
- Applying stochastic motion.
- Running for a specified number of steps.
- Recording trajectories.
- Reproducing runs from a specified random seed.
- Visualizing trajectories.
- Computing basic statistics.

---

# 11. Initial Data Model

The first version should probably contain something conceptually similar to:

```text
Particle
    id
    x
    y

Simulation
    width
    height
    particles
    random_seed
    timestep

SimulationResult
    trajectories
    metadata
```

The coding agent should decide whether these should be classes, dataclasses, or another structure and explain the choice.

Do not prematurely create a giant object hierarchy.

---

# 12. Agent Prompt — Module 1

Copy the following prompt into an agentic coding system.

---

## BEGIN AGENT PROMPT

You are acting as a senior Python software engineer and computational biologist.

We are beginning a long-term educational project called **Computational Cell Biology Through Code**.

The purpose of this project is to progressively construct a stochastic simulation environment that teaches the learner about physical and biological processes inside cells.

### Current milestone

Implement **Module 1: Brownian Motion / Random Walks**.

### Important constraints

1. Use Python.
2. Use clean, understandable code.
3. Use type hints.
4. Use automated tests.
5. Make stochastic behavior reproducible through explicit random seeds.
6. Keep simulation logic separate from visualization.
7. Do not introduce unnecessary dependencies.
8. Do not build future modules yet.
9. Document biological and mathematical simplifications.
10. Do not claim that this first model is a physically complete simulation of molecular Brownian motion.

### Before writing code

First provide:

1. Proposed repository structure.
2. Explanation of the simulation model.
3. Explanation of the mathematical abstraction.
4. Proposed classes/functions.
5. Dependency choices.
6. Testing strategy.
7. Known simplifications.

Wait for approval before implementing if the environment allows interactive approval. If it does not, proceed with the smallest reasonable implementation.

### Required functionality

Implement a simulation in which particles undergo two-dimensional stochastic motion.

The simulation must allow:

- configurable number of particles
- configurable simulation dimensions
- configurable number of time steps
- configurable step-size/noise parameter
- configurable random seed
- recording of particle trajectories

Implement at least one visualization method.

### Reproducibility requirement

Two simulations with identical:

- parameters
- initial conditions
- random seed

must produce identical trajectories.

Different seeds should normally produce different trajectories.

### Tests

Create automated tests for:

1. Simulation construction.
2. Correct particle count.
3. Correct trajectory length.
4. Seed reproducibility.
5. Different seeds producing different stochastic outcomes.
6. Particles remaining inside the configured simulation domain if boundary handling is enabled.
7. Basic statistical sanity checks.

Do not write fragile tests that expect a particular random trajectory.

### Experiments

Create a small experiment script or notebook that can investigate:

1. One particle.
2. Ten particles.
3. One hundred particles.
4. Different noise levels.
5. Different simulation durations.
6. Different random seeds.

Produce trajectory plots.

Also calculate at least:

- mean displacement
- displacement variance
- mean squared displacement

### Scientific honesty

Clearly label which aspects are:

- biological observations
- mathematical assumptions
- software implementation choices

Do not silently equate the simulation with actual molecular dynamics.

### Educational requirement

After implementation, provide a concise explanation aimed at a programmer who is learning biology.

Explain:

- what stochasticity means
- why individual trajectories are random
- why statistics can still be predictable
- what the simulation does and does not demonstrate

### Completion report

When finished, report:

1. Files created/changed.
2. Tests implemented.
3. Test results.
4. How to run the simulation.
5. How to reproduce an experiment.
6. Scientific assumptions.
7. Known limitations.
8. Suggested next experiment.

Do not implement Module 2.

## END AGENT PROMPT

---

# 13. Module 1 Acceptance Criteria

Module 1 is complete only when all of the following are true:

- [ ] The simulation runs from a clean environment.
- [ ] Particle trajectories are generated.
- [ ] A random seed reproduces a run.
- [ ] Tests pass.
- [ ] Visualization works independently of the simulation engine.
- [ ] Basic displacement statistics can be calculated.
- [ ] The learner can explain what stochasticity means.
- [ ] The learner can explain why random individual trajectories can produce stable population statistics.
- [ ] The model's simplifications are documented.
- [ ] The coding agent has not silently implemented later modules.

---

# 14. Module 1 Experiments

Do not merely run the simulator. Treat each experiment as a scientific investigation.

## Experiment A — One Particle

Run a single particle for a long trajectory.

Questions:

- Does the trajectory look predictable?
- Could you predict its next position?
- Does the trajectory resemble a straight line?
- What happens as the number of steps increases?

---

## Experiment B — Many Particles

Run 100 particles from the same starting position.

Questions:

- Are individual trajectories different?
- Is there a recognizable overall pattern?
- Does the cloud of particles become more spread out over time?

---

## Experiment C — Change the Noise

Run otherwise identical simulations with:

- low noise
- medium noise
- high noise

Questions:

- How does spread change?
- How does mean squared displacement change?
- Does the individual trajectory become more or less predictable?

---

## Experiment D — Reproducibility

Run the same simulation twice with the same seed.

Verify:

```text
run A == run B
```

Then change only the seed.

Verify that:

```text
run A != run C
```

This demonstrates an important computational distinction:

> Random does not have to mean irreproducible.

---

# 15. Research Notebook

For every experiment, record:

```text
Experiment:
Date:
Code version:
Random seed:
Parameters:

Hypothesis:

What I expected:

What happened:

What surprised me:

What the simulation actually demonstrates:

What it does NOT demonstrate:

Biological relevance:

Model assumptions:

Open questions:
```

---

# 16. Important Conceptual Question

One of the deeper questions motivating this entire curriculum is:

> How can systems containing stochastic microscopic events nevertheless produce reliable macroscopic behavior?

This question will recur throughout the curriculum.

For example:

- molecular diffusion
- enzyme reactions
- gene expression
- signaling
- metabolism
- cellular decision-making

The goal is not to prejudge the philosophical interpretation of these phenomena.

The simulator should instead make the mechanisms explicit enough that the learner can examine what follows from the stated assumptions.

---

# 17. Scientific Discussion Framework

As the curriculum progresses, distinguish four different questions.

### Question 1 — What happens?

An empirical question.

Example:

> Do molecules diffuse through a particular medium at a measurable rate?

### Question 2 — What mechanism explains it?

A mechanistic question.

Example:

> Can random molecular motion account for the observed diffusion behavior?

### Question 3 — What model reproduces it?

A computational question.

Example:

> Can a stochastic random-walk model reproduce the observed distribution?

### Question 4 — What does it ultimately mean?

A philosophical or foundational question.

Example:

> Does apparent organization require intelligence, or can specified physical processes generate it?

The project should not silently answer Question 4 while pretending it has answered Questions 1–3.

---

# 18. Future Expansion

Once Module 1 is complete, the next major step is **diffusion**.

The key conceptual transition will be:

```text
Random individual motion
        ↓
Many particles
        ↓
Spatial distribution
        ↓
Concentration gradient
        ↓
Predictable diffusion behavior
```

Then:

```text
Diffusion
    ↓
Molecular encounters
    ↓
Chemical reactions
    ↓
Reaction networks
    ↓
Gene expression
    ↓
Regulation
    ↓
Cellular systems
```

Each step should be earned by experiment rather than simply added as a software feature.

---

# 19. Final Principle

The central philosophy of this project is:

> **Build the mechanism. Run the experiment. Examine the result. Then ask what the result actually establishes.**

The purpose is not merely to create a sophisticated piece of software.

It is to develop the ability to move fluently between:

**biology → mathematics → code → experiment → observation → interpretation.**

That is the skill this curriculum is designed to develop.
