# 1. Source Ledger present?

YES. The controller-facing Citation Generator Source Ledger appears after the submitted standalone LaTeX proof under the heading "Citation Generator Source Ledger", with entries CG-SL1 through CG-SL23.

# 2. Source inventory

## provided definitions / notation / assumptions

- CG-SL1: Notation \([n]\), the standing assumption that \(n\) is positive, the function space \(\mathcal F_n\), the associated directed graph \(G_f\), and the definition of cyclic vertex. Used in the final proof opening paragraph and Steps 1, 2, and 4.

## allowed supporting statements

- CG-SL4: Uniform finite probability convention: a uniform random function is chosen uniformly from the finite function set, so event probability is favorable count divided by sample-space count. Used in final proof Steps 1 and 5.

## additional mathematical guidance items

- None. The packet states that no additional mathematical guidance is supplied.

## standard background facts

- CG-SL3: Elementary multiplication principle for the tuple count \(|[n]^n|=n^n\). Used in final proof Step 1.
- CG-SL5: Finite pigeonhole principle. Used in final proof Step 2 to obtain a repeated iterate.
- CG-SL19: Elementary finite word count: there are \(n^{n-2}\) words of length \(n-2\) over \([n]\). Used in final proof Step 3.
- CG-SL21: Finite disjoint-union counting. Used in final proof Step 4.
- CG-SL23: Elementary exponent arithmetic and cancellation, including \(n^{n-1}/n^n=1/n\). Used in final proof Step 5.

## proved inside the current proof

- CG-SL2: Tuple encoding \(f\mapsto(f(1),\ldots,f(n))\) is a bijection from \(\mathcal F_n\) to \([n]^n\). Used in final proof Step 1.
- CG-SL6: First-repetition cycle construction in a finite forward orbit. Used in final proof Step 2.
- CG-SL7: Unique-cyclic-vertex structure: the unique cyclic vertex \(r\) is fixed, and every vertex reaches \(r\). Used in final proof Step 2 and then in Step 3.
- CG-SL8: The \(n=1\) fixed-root case. Used in final proof Step 3 and Step 4.
- CG-SL9: Internal fixed-root encoding construction. Used in final proof Step 3.
- CG-SL10: Existence of a non-root \(R_k\)-leaf at each encoding step. Used in final proof Step 3.
- CG-SL11: Deleting the selected leaf preserves closure and reachability. Used in final proof Step 3.
- CG-SL12: Two-vertex terminal step \(f(b)=r\). Used in final proof Step 3.
- CG-SL13: Suffix length count for the decoding choice. Used in final proof Step 3.
- CG-SL14: Parent-remains check for the decoding assignment. Used in final proof Step 3.
- CG-SL15: The decoded function belongs to \(\mathcal A_{n,r}\). Used in final proof Step 3.
- CG-SL16: Leaf-suffix equivalence for an encoded valid function. Used in final proof Step 3.
- CG-SL17: Decoded least-leaf property. Used in final proof Step 3.
- CG-SL18: \(\Phi\) and \(\Psi\) are mutual inverses, giving the fixed-root bijection. Used in final proof Step 3.
- CG-SL20: \(A_n\) is the pairwise disjoint union of the fixed-root events \(A_{n,r}\). Used in final proof Step 4.
- CG-SL22: Assembly of the total favorable count \(|A_n|=n^{n-1}\), with \(n=1\) handled separately. Used in final proof Step 4 and Step 5.

## external cited sources

- None.

## unsupported or unclear sources

- None.

# 3. Source accuracy check

| Ledger entry | Mark | Check |
|---|---|---|
| CG-SL1 | ACCURATE | The definitions and notation appear in the supplied packet and allowed support list, and the proof uses them only as definitions. |
| CG-SL2 | ACCURATE | The tuple-encoding bijection is proved directly in Step 1. |
| CG-SL3 | ACCURATE | The multiplication principle is genuinely elementary finite-set counting and is used only for \(|[n]^n|=n^n\). |
| CG-SL4 | ACCURATE | The uniform finite probability convention is explicitly supplied and is used at the stated strength. |
| CG-SL5 | ACCURATE | The finite pigeonhole principle is standard elementary finite-set reasoning and the hypotheses are visible. |
| CG-SL6 | ACCURATE | The first-repetition cycle construction is proved in Step 2 from the directed-edge definition. |
| CG-SL7 | ACCURATE | The fixedness of \(r\) and reachability of \(r\) are proved in Step 2 under the unique-cyclic-vertex hypothesis. |
| CG-SL8 | ACCURATE | The one-point fixed-root case is proved directly in Step 3. |
| CG-SL9 | ACCURATE | The encoding construction is introduced internally, and its needed well-definedness is accounted for in CG-SL10 and CG-SL11. |
| CG-SL10 | ACCURATE | The non-root leaf existence argument is supplied in Step 3 using finite predecessor iteration and reachability to \(r\). |
| CG-SL11 | ACCURATE | Closure and reachability after leaf deletion are proved in Step 3 and are not imported. |
| CG-SL12 | ACCURATE | The terminal fact \(f(b)=r\) is proved from closure, \(f(r)=r\), and reachability. |
| CG-SL13 | ACCURATE | The suffix-length existence argument is elementary finite counting and is stated in the decoding construction. |
| CG-SL14 | ACCURATE | The proof checks both \(w_k\ne a_k\) and that \(w_k\) has not been removed earlier. |
| CG-SL15 | ACCURATE | The decoded function is shown to have only the loop at \(r\) by the increasing-index argument. |
| CG-SL16 | ACCURATE | The leaf-suffix equivalence is proved in the \(\Psi(\Phi(f))=f\) argument. |
| CG-SL17 | ACCURATE | The decoded least-leaf property is proved in the \(\Phi(\Psi(w))=w\) argument. |
| CG-SL18 | ACCURATE | The mutual-inverse conclusion follows from the two inverse checks in Step 3. |
| CG-SL19 | ACCURATE | The finite word count is elementary multiplication and is used only after the bijection is established. |
| CG-SL20 | ACCURATE | The disjoint-union decomposition is proved directly from uniqueness and the definitions of \(A_n\) and \(A_{n,r}\). |
| CG-SL21 | ACCURATE | Finite disjoint-union counting is standard background and its hypotheses are checked by Step 4. |
| CG-SL22 | ACCURATE | The total favorable count is assembled inside Step 4 from the proved fixed-root count and disjoint union. |
| CG-SL23 | ACCURATE | The exponent arithmetic and cancellation are elementary and require only \(n>0\), which is a standing assumption. |

No Source Ledger entry is overstrengthened, misquoted, assigned the wrong source status, missing a visible hypothesis check, not found, or unclear.

# 4. Missing source entries

None. The ledger accounts for the load-bearing definitions, finite-probability conversion, finite-set background facts, orbit-structure facts, fixed-root encoding/decoding proof, disjoint-union assembly, and final arithmetic. The ordinary least-element choices in finite subsets are covered within the encoding and decoding well-definedness entries and do not require an external source.

# 5. Disallowed source check

None. The proof does not cite or use the target theorem, an equivalent imported theorem, Cayley's formula, the excluded rooted-tree correspondence, the excluded height-distribution statement, or any external source. The fixed-root count is target-level load-bearing material, but it is proved inside the current proof rather than imported as a source.

# 6. Internet/source-check report

Internet used? NO

Sources checked:
None.

URLs or references checked:
None.

Any source inaccessible? NO

Possible target-source leakage encountered? NO

# 7. Controller-facing summary

Citation gate result: GOOD_TO_GO

Source Ledger present? YES

Missing source entries present? NO

Disallowed sources present? NO

Overstrengthened or misquoted sources present? NO

Suspicious standard-background claims present? NO

External source issue present? NO

Citation-only repair needed? NO

Substantive source issue present? NO

Candidate guidance seed, if any: None
