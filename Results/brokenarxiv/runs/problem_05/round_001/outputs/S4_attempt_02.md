1. Assignment restatement

S-ID: S4

assigned subclaim(s): Conditional obstruction claims (a)-(d), plus boundary-compression-only assessment.

what must be proved: Each named object, if produced by S3 in \(X_L\), contradicts either incompressibility of \(P\) or standard topological consequences of \(X_L\) being a hyperbolic link exterior.

declared prerequisite subclaims: Conditional on S3 producing the relevant object: a compressing disk for \(P\), an essential sphere, an essential torus, an essential non-boundary-parallel annulus, or only a boundary-compressing disk.

2. Subproof or failure

Let \(X_L\) be the exterior of a hyperbolic link. By the meaning of “hyperbolic link exterior,” \(\operatorname{int}(X_L)\) admits a complete finite-volume hyperbolic metric. Standard consequences are that \(X_L\) is irreducible, atoroidal, and contains no essential properly embedded annulus except boundary-parallel cusp annuli.

(a) If S3 produces a compressing disk \(D\) for \(P\) in \(X_L\), then \(\partial D\subset P\) is an essential simple closed curve in \(P\), and \(D\cap P=\partial D\). This is exactly what the hypothesis “\(P\) is incompressible” excludes. Hence this case contradicts incompressibility of \(P\).

(b) If S3 produces an essential embedded \(2\)-sphere \(S\subset X_L\), then \(S\) does not bound a \(3\)-ball in \(X_L\). But hyperbolic link exteriors are irreducible, so every embedded \(2\)-sphere in \(X_L\) bounds a \(3\)-ball. Contradiction.

(c) If S3 produces an essential torus \(T\subset X_L\), then \(T\) is incompressible and not boundary-parallel. But hyperbolic link exteriors are atoroidal: every incompressible torus is boundary-parallel to a cusp torus. Contradiction.

(d) If S3 produces an essential annulus \(A\subset X_L\) whose image is not boundary-parallel, then \(A\) is a properly embedded incompressible annulus not parallel into \(\partial X_L\). Finite-volume hyperbolic link exteriors are acylindrical/anannular in this sense: every essential annulus is boundary-parallel into the cusp boundary. Thus such an annulus cannot exist. Contradiction.

Boundary-compression-only case: incompressibility alone does not rule out a boundary-compressing disk. A compressing disk has boundary a closed essential curve on \(P\), whereas a boundary-compressing disk has boundary equal to an essential arc in \(P\) together with an arc in \(\partial X_L\). These are distinct notions. To obtain a contradiction from boundary-compression alone, one needs the additional hypothesis that \(P\) is boundary-incompressible, or an additional argument converting the boundary-compression into one of the forbidden objects above.

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
proof_location: 2(a)  
claim_or_fact_used: A compressing disk for \(P\) contradicts incompressibility of \(P\).  
source_status: provided definition / notation / assumption  
cited_label_or_name: incompressibility of \(P\)  
exact_statement_used: \(P\) has no compressing disk in \(X_L\).  
hypotheses_or_conditions_needed: \(P\subset X_L\) is incompressible; S3 produces a compressing disk for \(P\).  
where_hypotheses_are_checked: Target theorem and conditional assignment.  
strength_used: Exact.  
notes: This is definitional.

claim_id: C2  
proof_location: 2(b)  
claim_or_fact_used: A finite-volume hyperbolic link exterior is irreducible.  
source_status: standard background fact  
cited_label_or_name: hyperbolic 3-manifolds are irreducible  
exact_statement_used: If \(\operatorname{int}(X_L)\) is complete finite-volume hyperbolic, then every embedded \(S^2\subset X_L\) bounds a \(3\)-ball.  
hypotheses_or_conditions_needed: \(L\) is hyperbolic.  
where_hypotheses_are_checked: Target theorem.  
strength_used: Rules out essential spheres.  
notes: Standard topological consequence of hyperbolicity.

claim_id: C3  
proof_location: 2(c)  
claim_or_fact_used: A finite-volume hyperbolic link exterior is atoroidal.  
source_status: standard background fact  
cited_label_or_name: hyperbolic 3-manifolds are atoroidal  
exact_statement_used: Every incompressible embedded torus in \(X_L\) is boundary-parallel to a cusp torus.  
hypotheses_or_conditions_needed: \(L\) is hyperbolic; torus is essential.  
where_hypotheses_are_checked: Target theorem and conditional assignment.  
strength_used: Rules out essential non-boundary-parallel tori.  
notes: Standard consequence of finite-volume hyperbolicity.

claim_id: C4  
proof_location: 2(d)  
claim_or_fact_used: A finite-volume hyperbolic link exterior has no essential non-boundary-parallel annuli.  
source_status: standard background fact  
cited_label_or_name: acylindricity/anannularity of finite-volume hyperbolic link exteriors  
exact_statement_used: Every properly embedded incompressible annulus in \(X_L\) is boundary-parallel into \(\partial X_L\).  
hypotheses_or_conditions_needed: \(L\) is hyperbolic; S3 produces an essential annulus with non-boundary-parallel image.  
where_hypotheses_are_checked: Target theorem and conditional assignment.  
strength_used: Rules out the annulus from S3.  
notes: This is exactly the conditional obstruction requested in part (d).

claim_id: C5  
proof_location: Boundary-compression-only paragraph  
claim_or_fact_used: Incompressibility does not by itself imply boundary-incompressibility.  
source_status: standard background fact  
cited_label_or_name: distinction between compressing disks and boundary-compressing disks  
exact_statement_used: A compressing disk has closed essential boundary on \(P\); a boundary-compressing disk has boundary consisting of an essential arc on \(P\) and an arc on \(\partial X_L\).  
hypotheses_or_conditions_needed: Definitions of compressibility and boundary-compressibility for properly embedded surfaces.  
where_hypotheses_are_checked: Standard definitions applicable to \(P\subset X_L\).  
strength_used: Shows boundary-compression alone is not a contradiction to incompressibility.  
notes: Additional missing hypothesis: boundary-incompressibility of \(P\), or a separate conversion argument.

5. Interface notes for S6

what this subproof establishes: The four S3-produced forbidden objects listed in (a)-(d) each give an immediate contradiction under the stated hypotheses and standard hyperbolic-link-exterior consequences.

what remains conditional: This proves only conditional contradictions. It does not prove that S3 actually produces any such object.

failure_output_type: solved

candidate guidance sentence, if any: null

auxiliary lemma candidate, if any: null

notation introduced: \(D\) for a compressing disk, \(S\) for a sphere, \(T\) for a torus, \(A\) for an annulus.

risk points: Boundary-compression alone is not excluded by incompressibility; S6 should require boundary-incompressibility or an argument converting boundary-compression into a listed forbidden object.

6. Web-source confirmation

no web sources used