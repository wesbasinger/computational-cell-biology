# Module 3 Comprehension Questions

Use the Module 3 figures you generated in `data/module_03/` while answering. When you refer to a particular experiment, name its command, seed, and the parameter values you changed.

## Reading the Experiments

1. Compare `no_binding.png` with `irreversible_binding.png`. What is the only interaction-rule difference between the two runs, and how does it explain the difference in the bound-$AB$ curve?
**Binding probability is the only difference and it explains the no-change results vs the almost 98% bind**
> **Feedback:** Correct. The control has `binding_probability=0`, so eligible encounters never form $AB$ and the bound curve stays at zero. The irreversible run uses `binding_probability=0.2` with no dissociation, so successful encounters accumulate over time. State the parameter values explicitly when comparing figures: both runs use `dissociation_probability=0`, but their binding probabilities differ.

2. In the irreversible-binding experiment, why can the bound-$AB$ count increase but not decrease? Identify the specific model rule responsible, then name one real biological process that the model is omitting when that rule is set to zero.
**It's the dissociation-probability that governs the bound AB count having regression.  when I was asking the AI chat for details, it gave proteins separating as one of the ways that molecules can dissassociate**
> **Feedback:** Right. Setting `dissociation_probability=0` removes the model's only rule for $AB \rightarrow A+B$, so complexes can form but cannot break apart. Protein complexes separating is a good biological example; more specifically, this can occur when noncovalent interactions become unstable because of thermal motion or changes in the local chemical environment.

3. Compare `irreversible_binding.png` with `reversible_binding.png`. Describe the long-term behavior of bound $AB$ in each plot. Why should the reversible run not be expected to rise monotonically?
**Irreversible trends quickly almost to 100% bound, the reversible trends closely to 50/50%**
> **Feedback:** Good observation. In the irreversible condition, $AB$ accumulates toward the maximum possible value because complexes never dissociate. In the reversible condition, binding and dissociation both occur, so the bound population fluctuates around a changing or approximate balance rather than only rising. The roughly 50% level is an outcome of this particular parameter set and seed, not a universal equilibrium value.

4. Compare `radius_025.png` and `radius_10.png`. Before looking at the plots, state a prediction for which run should generally produce more binding. Then explain why this model supports that prediction without claiming that a larger radius represents a physically larger binding site.
**I looked at the graph first, but it's clear that the larger radius encouraging binding**
> **Feedback:** Correct conclusion. A radius of `1.0` makes more $A$-$B$ pairs count as eligible encounters than a radius of `0.25`, giving the model more opportunities to sample the same binding probability. Here, encounter radius is a coarse interaction-range parameter. It does not literally model a molecule's physical diameter or the size of its binding site.

5. Compare `reversible_binding.png` and `higher_diffusion.png`. Did the higher-diffusion run produce more, less, or roughly the same final binding for this seed? Why is one seeded run insufficient evidence for a general conclusion about the effect of diffusion coefficient?
**Diffusion produced about the same final binding for this seed.  The random seed has implication for both binding and disassociation.  I'm not sure I see exactly in code how diffision changes the run.  I see it used in the move methods, but maybe not the dissassociation method?**
> **Feedback:** Correct on both the observation and the seed caveat. Diffusion coefficients affect position updates in `_move_free_molecules()` and `_move_complexes()` through `_move_position()`, where the coordinate noise scale is $\sqrt{2D\Delta t}$. They do not enter `_dissociate_complexes()`; dissociation uses only `dissociation_probability`. Diffusion can still affect binding indirectly by changing which free molecules get within the encounter radius. One seed gives one random realization, so several seeds are needed to assess an average effect.

## Reasoning About the Model

6. At every recorded timepoint, which two conservation relationships should hold between free and bound populations? Write them using the initial totals $A_{\mathrm{total}}$ and $B_{\mathrm{total}}$. Explain why one $AB$ complex changes both free populations by one.
**Generally, free + bound should equal the total initial population**
> **Feedback:** That is the essential idea. Write the two relationships separately: $A_{\mathrm{total}} = A_{\mathrm{free}} + AB$ and $B_{\mathrm{total}} = B_{\mathrm{free}} + AB$. Each complex contains exactly one $A$ molecule and one $B$ molecule, so creating one $AB$ reduces both free counts by one; dissociation reverses that change.

7. A pair of molecules is within the encounter radius, but does not bind during the timestep. What does the model do on that timestep, and what does it deliberately not attempt to represent about molecular recognition or chemistry?
**I'm not sure about this one.**
> **Feedback:** The pair remains as two free molecules after the failed Bernoulli binding trial. They may diffuse, encounter again, and get another opportunity to bind in a later timestep. The model does not represent molecular orientation, shaped binding pockets, electrostatic forces, solvent effects, or the atom-by-atom chemical mechanism that determines whether a real encounter produces a complex.

8. The code processes dissociation before it searches for new $A$-$B$ encounters. Give one consequence this ordering has for a complex that dissociates during a timestep. Why is stating the update order important for reproducibility and interpretation?
**I think that means that models cannot dissassociate and bind on the same timestep, I think this decision favors binding over dissassoicateion.**
> **Feedback:** Close, but the first conclusion is reversed. A complex that dissociates is returned to two free molecules at the complex position before the encounter search. It can therefore be considered for binding again in that same timestep, and it will re-form if it encounters an eligible partner and the binding draw succeeds. The order does not inherently favor binding or dissociation; it specifies exactly when each rule can act. That precision matters because changing the order changes outcomes even with the same seed and parameters.

## Experiment Reflection

Choose the experiment that surprised you most and record:

```text
Command:
Seed:
Prediction before running it:
Observation from the plot:
Model rule that most directly explains the observation:
What the observation does not establish about real cellular molecules:
One follow-up experiment, including the parameter you would change:
```

This is the experiment that suprised me the most.  I had no prediction before running it, but I was suprised at how fast the population approached 100% bind.
```
python experiments/module_03/run_binding_experiment.py --binding-probability 0.2 --dissociation-probability 0 --seed 42 --output data/module_03/irreversible_binding.png
```
> **Feedback:** This is a useful observation. The rapid rise follows from a combination of 100 initial molecules of each species, reflecting boundaries that keep them in the domain, repeated encounter opportunities over 500 steps, a 20% chance of binding at each eligible encounter, and no dissociation. To make the reflection a complete scientific record, add the remaining fields from the template: the seed is `42`; describe the curve as your observation; identify irreversible binding as the governing rule; state that the plot does not establish real cellular binding rates; and propose one parameterized follow-up, such as lowering `--binding-probability` to `0.05` or increasing the domain dimensions to reduce encounter frequency.
