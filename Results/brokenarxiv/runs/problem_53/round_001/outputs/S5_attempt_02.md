1. Assignment restatement

S-ID: S5

assigned subclaim(s): Assemble S1-S4 into the final contradiction.

what must be proved: Conditional on the needed S1-S4 subclaims, prove that if finite-time material self-intersection occurs at \(T_*\), then
\[
\limsup_{t\uparrow T_*} K(t)=+\infty .
\]

declared prerequisite subclaims:

- P1: If the target conclusion fails, then there exist \(M<\infty\) and \(t_0<T_*\) such that \(K(t)\le M\) for all \(t\in[t_0,T_*)\), while there are distinct labels \(a\ne b\) with \(|X(t,a)-X(t,b)|\to0\) as \(t\uparrow T_*\).
- P2: Under the bound \(K(t)\le M\) near \(T_*\), the approaching material points generate a limiting two-sheet contact configuration at time \(T_*\).
- P3: Under the same curvature bound, the local free-boundary Navier-Stokes solution has enough uniform regularity up to \(T_*\) near the limiting contact configuration for the no-first-contact principle to apply.
- P4: No-first-contact principle: a first finite-time contact of two distinct material free-boundary sheets satisfying the regularity in P3 is impossible.

2. Subproof or failure

Assume P1-P4.

Suppose, toward contradiction, that the target theorem is false. Then there is a classical smooth solution on \([0,T_*)\) whose free boundary self-intersects in the material sense at \(T_*\), but
\[
\limsup_{t\uparrow T_*}K(t)<+\infty .
\]
By P1, after possibly restricting to times \(t\in[t_0,T_*)\), there is a finite constant \(M\) such that \(K(t)\le M\), and there are distinct labels \(a\ne b\) with
\[
|X(t,a)-X(t,b)|\to0 \qquad \text{as } t\uparrow T_* .
\]

Applying P2 to this bounded-curvature collapsing configuration gives a limiting two-sheet contact configuration at time \(T_*\), arising from the two distinct material sheets associated with the labels \(a\) and \(b\). Since \(\Gamma(t)\) is smooth and embedded for every \(t<T_*\), these two sheets do not intersect before \(T_*\). Thus their limiting contact at \(T_*\) is a first contact.

By P3, the local solution near this limiting configuration has the regularity required for the no-first-contact principle. Therefore P4 applies and says that such a first finite-time contact of two distinct material sheets is impossible.

This contradiction shows that the assumption
\[
\limsup_{t\uparrow T_*}K(t)<+\infty
\]
cannot hold whenever material self-intersection occurs at \(T_*\). Hence
\[
\limsup_{t\uparrow T_*}K(t)=+\infty .
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
proof_location: Section 2, first paragraph  
claim_or_fact_used: Failure of the desired blow-up conclusion gives finite curvature limsup.  
source_status: provided definition / notation / assumption  
cited_label_or_name: target theorem negation  
exact_statement_used: If the desired conclusion is false, then self-intersection occurs at \(T_*\) and \(\limsup_{t\uparrow T_*}K(t)<+\infty\).  
hypotheses_or_conditions_needed: Target theorem is assumed false.  
where_hypotheses_are_checked: Section 2 contradiction assumption.  
strength_used: Exact negation of the desired conditional conclusion.  
notes: No external theorem used.

claim_id: C2  
proof_location: Section 2, second paragraph  
claim_or_fact_used: P1 gives bounded curvature near \(T_*\) and approaching distinct material labels.  
source_status: proved inside current proof conditionally from declared prerequisite  
cited_label_or_name: P1  
exact_statement_used: If the target conclusion fails, then \(K(t)\le M\) near \(T_*\) and distinct labels \(a\ne b\) satisfy \(|X(t,a)-X(t,b)|\to0\).  
hypotheses_or_conditions_needed: Failure of target conclusion.  
where_hypotheses_are_checked: Section 2 first paragraph.  
strength_used: Full statement of P1.  
notes: This is conditional on S1 output.

claim_id: C3  
proof_location: Section 2, third paragraph  
claim_or_fact_used: Bounded curvature plus approaching labels yield a limiting two-sheet contact configuration.  
source_status: proved inside current proof conditionally from declared prerequisite  
cited_label_or_name: P2  
exact_statement_used: Under \(K(t)\le M\) near \(T_*\), the approaching material points generate a limiting local two-sheet contact configuration.  
hypotheses_or_conditions_needed: \(K(t)\le M\) near \(T_*\) and approaching distinct labels.  
where_hypotheses_are_checked: Section 2 second paragraph.  
strength_used: Full statement of P2.  
notes: This is conditional on S2 output.

claim_id: C4  
proof_location: Section 2, third paragraph  
claim_or_fact_used: Since \(\Gamma(t)\) is embedded for \(t<T_*\), the limiting contact is a first contact.  
source_status: provided definition / notation / assumption  
cited_label_or_name: definition of finite-time bubble collapse / self-intersection  
exact_statement_used: \(\Gamma(t)\) remains a smooth embedded hypersurface for \(t<T_*\), while distinct material images approach as \(t\uparrow T_*\).  
hypotheses_or_conditions_needed: Smooth embeddedness for all \(t<T_*\), distinct material labels approaching the same limiting point.  
where_hypotheses_are_checked: Skeleton packet and P1/P2.  
strength_used: Embeddedness before \(T_*\) rules out earlier intersection of the two sheets.  
notes: This only establishes “first” relative to the two approaching sheets.

claim_id: C5  
proof_location: Section 2, fourth paragraph  
claim_or_fact_used: Uniform local regularity up to \(T_*\) allows use of no-first-contact principle.  
source_status: proved inside current proof conditionally from declared prerequisite  
cited_label_or_name: P3  
exact_statement_used: Under the bounded curvature hypothesis, the local solution has enough uniform regularity near the limiting contact for P4 to apply.  
hypotheses_or_conditions_needed: \(K(t)\le M\) near \(T_*\) and the limiting contact configuration.  
where_hypotheses_are_checked: Section 2 second and third paragraphs.  
strength_used: Exact applicability condition for P4.  
notes: This is conditional on S3 output.

claim_id: C6  
proof_location: Section 2, fourth paragraph  
claim_or_fact_used: First finite-time contact of two distinct material sheets is impossible.  
source_status: proved inside current proof conditionally from declared prerequisite  
cited_label_or_name: P4  
exact_statement_used: A first contact of two distinct material free-boundary sheets satisfying the regularity in P3 cannot occur at finite time.  
hypotheses_or_conditions_needed: First contact and P3 regularity.  
where_hypotheses_are_checked: Section 2 third and fourth paragraphs.  
strength_used: Full contradiction.  
notes: This is conditional on S4 output.

claim_id: C7  
proof_location: Section 2, final paragraph  
claim_or_fact_used: Contradiction discharges the assumption of finite curvature limsup.  
source_status: standard background fact  
cited_label_or_name: proof by contradiction / classical logic  
exact_statement_used: If assuming \(A\) implies a contradiction, then \(\neg A\).  
hypotheses_or_conditions_needed: Classical logic.  
where_hypotheses_are_checked: Contradiction obtained from P2-P4.  
strength_used: Exact logical inference.  
notes: Genuinely standard logical rule.

5. Interface notes for S6

what this subproof establishes: Conditional on P1-P4, finite-time material self-intersection forces \(\limsup_{t\uparrow T_*}K(t)=+\infty\).

what remains conditional: The actual proofs of P1, P2, P3, and P4.

failure_output_type: solved

candidate guidance sentence, if any: none

auxiliary lemma candidate, if any: none

notation introduced: \(M\), \(t_0\), and prerequisite labels P1-P4.

risk points: The proof depends entirely on P3 and P4; pure bounded-curvature geometry alone does not rule out two embedded sheets approaching one another.

6. Web-source confirmation

no web sources used