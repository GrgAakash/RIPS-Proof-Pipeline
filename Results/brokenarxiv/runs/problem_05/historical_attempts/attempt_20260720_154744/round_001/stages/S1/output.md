1. Assignment restatement

S-ID: S1

assigned subclaim(s): Set up notation. Let \(T_i=\partial N(L_i)\), choose standard meridian-longitude coordinates \((\mu_i,\lambda_i)\), write each boundary slope as reduced \(a_i/p_i\), and prove the equivalence between “not meridional or integral” and \(p_i\ge 2\).

what must be proved: For each boundary component \(\partial P\cap T_i\), after writing its slope as \(r_i=a_i/p_i\) in reduced standard coordinates with \(p_i\ge 0\), the condition that this slope is neither meridional nor integral is equivalent to \(p_i\notin\{0,1\}\), equivalently \(p_i\ge 2\).

declared prerequisite subclaims: none.

2. Subproof or failure

Let
\[
L=L_1\cup\cdots\cup L_N\subset S^3
\]
and set
\[
T_i=\partial N(L_i)
\]
for \(i=1,\dots,N\). On each \(T_i\), choose the standard meridian-longitude basis \((\mu_i,\lambda_i)\), where \(\mu_i\) is the meridian of \(L_i\) and \(\lambda_i\) is the standard longitude.

Since \(P\) is a spanning surface with exactly one boundary component on each boundary torus \(T_i\), denote that boundary curve by
\[
\gamma_i=\partial P\cap T_i.
\]
By the slope notation in the target theorem, \(\gamma_i\) has a slope
\[
r_i=\frac{a_i}{p_i}
\]
in standard meridian-longitude coordinates. Choose this expression reduced, with \(p_i\ge 0\). Thus \(\gcd(a_i,p_i)=1\), with the usual convention that \(p_i=0\) gives the meridional slope \(1/0\), up to sign.

By the convention explicitly used in the target theorem, a boundary slope \(a_i/p_i\) is meridional or integral exactly when
\[
p_i\in\{0,1\}.
\]
Indeed, \(p_i=0\) is the meridional case, while \(p_i=1\) gives an integral slope \(a_i/1\). Conversely, every meridional slope is represented by denominator \(0\), and every integral slope is represented by denominator \(1\).

Therefore the negation of “meridional or integral” is
\[
p_i\notin\{0,1\}.
\]
Since \(p_i\) is a nonnegative integer, this is equivalent to
\[
p_i\ge 2.
\]

Thus, assuming for contradiction that no boundary component of \(P\) has meridional or integral slope is exactly the same as assuming
\[
p_i\ge 2
\]
for every \(i=1,\dots,N\).

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

claim_id: S1-1  
proof_location: Section 2, first paragraph  
claim_or_fact_used: The boundary tori are \(T_i=\partial N(L_i)\).  
source_status: provided definition / notation / assumption  
cited_label_or_name: Target theorem notation  
exact_statement_used: \(X_L=S^3\setminus \operatorname{int}(N(L))\), with one boundary torus corresponding to each component \(L_i\).  
hypotheses_or_conditions_needed: \(L=L_1\cup\cdots\cup L_N\) is an \(N\)-component link.  
where_hypotheses_are_checked: Target theorem assumes \(L\) is an \(N\)-component link.  
strength_used: Only the notation for boundary tori is used.  
notes: None.

claim_id: S1-2  
proof_location: Section 2, first paragraph  
claim_or_fact_used: Each \(T_i\) has standard meridian-longitude coordinates \((\mu_i,\lambda_i)\).  
source_status: provided definition / notation / assumption  
cited_label_or_name: Target theorem, “standard meridian-longitude coordinates”  
exact_statement_used: Boundary slopes are written as \(a/p\) in standard meridian-longitude coordinates.  
hypotheses_or_conditions_needed: \(T_i\) is a boundary torus of a link exterior in \(S^3\).  
where_hypotheses_are_checked: Target theorem.  
strength_used: Only coordinate notation is used.  
notes: None.

claim_id: S1-3  
proof_location: Section 2, second paragraph  
claim_or_fact_used: Each boundary component \(\gamma_i=\partial P\cap T_i\) has a slope \(r_i=a_i/p_i\).  
source_status: provided definition / notation / assumption  
cited_label_or_name: Target theorem  
exact_statement_used: The theorem refers to “at least one boundary component of \(P\)” having slope \(a/p\).  
hypotheses_or_conditions_needed: \(P\) has exactly one boundary component on each boundary torus.  
where_hypotheses_are_checked: Target theorem definition of incompressible spanning planar surface.  
strength_used: Only existence of a slope for each boundary component is used.  
notes: No additional essentiality claim is needed beyond the theorem’s own slope notation.

claim_id: S1-4  
proof_location: Section 2, second paragraph  
claim_or_fact_used: A slope may be written in reduced form \(a_i/p_i\) with \(p_i\ge 0\).  
source_status: standard background fact  
cited_label_or_name: Standard parametrization of slopes on an oriented torus by primitive homology classes  
exact_statement_used: Given a chosen basis \((\mu,\lambda)\) for \(H_1(T^2)\), an unoriented essential simple closed curve slope is represented by a primitive pair \((a,p)\), unique up to simultaneous sign; choosing \(p\ge 0\) fixes the denominator sign convention.  
hypotheses_or_conditions_needed: A slope on a torus and a chosen basis \((\mu,\lambda)\).  
where_hypotheses_are_checked: Each \(\gamma_i\) is given as having a slope on \(T_i\), and \((\mu_i,\lambda_i)\) is chosen.  
strength_used: Only reduced notation with nonnegative denominator is used.  
notes: This is standard slope notation, not a link-specific theorem.

claim_id: S1-5  
proof_location: Section 2, third paragraph  
claim_or_fact_used: \(p_i=0\) corresponds to the meridional slope, and \(p_i=1\) corresponds to an integral slope.  
source_status: provided definition / notation / assumption  
cited_label_or_name: Target theorem convention  
exact_statement_used: The target theorem states that a slope \(a/p\) is “meridional or integral, i.e. \(p\in\{0,1\}\).”  
hypotheses_or_conditions_needed: Slope is written as \(a_i/p_i\) in standard meridian-longitude coordinates with \(p_i\ge 0\).  
where_hypotheses_are_checked: Section 2.  
strength_used: Exact equivalence between meridional/integral and denominator \(0\) or \(1\).  
notes: This is the central assigned equivalence.

claim_id: S1-6  
proof_location: Section 2, fourth paragraph  
claim_or_fact_used: For a nonnegative integer \(p_i\), \(p_i\notin\{0,1\}\) iff \(p_i\ge 2\).  
source_status: standard background fact  
cited_label_or_name: Elementary order property of nonnegative integers  
exact_statement_used: If \(p\in\mathbb Z_{\ge 0}\), then exactly one of \(p=0\), \(p=1\), or \(p\ge 2\) holds.  
hypotheses_or_conditions_needed: \(p_i\in\mathbb Z_{\ge 0}\).  
where_hypotheses_are_checked: Section 2, reduced slope convention.  
strength_used: Full elementary equivalence.  
notes: Pure arithmetic.

5. Interface notes for S6

what this subproof establishes: Each boundary slope can be written as \(r_i=a_i/p_i\) with \(p_i\ge 0\), and “not meridional or integral” is equivalent to \(p_i\ge 2\).

what remains conditional: Nothing inside S1; later use of Dehn filling, capped surfaces, reducibility, and the obstruction lemma remains outside this subproblem.

failure_output_type: solved

candidate guidance sentence, if any: none

auxiliary lemma candidate, if any: none

notation introduced: \(T_i=\partial N(L_i)\), \((\mu_i,\lambda_i)\), \(\gamma_i=\partial P\cap T_i\), \(r_i=a_i/p_i\), \(p_i\ge 0\).

risk points: The proof relies on the target theorem’s own convention that “meridional or integral” means \(p\in\{0,1\}\). No stronger slope-distance statement is used.

6. Web-source confirmation

no web sources used