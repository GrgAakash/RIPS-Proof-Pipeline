# Composer A gold Verifier A evidence report

## 1. Gold step status

1. ALL-ACCEPTED: Definitions of \(\mathcal F_n=\{f:[n]\to[n]\}\) and \(A_n=\{f\in\mathcal F_n:G_f\text{ has a unique cyclic vertex}\}\). Reports: A1 step 1, A2 step 1, A3 step 1.

2. ALL-ACCEPTED: The map \(f\mapsto(f(1),\ldots,f(n))\) is a bijection from \(\mathcal F_n\) to \([n]^n\). Reports: A1 step 2, A2 step 2, A3 step 2.

3. ALL-ACCEPTED: \(|\mathcal F_n|=n^n\). Reports: A1 step 3, A2 step 3, A3 step 3.

4. ALL-ACCEPTED: \(\Pr(A_n)=|A_n|/n^n\). Reports: A1 step 4, A2 step 4, A3 step 4.

5. ALL-ACCEPTED: Every forward orbit eventually repeats and enters a directed cycle. Reports: A1 step 5, A2 steps 5-6, A3 step 5.

6. ALL-ACCEPTED: If \(G_f\) has unique cyclic vertex \(r\), then \(f(r)=r\). Reports: A1 step 6, A2 step 7, A3 step 6.

7. ALL-ACCEPTED: If \(G_f\) has unique cyclic vertex \(r\), then every vertex reaches \(r\). Reports: A1 step 6, A2 step 8, A3 step 7.

8. ALL-ACCEPTED: For fixed \(r\), the class \(\mathcal A_{n,r}\) is defined as the functions for which \(r\) is the unique cyclic vertex. Reports: A2 step 9; A1 and A3 use this class in their fixed-root count ledgers without raising any concern.

9. ALL-ACCEPTED: For \(n=1\), the fixed-root count is \(|\mathcal A_{1,1}|=1\). Reports: A1 step 7, A2 step 10, A3 step 8.

10. ALL-ACCEPTED: For \(n\ge2\), the leaf-removal encoding \(\Phi:\mathcal A_{n,r}\to[n]^{n-2}\) is defined by repeatedly removing the least non-root \(R_k\)-leaf and recording \(w_k=f(a_k)\). Reports: A1 step 8, A2 step 11, A3 step 9.

11. ALL-ACCEPTED: A non-root \(R_k\)-leaf exists at each encoding step. Reports: A1 step 9, A2 step 12, A3 step 9.

12. ALL-ACCEPTED: Deleting the chosen encoding leaf preserves closure under \(f\) and reachability to \(r\). Reports: A1 step 10, A2 step 13, A3 step 10.

13. ALL-ACCEPTED: After \(n-2\) removals, the final non-root vertex \(b\) satisfies \(f(b)=r\). Reports: A1 step 10, A2 step 14, A3 step 11.

14. ALL-ACCEPTED: The decoding algorithm can choose the least non-root remaining element absent from the suffix \(w_k,\ldots,w_{n-2}\). Reports: A1 step 11, A2 step 15, A3 step 12.

15. ALL-ACCEPTED: The decoding assignment \(f(a_k)=w_k\) is legitimate. Reports: A1 step 12, A2 step 16, A3 step 13.

16. ALL-ACCEPTED: The decoded function lies in \(\mathcal A_{n,r}\). Reports: A1 step 13, A2 step 17, A3 step 14.

17. ALL-ACCEPTED: For an encoded valid function, a non-root remaining vertex is an \(R_k\)-leaf iff it is absent from the remaining suffix. Reports: A1 step 14, A2 step 18, A3 step 15.

18. ALL-ACCEPTED: \(\Psi(\Phi(f))=f\) for every \(f\in\mathcal A_{n,r}\). Reports: A1 step 15, A2 step 19, A3 step 16.

19. ALL-ACCEPTED: \(\Phi(\Psi(w))=w\) for every \(w\in[n]^{n-2}\). Reports: A1 step 16, A2 step 20, A3 step 17.

20. ALL-ACCEPTED: \(\Phi\) is a bijection and \(|\mathcal A_{n,r}|=n^{n-2}\) for \(n\ge2\). Reports: A1 step 17, A2 step 21, A3 step 18.

21. ALL-ACCEPTED: \(A_n=\bigsqcup_{r\in[n]}A_{n,r}\). Reports: A1 step 18, A2 step 22, A3 step 19.

22. ALL-ACCEPTED: \(|A_n|=n^{n-1}\) for every positive integer \(n\). Reports: A1 step 19, A2 step 23, A3 step 20.

23. ALL-ACCEPTED: \(\Pr(A_n)=1/n\). Reports: A1 step 20, A2 step 24, A3 step 21.

No CHALLENGED steps.

No UNALIGNED steps.

## 2. Gold unfilled gaps (union)

Empty list.

## 3. Gold disallowed premises (union)

Empty list.

## 4. Gold scope check

full

## 5. Gold coupling inventory

Allowed formal skeleton statements used beyond definitions/notation/assumptions: 0; none.

Disallowed skeleton statements cited: 0; none.

Standard-background-heavy? NO.

## 6. Disagreement map

Step/gap disagreement: none. All three reports marked all addressed proof steps justified and listed no unfilled gaps.

Fillability disagreement: none. No report raised a gap, so no fillability disagreement appears.

Disallowed-premise disagreement: none. All three reports listed no disallowed premises.

Scope disagreement: none. All three reports said the full target statement was established for every positive integer \(n\), with \(n=1\) and \(n\ge2\) covered.

Coupling-count disagreement: none for the required coupling inventory categories. All three reports listed 0 allowed formal skeleton statements used beyond definitions/notation/assumptions, 0 disallowed skeleton statements cited, and Standard-background-heavy? NO. A non-verdict inventory difference appears only in definitions/notation/assumptions counted from the cleaned skeleton: A1 counted 6, A2 counted 7, and A3 counted 6.

Same controller verdict across reports: all agree. Each run's report, on its own, would imply the same controller verdict: no non-fillable gaps, no fillable-only gaps, no disallowed premises, no omitted case or weaker statement, no web-source issue, and candidate guidance seed None.

## 7. Web-source roll-up

Empty list.

## 8. Gold Verifier A evidence report for the Decision Controller

Non-fillable gaps present? NO

Fillable-only gaps present? NO

Disallowed premises present? NO

Omitted case / weaker statement present? NO

Allowed formal skeleton statements used beyond definitions: 0 + []

Disallowed skeleton statements cited: 0 + []

Standard-background-heavy? NO

Web-source issue? NO

Same issue recurring across reports? NO

Candidate guidance seed, if any: None
