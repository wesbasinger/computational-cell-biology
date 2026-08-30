# Computational Cell Biology Through Code

An AI-driven, human-guided exploration of computational cell biology. This repository builds small, testable Python simulations that connect biological ideas to stochastic models, mathematical expectations, and reproducible experiments.

The project uses an AI coding agent throughout the development process: turning learning goals into software designs, implementing focused increments, generating tests, running experiments, and explaining results. The learner directs the questions, evaluates the evidence, and remains responsible for distinguishing a model from the biological system it represents.

## Current Modules

### Module 1: Brownian Motion

A configurable two-dimensional random-walk simulation with seeded randomness, optional reflecting boundaries, trajectory plots, and final-displacement statistics.

### Module 2: Diffusion

An idealized, noninteracting two-dimensional diffusion model. The diffusion factory derives Gaussian coordinate motion from the diffusion coefficient $D$ and timestep $\Delta t$:

$$
\Delta x, \Delta y \sim \mathcal{N}(0, \sqrt{2D\Delta t})
$$

For an unbounded two-dimensional ensemble, the expected mean squared displacement (MSD) is:

$$
\mathbb{E}[r^2(t)] = 4Dt
$$

Module 2 measures the observed MSD across simulated particles and compares it with that idealized prediction. Reflecting boundaries are included to demonstrate how cellular-scale confinement changes long-term spreading.

## Run the Diffusion Experiment

From the repository root, activate the virtual environment and run:

```powershell
python experiments/module_02/run_diffusion_experiment.py --particles 10000 --steps 500 --width 1000 --height 1000 --timestep 0.1 --diffusion-coefficient 1.0 --boundary-policy none --seed 42 --output data/module_02/msd_growth.png
```

The command writes an MSD plot to `data/module_02/` and reports the observed final MSD alongside the unbounded $4Dt$ expectation. Additional reproducible comparisons are documented in [docs/module_02_diffusion_design.md](docs/module_02_diffusion_design.md).

## Setup and Verification

The project requires Python 3.10 or newer. Install the package and test dependencies in editable mode:

```powershell
python -m pip install -e .
python -m pytest
```

## Model Boundaries

These simulations are learning models, not complete virtual cells. The current diffusion model does not include molecular shape, solvent dynamics, crowding, chemical reactions, binding, active transport, or a specific cellular environment. Results should be interpreted as consequences of the model's explicit assumptions, not direct claims about every biological system.

## Roadmap

The curriculum advances from stochastic motion and diffusion to molecular encounters, reactions, enzymes, membranes, gene expression, regulatory networks, metabolism, and eventually minimal synthetic-cell models. See [computational_cell_biology_curriculum.md](computational_cell_biology_curriculum.md) for the full roadmap and project principles.
