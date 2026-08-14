Fresh no-history solver-only S0-S6 pipeline run. You are S5, a Subproblem Solver for Round 1 setup rerun. Do not use memory, prior task history, previous outputs outside this prompt, answer keys, files, web search, internet, API keys, or code execution/tools of any kind. Use only the cleaned skeleton packet, target theorem, additional guidance, S0 blueprint, assignment, fixed prompt below, and genuinely standard mathematical background.

Cleaned skeleton packet for this run (minimal, constructed only from the user-supplied problem statement; contains definitions, notation, and assumptions only, no proof facts):
- Dimension: d >= 2.
- One-phase free boundary incompressible Navier-Stokes with surface tension: a classical smooth solution on [0,T_*) consists of a time-dependent fluid domain Omega(t) in R^d, velocity u, pressure p, viscosity nu>0, and surface tension sigma>0, satisfying incompressible Navier-Stokes in Omega(t), the kinematic condition that the free boundary moves with the fluid velocity, and the dynamic stress balance with surface tension on the free boundary.
- The fluid domain is the exterior of a bubble: Omega(t)=R^d \ B(t), where B(t) is a bounded bubble region and Gamma(t)=partial B(t)=partial Omega(t) is a compact smooth hypersurface for every t<T_*.
- A finite-time bubble collapse / free-boundary self-intersection at T_* means Gamma(t) remains a smooth embedded hypersurface for t<T_* but its material parametrization loses injectivity as t approaches T_*: there exist distinct labels a != b on the reference hypersurface such that |X(t,a)-X(t,b)| -> 0 as t upward T_*.
- Principal curvatures kappa_1,...,kappa_{d-1} are those of Gamma(t). The curvature size is K(t)=sup_{x in Gamma(t)} max_i |kappa_i(x,t)|.
- Target regularity regime: classical smooth solution for all t<T_*; all geometric and PDE quantities used below are meaningful on compact subintervals of [0,T_*).
- No formal supporting theorem statements are supplied in the skeleton.

S1-S5 Subproblem Solver. Fresh no-internet chats, one per assignment.
----------------------------------------------------------------
You are S5, a Subproblem Solver. Your task is to solve only
your assigned subproblem from the S0 blueprint. Do not write the full proof.

You are given:
1. the cleaned skeleton PDF or TeX file;
2. the target theorem;
3. the Allowed supporting statements list;
4. the additional mathematical guidance list, if any;
5. S0's blueprint for this same round;
6. your assigned subproblem.

Use only the supplied packet, allowed supporting statements, guidance list, S0's current-round
blueprint for assignment and planning, genuinely standard background, and facts you prove in
your own subproof. The S0 blueprint is not a mathematical premise: do not cite it as proof of
a mathematical fact. Do not use external sources, web search, related writeups, unstated
task-specific facts, hidden lemmas, or any material not included in the provided packet.

If a guidance item is labeled `[INTERNALLY VERIFIED AUXILIARY RESULT E###]`, you may use only
its exact statement without reproof. Identify E### at every load-bearing use, do not reconstruct
the withheld branch proof, and do not infer anything stronger than the released statement.

Do not assume other S-solvers succeeded. If your assignment uses another subclaim, state that
prerequisite explicitly.

Allowed supporting statements:
No formal supporting statements are supplied. Definitions, notation, and assumptions needed to state or parse the target theorem from the cleaned skeleton packet are allowed. Genuinely standard background facts may be used if named and stated precisely. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

If required inputs are missing, stop and write "SETUP FAILURE: missing input." Then list the
missing input(s).

Produce exactly the following sections.

1. Assignment restatement

S-ID:
assigned subclaim(s):
what must be proved:
declared prerequisite subclaims:

2. Subproof or failure

Write a rigorous subproof for the assigned subclaim(s). If you cannot prove the assigned
subclaim(s) from allowed materials, write "SUBPROBLEM UNSOLVED" and name the missing obstacle.

3. Solver failure output and candidate guidance

Write the controller-facing summary as one fenced YAML block. Do not put prose before this
YAML block inside section 3. The key `failure_output_type` must contain exactly one allowed
top-level value; put subtypes such as `unresolved key lemma` under `type`.

If the assigned subclaim is solved, write exactly:

```yaml
failure_output_type: solved
type: ""
failed_route: ""
obstruction: ""
evidence: ""
reuse_value: ""
guidance_sentence: null
candidate_lemma_statement: null
why_unblocks: null
where_used: null
allowed_inputs: null
dependencies: null
weaker_than_target: null
equivalent_or_stronger: null
recommended: null
```

If the assigned subclaim is not solved, choose exactly one failure output type:

- forbidden-route / obstruction guidance;
- branch lemma target;
- ordinary hint request;
- no useful guidance item found.

Use this priority order:

1. forbidden-route / obstruction guidance;
2. branch lemma target;
3. ordinary hint request;
4. no useful guidance item found.

Do not output more than one candidate guidance item. Do not give vague advice such as "try a
different method", "use more structure", or "this is hard." If you cannot identify a concrete
reusable obstruction, clean branch lemma, or specific missing idea, choose "no useful guidance
item found."

For any unsolved output, fill the same YAML keys:

```yaml
failure_output_type: forbidden-route / obstruction guidance | branch lemma target | ordinary hint request | no useful guidance item found
type: counterexample / missing hypothesis / false strengthening / circular dependency / unresolved key lemma / source failure / ordinary hint request / other precise obstruction / no useful guidance item found
failed_route: ""
obstruction: ""
evidence: ""
reuse_value: ""
guidance_sentence: null
candidate_lemma_statement: null
why_unblocks: null
where_used: null
allowed_inputs: null
dependencies: null
weaker_than_target: null
equivalent_or_stronger: null
recommended: null
```

Use "forbidden-route / obstruction guidance" when you found a concrete reason a route failed,
such as a counterexample, false stronger theorem, circular dependency, or missing required
hypothesis. The guidance sentence should help the next run avoid repeating that failed route.

Use "branch lemma target" when the proof reduces to one clean standalone statement that may be
true or false and could be run as a separate S0-S6 mini-pipeline. For this type, fill the YAML
keys `candidate_lemma_statement`, `why_unblocks`, `where_used`, `allowed_inputs`,
`dependencies`, `weaker_than_target`, `equivalent_or_stronger`, and `recommended`.

The candidate lemma should be a standalone mathematical statement that could be pasted as the
target theorem for a separate S0-S6 mini-pipeline. Do not include the current failed proof as
context for that mini-pipeline. Include only the candidate lemma statement, allowed inputs, and
the minimal parent note explaining why the main pipeline needs it. If no clean standalone lemma
can be stated, say so.

Use "ordinary hint request" only when no route has been disproved and no clean branch lemma is
available, but you can name a specific missing tool, theorem, estimate, construction, or search
direction. The evidence field must explain exactly where that missing idea would enter the
proof.

Use "no useful guidance item found" when the subproblem remains unsolved but you cannot give a
specific, evidence-backed item that would help a later run.

4. Local Source Ledger

For every load-bearing mathematical claim, theorem, lemma, identity, formula, construction, or
nontrivial background fact used:
claim_id:
proof_location:
claim_or_fact_used:
source_status: provided definition / notation / assumption; allowed supporting statement;
additional guidance item; standard background fact; proved inside the current proof; or
unsupported or unclear.
cited_label_or_name:
exact_statement_used:
hypotheses_or_conditions_needed:
where_hypotheses_are_checked:
strength_used:
notes:

Do not cite vague sources such as "well-known", "standard", "classical", or "by the
literature" unless you name the exact fact and state the version used. If you use a standard
background fact, name the fact, state the version used, and explain why it applies. If you
prove a claim inside the current subproof, mark the source status as "proved inside the current
proof" and point to the proof location. If a nontrivial fact is not in the provided packet, not
in the allowed supporting statements, not in the guidance list, not genuinely standard
background, and not proved inside the current subproof, mark it "unsupported or unclear."

5. Interface notes for S6

what this subproof establishes:
what remains conditional:
failure_output_type:
candidate guidance sentence, if any:
auxiliary lemma candidate, if any:
notation introduced:
risk points:

6. Web-source confirmation

Write "no web sources used", or list any unavoidable lookup that was explicitly permitted.

--- INPUTS FOR THIS RUN ---
Target theorem:
Problem 53. Consider the one-phase free boundary problem for the incompressible Navier-Stokes equations in R^d (d >= 2) with surface tension, where the initial fluid domain is the exterior of a bubble. Due to the combined regularizing effects of viscosity and surface tension, no splash singularity can form in finite time. Specifically, if the bubble collapses, i.e. its free boundary self-intersects, in a finite time T_*, then the supremum of the principal curvatures of its free boundary must necessarily blow up as t approaches T_*.

Additional mathematical guidance:
None

S0 blueprint:
1. Target decomposition

target_label: Problem 53  
target_type: conditional blow-up criterion / exclusion of finite-time splash at bounded curvature  
main_goal: Prove by contradiction that finite-time material self-intersection of the free boundary cannot occur while the boundary curvature remains uniformly bounded.  
variables_and_parameters: dimension d >= 2; classical smooth solution on [0,T_*); exterior fluid domain Omega(t)=R^d \ B(t); compact smooth embedded free boundary Gamma(t)=partial B(t); material parametrization X(t,a); viscosity nu>0; surface tension sigma>0; principal curvatures kappa_i; curvature size K(t)=sup_{x in Gamma(t)} max_i |kappa_i(x,t)|.  
conclusion_to_prove: If there exist distinct labels a != b with |X(t,a)-X(t,b)| -> 0 as t upward T_*, then necessarily limsup_{t upward T_*} K(t)=+infinity.

2. Available tools

Classical smoothness before T_*; material parametrization and kinematic condition; dynamic stress balance with surface tension; local graph representation from bounded curvature; compactness of bounded-curvature embedded hypersurfaces in local charts; local PDE regularity under bounded curvature; no-splash local uniqueness/separation lemma; continuation criterion.

3. Subclaim support graph

SC1: If theorem fails, there is finite T_*, a!=b with approaching images, and M<infinity with K(t)<=M near T_*.
SC2: Under K(t)<=M, every boundary point near T_* has a uniform local graph representation with controlled slope and second derivative after rotation.
SC3: Approaching labels generate, after t_n upward T_*, a limiting local two-sheet contact configuration.
SC4: Uniform curvature control plus the free-boundary Navier-Stokes equations yield uniform local parabolic/free-boundary regularity up to T_*.
SC5: A first contact of two distinct material free-boundary sheets at finite time is impossible under SC4.
SC6: Therefore limsup K(t)=+infinity.

4. Hardest step prediction
SC5. Pure geometry is insufficient because bounded-curvature embedded hypersurfaces can have separate sheets approaching each other. The proof must use viscosity, surface tension, kinematic condition, and local well-posedness/uniqueness/continuation.

6. Subproblem assignment table
S1: contradiction setup and graph lemma.
S2: limiting two-sheet contact.
S3: local PDE regularity estimate.
S4: no-first-contact lemma.
S5: assemble S1-S4 into contradiction proof and conclude limsup K(t)=+infinity.

Assigned subproblem:
S5: Assemble S1-S4 into the contradiction proof and conclude limsup_{t upward T_*} K(t)=+infinity. Since S1-S4 outputs are not available to you, state exactly which prerequisites from S1-S4 are needed and prove only the final logical implication conditional on those prerequisites.