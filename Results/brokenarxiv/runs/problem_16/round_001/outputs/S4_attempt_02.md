1. Assignment restatement

S-ID:
S4

assigned subclaim(s):
Assemble C3 and C4 into the target factorization.

what must be proved:
For every `t in T(Q_p)`, assuming C3 supplies `q in T(Q)` with the same local character valuations as `t`, and assuming C4 converts equality of those valuations into compactness of `tq^{-1}`, prove that `t = kq` with `k in T(Z_p)` and `q in T(Q)`. Conclude `T(Q_p) = T(Z_p)T(Q)`.

declared prerequisite subclaims:
C3 and C4.

2. Subproof or failure

Assume C3 and C4.

Let `t in T(Q_p)` be arbitrary. By C3, there exists `q in T(Q)` such that, after choosing the fixed finite Galois splitting field `K/Q`, a place `w | p`, and character lattice `X = X^*(T_K)`, the local character valuations of `q` and `t` agree:
`v_w(χ(q)) = v_w(χ(t))` for every `χ in X`.

View `q` as an element of `T(Q_p)` via the field embedding `Q -> Q_p`. Set
`k = tq^{-1}` in `T(Q_p)`. Since `t` and `q` have identical local character valuations, C4 applies and gives
`k = tq^{-1} in T(Z_p)`.

Therefore
`t = kq`
with `k in T(Z_p)` and `q in T(Q)`. Since `t in T(Q_p)` was arbitrary, this proves
`T(Q_p) subset T(Z_p)T(Q)`.

The reverse inclusion is immediate from functoriality and the group law: `T(Z_p) subset T(Q_p)`, and `T(Q)` maps into `T(Q_p)`, so every product of an element of `T(Z_p)` and an element of `T(Q)` lies in `T(Q_p)`. Hence
`T(Q_p) = T(Z_p)T(Q)`.

3. Solver failure output and candidate guidance

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

claim_id: L1
proof_location: Section 2, first paragraph
claim_or_fact_used: C3 provides a rational point with matching local character valuations.
source_status: allowed supporting statement
cited_label_or_name: C3
exact_statement_used: For any `t in T(Q_p)`, there exists `q in T(Q)` such that `v_w(χ(q)) = v_w(χ(t))` for every `χ in X`.
hypotheses_or_conditions_needed: Fixed splitting setup for `T`, with `K/Q`, `w | p`, and `X = X^*(T_K)`.
where_hypotheses_are_checked: Declared prerequisite subclaim C3.
strength_used: Exact valuation matching for all characters.
notes: Used as a prerequisite, not reproved.

claim_id: L2
proof_location: Section 2, second paragraph
claim_or_fact_used: Rational points map to local points.
source_status: standard background fact
cited_label_or_name: Functoriality of points under field extension
exact_statement_used: For an algebraic group `T` over `Q` and a field embedding `Q -> Q_p`, there is a natural group homomorphism `T(Q) -> T(Q_p)`.
hypotheses_or_conditions_needed: `T` is a `Q`-group and `Q -> Q_p` is a field embedding.
where_hypotheses_are_checked: Given in the target setup.
strength_used: Allows `q in T(Q)` to be multiplied with `t in T(Q_p)`.
notes: This is also implicit in the notation `T(Z_p)T(Q)`.

claim_id: L3
proof_location: Section 2, second paragraph
claim_or_fact_used: C4 converts equal local character valuations into compactness.
source_status: allowed supporting statement
cited_label_or_name: C4
exact_statement_used: If `t in T(Q_p)` and `q in T(Q)` have identical local character valuations over `K_w`, then `tq^{-1} belongs to T(Z_p)`.
hypotheses_or_conditions_needed: `t` and `q` have identical local character valuations.
where_hypotheses_are_checked: Established by C3 in Section 2.
strength_used: Membership of `tq^{-1}` in `T(Z_p)`.
notes: Used as a prerequisite, not reproved.

claim_id: L4
proof_location: Section 2, final paragraph
claim_or_fact_used: Product inclusion into local points.
source_status: standard background fact
cited_label_or_name: Group law and subgroup inclusion
exact_statement_used: If `A subset G` and `B subset G`, then `AB subset G`; here `T(Z_p) subset T(Q_p)` and `T(Q)` maps into `T(Q_p)`.
hypotheses_or_conditions_needed: `T(Z_p)` is a subgroup of `T(Q_p)` and `T(Q)` is viewed inside `T(Q_p)`.
where_hypotheses_are_checked: `T(Z_p)` is given as the maximal compact subgroup of `T(Q_p)`; `T(Q) -> T(Q_p)` follows from L2.
strength_used: Reverse inclusion `T(Z_p)T(Q) subset T(Q_p)`.
notes: Elementary group-theoretic step.

5. Interface notes for S6

what this subproof establishes:
Conditional on C3 and C4, it proves the desired factorization `T(Q_p) = T(Z_p)T(Q)`.

what remains conditional:
C3 and C4 must be established elsewhere.

failure_output_type:
solved

candidate guidance sentence, if any:
null

auxiliary lemma candidate, if any:
null

notation introduced:
`k = tq^{-1}`.

risk points:
The proof depends entirely on exact valuation matching in C3 and the compactness criterion in C4.

6. Web-source confirmation

no web sources used