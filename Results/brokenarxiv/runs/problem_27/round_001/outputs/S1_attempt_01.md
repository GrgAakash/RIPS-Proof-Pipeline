1. Assignment Restatement

S-ID: S1

assigned subclaim(s): SC1 and SC2

what must be proved:
SC1: If `W` is finite, then for each fixed `k >= 0`, only finitely many Bruhat intervals of length `k` occur, hence only finitely many isomorphism types occur.

SC2: For the converse direction, it is enough to prove the contrapositive: if `W` is infinite and irreducible, then there exists some fixed `k >= 0` for which infinitely many Bruhat-interval isomorphism types of length `k` occur.

declared prerequisite subclaims: none

2. Subproof or Failure

Let `W` be an irreducible Coxeter group.

SC1. Assume `W` is finite. Fix an integer `k >= 0`. The Bruhat intervals of length `k` are indexed by pairs `(u,v)` such that `u <= v` in Bruhat order and `ell(v)-ell(u)=k`. Since `W` is finite, the Cartesian product `W x W` is finite. Therefore the subset
\[
\{(u,v)\in W\times W : u\le v,\ \ell(v)-\ell(u)=k\}
\]
is finite.

Each such pair determines one Bruhat interval `[u,v]`, viewed as a finite poset under the inherited Bruhat order. Thus only finitely many actual intervals of length `k` occur. The set of isomorphism types represented by a finite collection of finite posets is finite, since it is the image of a finite set under the map sending a finite poset to its isomorphism type. Hence, for this fixed `k`, only finitely many isomorphism types occur. Since `k >= 0` was arbitrary, the asserted property holds for every fixed `k`.

This proves SC1.

SC2. Define the property
\[
P(W):\quad \text{for every fixed integer } k\ge 0,\text{ only finitely many isomorphism types of Bruhat intervals of length }k\text{ occur in }W.
\]
The converse implication in the target theorem is
\[
P(W)\Longrightarrow W\text{ is finite},
\]
under the standing hypothesis that `W` is irreducible.

The contrapositive of this implication is
\[
W\text{ is infinite}\Longrightarrow \neg P(W),
\]
again under the standing irreducibility hypothesis. Since
\[
\neg P(W)
\]
is precisely the statement that there exists at least one fixed integer `k >= 0` such that infinitely many isomorphism types of Bruhat intervals of length `k` occur in `W`, it is sufficient for the converse to prove:

If `W` is infinite and irreducible, then there exists some fixed `k >= 0` for which infinitely many Bruhat-interval isomorphism types of length `k` occur.

This proves SC2 as a matter of elementary logic. It does not supply the infinite-family construction.

3. Solver Failure Output And Candidate Guidance

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

4. Local Source Ledger

claim_id: S1-C1  
proof_location: Section 2, SC1  
claim_or_fact_used: If `W` is finite, then `W x W` is finite.  
source_status: standard background fact  
cited_label_or_name: finiteness of Cartesian products  
exact_statement_used: The Cartesian product of two finite sets is finite.  
hypotheses_or_conditions_needed: `W` is finite.  
where_hypotheses_are_checked: SC1 begins by assuming `W` is finite.  
strength_used: Applied only to `W x W`.  
notes: Purely set-theoretic.

claim_id: S1-C2  
proof_location: Section 2, SC1  
claim_or_fact_used: The set of pairs `(u,v)` with `u <= v` and `ell(v)-ell(u)=k` is finite.  
source_status: proved inside the current proof  
cited_label_or_name: finite subset argument  
exact_statement_used: Any subset of a finite set is finite.  
hypotheses_or_conditions_needed: The set is a subset of finite `W x W`.  
where_hypotheses_are_checked: Section 2, SC1.  
strength_used: Applied to the indexing set of length-`k` intervals.  
notes: Uses only the definitions of Bruhat order, length function, and interval length.

claim_id: S1-C3  
proof_location: Section 2, SC1  
claim_or_fact_used: A finite collection of finite posets realizes only finitely many isomorphism types.  
source_status: standard background fact  
cited_label_or_name: finite image principle  
exact_statement_used: The image of a finite set under any function is finite.  
hypotheses_or_conditions_needed: The collection of intervals is finite.  
where_hypotheses_are_checked: Section 2, SC1.  
strength_used: Applied to the map sending `[u,v]` to its finite-poset isomorphism type.  
notes: Purely set-theoretic.

claim_id: S1-C4  
proof_location: Section 2, SC2  
claim_or_fact_used: The contrapositive of `P(W) => W is finite` is `W is infinite => not P(W)`.  
source_status: standard background fact  
cited_label_or_name: contrapositive equivalence  
exact_statement_used: An implication `A => B` is logically equivalent to `not B => not A`.  
hypotheses_or_conditions_needed: The standing theorem hypothesis that `W` is irreducible remains fixed.  
where_hypotheses_are_checked: Section 2, SC2.  
strength_used: Used only to justify the proof strategy for the converse.  
notes: No Coxeter-specific fact used.

claim_id: S1-C5  
proof_location: Section 2, SC2  
claim_or_fact_used: Negating “for every fixed `k >= 0`, finitely many types occur” gives “there exists a fixed `k >= 0` for which infinitely many types occur.”  
source_status: standard background fact  
cited_label_or_name: quantifier negation over finite/infinite alternative  
exact_statement_used: The negation of `for all k, T_k is finite` is `there exists k such that T_k is not finite`; here “not finite” means infinite.  
hypotheses_or_conditions_needed: Each `T_k` is a set of isomorphism types.  
where_hypotheses_are_checked: Section 2, SC2 defines `P(W)`.  
strength_used: Used to identify `not P(W)` with the desired fixed-length failure statement.  
notes: Purely logical/set-theoretic.

5. Interface Notes For S6

what this subproof establishes: SC1 and SC2 are proved. The finite direction is complete, and the converse may be proved by showing that every infinite irreducible Coxeter group fails the fixed-length finiteness property for at least one `k`.

what remains conditional: The infinite irreducible construction is not proved here and remains for SC3-SC6.

failure_output_type: solved

candidate guidance sentence, if any: none

auxiliary lemma candidate, if any: none

notation introduced: `P(W)` for the property that every fixed interval length has only finitely many Bruhat-interval isomorphism types.

risk points: SC2 is only a logical reduction; it does not prove the existence of infinite fixed-length families.

6. Web-Source Confirmation

no web sources used