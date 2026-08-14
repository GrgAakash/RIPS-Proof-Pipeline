1. Assignment restatement

S-ID: S5

assigned subclaim(s): SC5 and SC6

what must be proved: Track equality cases through the preceding normalization, area decomposition, and sharp quadratic inequality; prove equality in the target inequality forces equal turning angles and equal side lengths, hence a regular \(2n\)-gon; verify directly that a regular \(2n\)-gon attains equality.

declared prerequisite subclaims: SC1, SC2, SC3, SC4, including the exact quadratic forms from SC3 and the exact equality conditions in the sharp inequality proof from SC4.

2. Subproof or failure

SUBPROBLEM UNSOLVED.

The missing obstacle is the exact equality analysis of SC4. The supplied packet gives no actual SC3 quadratic forms and no proof of SC4, so there is no legitimate way to track equality through Cauchy/Jensen/spectral steps or determine whether equality forces the antisymmetric paired-edge variables to vanish.

However, the converse regular-polygon verification can be checked directly.

Let \(\mathcal P\) be a regular \(2n\)-gon with side length \(a>0\). Its exterior turning angle is
\[
\theta=\frac{2\pi}{2n}=\frac{\pi}{n}.
\]
The hypothesis \(\langle e_i,e_{i+1}\rangle>0\) is equivalent to \(\cos\theta>0\), hence requires
\[
\frac{\pi}{n}<\frac{\pi}{2},
\]
so the regular \(2n\)-gon satisfies the strict dot-product hypothesis exactly when \(n>2\). For \(n=2\), a regular \(4\)-gon has adjacent edges perpendicular, so \(\langle e_i,e_{i+1}\rangle=0\), and it does not satisfy the stated strict hypothesis.

For a regular \(2n\)-gon, opposite vertices satisfy
\[
P_{i+n}=-P_i
\]
after placing the center at the origin. Therefore
\[
W_i=\frac{P_i+P_{i+n}}2=0
\]
for every \(i\), so the Wigner caustic degenerates to the single point \(0\), and
\[
A^\ast(\mathrm E_{0.5}(\mathcal P))=0.
\]

The area of a regular \(m\)-gon with side length \(a\) is
\[
A=\frac{m a^2}{4\tan(\pi/m)}.
\]
With \(m=2n\), this gives
\[
A(\mathcal P)=\frac{2n\,a^2}{4\tan(\pi/(2n))}
=\frac{n a^2}{2\tan(\pi/(2n))}.
\]
The perimeter is
\[
L(\mathcal P)=2n a,
\]
so
\[
L(\mathcal P)^2=4n^2a^2.
\]
On the other hand,
\[
8n\tan\left(\frac{\pi}{2n}\right)A(\mathcal P)
=
8n\tan\left(\frac{\pi}{2n}\right)
\frac{n a^2}{2\tan(\pi/(2n))}
=
4n^2a^2.
\]
Since \(A^\ast=0\), this is exactly
\[
L(\mathcal P)^2
=
8n\tan\left(\frac{\pi}{2n}\right)
\left(A(\mathcal P)+2|A^\ast(\mathrm E_{0.5}(\mathcal P))|\right).
\]

Thus, for \(n>2\), the regular \(2n\)-gon satisfies the hypotheses and attains equality. For \(n=2\), the stated equality case is incompatible with the strict condition \(\langle e_i,e_{i+1}\rangle>0\).

3. Solver failure output and candidate guidance

```yaml
failure_output_type: branch lemma target
type: unresolved key lemma
failed_route: "Attempted to track equality through S1-S4, but the exact SC3 quadratic forms and SC4 equality conditions are not provided in the packet."
obstruction: "The S5 equality-forcing direction depends on equality conditions inside SC4. Without the actual sharp quadratic inequality proof, one cannot know which intermediate inequalities must be sharp or whether equality forces vanishing antisymmetric paired-edge variables."
evidence: "The prompt supplies only the target theorem and an S0 blueprint. The blueprint says SC4 must prove a sharp quadratic inequality and SC5 must track equality, but it does not provide the algebraic inequality, the quadratic forms, or the equality cases from the proof."
reuse_value: "A standalone equality-case lemma for the SC4 quadratic estimate would allow S5 to complete the equality-forcing direction without reconstructing all of SC4."
guidance_sentence: null
candidate_lemma_statement: "Let the paired-edge variables and turning angles be those arising from SC1-SC3, and let Q_+ and Q_- be the two quadratic forms representing A(P)+2A^*(E_{0.5}(P)) and A(P)-2A^*(E_{0.5}(P). If the sharp inequalities 8n tan(pi/(2n)) Q_+ <= L(P)^2 or 8n tan(pi/(2n)) Q_- <= L(P)^2 hold with equality, then all turning angles are equal to pi/n, all paired symmetric edge variables are equal, and all antisymmetric paired-edge variables vanish."
why_unblocks: "This is precisely the missing equality propagation needed to prove that equality in the target inequality forces the original polygon to have equal exterior angles and equal side lengths."
where_used: "S5 equality-forcing direction after reducing A+2|A^*| to the larger of the two SC3 quadratic forms."
allowed_inputs: "Definitions and assumptions from the target theorem; SC1 normalization; SC3 exact quadratic-form representations; the internally proved SC4 sharp quadratic inequalities."
dependencies: "Requires the exact SC3 formulas and the full SC4 proof or at least its equality cases."
weaker_than_target: true
equivalent_or_stronger: false
recommended: true
```

4. Local Source Ledger

claim_id: C1  
proof_location: Section 2, regular-polygon verification  
claim_or_fact_used: Exterior turning angle of a regular \(m\)-gon  
source_status: standard background fact  
cited_label_or_name: regular polygon exterior-angle formula  
exact_statement_used: A regular \(m\)-gon has exterior turning angle \(2\pi/m\).  
hypotheses_or_conditions_needed: The polygon is regular with \(m=2n\) sides.  
where_hypotheses_are_checked: Section 2 begins with a regular \(2n\)-gon.  
strength_used: Used with \(m=2n\), giving \(\theta=\pi/n\).  
notes: This is elementary Euclidean geometry.

claim_id: C2  
proof_location: Section 2, dot-product check  
claim_or_fact_used: Dot product of adjacent side vectors by turning angle  
source_status: standard background fact  
cited_label_or_name: dot product angle formula  
exact_statement_used: If two nonzero vectors have angle \(\theta\), then \(\langle u,v\rangle=|u||v|\cos\theta\).  
hypotheses_or_conditions_needed: Adjacent side vectors of the regular polygon have angle \(\theta=\pi/n\).  
where_hypotheses_are_checked: Section 2 after C1.  
strength_used: Determines \(\langle e_i,e_{i+1}\rangle>0\iff \cos(\pi/n)>0\iff n>2\).  
notes: Important risk point: the stated theorem’s equality case fails the strict hypothesis when \(n=2\).

claim_id: C3  
proof_location: Section 2, Wigner caustic degeneracy  
claim_or_fact_used: Opposite vertices of a centered regular \(2n\)-gon are negatives  
source_status: standard background fact  
cited_label_or_name: central symmetry of regular even-gon  
exact_statement_used: A regular polygon with an even number of vertices is centrally symmetric; after placing its center at the origin, \(P_{i+n}=-P_i\).  
hypotheses_or_conditions_needed: \(\mathcal P\) is a regular \(2n\)-gon.  
where_hypotheses_are_checked: Section 2.  
strength_used: Gives \(W_i=0\) for all \(i\).  
notes: Translation does not affect \(W_i\)-edge degeneracy or oriented area.

claim_id: C4  
proof_location: Section 2, Wigner area calculation  
claim_or_fact_used: Oriented area definition from target theorem  
source_status: provided definition / notation / assumption  
cited_label_or_name: definition of \(A^\ast(\mathrm E_{0.5}(\mathcal P))\)  
exact_statement_used: \(A^\ast=\frac12\sum_{i=1}^{2n}\det(W_i,W_{i+1})\).  
hypotheses_or_conditions_needed: Wigner vertices \(W_i\) are defined by \(W_i=(P_i+P_{i+n})/2\).  
where_hypotheses_are_checked: Target theorem statement and Section 2.  
strength_used: Since all \(W_i=0\), every determinant vanishes and \(A^\ast=0\).  
notes: No external Wigner-caustic facts used.

claim_id: C5  
proof_location: Section 2, regular polygon area  
claim_or_fact_used: Area formula for a regular polygon  
source_status: standard background fact  
cited_label_or_name: regular polygon area formula  
exact_statement_used: A regular \(m\)-gon with side length \(a\) has area \(m a^2/(4\tan(\pi/m))\).  
hypotheses_or_conditions_needed: The polygon is regular with \(m\) sides and side length \(a\).  
where_hypotheses_are_checked: Section 2.  
strength_used: Applied with \(m=2n\).  
notes: Derivable by decomposing into \(m\) congruent isosceles triangles.

claim_id: C6  
proof_location: Section 2, perimeter calculation  
claim_or_fact_used: Perimeter of an equilateral \(2n\)-gon  
source_status: standard background fact  
cited_label_or_name: perimeter definition  
exact_statement_used: If a polygon has \(2n\) sides each of length \(a\), then \(L=2na\).  
hypotheses_or_conditions_needed: The polygon is regular with side length \(a\).  
where_hypotheses_are_checked: Section 2.  
strength_used: Used to compute \(L^2=4n^2a^2\).  
notes: Direct from definition of perimeter.

claim_id: C7  
proof_location: Section 2, equality-forcing failure  
claim_or_fact_used: Need for SC4 equality conditions  
source_status: unsupported or unclear  
cited_label_or_name: SC4 equality analysis  
exact_statement_used: Equality in the relevant SC4 sharp quadratic inequality forces equal turning angles, equal symmetric paired variables, and zero antisymmetric paired variables.  
hypotheses_or_conditions_needed: Exact SC3 quadratic forms and SC4 proof.  
where_hypotheses_are_checked: Not available in the prompt.  
strength_used: Would be necessary to prove equality implies regularity.  
notes: This is the unresolved obstacle.

5. Interface notes for S6

what this subproof establishes: It verifies directly that a regular \(2n\)-gon has \(A^\ast=0\) and satisfies the equality formula, provided \(n>2\) so that the strict adjacent dot-product hypothesis holds.

what remains conditional: The forward equality implication remains conditional on exact SC3 formulas and SC4 equality conditions. In particular, S5 cannot prove from the supplied packet that equality forces equal turning angles, equal side lengths, and zero antisymmetric component.

failure_output_type: branch lemma target

candidate guidance sentence, if any: Prove a standalone equality-case version of the SC4 sharp quadratic estimate, including vanishing of the antisymmetric paired-edge variables.

auxiliary lemma candidate, if any: The candidate lemma is stated in the YAML block in Section 3.

notation introduced: Side length \(a\); regular polygon exterior angle \(\theta=\pi/n\).

risk points: The theorem’s equality statement appears incompatible with the strict condition \(\langle e_i,e_{i+1}\rangle>0\) when \(n=2\), since a regular quadrilateral has adjacent edges perpendicular.

6. Web-source confirmation

no web sources used