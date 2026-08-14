1. Assignment restatement

Prove the inadmissibility half for `0 < alpha <= 1`: construct a bounded perturbation `h`, use it to obtain a predictive density that dominates the Jeffreys predictive density under KL risk for every `beta > 0`, and treat the boundary case `alpha = 1`.

2. Subproof or failure

SETUP FAILURE: missing input.

The assigned task asks me to “prove the displayed risk-improvement inequality,” but the displayed inequality itself is not included in the supplied packet. The S0 blueprint only describes its existence at a planning level and is explicitly not a mathematical premise. Since no allowed supporting statements are provided, I cannot cite or reconstruct a hidden inequality without risking use of an unstated downstream lemma.

Missing input:

- The actual displayed risk-improvement inequality referred to in the S4 assignment.
- The precise definition of the perturbation class or predictive density to which that inequality applies.

3. Solver failure output and candidate guidance with the required YAML

```yaml
solver_status: failed_setup
failure_type: missing_input
missing_inputs:
  - displayed risk-improvement inequality referenced by S4 assignment
  - exact perturbation/predictive-density framework for h
candidate_guidance:
  - Provide the explicit inequality S4 is supposed to prove.
  - Specify whether h perturbs the prior, the marginal, the predictive density directly, or a scale parameter inside q_J.
  - Include the normalization formula for the perturbed predictive density.
```

4. Local Source Ledger

Used only:

- Target theorem statement supplied in the prompt.
- S0 blueprint for assignment/planning only.
- Standard definitions of Gamma density, KL loss, Bayesian predictive density, and admissibility.

No external sources, tools, files, web search, simulations, CAS, notebooks, or prior history were used.

5. Interface notes for S6

S6 should not treat this as a completed proof of the `0 < alpha <= 1` half. The missing displayed inequality is load-bearing. Once supplied, S4’s proof should verify:

- the perturbation is bounded and yields a valid predictive density;
- the KL risk gap is nonnegative for every `beta > 0`;
- strict improvement holds for at least one `beta`, hence inadmissibility;
- the limiting or logarithmic construction for `alpha = 1` is handled separately.

6. Web-source confirmation

No web sources were used.