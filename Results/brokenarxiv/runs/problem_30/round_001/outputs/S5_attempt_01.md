1. Assignment Restatement

S-ID: S1

assigned subclaim(s): Compute the posterior under `pi(beta) proportional to 1/beta`, derive `q_J(y|x)`, verify it integrates to one, and record useful forms involving `x+y` and `y/(x+y)`.

what must be proved: For observed `x>0`, the Jeffreys posterior is proper and the resulting Bayesian predictive density is
\[
q_J(y\mid x)=
\frac{\Gamma((T+1)\alpha)}{\Gamma(\alpha)\Gamma(T\alpha)}
\frac{x^\alpha y^{T\alpha-1}}{(x+y)^{(T+1)\alpha}},\qquad y>0.
\]
Also verify normalization and record equivalent beta-prime/Beta-ratio forms.

declared prerequisite subclaims: None.

2. Subproof or Failure

Let `x>0` be observed. The sampling density of `x` is
\[
p(x\mid \beta)=\frac{x^{\alpha-1}}{\beta^\alpha\Gamma(\alpha)}\exp(-x/\beta),
\qquad \beta>0.
\]
With prior \(\pi(\beta)\propto 1/\beta\), the unnormalized posterior density is
\[
p(x\mid\beta)\pi(\beta)
\propto
\beta^{-\alpha-1}\exp(-x/\beta).
\]
Its normalizing integral is
\[
\int_0^\infty \beta^{-\alpha-1}e^{-x/\beta}\,d\beta
=
x^{-\alpha}\Gamma(\alpha),
\]
by the substitution \(u=x/\beta\). Therefore
\[
\pi_J(\beta\mid x)
=
\frac{x^\alpha}{\Gamma(\alpha)}
\beta^{-\alpha-1}e^{-x/\beta},
\qquad \beta>0.
\]
Equivalently, \(1/\beta\mid x\sim \mathrm{Gamma}(\alpha,\text{ rate }x)\).

The predictive density is
\[
q_J(y\mid x)
=
\int_0^\infty p(y\mid\beta)\pi_J(\beta\mid x)\,d\beta.
\]
Since
\[
p(y\mid\beta)
=
\frac{y^{T\alpha-1}}{\beta^{T\alpha}\Gamma(T\alpha)}
e^{-y/\beta},
\]
we obtain
\[
q_J(y\mid x)
=
\frac{x^\alpha y^{T\alpha-1}}{\Gamma(\alpha)\Gamma(T\alpha)}
\int_0^\infty
\beta^{-(T+1)\alpha-1}
e^{-(x+y)/\beta}\,d\beta.
\]
Again using \(u=(x+y)/\beta\),
\[
\int_0^\infty
\beta^{-(T+1)\alpha-1}e^{-(x+y)/\beta}\,d\beta
=
\frac{\Gamma((T+1)\alpha)}{(x+y)^{(T+1)\alpha}}.
\]
Thus
\[
q_J(y\mid x)=
\frac{\Gamma((T+1)\alpha)}{\Gamma(\alpha)\Gamma(T\alpha)}
\frac{x^\alpha y^{T\alpha-1}}{(x+y)^{(T+1)\alpha}},
\qquad y>0.
\]

To verify that this integrates to one, set
\[
r=\frac{y}{x+y},\qquad y=\frac{xr}{1-r},\qquad dy=\frac{x}{(1-r)^2}\,dr.
\]
As \(y\in(0,\infty)\), \(r\in(0,1)\). Then
\[
\int_0^\infty
\frac{x^\alpha y^{T\alpha-1}}{(x+y)^{(T+1)\alpha}}\,dy
=
\int_0^1 r^{T\alpha-1}(1-r)^{\alpha-1}\,dr
\cdot
\frac{\Gamma(\alpha)\Gamma(T\alpha)}{\Gamma((T+1)\alpha)}
\cdot
\frac{1}{\Gamma(\alpha)\Gamma(T\alpha)/\Gamma((T+1)\alpha)}.
\]
More directly,
\[
\int_0^\infty
\frac{x^\alpha y^{T\alpha-1}}{(x+y)^{(T+1)\alpha}}\,dy
=
B(T\alpha,\alpha)
=
\frac{\Gamma(T\alpha)\Gamma(\alpha)}{\Gamma((T+1)\alpha)}.
\]
Multiplying by the leading constant gives \(1\). Hence \(q_J(\cdot\mid x)\) is a proper density.

Useful equivalent forms are as follows. Let
\[
r=\frac{y}{x+y},\qquad 1-r=\frac{x}{x+y}.
\]
Then
\[
q_J(y\mid x)
=
\frac{\Gamma((T+1)\alpha)}{\Gamma(\alpha)\Gamma(T\alpha)}
\frac{1}{x+y}
\left(\frac{x}{x+y}\right)^\alpha
\left(\frac{y}{x+y}\right)^{T\alpha-1}.
\]
Also, if \(R=Y/(x+Y)\) under the predictive law conditional on \(x\), then
\[
R\mid x\sim \mathrm{Beta}(T\alpha,\alpha),
\]
because
\[
q_J(y\mid x)\,dy
=
\frac{\Gamma((T+1)\alpha)}{\Gamma(T\alpha)\Gamma(\alpha)}
r^{T\alpha-1}(1-r)^{\alpha-1}\,dr.
\]
Equivalently, \(Z=Y/x\) has beta-prime density
\[
f_Z(z)
=
\frac{\Gamma((T+1)\alpha)}{\Gamma(T\alpha)\Gamma(\alpha)}
\frac{z^{T\alpha-1}}{(1+z)^{(T+1)\alpha}},
\qquad z>0,
\]
and
\[
q_J(y\mid x)=\frac1x f_Z(y/x).
\]

3. Solver Failure Output and Candidate Guidance

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
proof_location: Section 2, posterior computation  
claim_or_fact_used: Gamma likelihood for observed `x`  
source_status: provided definition / notation / assumption  
cited_label_or_name: Target theorem Gamma density definition  
exact_statement_used: \(p(x\mid\beta)=x^{\alpha-1}\beta^{-\alpha}\Gamma(\alpha)^{-1}e^{-x/\beta}\) for \(x>0\).  
hypotheses_or_conditions_needed: \(\alpha>0,\beta>0,x>0\).  
where_hypotheses_are_checked: Target theorem and observed sample space.  
strength_used: Exact density.  
notes: Same parametrization as target theorem.

claim_id: C2  
proof_location: Section 2, posterior computation  
claim_or_fact_used: Bayes posterior density with prior proportional to \(1/\beta\)  
source_status: standard background fact  
cited_label_or_name: Bayes formula for densities  
exact_statement_used: Posterior density is proportional to likelihood times prior, then normalized if the integral is finite.  
hypotheses_or_conditions_needed: Nonnegative likelihood-prior product with finite positive integral.  
where_hypotheses_are_checked: Normalizing integral computed as \(x^{-\alpha}\Gamma(\alpha)\in(0,\infty)\).  
strength_used: Density-level posterior formula.  
notes: No proper prior assumption needed once posterior is proper.

claim_id: C3  
proof_location: Section 2, posterior normalization  
claim_or_fact_used: Reciprocal-gamma integral  
source_status: proved inside the current proof  
cited_label_or_name: Substitution \(u=x/\beta\)  
exact_statement_used: \(\int_0^\infty \beta^{-\alpha-1}e^{-x/\beta}\,d\beta=x^{-\alpha}\Gamma(\alpha)\).  
hypotheses_or_conditions_needed: \(x>0,\alpha>0\).  
where_hypotheses_are_checked: Target theorem and observed sample space.  
strength_used: Exact normalization.  
notes: Follows by direct change of variables.

claim_id: C4  
proof_location: Section 2, predictive computation  
claim_or_fact_used: Conditional density of \(y\mid\beta\)  
source_status: provided definition / notation / assumption  
cited_label_or_name: Target theorem Gamma density definition  
exact_statement_used: \(p(y\mid\beta)=y^{T\alpha-1}\beta^{-T\alpha}\Gamma(T\alpha)^{-1}e^{-y/\beta}\).  
hypotheses_or_conditions_needed: \(T>0,\alpha>0,\beta>0,y>0\).  
where_hypotheses_are_checked: Target theorem and sample space.  
strength_used: Exact density.  
notes: Uses shape \(T\alpha\).

claim_id: C5  
proof_location: Section 2, predictive computation  
claim_or_fact_used: Bayesian predictive density formula  
source_status: standard background fact  
cited_label_or_name: Posterior predictive density formula  
exact_statement_used: \(q(y\mid x)=\int p(y\mid\beta)\pi(\beta\mid x)d\beta\).  
hypotheses_or_conditions_needed: Conditional independence of \(x,y\) given \(\beta\), posterior density proper.  
where_hypotheses_are_checked: Target theorem says independent observation/prediction under common \(\beta\); posterior propriety shown in C3.  
strength_used: Exact predictive mixture.  
notes: Standard Bayesian conditioning.

claim_id: C6  
proof_location: Section 2, predictive integral  
claim_or_fact_used: General reciprocal-gamma integral  
source_status: proved inside the current proof  
cited_label_or_name: Substitution \(u=(x+y)/\beta\)  
exact_statement_used: \(\int_0^\infty \beta^{-a-1}e^{-c/\beta}d\beta=\Gamma(a)c^{-a}\), for \(a,c>0\).  
hypotheses_or_conditions_needed: \(a=(T+1)\alpha>0\), \(c=x+y>0\).  
where_hypotheses_are_checked: \(\alpha,T,x,y>0\).  
strength_used: Exact integral value.  
notes: Applied with \(a=(T+1)\alpha\).

claim_id: C7  
proof_location: Section 2, normalization of \(q_J\)  
claim_or_fact_used: Beta integral identity  
source_status: standard background fact  
cited_label_or_name: Euler beta integral  
exact_statement_used: \(B(a,b)=\int_0^1 r^{a-1}(1-r)^{b-1}dr=\Gamma(a)\Gamma(b)/\Gamma(a+b)\), for \(a,b>0\).  
hypotheses_or_conditions_needed: \(a=T\alpha>0,b=\alpha>0\).  
where_hypotheses_are_checked: Target theorem has \(T>0,\alpha>0\).  
strength_used: Exact normalization integral.  
notes: Standard Gamma/Beta identity.

claim_id: C8  
proof_location: Section 2, ratio forms  
claim_or_fact_used: Change-of-variables density transformation  
source_status: standard background fact  
cited_label_or_name: One-dimensional density transformation formula  
exact_statement_used: If \(r=y/(x+y)\), then \(f_R(r)=q_J(xr/(1-r)\mid x)\,x/(1-r)^2\).  
hypotheses_or_conditions_needed: \(x>0\), smooth bijection \(y\in(0,\infty)\leftrightarrow r\in(0,1)\).  
where_hypotheses_are_checked: \(x>0\) and derivative computed explicitly.  
strength_used: Exact transformed density.  
notes: Gives \(R\mid x\sim\mathrm{Beta}(T\alpha,\alpha)\).

5. Interface Notes for S6

what this subproof establishes: The Jeffreys posterior is inverse-gamma with density \(\frac{x^\alpha}{\Gamma(\alpha)}\beta^{-\alpha-1}e^{-x/\beta}\), and the predictive density is the stated beta-prime form.

what remains conditional: Nothing within this assigned computational subclaim.

failure_output_type: solved

candidate guidance sentence, if any: None.

auxiliary lemma candidate, if any: None.

notation introduced: \(R=Y/(x+Y)\), \(Z=Y/x\), and \(A=(T+1)\alpha\) implicitly in computations.

risk points: Later solvers should track the Gamma parametrization carefully: \(\beta\) is a scale parameter, while \(1/\beta\mid x\) has Gamma rate \(x\). The ratio \(Y/(x+Y)\mid x\) is \(\mathrm{Beta}(T\alpha,\alpha)\), with the order of parameters depending on numerator \(Y\).

6. Web-Source Confirmation

no web sources used