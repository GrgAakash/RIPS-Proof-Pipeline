Fresh no-history S0-S6 solver-only pipeline task. You are a fresh S6 subagent with fork_context=false. Do not use memory, prior task history, answer keys, files, web search, internet, API keys, terminal commands, code execution, simulations, CAS, notebooks, parsers, or helper programs. Work only from this prompt and ordinary mathematical reasoning. Do not call tools.

Use the fixed S6 Composer Solver role. Your task is to compose a single final candidate proof of the target theorem from the current-round S0 blueprint and S1-S5 subproblem outputs. Use only the supplied packet, allowed supporting statements, guidance list, S0 blueprint for organization, S1-S5 outputs that actually prove their claimed subclaims, genuinely standard background, and facts proved inside your composed proof. The S0 blueprint is not a mathematical premise. Do not silently fill a missing major subproof. If S1-S5 leave a required subclaim unsolved, either prove it fully from allowed materials in the composed proof and mark it as proved inside current proof, or report the obstacle. Do not cite the target theorem, an equivalent theorem, a stronger theorem, or a logically downstream statement.

Allowed supporting statements: definitions, notation, and assumptions needed to parse the target theorem; genuinely standard background. No formal skeleton statements beyond the target are supplied. Additional mathematical guidance: None.

Produce exactly these sections: 1. Composition map; 2. Final proof wrapped in <!-- BEGIN_FINAL_PROOF --> and <!-- END_FINAL_PROOF -->; 3. Composer failure output and candidate guidance with the required YAML schema; 4. Source Ledger wrapped in <!-- BEGIN_SOURCE_LEDGER --> and <!-- END_SOURCE_LEDGER -->; 5. Completion checklist wrapped in <!-- BEGIN_COMPLETION_CHECKLIST --> and <!-- END_COMPLETION_CHECKLIST -->; 6. Web-source confirmation wrapped in <!-- BEGIN_WEB_SOURCE_CONFIRMATION --> and <!-- END_WEB_SOURCE_CONFIRMATION -->; 7. LaTeX artifact. If complete proof is not possible, write FINAL PROOF NOT COMPLETED and identify the exact blocking point. Do not fake a complete proof.

Required YAML if solved:
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
If incomplete, choose exactly one from: forbidden-route / obstruction guidance; branch lemma target; ordinary hint request; no useful guidance item found. Fill the same YAML keys.

--- INPUTS FOR THIS RUN ---
Target theorem:
Problem 01:

Consider Bernoulli bond percolation with fixed retention parameter p in (0,1] on the random recursive tree, coupled through the natural growth process (where at each step n >= 1, a new vertex n attaches to a uniformly chosen existing vertex in {0, ..., n-1}, and the connecting edge is retained with probability p). Let P(p) be the probability that the root cluster remains a largest cluster at every time step n. There exists a critical probability p_c in (0, 1) such that P(p) = 0 for p < p_c and P(p) > 0 for p > p_c.

Prove the statement.

Additional mathematical guidance:
None

S0 blueprint summary:
S0 decomposed the target into: SC1 cluster-size Markov chain; SC2 continuous-time Yule/mutation embedding; SC3 challenger process; SC4 spectral-radius criterion; SC5 continuity and monotonicity of rho(p); SC6 endpoint regimes; SC7 threshold assembly. S0 predicted hardest step SC3-SC4: define challenger process exactly enough for barrier crossing and root-leadership equivalence, then obtain extinction/survival criterion. S0 noted “largest” allows ties.

S1 output:
S1 solved. It proves that if X_i(n) are cluster sizes, then from state (x_0,...,x_m), total N, the cluster-size process moves to (x_0,...,x_i+1,...,x_m) with probability p x_i/N and to (x_0,...,x_m,1) with probability 1-p. It proves the root-leadership event is {X_0(n) >= X_i(n) for all i,n}, with ties allowed. It also constructs the continuous-time Yule/mutation embedding: each individual gives birth at rate 1; child has parent type with probability p and new type with probability 1-p; at birth times, type sizes have the same transition kernel. It cites standard equal-rate exponential clock symmetry and Poisson thinning.

S2 output:
S2 solved the deficit-process identification. Let R_n be root cluster size and for each non-root cluster C, D_n(C)=R_n-|C|_n. The challenger state is the multiset X_n={D_n(C)}. Dynamics: retained edge to root increases all deficits by 1; retained edge to a non-root cluster decreases that cluster's deficit by 1; unretained edge creates a new singleton with deficit R_n-1. Barrier crossing min X_n <=0 is exactly failure of strict root leadership. S2 flags that the target allows ties, so for the target event failure is strict overtake |C|_n>R_n, equivalently D_n(C)<0; the target barrier should be negative deficit rather than <=0.

S3 output:
S3 did not solve SC4/SC5. It reports that the supplied packet does not define the challenger process as a branching process, its type space, its offspring law, its mean operator K_p, or rho(p). It says a generic multitype branching-process spectral-radius criterion is standard, but applying it here and proving continuity/strict monotonicity requires the actual kernel or verified monotone coupling. Candidate guidance: First supply a rigorous SC3 lemma defining the challenger process and K_p, including enough regularity/irreducibility hypotheses to apply a spectral-radius extinction criterion and enough p-dependence to prove continuity and strict monotonicity.

S4 output:
S4 did not solve SC6. It reports that the challenger process, mean operator K_p, supercritical/subcritical meanings, and spectral-radius expression are not defined from the supplied packet alone. Candidate lemma: Let K_p be the mean operator of the challenger branching process defined in S2/S3. Then there exist epsilon_0, epsilon_1 >0 such that rho(K_p)>1 for 0<p<epsilon_0 and rho(K_p)<1 for 1-epsilon_1<p<1.

S5 output:
S5 did not solve the final assembly unconditionally. It says the assembly would be immediate if one had a continuous strictly decreasing function rho:(0,1)->(0,infinity) such that P(p)>0 iff rho(p)<1, P(p)=0 whenever rho(p)>1, rho(p)>1 for sufficiently small p, and rho(p)<1 for sufficiently large p. Then p_c=inf{p:rho(p)<1} gives the theorem. It flags that these are not allowed premises unless proved upstream.