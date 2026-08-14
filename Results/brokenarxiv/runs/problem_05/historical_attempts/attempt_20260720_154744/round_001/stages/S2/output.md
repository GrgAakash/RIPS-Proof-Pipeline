1. Assignment restatement

S-ID: S2

assigned subclaim(s): C2, plus the explicit interface fact that each filling core intersects the capped surface exactly once.

what must be proved: After Dehn filling each boundary torus `T_i` along the slope `r_i` of `∂P ∩ T_i`, the surface `P` caps off by meridian disks to an embedded sphere `\widehat P`; moreover, the core of each attached filling solid torus intersects `\widehat P` exactly once.

declared prerequisite subclaims: The boundary slope `r_i` of `∂P ∩ T_i` is defined for each `i`, and Dehn filling is performed along these slopes. No use is made of the contradiction assumption `p_i >= 2`.

2. Subproof or failure

Let `T_i = ∂N(L_i)` for `i = 1, ..., N`. Since `P` is a spanning planar surface, `P` has exactly one boundary component on each `T_i`. Denote this boundary component by `γ_i = ∂P ∩ T_i`, and let its slope be `r_i`.

Perform Dehn filling of `X_L` along the slopes `r_i`. Thus for each `i`, attach a solid torus `V_i` to `T_i` so that the meridian slope of `V_i` is identified with `r_i` on `T_i`. Equivalently, a meridian disk `D_i ⊂ V_i` has boundary `∂D_i = γ_i` after the gluing.

Because the tori `T_i` are distinct boundary components, the attached solid tori `V_i` are pairwise disjoint. Choose one meridian disk `D_i` in each `V_i` with boundary `γ_i`. Each `D_i` lies in the interior of its filling solid torus except along its boundary, and `D_i ∩ X_L = γ_i`. Therefore

```text
\widehat P = P ∪ D_1 ∪ ... ∪ D_N
```

is an embedded closed surface in the filled manifold.

Topologically, `P` is planar and has exactly `N` boundary components. Capping all `N` boundary components by disks produces a closed connected genus-zero surface. Hence `\widehat P` is homeomorphic to `S^2`.

It remains to check the core-intersection statement. Let `c_i` be the core curve of the filling solid torus `V_i`. In a solid torus, the core intersects any meridian disk transversely in exactly one point after the usual choice of transverse core and meridian disk. Since `\widehat P ∩ V_i = D_i`, the curve `c_i` intersects `\widehat P` exactly in the single point `c_i ∩ D_i`. For `j ≠ i`, `c_i` is contained in `V_i` and hence is disjoint from `D_j ⊂ V_j`; also `c_i` is disjoint from `P ⊂ X_L` except possibly at the boundary before gluing, but after choosing `c_i` in the interior of `V_i`, it is disjoint from `X_L`. Thus each filling core intersects `\widehat P` exactly once.

3. Solver failure output and candidate guidance

```yaml
status: solved
s_id: S2
proved_claims:
  - Dehn filling X_L along the boundary slopes r_i caps P by meridian disks to an embedded closed surface \widehat P.
  - The capped surface \widehat P is a sphere.
  - Each filling solid-torus core intersects \widehat P exactly once.
declared_prerequisites:
  - Each component of boundary P on T_i has slope r_i, and the filling on T_i is along r_i.
conditional_on: []
failure_output_type: null
candidate_guidance: null
```

4. Local Source Ledger

- claim_id: S2-1  
  proof_location: Section 2, paragraphs 1-2  
  claim_or_fact_used: Dehn filling along slope `r_i` attaches a solid torus whose meridian disk has boundary slope `r_i`.  
  source_status: standard background  
  cited_label_or_name: Definition of Dehn filling along a slope  
  exact_statement_used: If a torus boundary component is filled along slope `r`, the attached solid torus has meridian curve identified with slope `r`.  
  hypotheses_or_conditions_needed: `r_i` is a slope on `T_i`; filling is performed along `r_i`.  
  where_hypotheses_are_checked: `r_i` is the slope of `∂P ∩ T_i` by the problem setup.  
  strength_used: Existence of a meridian disk `D_i` with boundary equal to the capped boundary curve.  
  notes: No hyperbolicity assumption is used here.

- claim_id: S2-2  
  proof_location: Section 2, paragraphs 2-3  
  claim_or_fact_used: The union of an embedded surface with disjoint capping disks in attached solid tori is embedded.  
  source_status: standard background  
  cited_label_or_name: Elementary topology of gluing manifolds along boundary  
  exact_statement_used: If disks are attached along distinct boundary components of an embedded surface and otherwise lie in disjoint attached manifolds, the resulting closed surface is embedded.  
  hypotheses_or_conditions_needed: One boundary component of `P` lies on each distinct `T_i`; the attached solid tori are pairwise disjoint.  
  where_hypotheses_are_checked: `P` is spanning with exactly one boundary component on each boundary torus.  
  strength_used: Embeddedness of `\widehat P`.  
  notes: The disks are chosen one per filling solid torus.

- claim_id: S2-3  
  proof_location: Section 2, paragraph 4  
  claim_or_fact_used: Capping a connected planar surface along all boundary components gives `S^2`.  
  source_status: standard background  
  cited_label_or_name: Classification of compact connected surfaces  
  exact_statement_used: A compact connected genus-zero surface with all boundary components capped by disks becomes a closed connected genus-zero surface, hence is homeomorphic to `S^2`.  
  hypotheses_or_conditions_needed: `P` is planar and has exactly `N` boundary components.  
  where_hypotheses_are_checked: This is part of the target theorem’s definition of incompressible spanning planar surface.  
  strength_used: Identification of `\widehat P` as a sphere.  
  notes: Uses the standard convention that “surface” here is connected.

- claim_id: S2-4  
  proof_location: Section 2, paragraph 5  
  claim_or_fact_used: The core of a solid torus intersects a meridian disk exactly once.  
  source_status: standard background  
  cited_label_or_name: Standard model of a solid torus  
  exact_statement_used: In `D^2 × S^1`, the core `{0} × S^1` intersects a meridian disk `D^2 × {pt}` transversely in one point.  
  hypotheses_or_conditions_needed: `D_i` is a meridian disk of `V_i`; `c_i` is the core of `V_i`.  
  where_hypotheses_are_checked: By construction of the filling solid torus and choice of `D_i`.  
  strength_used: Exact one-point geometric intersection.  
  notes: This gives one intersection with `\widehat P` because `\widehat P ∩ V_i = D_i`.

5. Interface notes for S6

what this subproof establishes: Full Dehn filling along the boundary slopes of `P` produces an embedded sphere `\widehat P`, and every filling core intersects `\widehat P` exactly once.

what remains conditional: Essentiality of `\widehat P` is not proved here. Any later use of reducibility must separately prove that `\widehat P` does not bound a ball.

failure_output_type: null

candidate guidance sentence, if any: null

auxiliary lemma candidate, if any: If a compact connected planar surface with one boundary component on each filled torus is capped by meridian disks under filling along those boundary slopes, the result is an embedded sphere meeting each filling core exactly once.

notation introduced: `γ_i = ∂P ∩ T_i`; `V_i` for the filling solid torus; `D_i` for the meridian capping disk; `c_i` for the filling core; `\widehat P = P ∪_i D_i`.

risk points: The proof uses the standard convention that “planar surface” means connected genus-zero surface. If disconnected planar surfaces were allowed, the conclusion “a sphere” would need adjustment.

6. Web-source confirmation

no web sources used