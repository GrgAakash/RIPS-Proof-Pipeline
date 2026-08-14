1. Assignment restatement

S-ID: S3

assigned subclaim(s): State the standard Schur-concavity derivative criterion for differentiable symmetric functions on the simplex interior.

what must be proved: For a differentiable symmetric function \(F\) on the interior of the probability simplex, Schur-concavity imposes
\[
(p_a-p_b)(\partial_aF(p)-\partial_bF(p))\le 0
\]
for every pair of coordinates \(a,b\).

declared prerequisite subclaims: None.

2. Subproof or failure

Let
\[
\Delta_N^\circ=\{p\in \mathbb R^N:p_i>0,\ \sum_{i=1}^N p_i=1\}.
\]
For a differentiable symmetric function \(F:\Delta_N^\circ\to \mathbb R\), the standard Schur-concavity derivative criterion says:

If \(F\) is Schur-concave on \(\Delta_N^\circ\), then for every \(p\in\Delta_N^\circ\) and every pair \(a,b\),
\[
(p_a-p_b)(\partial_aF(p)-\partial_bF(p))\le 0,
\]
where \(\partial_aF-\partial_bF\) denotes the directional derivative of \(F\) in the simplex direction \(e_a-e_b\), equivalently the difference of ambient partial derivatives for any \(C^1\) extension.

More strongly, under the usual \(C^1\) regularity hypothesis, this inequality for all \(p,a,b\) is also sufficient for Schur-concavity.

Thus, in the concrete application with coordinates \(x=p_a\) and \(y=p_b\), Schur-concavity would require
\[
(x-y)(\partial_xF-\partial_yF)\le 0.
\]

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

claim_id: C1  
proof_location: Section 2  
claim_or_fact_used: Definition of simplex interior  
source_status: provided definition / notation / assumption  
cited_label_or_name: probability simplex notation  
exact_statement_used: \(\Delta_N^\circ=\{p\in\mathbb R^N:p_i>0,\sum_i p_i=1\}\).  
hypotheses_or_conditions_needed: \(p\) is a probability vector with strictly positive entries.  
where_hypotheses_are_checked: Target theorem uses probability vectors \(p\).  
strength_used: Notational only.  
notes: Used to state the domain of the derivative criterion.

claim_id: C2  
proof_location: Section 2  
claim_or_fact_used: Schur-concavity derivative criterion  
source_status: standard background fact  
cited_label_or_name: Schur-Ostrowski derivative criterion  
exact_statement_used: If \(F\) is differentiable and symmetric on the simplex interior, then Schur-concavity implies \((p_a-p_b)(\partial_aF(p)-\partial_bF(p))\le0\) for all \(p,a,b\); with \(C^1\) regularity this condition is also sufficient.  
hypotheses_or_conditions_needed: \(F\) differentiable, symmetric, defined on \(\Delta_N^\circ\); derivatives interpreted along simplex directions or via a \(C^1\) extension.  
where_hypotheses_are_checked: The assigned subproblem asks specifically for the criterion for differentiable symmetric functions on the simplex interior.  
strength_used: Necessary condition; sufficiency stated but not needed for later contradiction.  
notes: This is the load-bearing criterion for S4.

claim_id: C3  
proof_location: Section 2  
claim_or_fact_used: Coordinate specialization  
source_status: proved inside the current proof  
cited_label_or_name: none  
exact_statement_used: Setting \(x=p_a\) and \(y=p_b\), the criterion becomes \((x-y)(\partial_xF-\partial_yF)\le0\).  
hypotheses_or_conditions_needed: Coordinates \(x,y\) correspond to two entries of \(p\).  
where_hypotheses_are_checked: Direct substitution into C2.  
strength_used: Exact specialization.  
notes: This is the form needed by later subclaims.

5. Interface notes for S6

what this subproof establishes: Schur-concavity requires the derivative inequality \((p_a-p_b)(\partial_aF-\partial_bF)\le0\) on the simplex interior.

what remains conditional: Later use requires the concrete signs for \(x-y\) and \(\partial_xF-\partial_yF\).

failure_output_type: solved

candidate guidance sentence, if any: None.

auxiliary lemma candidate, if any: None.

notation introduced: \(\Delta_N^\circ\), \(e_a-e_b\).

risk points: The derivative difference must be interpreted as a simplex-direction derivative or via a compatible \(C^1\) extension.

6. Web-source confirmation

no web sources used