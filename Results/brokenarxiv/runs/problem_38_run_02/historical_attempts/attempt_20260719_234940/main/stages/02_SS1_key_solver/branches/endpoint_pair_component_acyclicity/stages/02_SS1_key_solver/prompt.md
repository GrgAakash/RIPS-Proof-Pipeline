Fresh no-history solver-only M/S BRANCH PIPELINE, SS1 Global/Key Solver. Use canonical prompt source `pipeline_sources/Prompt Packet/Prompts.md` (`pipeline_sources` copy, not mirrored `integrated_pipeline/Codes`). Do not read memory, prior task history, previous outputs outside this input bundle, answer keys, or the private memory directory. Do not use web search/internet. Do not use API keys. You are spawned with `fork_context=false`; treat this prompt as your full input.

You are SS1, a Subproblem Solver with work_scope `global_solution`. Follow the canonical Dynamic Subproblem Solver behavior: first solve mathematically, then annotate status/source/unknowns. Do not certify an unsupported candidate as established. Do not cite the target theorem, any specialized line-transversal acyclicity theorem, or parent theorem outputs.

Allowed supporting statements for this branch:
Definitions, notation, and assumptions needed to parse the target theorem are allowed. No formal paper skeleton is supplied. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed. Standard elementary convexity, basic Euclidean topology, and ordinary singular homology facts may be used only at exact stated strength or proved in-artifact. Specialized line-transversal acyclicity theorems may not be cited.

Target theorem for this branch:
Let d>=1, m>=2, and let C_1,...,C_m be pairwise disjoint open convex subsets of R^d. Define
P = { (a,b) in C_1 x C_m : there exist parameters 0 < lambda_2 < ... < lambda_{m-1} < 1 such that (1-lambda_i)a + lambda_i b in C_i for every i=2,...,m-1 }.
For m=2 this means P=C_1 x C_2. Prove that every connected component of P is acyclic (has trivial reduced singular homology).

Additional mathematical guidance: None.

S0 branch blueprint summary:
- Task: prove every connected component K of P has trivial reduced singular homology.
- Edge cases: if some C_i empty or P empty, vacuous. If m=2, P=C_1 x C_2, product of convex sets. Handle d=1, unbounded sets, touching closures, strict order.
- S0 claims/unknowns:
  TDC-1: strict ordered parameters are part of the target definition.
  TDC-2: acyclic means reduced singular homology of each connected component vanishes.
  TDC-3: endpoint/witness projection homology transfer must be proved for these spaces, not assumed from generic convex fibers.
  TDC-4: ordered oriented line-transversal components are acyclic if used; must be derived, not cited.
  U001: exact nonproper convex-fiber transfer principle for witness/endpoint projections is open.
  U002: ordered line-space acyclicity cannot be imported; must be self-contained if used.
- S0 suggested route:
  SC1: P open; m=2 base.
  SC3/SC6: possible reduction through ordered oriented line space and projection transfer.
  SC4: for fixed direction, ordered transversal offsets are convex.
  SC5: hard central ordered line-space acyclicity from scratch if route uses it.
- Your assignment: Produce one coherent complete candidate proof of the exact branch target. Build any needed model, prove the core geometry from scratch, transfer back to endpoint components, and handle all edge cases. If you cannot prove it, write SUBPROBLEM UNSOLVED and preserve the strongest partial result and the exact obstruction. If a clean counterexample emerges, present it rigorously.

Output exactly these sections:
1. Assignment restatement
2. Subproof or failure
3. Solver failure output and candidate guidance (one fenced YAML block)
4. Local Source Ledger, including TDC reports and Unknowns addendum
5. Interface notes for S6
6. Web-source confirmation: write `no web sources used`.