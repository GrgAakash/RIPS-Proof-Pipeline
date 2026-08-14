Fresh no-history solver-only M/S BRANCH PIPELINE, S0 Blueprint Solver. Use the latest canonical Messi/Scaloni prompt source for this experiment: `pipeline_sources/Prompt Packet/Prompts.md` (canonical `pipeline_sources` copy, not mirrored `integrated_pipeline/Codes`). This prompt includes the relevant S0 instructions. Do not use memory, prior task history, previous outputs, answer keys, files outside this fresh input bundle, or the private memory directory. Do not use web search/internet. Do not use API keys. You are spawned with `fork_context=false`; treat this as your complete context.

You are S0, the Blueprint Solver. Your task is to create an executable solution blueprint for the normalized target problem. Do not write the final solution. Do not certify an unsupported candidate as established. Use a global-first architecture: one Global/Key Solver attempts the entire target plus one separate Adversarial Stress Tester, adding targeted specialists only for concrete independent obligations. Work in two passes: semantic reading and mathematical mechanism first; provenance/unknown ledger second.

Allowed supporting statements for this branch:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. No formal paper skeleton is supplied. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed. Standard elementary convexity, basic Euclidean topology, and ordinary singular homology facts may be used only at exact stated strength or proved in-artifact. Specialized line-transversal acyclicity theorems may not be cited.

Target theorem for this branch:
Let d>=1, m>=2, and let C_1,...,C_m be pairwise disjoint open convex subsets of R^d. Define
P = { (a,b) in C_1 x C_m : there exist parameters 0 < lambda_2 < ... < lambda_{m-1} < 1 such that (1-lambda_i)a + lambda_i b in C_i for every i=2,...,m-1 }.
For m=2 this means P=C_1 x C_2. Prove that every connected component of P is acyclic (has trivial reduced singular homology).

Additional mathematical guidance: None.

Produce exactly the S0 sections from the canonical prompt:
1. Target normalization
2. Task-adaptive proof obligations
3. Available tools
4. Subclaim support graph
5. Target-determining claim register
6. Mathematical Unknowns Ledger
7. Key-step and key-solver selection
8. Failure-mode checks
9. Subsolver execution plan
10. Subsolver assignment table
11. Web-source confirmation

Use contiguous active IDs SS1, SS2, ... and include exactly one adversarial stress tester. End with `no web sources used`.