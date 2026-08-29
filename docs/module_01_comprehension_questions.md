# Module 1 Comprehension Questions

Use a recorded experiment and its trajectory plot when answering these questions. State the seed and parameters you used whenever a question asks about a specific run.

## Reading One Trajectory

1. Follow one particle from its starting point to its final point. Does its path resemble a straight line? What visible features support your answer?
**No, it is a very jagged line.  I ran one particle for 500 steps with 0.25 noise factor.**
> **Feedback:** Correct. The jagged path is the visible consequence of many independent random increments. Record the seed as well as the number of steps and noise scale for a particular run.

2. At any point along that trajectory, could you have reliably predicted its next direction from the plot alone? Why or why not?
**No, althought I need more explanation on what the Gauss factor is in the randomness.**
> **Feedback:** `gauss(0, noise_scale)` samples a displacement from a normal (Gaussian) distribution with mean $0$ and standard deviation `noise_scale`. Mean $0$ means no preferred $x$ or $y$ direction across many steps, not that an individual step is zero. Each step draws fresh independent values for $x$ and $y$, so the plot cannot predict the next direction.

3. Does ending close to the starting position mean that the particle moved very little during the experiment? Explain using the plotted path.
**No, it moves according the number of steps**
> **Feedback:** Good direction. Ending near the start means **net displacement** is small, but the particle may still have traveled a long total path while repeatedly changing direction. More steps create more opportunities to move; they do not guarantee a large final displacement.

4. What does the trajectory plot show directly? What information about the simulation does it not show directly?
**It shows jagged paths**
> **Feedback:** It directly shows the recorded $x,y$ positions and their order. It does not directly show the random draws, their distribution, molecular collisions, a physical time calibration, or biological accuracy.

5. In this model, what does one plotted segment represent mathematically?
**One segment represents a vector**
> **Feedback:** Correct. More precisely, it is the displacement vector between consecutive recorded positions: $(\Delta x, \Delta y)$.

## Comparing Many Particles

6. Run one particle and then 100 particles with the same seed, noise scale, number of steps, and domain. What changes in the visualization?
**There are many more colors**
> **Feedback:** Correct. The larger run also makes the population's spread easier to see because it provides many samples of the same stochastic process.

7. Which behavior appears more predictable: an individual trajectory or the overall distribution of many particle positions? Describe the evidence in the plot.
**The overall distribution seems much more predictable**
> **Feedback:** Correct. Individual paths remain unpredictable, but many independent particles reveal a more stable aggregate spatial pattern.

8. Do particles that start from the same position follow identical paths? Which model rule explains the result?
**No, I think it's the randomness**
> **Feedback:** Correct. Each particle receives separate random $x$ and $y$ draws on every step, so shared starting positions do not produce shared trajectories.

9. Is a visibly spread-out group of particles evidence that every particle has moved the same distance? How could you check?
**I'm not sure.**
> **Feedback:** No. A spread-out cloud means final positions differ; it does not mean final distances are equal. Compare individual final displacements or the printed displacement variance. A nonzero variance means the distances are not all the same.

10. Why can a collection of unpredictable paths still form a recognizable cloud of positions?
**I'm not sure**
> **Feedback:** Repeated independent random steps produce a distribution of outcomes. One path is noisy, but many particles sample that distribution, making the overall cloud more regular and interpretable.

## Noise Scale

11. Compare runs with low, medium, and high `--noise-scale`, keeping all other parameters fixed. How does the typical distance from the start change?
**Distance from the start goes up with noise.**
> **Feedback:** Correct. In an unbounded run, larger `noise_scale` produces larger typical steps and therefore generally larger final displacements.

12. How does increasing noise scale affect the visual jaggedness of individual paths?
**I don't think there's any effect**
> **Feedback:** There is an effect, though it can be subtle: higher noise makes step vectors longer on average, so paths cover more space and have larger visible excursions. Their angular unpredictability remains random at every noise level.

13. Which printed statistic changes most clearly as you increase noise scale: mean displacement, displacement variance, or mean squared displacement? Report the values you observe.
**Mean displacement**
> **Feedback:** That may be true for one small sample. For this model, mean squared displacement is usually the most informative: in unbounded independent Gaussian walks, its expected value grows with the square of noise scale. Reflecting boundaries limit that growth in a finite domain.

14. Why does the model use a distribution of step sizes instead of a single fixed step length?
**I'm not sure**
> **Feedback:** This is a modeling choice, not a requirement for every random walk. A normal distribution makes small displacements common and large ones rare, approximating varying net effects of many unmodeled collisions. A fixed-length, random-direction walk would be another valid model.

15. Does a larger noise scale make a trajectory more biologically realistic by itself? What additional physical information would be required before making that claim?
**I'm not sure**
> **Feedback:** No. A physical claim would need a relation to elapsed time, temperature, fluid viscosity, molecular size or shape, and a measured or justified diffusion coefficient.

## Duration And Statistics

16. Compare a short and long run with every other parameter fixed. How does trajectory length in the plot change?
**I think trajectory length would increase**
> **Feedback:** Correct. A longer run adds more plotted segments and generally increases total path length, but it does not necessarily move the final point farther from the start.

17. Does a longer run guarantee that every particle ends farther from its starting point? Explain why a random walk can return toward its start.
**No, I think a particle always has a chance to reverse course**
> **Feedback:** Correct. Later random steps can partially or fully cancel earlier ones, allowing a particle to return near its start after extensive movement.

18. What is the difference between mean displacement and mean squared displacement in this experiment?
**I'm not sure**
> **Feedback:** Mean displacement averages the final distances $d$ from start to finish. Mean squared displacement averages $d^2$. Squaring gives greater weight to particles ending farther away and connects to random-walk and diffusion theory.

19. Why might mean squared displacement be useful when a population's average signed movement in any particular direction is near zero?
**I'm not sure**
> **Feedback:** This implementation uses distance rather than signed displacement. More generally, signed $x$ or $y$ movement can cancel in a symmetric population even while particles spread. Squared displacement stays positive and captures that spreading.

20. If two runs have the same noise scale but different seeds, should their summary statistics be exactly equal? Why or why not?
**No, but I'm not sure why**
> **Feedback:** Different seeds select different sequences of random draws, so finite runs generally have different paths and sample statistics. Larger runs should show similar broad behavior, not exactly equal values.

## Reproducibility

21. Run the exact same command twice. Are the printed statistics and trajectory plot identical? What role does `--seed` play?
**Yes, --seed probably generates the same sequence of random numbers**
> **Feedback:** Correct. The seed initializes the pseudorandom-number generator so it produces the same sequence for the same program and configuration.

22. Change only `--seed`. Which parts of the result should change, and which configuration values should remain the same?
**I'm not sure**
> **Feedback:** Paths, final positions, and summary statistics generally change. Particle count, steps, dimensions, timestep, noise scale, boundary policy, and initial positions remain the same; the seed value changes by design.

23. Is a seeded random simulation no longer stochastic? Distinguish reproducibility from predictability.
**It is still stochastic, it just makes the experiment repeatable**
> **Feedback:** Correct. The model still specifies probabilistic sampling; the seed merely lets the computer replay one particular sampled outcome.

24. What minimum information would another person need to reproduce one of your plots exactly?
**They would need the code, the parameters and the seed value**
> **Feedback:** Good answer. For stronger reproducibility, also include initial conditions, boundary policy, code version or commit, and Python/package versions.


## Scientific Interpretation

> **Note:** Questions 25-28, on reflecting versus unbounded boundaries, are absent from this version of the worksheet. A useful follow-up is a small-domain, high-noise comparison using `--boundary-policy reflecting` and `--boundary-policy none`.

29. Identify one biological observation that motivates this model, one mathematical assumption the model makes, and one software choice made by this implementation.
**I think we're trying to model how materials move inside cells, it assumes that movement is totally random, and I'm not sure about the software choice**
> **Feedback:** A sharper version: the motivating observation is continual thermally driven molecular motion and collisions; the mathematical assumption is independent, discrete Gaussian position increments; and one software choice is Python's seeded pseudorandom generator with every trajectory position stored. "Totally random" is too broad because the model omits interactions, drift, and other constraints.

30. What does this simulation demonstrate about random microscopic motion and population-level patterns?
**There is definitely some clustering and patterns that emerge**
> **Feedback:** Be cautious with "clustering." The model demonstrates that unpredictable individual motion can produce population-level spatial spread and distributions. Dense patches in one finite plot may be chance overlap, not a persistent biological cluster or organized structure.

31. What does it not demonstrate about real molecules in a cell?
**It doesn't demonstrate the actual physical properties of molecules**
> **Feedback:** Correct. It does not establish real molecular transport rates or physical properties, and it omits molecular size, interactions, energy landscapes, solvent behavior, and chemical reactions.

32. List at least three omitted mechanisms that would matter in a more physical model of molecular motion.
**Ion attraction or bonding, and I'm not sure on the others**
> **Feedback:** Good first example. Other omissions include molecular size and excluded-volume collisions, solvent viscosity and hydrodynamic effects, temperature-dependent diffusion, membrane interactions, active transport, and binding or unbinding reactions.

33. The timestep is recorded as metadata in Module 1. Does it yet change the scale of the random displacement? How could you verify your answer from the available experiment controls and code?
**Not sure**
> **Feedback:** No. In the current code, `timestep` is metadata only and does not scale displacement. Run otherwise identical commands with the same seed but different `--timestep` values: the trajectories and displacement statistics will match, apart from reported timestep metadata.

34. What result would make you question whether the implementation is behaving as intended? Propose one automated test or manual experiment that could investigate it.
**I would question the experiement if I got something that looked like a diagram from a science book**
> **Feedback:** The instinct is sensible, but make the check falsifiable. For example: `--noise-scale 0` should leave every position unchanged; matching seeds and parameters should reproduce identical trajectories; and reflecting boundaries should never record a position outside the domain. A textbook-like image alone does not prove an error.

## Experiment Reflection

For one experiment of your choice, record:

```text
Command:
Seed:
Hypothesis:
Observation from the plot:
Printed statistics:
What the model demonstrates:
What it does not demonstrate:
One follow-up experiment:
```

```
PS C:\Users\wbasinger\OneDrive - PCI\Personal\computational-cell-biology> python experiments\module_01\run_experiment.py --particles 10 --steps 50 --noise-scale 0.6 --seed 55
Random seed: 55
Particles: 10
Steps: 50
Mean displacement: 4.549541
Displacement variance: 4.518064
Mean squared displacement: 25.216388
Trajectory plot: data\module_01\trajectories.png
PS C:\Users\wbasinger\OneDrive - PCI\Personal\computational-cell-biology> 
```
> **Feedback:** This output records 10 particles, 50 steps, noise scale 0.6, seed 55, mean displacement 4.549541, variance 4.518064, and mean squared displacement 25.216388. Before the next run, record a hypothesis, an observation from the plot, and one model limitation so the command becomes a scientific experiment rather than only a generated image.