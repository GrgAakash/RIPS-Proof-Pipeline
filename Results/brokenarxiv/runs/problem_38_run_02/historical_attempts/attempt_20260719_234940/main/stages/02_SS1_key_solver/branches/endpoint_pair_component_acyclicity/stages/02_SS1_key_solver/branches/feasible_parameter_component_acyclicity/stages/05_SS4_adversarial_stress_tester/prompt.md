Fresh no-history solver-only M/S NESTED BRANCH PIPELINE, SS4 Adversarial Stress Tester. Use canonical prompt source `pipeline_sources/Prompt Packet/Prompts.md` (`pipeline_sources` copy, not mirrored `integrated_pipeline/Codes`). Do not read memory, prior task history, previous outputs outside this input bundle, answer keys, or the private memory directory. Do not use web search/internet. Do not use API keys. You are spawned with `fork_context=false`; treat this prompt as your full input.

You are SS4, the nested branch Adversarial Stress Tester. Run last after constructive outputs. Try to break the proposed derivations; do not compose final answer. Attack SC5, U001-U002, infinite-cover handling, component-locality, edge cases, and any hidden citation/theorem-strength mismatch. Block if the proof proves only connectedness, finite nerve acyclicity, or a stronger unsupported theorem.

Allowed supporting statements:
Definitions, notation, and assumptions needed to parse the target are allowed. Standard elementary convexity, exact finite-dimensional topology/homology facts at stated strength, and ordinary singular homology facts may be used. No web. No specialized line-transversal acyclicity theorem.

Nested branch target theorem:
Let d>=1, m>=2, and let C_1,...,C_m be pairwise disjoint open convex subsets of R^d. Let
Delta = { (lambda_2,...,lambda_{m-1}) : 0 < lambda_2 < ... < lambda_{m-1} < 1 }, with lambda_1=0 and lambda_m=1. For lambda in Delta define
P_lambda = { (a,b) in C_1 x C_m : (1-lambda_i)a + lambda_i b in C_i for every i=2,...,m-1 }.
Let D = { lambda in Delta : P_lambda is nonempty }.
Prove every connected component of D is acyclic. For m=2, Delta is a point and D is that point if C_1,C_2 are nonempty, otherwise empty.

S0 nested blueprint summary:
- TDC-1 fixed-parameter fibers P_lambda convex.
- TDC-2 fixed-endpoint parameter sets B_(a,b) convex and component-local.
- TDC-3 central topological box-incidence lemma must prove full component reduced homology, not just finite nerves/connectedness.
- TDC-4 m=2 and empty-set conventions.
- U001 exact box-incidence acyclicity lemma validity.
- U002 infinite/open covers finite cycle passage.
- U003 pairwise disjointness role, non-target-determining.
- U004 edge convention.

Constructive SS1 global summary:
- SUBPROBLEM UNSOLVED.
- Proved edge cases m=2, empty sets, m=3; P_lambda open convex; B_x open convex and component-local.
- Reduced D to union of convex parameter boxes B_x with convex opposite fibers P_lambda.
- Did not prove the box-incidence acyclicity lemma; warned generic good-cover/nerve acyclicity is insufficient because finite unions of convex boxes can have holes.
- Proposed stronger abstract lemma: if X open convex, Delta open simplex, R={(x,lambda): lambda in B_x} open, B_x open convex boxes, and X_lambda={x:lambda in B_x} convex, then every component of union_x B_x is acyclic.
- TDC-3 UNESTABLISHED; U001/U002 OPEN.

Constructive SS2 topological specialist summary:
- SUBPROBLEM UNSOLVED as originally stated; found counterexample to general convex-fiber incidence lemma.
- Counterexample: Y closed 2-simplex, p interior, X=R^2, R={(x,y): x dot (y-p)>0}. For y!=p, vertical fiber P_y open convex halfspace; P_p empty; hence D=Y\{p}. For each x, B_x={y in Y: x dot(y-p)>0} is relatively open convex. But D deformation retracts to boundary S^1, so H_1 nonzero. Therefore convex vertical/horizontal fibers alone cannot imply D-component acyclicity.
- Proved narrowed lemma: for a component Omega of D, let E_Omega={x:B_x cap Omega nonempty}. Since B_x connected, B_x subset Omega if nonempty intersection. If E_Omega is acyclic, then Omega is acyclic via R_Omega homotopy equivalences. Chain-level finite-subcover reduction works under this narrowed hypothesis.
- New open unknown: whether actual endpoint-interpolation box structure implies E_Omega acyclic/convex for every Omega.

Constructive SS3 geometric/edge summary:
- SOLVED assigned SC1-SC3.
- Empty C_i => D empty; m=2 => D empty or point.
- P_lambda open convex via affine preimages/intersections.
- B_(a,b)=Delta cap intersections of affine preimages C_i is open convex; nonempty B_(a,b) lies in one component of D. Pairwise disjointness not used locally.
- Resolved U003 locally and U004 edge convention; no global acyclicity proof.

Required stress output sections:
1. Attack inventory
2. Findings
3. Stress-test verdict fenced YAML:
```yaml
role_task_status: completed
stress_test_verdict: PASS | BLOCK | INCONCLUSIVE
blocks_acceptance: true | false
ledger_underreach_audit: PASS | FAIL
ledger_overreach_audit: PASS | FAIL
background_manifest_underreach_audit: PASS | FAIL
background_manifest_misclassification_audit: PASS | FAIL
attacked_claims: []
challenged_claim_ids: []
competing_candidates: []
obstruction: ""
required_resolution: ""
```
4. Role-completion summary fenced YAML with keys: failure_output_type, type, failed_route, obstruction, evidence, reuse_value, guidance_sentence, candidate_lemma_statement, why_unblocks, where_used, allowed_inputs, dependencies, weaker_than_target, equivalent_or_stronger, recommended.
5. Local Source Ledger with statuses.
6. Web-source confirmation: `no web sources used`.

Verdict guidance: PASS only if constructive outputs prove nested target. BLOCK if central U001/U002 remains open, if the broad lemma is false, or if only a conditional/narrowed lemma remains.