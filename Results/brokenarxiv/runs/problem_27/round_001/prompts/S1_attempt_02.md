Fresh no-history solver-only S1 run. Do not use memory, prior task history, answer keys, web search, internet, API keys, terminal, code execution, files, or tools. Use only the mathematical input in this prompt and genuinely standard background. If the assigned claim is false or insufficient, say so; do not fabricate a proof.

You are S1, a Subproblem Solver. Your task is to solve only your assigned subproblem from the S0 blueprint. Do not write the full proof. Use the fixed S1-S5 solver protocol: produce exactly sections 1. Assignment restatement, 2. Subproof or failure, 3. Solver failure output and candidate guidance as a fenced YAML block using the specified solved/unsolved keys, 4. Local Source Ledger, 5. Interface notes for S6, 6. Web-source confirmation. The S0 blueprint is not a mathematical premise. Do not assume other S-solvers succeeded.

Cleaned skeleton packet for this run:
The target theorem statement below is the complete mathematical packet. Definitions/notation appearing in the statement are available: Coxeter group W, irreducible Coxeter group, length function ell, Bruhat order and Bruhat interval [u,v], interval length ell(v)-ell(u), isomorphism type of a finite poset interval. No paper skeleton, bibliography, or additional formal supporting statements are supplied.

Allowed supporting statements:
No formal supporting statements are supplied. Definitions, notation, and assumptions needed to state or parse the target theorem are allowed. Genuinely standard background about Coxeter systems, the length function, Bruhat order, reduced expressions, and the subword criterion may be used only if explicitly stated as standard background. No statement equivalent to, stronger than, or logically downstream from the target theorem is allowed.

Target theorem:
Problem 27: Let W be an irreducible Coxeter group. For each fixed integer k >= 0, only finitely many isomorphism types of Bruhat intervals of length k (where the length of an interval [u,v] is defined as ell(v)-ell(u) with ell being the length function on W) occur in W if and only if W is a finite Coxeter group.

Additional mathematical guidance:
None

S0 blueprint:
1. Target decomposition

target_label:
Problem 27

target_type:
if and only if classification theorem

main_goal:
Show that an irreducible Coxeter group W has finitely many Bruhat-interval isomorphism types in every fixed interval length k >= 0 exactly when W is finite.

variables_and_parameters:
W: irreducible Coxeter group. ell: length function. [u,v]: Bruhat interval with u <= v. k >= 0: fixed integer interval length ell(v)-ell(u).

conclusion_to_prove:
For every fixed k >= 0, only finitely many finite-poset isomorphism types of Bruhat intervals [u,v] with ell(v)-ell(u)=k occur in W if and only if W is finite.

2. Available tools
Finite Coxeter group has finitely many intervals: If W is finite, then there are only finitely many pairs (u,v) with u <= v; hence only finitely many Bruhat intervals, and therefore only finitely many isomorphism types in each fixed length.
Subword criterion for Bruhat order: For a reduced expression of v, elements x <= v are represented by subwords of that reduced expression, with Bruhat order detected through subword containment after allowing reduced representatives.
Infinite irreducible Coxeter groups contain arbitrarily long reduced words with controlled local Coxeter behavior: If W is infinite and irreducible, then one can find reduced words of arbitrarily large length whose Bruhat subword structure contains arbitrarily large distinguishable finite configurations. This must be made precise in the final proof.
Ranked-poset invariants distinguish interval isomorphism types: If two finite Bruhat intervals are isomorphic as posets, then they have the same rank sizes, covering graph degrees, numbers of elements in each rank, and comparable-element counts.
Construction of fixed-length intervals with unbounded internal size/invariant: For some fixed k, depending only on the infinite irreducible Coxeter system, there exists an infinite family of intervals [u_n,v_n] with ell(v_n)-ell(u_n)=k whose poset invariants are pairwise distinct. This must be proved inside the current proof.

3. Subclaim support graph
SC1: If W is finite, then for each fixed k >= 0, only finitely many Bruhat intervals of length k occur, hence only finitely many isomorphism types occur. Uses none. Suggested S1.
SC2: It suffices for the converse to prove the contrapositive: if W is infinite and irreducible, then there exists at least one fixed integer k >= 0 for which infinitely many Bruhat-interval isomorphism types of length k occur. Uses none. Suggested S1.
SC3: In an infinite irreducible Coxeter group, one can construct an infinite sequence of comparable pairs u_n <= v_n with a common difference ell(v_n)-ell(u_n)=k, where the Bruhat intervals [u_n,v_n] contain a numerical poset invariant growing with n. Uses SC2. Suggested S2.
SC4: The invariant chosen in SC3 is preserved by finite-poset isomorphism. Uses SC3. Suggested S3.
SC5: The intervals constructed in SC3 really have the same fixed length k. Uses SC3. Suggested S4.
SC6: Combining SC3-SC5 gives infinitely many isomorphism types of Bruhat intervals of one fixed length k in every infinite irreducible Coxeter group. Uses SC3, SC4, SC5. Suggested S5.

4. Hardest step prediction
hardest_step_id: SC3
hardest_step_description: The hard point is producing, in every infinite irreducible Coxeter group, intervals of one fixed length whose isomorphism types vary infinitely. The proof must not merely use arbitrarily long intervals [e,w]; the length difference must remain fixed.
risk_if_wrong: If the construction only gives intervals of increasing length, or if the proposed invariant is not actually unbounded at fixed interval length, the converse fails. This is also the point where circular use of the target theorem is most likely.
how_final_proof_should_handle_it: The final proof should give an explicit uniform construction of pairs u_n <= v_n, verify reducedness and Bruhat comparability using the subword criterion, compute ell(v_n)-ell(u_n)=k, and exhibit a concrete isomorphism invariant such as rank cardinalities, covering degrees, or number of elements with a specified local order property.

5. Failure-mode checks
circularity_check: Do not assume any known classification theorem saying the target statement is true. The infinite-case construction must be proved directly from standard Coxeter/Bruhat facts.
full_theorem_check: Both directions must be proved. The finite case is immediate; the infinite irreducible case requires producing failure for at least one fixed k.
source_check: No formal supporting statements or additional guidance are supplied. Only standard Coxeter background and facts proved inside the current proof may be used.
hypothesis_check: Irreducibility must be used in the infinite-case construction. The proof should not silently pass to reducible products or assume finite rank unless justified.
notation_check: length of an interval means ell(v)-ell(u), not cardinality of the interval.
standard_background_check: Allowed standard background includes Coxeter systems, reduced expressions, length, Bruhat order, and the subword criterion. Any stronger structural claim about infinite irreducible Coxeter groups must be proved inside the current proof unless genuinely standard and explicitly stated.

6. Subproblem assignment table
S1: Prove SC1 and SC2. Give the finite-group argument and restate the converse as a contrapositive. Do not address the construction of infinite families.
S2: Prove SC3. Starting only from standard Coxeter/Bruhat facts, construct in an arbitrary infinite irreducible Coxeter group an infinite family of comparable pairs u_n <= v_n whose Bruhat intervals have one fixed length and a growing finite-poset invariant.
S3: Prove SC4. Identify exactly which invariant from S2 is used and prove it is preserved by finite-poset isomorphism.
S4: Prove SC5. Check reduced expressions, Bruhat comparability, and the exact equality ell(v_n)-ell(u_n)=k for the construction from S2.
S5: Assemble SC1-SC5 into the theorem. Verify that the argument proves the stated “for each fixed k” property for finite W, and its failure for infinite irreducible W.

7. Web-source confirmation
no web sources used

Assigned subproblem:
Prove SC1 and SC2. Give the finite-group argument and restate the converse as a contrapositive. Do not address the construction of infinite families.