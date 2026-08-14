1. Assignment restatement

S-ID: S3

assigned subclaim(s): Constant branch.

what must be proved: If \(f\) is constant on an open interval \(I\), then \(f\) is differentiable at every point of \(I\), and \(f'(a)=0\) for every \(a\in I\).

declared prerequisite subclaims: None.

2. Subproof or failure

Let \(I\subseteq M\) be an open interval, and suppose \(f:I\to M\) is constant on \(I\). Thus there is some \(c\in M\) such that \(f(x)=c\) for every \(x\in I\).

Fix \(a\in I\). We prove that \(f\) is differentiable at \(a\) with derivative \(0\). Since \(I\) is open and \(a\in I\), there exists \(\delta_0>0\) such that whenever \(x\in M\) and \(|x-a|<\delta_0\), then \(x\in I\).

Let \(\varepsilon>0\). Choose \(\delta=\delta_0\). If \(0<|x-a|<\delta\), then \(x\in I\), and since \(f\) is constant on \(I\),
\[
\frac{f(x)-f(a)}{x-a}
=
\frac{c-c}{x-a}
=
0.
\]
Therefore
\[
\left|\frac{f(x)-f(a)}{x-a}-0\right|=0<\varepsilon.
\]
This is exactly the ordered-field \(\varepsilon\)-\(\delta\) definition of differentiability at \(a\) with derivative \(0\).

Since \(a\in I\) was arbitrary, \(f\) is differentiable everywhere on \(I\), with derivative identically \(0\).

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

claim_id: S3-C1  
proof_location: Section 2, first paragraph  
claim_or_fact_used: A function constant on \(I\) has one value \(c\) on all of \(I\).  
source_status: proved inside the current proof  
cited_label_or_name: Definition of constant function  
exact_statement_used: If \(f\) is constant on \(I\), then there exists \(c\in M\) such that \(f(x)=c\) for all \(x\in I\).  
hypotheses_or_conditions_needed: \(f\) is constant on \(I\).  
where_hypotheses_are_checked: Assumption of assigned subclaim.  
strength_used: Exact.  
notes: No definability is needed for this branch.

claim_id: S3-C2  
proof_location: Section 2, second paragraph  
claim_or_fact_used: An open interval is open in the ordered-field topology, so each point has a small open neighborhood contained in it.  
source_status: standard background fact  
cited_label_or_name: Interior-neighborhood property of open intervals  
exact_statement_used: If \(I\) is an open interval and \(a\in I\), then there exists \(\delta_0>0\) such that \(|x-a|<\delta_0\) implies \(x\in I\).  
hypotheses_or_conditions_needed: \(I\) is an open interval; \(a\in I\).  
where_hypotheses_are_checked: Fixed \(a\in I\) in Section 2.  
strength_used: Exact.  
notes: This is part of the usual topology induced by the order.

claim_id: S3-C3  
proof_location: Section 2, displayed quotient computation  
claim_or_fact_used: For \(x\neq a\), the difference quotient of a constant function is \(0\).  
source_status: proved inside the current proof  
cited_label_or_name: Ordered-field arithmetic  
exact_statement_used: If \(f(x)=f(a)=c\) and \(x\neq a\), then \((f(x)-f(a))/(x-a)=0\).  
hypotheses_or_conditions_needed: \(x,a\in I\), \(x\neq a\), \(f\) constant on \(I\).  
where_hypotheses_are_checked: \(0<|x-a|<\delta\) gives \(x\neq a\), and \(\delta=\delta_0\) gives \(x\in I\).  
strength_used: Exact.  
notes: Uses only field arithmetic.

claim_id: S3-C4  
proof_location: Section 2, final paragraph  
claim_or_fact_used: Ordered-field \(\varepsilon\)-\(\delta\) definition of derivative.  
source_status: provided definition / notation / assumption  
cited_label_or_name: Usual one-variable derivative over the ordered-field topology  
exact_statement_used: \(f'(a)=L\) iff for every \(\varepsilon>0\) there exists \(\delta>0\) such that \(0<|x-a|<\delta\) and \(x\) in the domain imply \(\left|\frac{f(x)-f(a)}{x-a}-L\right|<\varepsilon\).  
hypotheses_or_conditions_needed: \(a\) is an interior point of the domain.  
where_hypotheses_are_checked: \(a\in I\) and \(I\) is open.  
strength_used: Exact.  
notes: Applied with \(L=0\).

5. Interface notes for S6

what this subproof establishes: If a definable function is constant on an open interval \(I\), then it is differentiable at every point of \(I\), with derivative \(0\).

what remains conditional: Nothing inside S3; this branch only requires that the assembler has already obtained an open interval on which \(f\) is constant.

failure_output_type: solved

candidate guidance sentence, if any: None.

auxiliary lemma candidate, if any: None.

notation introduced: \(I\) for the constant interval; \(c\) for the constant value; \(a\) for an arbitrary point of \(I\).

risk points: The proof uses the usual derivative definition at interior points of the domain; this is valid because \(I\) is open.

6. Web-source confirmation

no web sources used