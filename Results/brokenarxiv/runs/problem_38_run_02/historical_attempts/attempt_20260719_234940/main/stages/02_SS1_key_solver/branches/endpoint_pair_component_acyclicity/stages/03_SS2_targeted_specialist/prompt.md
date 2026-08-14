Fresh no-history solver-only M/S BRANCH PIPELINE, SS2 Targeted Specialist. Use canonical prompt source `pipeline_sources/Prompt Packet/Prompts.md` (`pipeline_sources` copy, not mirrored `integrated_pipeline/Codes`). Do not read memory, prior task history, previous outputs outside this input bundle, answer keys, or the private memory directory. Do not use web search/internet. Do not use API keys. You are spawned with `fork_context=false`; treat this prompt as your full input.

You are SS2, a Subproblem Solver with work_scope `assigned_subclaim`. Follow the canonical Dynamic Subproblem Solver behavior: first solve mathematically, then annotate status/source/unknowns. Do not certify unsupported claims. Do not prove the full target; solve only SC2/TDC-3: the exact componentwise homology-transfer lemma needed for witness and endpoint/witness projections.

Allowed supporting statements for this branch:
Definitions, notation, and assumptions needed to parse the target theorem are allowed. No formal paper skeleton is supplied. Standard elementary convexity, basic Euclidean topology, paracompactness/partition of unity on Euclidean open sets if stated exactly, and ordinary singular homology facts may be used only at exact stated strength or proved in-artifact. No specialized line-transversal acyclicity theorem.

Branch target theorem context:
Let d>=1, m>=2, and let C_1,...,C_m be pairwise disjoint open convex subsets of R^d. Define
P = { (a,b) in C_1 x C_m : there exist parameters 0 < lambda_2 < ... < lambda_{m-1} < 1 such that (1-lambda_i)a + lambda_i b in C_i for every i=2,...,m-1 }.
For m=2 P=C_1 x C_2. The branch aims to prove every connected component of P is acyclic.

Your assigned subclaim SC2:
Prove the exact componentwise homology-transfer lemma needed for witness and endpoint/witness projections, using only ordinary singular homology and verified local convex/good-cover properties. The intended incidence space may be
Delta={0<lambda_2<...<lambda_{m-1}<1},
P_lambda={(a,b) in C_1 x C_m : (1-lambda_i)a+lambda_i b in C_i for all intermediates},
W={(a,b,lambda): lambda in Delta and (a,b) in P_lambda},
D={lambda in Delta : P_lambda nonempty}.
You may prove a general lemma of the form: if E subset B x R^N is open and every fiber E_b is nonempty convex, then projection E->B is a homotopy equivalence on each connected component, via continuous section and fiberwise straight-line deformation. Then verify it applies to W->P and W->D, or state exactly why it does not.

S0 branch blueprint summary relevant to you:
- TDC-3: endpoint-to-line and witness projections used in route preserve component homology; expected basis derived_here.
- U001 required_resolution_test: State and prove exact projection lemma used, then verify its hypotheses for witness and endpoint-to-line maps componentwise.
- Do not infer total acyclicity from arbitrary convex fibers unless your exact hypotheses justify homotopy equivalence.

Output exactly these sections:
1. Assignment restatement
2. Subproof or failure
3. Solver failure output and candidate guidance (one fenced YAML block)
4. Local Source Ledger, including TDC reports and Unknowns addendum
5. Interface notes for S6
6. Web-source confirmation: write `no web sources used`.