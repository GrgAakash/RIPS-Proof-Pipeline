1. Assignment restatement

S-ID: S3

assigned subclaim(s): C4

what must be proved: If `t in T(Q_p)` and `q in T(Q)` have identical local character valuations over `K_w`, meaning
`v_w(χ(t)) = v_w(χ(q))` for every `χ in X = X^*(T_K)`, then `tq^{-1} belongs to T(Z_p)`.

declared prerequisite subclaims: C2, namely that the local character-valuation map on `T(Q_p)` has kernel exactly `T(Z_p)`. C1 is also used only for the standard notation/evaluation framework.

2. Subproof or failure

Assume the setup of C1: `K/Q` is a finite Galois splitting field for `T`, `w | p`, `K_w/Q_p` is the corresponding local splitting field, and `X = X^*(T_K)`.

Let `t in T(Q_p)` and `q in T(Q)`. View `q` as an element of `T(Q_p)` through the field embedding `Q -> Q_p`. Suppose that for every character `χ in X`,
\[
v_w(\chi(t)) = v_w(\chi(q)).
\]

Consider `tq^{-1} in T(Q_p)`. For any `χ in X`, since `χ` is a group homomorphism after base change to `K_w`,
\[
\chi(tq^{-1}) = \chi(t)\chi(q)^{-1}.
\]
Applying the additive valuation `v_w` on `K_w^*`, we get
\[
v_w(\chi(tq^{-1}))
= v_w(\chi(t)) - v_w(\chi(q))
= 0.
\]
Thus the local character-valuation map sends `tq^{-1}` to the zero homomorphism `X -> Z`.

By the declared prerequisite C2, the kernel of this local valuation map is exactly the maximal compact subgroup `T(Z_p)`. Therefore
\[
tq^{-1} \in T(Z_p).
\]
This proves C4, conditional on C2.

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
proof_location: Section 2, setup paragraph  
claim_or_fact_used: A rational point `q in T(Q)` may be viewed as a local point in `T(Q_p)`.  
source_status: standard background fact  
cited_label_or_name: Functoriality of points of an algebraic group under field extension  
exact_statement_used: For a `Q`-group `T` and a field embedding `Q -> Q_p`, there is an induced group homomorphism `T(Q) -> T(Q_p)`.  
hypotheses_or_conditions_needed: `T` is a `Q`-group; `Q` embeds into `Q_p`.  
where_hypotheses_are_checked: Target theorem setup.  
strength_used: Only the existence of the induced map.  
notes: Used to make `tq^{-1}` an element of `T(Q_p)`.

claim_id: L2  
proof_location: Section 2, character calculation  
claim_or_fact_used: Characters are multiplicative.  
source_status: provided definition / notation / assumption  
cited_label_or_name: Definition of character of an algebraic torus  
exact_statement_used: If `χ` is a character of `T_{K_w}`, then `χ(ab^{-1}) = χ(a)χ(b)^{-1}` for `a,b in T(K_w)`.  
hypotheses_or_conditions_needed: `χ` is a group morphism `T_{K_w} -> G_m`.  
where_hypotheses_are_checked: `χ in X = X^*(T_K)`, base-changed to `K_w`.  
strength_used: Multiplicativity and inverse compatibility.  
notes: Gives `χ(tq^{-1}) = χ(t)χ(q)^{-1}`.

claim_id: L3  
proof_location: Section 2, valuation calculation  
claim_or_fact_used: Additivity of a nonarchimedean discrete valuation on products.  
source_status: standard background fact  
cited_label_or_name: Additive valuation law  
exact_statement_used: For `a,b in K_w^*`, `v_w(ab^{-1}) = v_w(a) - v_w(b)`.  
hypotheses_or_conditions_needed: `a,b` are nonzero elements of `K_w`.  
where_hypotheses_are_checked: Character values lie in `K_w^*`.  
strength_used: Only additivity under multiplication and inversion.  
notes: Converts equal valuations into zero valuation for the quotient.

claim_id: L4  
proof_location: Section 2, final paragraph  
claim_or_fact_used: Kernel of the local character-valuation map is `T(Z_p)`.  
source_status: unsupported or unclear  
cited_label_or_name: Declared prerequisite C2  
exact_statement_used: For the local torus `T/Q_p`, the character-valuation map on `T(Q_p)` has kernel exactly `T(Z_p)`, the maximal compact subgroup.  
hypotheses_or_conditions_needed: The local valuation map is formed using a finite splitting field `K_w/Q_p`.  
where_hypotheses_are_checked: Setup inherited from C1/C2.  
strength_used: Exact identification of the kernel.  
notes: This is explicitly declared as a prerequisite subclaim, not proved in S3.

claim_id: L5  
proof_location: Section 2, conclusion before applying C2  
claim_or_fact_used: Equal character valuations imply `tq^{-1}` maps to zero under the local valuation map.  
source_status: proved inside the current proof  
cited_label_or_name: none  
exact_statement_used: If `v_w(χ(t)) = v_w(χ(q))` for all `χ`, then `v_w(χ(tq^{-1})) = 0` for all `χ`.  
hypotheses_or_conditions_needed: The equal-valuation assumption and L2-L3.  
where_hypotheses_are_checked: Section 2 assumptions.  
strength_used: Full statement.  
notes: This is the core internal step of C4.

5. Interface notes for S6

what this subproof establishes: C4 is proved conditional on C2: equal local character valuations for `t` and `q` force `tq^{-1} in T(Z_p)`.

what remains conditional: The proof depends on C2, the kernel identification for the local valuation map.

failure_output_type: solved

candidate guidance sentence, if any: none

auxiliary lemma candidate, if any: none

notation introduced: The local valuation expression `v_w(χ(tq^{-1}))`.

risk points: C2 must be available with the same valuation map and the same meaning of `T(Z_p)` as maximal compact subgroup.

6. Web-source confirmation

no web sources used