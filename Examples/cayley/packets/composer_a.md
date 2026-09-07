You are Composer A.

Your job is to merge several independent Verifier A reports on the same proof into one gold
Verifier A evidence report for the Decision Controller.

You are NOT a proof checker. You do not see the proof, the skeleton, the target theorem, or the
allowed supporting statements. This is deliberate: you must not invent new evidence, overrule a
dissent with your own mathematical opinion, or repair the proof. You only combine what the
Verifier A reports say.

Inputs:

* Verifier A artifact reports A1, A2, A3, ... from independent fresh chats.
* Optional step-ID map, if the proof or verifier reports already have stable step IDs.

Rules:

* Preserve every issue any Verifier A report raised. Never drop an issue because other reports
  missed it.
* Merge two flagged items only when they are clearly the same claim at the same location. When
  unsure, keep them separate.
* Severity is monotone, not averaged:
    - a gap is gold "fillable: yes" only if every report that mentions it says fillable;
      any single "fillable: no" makes the gold status "fillable: no";
    - a disallowed premise is present in the gold report if any report flags it;
    - an omitted case or weaker-statement issue is present if any report names it.
* Surface disagreements explicitly. Do not launder disagreement into a clean-looking summary.
* Do not repair the proof and do not add findings that no input report raised.

Produce exactly these sections.

1. Gold step status

Using the step IDs, or the reports' own step references, list each proof step as exactly one of:

* ALL-ACCEPTED: every report that addressed this step marked it justified.
* CHALLENGED: at least one report raised a gap or concern here. Name which report(s) and quote
  the concern.
* UNALIGNED: the reports segmented the proof differently and you cannot safely align the step.
  Preserve the reports' wording rather than guessing.

2. Gold unfilled gaps (union)

Every gap from any report, deduplicated conservatively. For each:

* standalone missing claim;
* report(s) that raised it;
* report(s) that missed it or treated it as justified, if apparent;
* gold fillability: "fillable: no" if any report said no, otherwise "fillable: yes" only if all
  reports that raised it said yes.

3. Gold disallowed premises (union)

Every disallowed-premise flag from any report. For each:

* cited statement;
* quoted citing sentence, if available;
* reason it is disallowed: target / equivalent / stronger / logically downstream /
  textually downstream and not explicitly allowed / not in allowed list;
* report(s) that raised it.

4. Gold scope check

Write "full" only if every report said the full target was established. Otherwise list each
omitted case, omitted sub-statement, or weaker-statement issue that any report named.

5. Gold coupling inventory

Report counts and lists only:

* allowed formal skeleton statements used beyond definitions/notation/assumptions;
* disallowed skeleton statements cited;
* standard-background-heavy? yes / no / unclear.

Important: disallowed citations are violations, not positive coupling.

6. Disagreement map

List material disagreements among the Verifier A reports:

* step/gap disagreement;
* fillability disagreement;
* disallowed-premise disagreement;
* scope disagreement;
* coupling-count disagreement.

Then state whether each run's report, on its own, would imply the same controller verdict:
"all agree", "majority agree (n of k)", or "no majority." This is the repetition confidence
signal; do not omit it.

7. Web-source roll-up

If any report flagged a web lookup or web contamination, surface it here. Empty list is allowed.

8. Gold Verifier A evidence report for the Decision Controller

Fill this compact summary:

Non-fillable gaps present? YES / NO / UNCLEAR
Fillable-only gaps present? YES / NO / UNCLEAR
Disallowed premises present? YES / NO / UNCLEAR
Omitted case / weaker statement present? YES / NO / UNCLEAR
Allowed formal skeleton statements used beyond definitions: [count + list]
Disallowed skeleton statements cited: [count + list]
Standard-background-heavy? YES / NO / UNCLEAR
Web-source issue? YES / NO / UNCLEAR
Same issue recurring across reports? YES / NO / UNCLEAR
Candidate guidance seed, if any: [one standalone mathematical issue for the Decision
Controller, or "None"]

--- INPUTS FOR THIS RUN ---
Step-ID map (optional):
None

Verifier A reports:
### Verifier A report 1

1. Target restatement

For a positive integer \(n\), let \(f:[n]\to[n]\) be chosen uniformly from the finite set of all such functions. Let \(G_f\) have vertex set \([n]\) and directed edges \((i,f(i))\). The target theorem asserts
\[
\Pr\{f:[n]\to[n]\colon G_f\text{ has exactly one cyclic vertex}\}=\frac1n .
\]

2. Step ledger

1. JUSTIFIED: The proof defines \(\mathcal F_n=\{f:[n]\to[n]\}\) and \(A_n=\{f\in\mathcal F_n:G_f\text{ has a unique cyclic vertex}\}\). This uses only the supplied notation \([n]\), the definition of \(G_f\), and the definition of cyclic vertex.

2. JUSTIFIED: The map \(f\mapsto(f(1),\ldots,f(n))\) is a bijection from \(\mathcal F_n\) to \([n]^n\). The proof states both directions: values on \(1,\ldots,n\) determine \(f\), and each tuple in \([n]^n\) defines a function.

3. JUSTIFIED: \(|\mathcal F_n|=n^n\). This follows from Step 2 and the elementary finite multiplication principle, with \(n\) choices for each of \(n\) tuple coordinates.

4. JUSTIFIED: \(\Pr(A_n)=|A_n|/n^n\). This uses the supplied uniform finite probability convention and Step 3's sample-space count.

5. JUSTIFIED: Every forward orbit eventually enters a directed cycle. The proof applies the finite pigeonhole principle to \(f^0(x),\ldots,f^n(x)\), then uses the first repeated index to obtain pairwise distinct vertices closed by the directed edges of \(G_f\).

6. JUSTIFIED: If \(G_f\) has a unique cyclic vertex \(r\), then \(f(r)=r\), and every vertex reaches \(r\). The cycle through \(r\) cannot contain any other vertex, and every eventual orbit cycle consists of cyclic vertices, hence must be the loop at \(r\).

7. JUSTIFIED: For fixed \(r\), \(|\mathcal A_{1,1}|=1\). In the case \(n=1\), the only function \([1]\to[1]\) maps \(1\) to \(1\), giving the single loop at \(1\).

8. JUSTIFIED: For \(n\ge2\), the encoding \(\Phi:\mathcal A_{n,r}\to[n]^{n-2}\) is defined by repeatedly removing the least non-root \(R_k\)-leaf and recording \(w_k=f(a_k)\). The notions \(R_k\), \(R_k\)-leaf, \(a_k\), and \(w_k\) are all defined in the proof.

9. JUSTIFIED: A non-root \(R_k\)-leaf exists at each encoding step. If none existed, choosing one predecessor \(p(u)\) for every non-root remaining \(u\) and iterating \(p\) in the finite non-root set would produce an \(f\)-cycle away from \(r\), contradicting Step 6's reachability to \(r\).

10. JUSTIFIED: Removing the selected leaf preserves \(f(R_{k+1})\subseteq R_{k+1}\) and reachability of \(r\), and after \(n-2\) removals the final non-root vertex \(b\) satisfies \(f(b)=r\). The proof uses \(f(a_k)\ne a_k\), the leaf condition, closure, and reachability.

11. JUSTIFIED: The decoding algorithm can choose the least non-root remaining element absent from the suffix \(w_k,\ldots,w_{n-2}\). The proof compares \(|R_k\setminus\{r\}|=n-k\) with suffix length \(n-k-1\).

12. JUSTIFIED: The decoding assignment \(f(a_k)=w_k\) is legitimate. The proof checks \(w_k\ne a_k\) and that \(w_k\) has not been removed earlier, so \(w_k\in R_k\setminus\{a_k\}\).

13. JUSTIFIED: The decoded function lies in \(\mathcal A_{n,r}\). The proof assigns increasing indices to removed vertices, the final non-root vertex, and \(r\), then shows \(f(v)\) has strictly larger index for every \(v\ne r\), while \(f(r)=r\).

14. JUSTIFIED: For an encoded valid function, a non-root remaining vertex is an \(R_k\)-leaf exactly when it is absent from the remaining suffix. The proof shows occurrence in the suffix gives a still-present preimage, and non-leafness gives a still-present preimage that is neither \(r\) nor final \(b\).

15. JUSTIFIED: \(\Psi(\Phi(f))=f\) for \(f\in\mathcal A_{n,r}\). Step 14 implies encoding and decoding choose the same least vertex at every stage, assign the same image values, and have the same terminal assignments.

16. JUSTIFIED: \(\Phi(\Psi(w))=w\) for \(w\in[n]^{n-2}\). In the decoded function, \(a_k\) is a leaf, and every smaller non-root remaining vertex occurs in the suffix and therefore has a still-present preimage, so the encoder removes \(a_k\) and records \(w_k\).

17. JUSTIFIED: \(|\mathcal A_{n,r}|=n^{n-2}\) for \(n\ge2\). Steps 8-16 prove a bijection with \([n]^{n-2}\), and the word count \(n^{n-2}\) is elementary finite multiplication.

18. JUSTIFIED: \(A_n=\bigsqcup_{r\in[n]}A_{n,r}\). The proof checks both inclusions from the definition of "unique cyclic vertex" and disjointness from uniqueness.

19. JUSTIFIED: \(|A_n|=n^{n-1}\) for every positive integer \(n\). For \(n=1\), Step 7 gives \(|A_n|=1=1^{1-1}\); for \(n\ge2\), Steps 17-18 and finite disjoint-union counting give \(n\cdot n^{n-2}=n^{n-1}\).

20. JUSTIFIED: \(\Pr(A_n)=1/n\). Step 4 gives \(\Pr(A_n)=|A_n|/n^n\), Step 19 gives \(|A_n|=n^{n-1}\), and elementary cancellation gives \(n^{n-1}/n^n=1/n\) for positive \(n\).

3. Unfilled gaps

Empty list.

4. Disallowed-premise check

Empty list. The proof does not cite the target theorem, the rooted-tree correspondence, Cayley's formula, any height-distribution statement, any formal skeleton statement not granted as support, or any external fact. The fixed-root count is proved inside the final proof rather than imported.

5. Scope check

The proof establishes the full target statement. It covers every positive integer \(n\), with \(n=1\) handled separately in the fixed-root enumeration and numerator assembly, and \(n\ge2\) handled by the explicit coding bijection.

No restriction, omitted case, omitted sub-statement, or weaker statement remains.

6. Coupling inventory

Definitions/notation/assumptions from the cleaned skeleton PDF or TeX file actually used: 6.

- \(n\) is a positive integer.
- \([n]=\{1,2,\ldots,n\}\).
- A function \(f:[n]\to[n]\) and the finite set of all such functions.
- The elementary finite probability convention for a uniform random function.
- \(G_f\) has vertex set \([n]\) and directed edges \((i,f(i))\).
- A cyclic vertex is a vertex belonging to a cycle of \(G_f\).

Allowed formal skeleton statements used beyond definitions/notation/assumptions (statements in the Allowed list, appearing before the target): 0; none.

Disallowed skeleton statements cited: 0; none.

Approved Source Ledger facts used: 0; none. No external Source Ledger fact is used as a mathematical premise.

Standard-background facts the core argument relies on:

- finite pigeonhole principle;
- elementary finite multiplication principle for tuples and words;
- existence of a least element in a nonempty finite subset of \([n]\);
- finite disjoint-union counting;
- elementary exponent arithmetic and cancellation;
- finite iteration/repetition reasoning for a self-map of a finite set.

Is the core argument carried mainly by standard background? no. The load-bearing fixed-root count is carried by the internally proved encoding/decoding bijection; standard background supplies only finite-set bookkeeping and arithmetic.

7. Blueprint and subproof consistency

Proof Blueprint present? YES

Subclaim graph present? YES

[KEY STEP] present? YES

Did the final proof follow the blueprint? YES

Blueprint smuggling issue? NO

Did any S1-S5 subproof leave a needed subclaim unsolved? NO. S4 and S5 are locally conditional on earlier subclaims, but those prerequisites are supplied by S1 and S3, and S6 reproves the needed material inline.

8. Web-source confirmation

no web sources used

9. Controller-facing summary

Non-fillable gaps present? NO

Fillable-only gaps present? NO

Disallowed premises present? NO

Omitted case / weaker statement present? NO

Allowed formal skeleton statements used beyond definitions: 0; none

Disallowed skeleton statements cited: 0; none

Approved Source Ledger facts used: 0; none

Standard-background-heavy? NO

Blueprint present? YES

[KEY STEP] present? YES

Blueprint smuggling issue? NO

Final proof follows blueprint? YES

Web-source issue? NO

Candidate guidance seed, if any: None

### Verifier A report 2

# 1. Target restatement

For every positive integer \(n\), let \(f:[n]\to[n]\) be chosen uniformly from the finite set of all functions \([n]\to[n]\). Let \(G_f\) have vertex set \([n]\) and directed edges \((i,f(i))\), and call a vertex cyclic if it lies on a directed cycle of \(G_f\). The target is
\[
\Pr\{f:[n]\to[n]\colon G_f\text{ has exactly one cyclic vertex}\}=\frac1n.
\]

# 2. Step ledger

1. JUSTIFIED: The proof defines \(\mathcal F_n=\{f:[n]\to[n]\}\) and \(A_n=\{f\in\mathcal F_n:G_f\text{ has a unique cyclic vertex}\}\). This uses the supplied notation \([n]\), function-space definition, \(G_f\), and cyclic-vertex definition.

2. JUSTIFIED: The map \(f\mapsto(f(1),\ldots,f(n))\) is a bijection from \(\mathcal F_n\) to \([n]^n\). The proof states that values on \(1,\ldots,n\) determine \(f\), and every \(n\)-tuple over \([n]\) determines such a function; this is elementary finite-function reasoning.

3. JUSTIFIED: \(|\mathcal F_n|=n^n\). The proof uses the preceding bijection and the elementary multiplication principle for \(n\) coordinates with \(n\) choices each.

4. JUSTIFIED: \(\Pr(A_n)=|A_n|/n^n\). The proof invokes the supplied uniform finite probability convention and the already established count \(|\mathcal F_n|=n^n\).

5. JUSTIFIED: Every forward orbit of \(f:[n]\to[n]\) eventually repeats. The proof applies the finite pigeonhole principle to \(f^0(x),\ldots,f^n(x)\) in the \(n\)-element set \([n]\).

6. JUSTIFIED: A first repeated forward-orbit segment forms a directed cycle in \(G_f\). The proof chooses minimal \(b>0\) with \(f^a(x)=f^b(x)\), proves pairwise distinctness before \(b\), and uses the edge definition \((i,f(i))\).

7. JUSTIFIED: If \(G_f\) has unique cyclic vertex \(r\), then \(f(r)=r\). The proof notes that the directed cycle through \(r\) cannot contain a distinct vertex, so it is the one-vertex loop at \(r\).

8. JUSTIFIED: Under the same uniqueness hypothesis, every vertex reaches \(r\). The proof combines the eventual-cycle result with the fact that every vertex on the eventual cycle is cyclic, hence must be \(r\).

9. JUSTIFIED: For fixed \(r\), the class \(\mathcal A_{n,r}\) is defined as functions for which \(r\) is the unique cyclic vertex. This uses only the supplied definitions of function, \(G_f\), and cyclic vertex.

10. JUSTIFIED: The \(n=1\) fixed-root count is \(1\). The proof observes that the sole function \([1]\to[1]\) maps \(1\) to \(1\), giving the single loop.

11. JUSTIFIED: The encoding \(\Phi:\mathcal A_{n,r}\to[n]^{n-2}\) is defined by iteratively removing the least non-root \(R_k\)-leaf and recording \(w_k=f(a_k)\). The construction is internal and uses the ordinary order on the finite set \([n]\).

12. JUSTIFIED: A non-root \(R_k\)-leaf exists at each encoding step. The proof argues that otherwise a chosen-predecessor map on the finite non-root set would repeat and yield an \(f\)-directed cycle outside \(r\), contradicting reachability to \(r\).

13. JUSTIFIED: Deleting the selected leaf preserves \(f(R_{k+1})\subseteq R_{k+1}\) and reachability of \(r\). The proof uses \(f(a_k)\ne a_k\) and the leaf property, so no remaining vertex maps to \(a_k\).

14. JUSTIFIED: After \(n-2\) encoding removals, the remaining non-root vertex \(b\) satisfies \(f(b)=r\). The proof uses \(R_{n-1}=\{r,b\}\), closure, \(f(r)=r\), and reachability of \(b\) to \(r\).

15. JUSTIFIED: The decoding algorithm can choose a least non-root remaining vertex absent from the suffix \(w_k,\ldots,w_{n-2}\). The proof compares \(|R_k\setminus\{r\}|=n-k\) with suffix length \(n-k-1\), using elementary finite counting.

16. JUSTIFIED: The decoded assignment \(f(a_k)=w_k\) is legitimate. The proof shows \(w_k\ne a_k\) and that \(w_k\) has not been removed earlier; hence \(w_k\in R_k\setminus\{a_k\}\).

17. JUSTIFIED: The decoded function lies in \(\mathcal A_{n,r}\). The proof assigns increasing removal indices and shows \(f(v)\) has strictly larger index for every \(v\ne r\), while \(f(r)=r\), so all non-root vertices reach \(r\) and no non-root cycle exists.

18. JUSTIFIED: For encoded \(f\), an element \(y\in R_k\setminus\{r\}\) is an \(R_k\)-leaf iff it is absent from \(w_k,\ldots,w_{n-2}\). The proof checks both directions using the remaining-set closure and terminal fact \(f(b)=r\).

19. JUSTIFIED: \(\Psi(\Phi(f))=f\) for every \(f\in\mathcal A_{n,r}\). The proof uses the leaf-suffix equivalence to show encoding and decoding choose the same least vertex at each step and assign the same image.

20. JUSTIFIED: \(\Phi(\Psi(w))=w\) for every \(w\in[n]^{n-2}\). The proof shows the decoded \(a_k\) is the least remaining leaf at step \(k\), so encoding records \(f(a_k)=w_k\).

21. JUSTIFIED: \(\Phi\) is a bijection and \(|\mathcal A_{n,r}|=n^{n-2}\) for \(n\ge2\). This follows from the mutual inverse proof and the elementary count of words of length \(n-2\) over an \(n\)-element alphabet.

22. JUSTIFIED: \(A_n=\bigsqcup_{r\in[n]}A_{n,r}\). The proof proves both inclusions from the definitions and disjointness from uniqueness of the cyclic vertex.

23. JUSTIFIED: \(|A_n|=n^{n-1}\) for every positive integer \(n\). The proof handles \(n=1\) by the one-point count and handles \(n\ge2\) by finite disjoint-union counting:
\[
\sum_{r\in[n]}n^{n-2}=n\cdot n^{n-2}=n^{n-1}.
\]

24. JUSTIFIED: \(\Pr(A_n)=1/n\). The proof substitutes \(|A_n|=n^{n-1}\) into \(\Pr(A_n)=|A_n|/n^n\) and uses elementary cancellation for positive \(n\), including \(n=1\).

# 3. Unfilled gaps

Empty list.

# 4. Disallowed-premise check

Empty list.

The proof does not cite the target theorem, an equivalent theorem, Cayley's formula, a rooted-tree correspondence, a height-distribution statement, a cleaned-skeleton formal result not in the allowed list, or any external fact.

# 5. Scope check

The proof establishes the full target statement for every positive integer \(n\). It separately proves the endpoint \(n=1\), proves the fixed-root count for all \(n\ge2\), assembles over all possible unique cyclic vertices, and then applies the uniform finite probability convention. No restriction, omitted case, omitted sub-statement, or weaker statement remains.

# 6. Coupling inventory

Definitions/notation/assumptions from the cleaned skeleton PDF or TeX file actually used: 7 items:
\([n]=\{1,\ldots,n\}\); \(n\) is a positive integer; functions \(f:[n]\to[n]\); the finite set of all such functions; uniform random function from that finite set; \(G_f\) with vertex set \([n]\) and edges \((i,f(i))\); cyclic vertex as a vertex belonging to a cycle of \(G_f\).

Allowed formal skeleton statements used beyond definitions/notation/assumptions (statements in the Allowed list, appearing before the target): 0 items: none.

Disallowed skeleton statements cited (the target itself, anything equivalent to / stronger than / downstream of it, or anything appearing after it): 0 items: none.

Approved Source Ledger facts used: 0 items: none; there were no external cited facts.

Standard-background facts the core argument relies on: finite multiplication principle; finite pigeonhole principle; existence of least elements in nonempty finite subsets of \([n]\); finite disjoint-union counting; elementary exponent arithmetic and cancellation.

Is the core argument carried mainly by standard background? no. Standard background supports finite bookkeeping, but the load-bearing fixed-root count is carried by the internally proved encoding/decoding bijection.

# 7. Blueprint and subproof consistency

Proof Blueprint present? YES

Subclaim graph present? YES

[KEY STEP] present? YES

Did the final proof follow the blueprint? YES

Blueprint smuggling issue? NO

Did any S1-S5 subproof leave a needed subclaim unsolved? NO

S4 and S5 were locally conditional on earlier subclaims, but S6 incorporated the needed S1, S3, and assembly arguments inline; no needed subclaim remains unsolved in the composed proof.

# 8. Web-source confirmation

no web sources used

# 9. Controller-facing summary

Non-fillable gaps present? NO

Fillable-only gaps present? NO

Disallowed premises present? NO

Omitted case / weaker statement present? NO

Allowed formal skeleton statements used beyond definitions: 0 items: none

Disallowed skeleton statements cited: 0 items: none

Approved Source Ledger facts used: 0 items: none

Standard-background-heavy? NO

Blueprint present? YES

[KEY STEP] present? YES

Blueprint smuggling issue? NO

Final proof follows blueprint? YES

Web-source issue? NO

Candidate guidance seed, if any: None

### Verifier A report 3

1. Target restatement

Let \(n\) be a positive integer. Choose a function \(f:[n]\to[n]\) uniformly from the finite set of all such functions. Let \(G_f\) be the directed graph with vertex set \([n]\) and directed edges \((i,f(i))\). The target is
\[
\Pr\{f:[n]\to[n]\colon G_f\text{ has exactly one cyclic vertex}\}=\frac1n.
\]

2. Step ledger

1. The proof defines \(\mathcal F_n=\{f:[n]\to[n]\}\) and \(A_n=\{f\in\mathcal F_n:G_f\text{ has a unique cyclic vertex}\}\).
JUSTIFIED: This uses only the supplied notation \([n]\), the supplied definition of \(G_f\), and the supplied definition of cyclic vertex.

2. The map \(f\mapsto(f(1),\ldots,f(n))\) is a bijection \(\mathcal F_n\to[n]^n\).
JUSTIFIED: The proof states that the \(n\) values determine \(f\), and every tuple in \([n]^n\) defines a function \([n]\to[n]\); this is elementary finite-function reasoning.

3. The sample space has size \(|\mathcal F_n|=n^n\).
JUSTIFIED: By Step 2 and the finite multiplication principle, an \(n\)-tuple over an \(n\)-element set has \(n^n\) choices.

4. \(\Pr(A_n)=|A_n|/n^n\).
JUSTIFIED: The supplied uniform finite probability convention gives \(\Pr(A_n)=|A_n|/|\mathcal F_n|\), and Step 3 gives \(|\mathcal F_n|=n^n\).

5. Every forward orbit of any \(f:[n]\to[n]\) eventually enters a directed cycle.
JUSTIFIED: The proof applies the finite pigeonhole principle to \(f^0(x),\ldots,f^n(x)\); a minimal repeated index gives pairwise distinct vertices closed by the directed edges \((v,f(v))\).

6. If \(G_f\) has unique cyclic vertex \(r\), then \(f(r)=r\).
JUSTIFIED: The cycle containing \(r\) contains only cyclic vertices; uniqueness forces it to contain only \(r\), hence the outgoing edge from \(r\) is \((r,r)\).

7. If \(G_f\) has unique cyclic vertex \(r\), then every vertex reaches \(r\) after finitely many iterates.
JUSTIFIED: By Step 5 every orbit reaches some directed cycle; all vertices on that cycle are cyclic, so uniqueness forces the cycle to be the loop at \(r\).

8. For fixed \(r\), the \(n=1\) fixed-root count is \(|\mathcal A_{1,1}|=1\).
JUSTIFIED: The proof notes that \([1]=\{1\}\), the only function sends \(1\) to \(1\), and the associated graph has the single loop at \(1\).

9. For \(n\ge2\) and \(f\in\mathcal A_{n,r}\), the leaf-removal encoding \(\Phi(f)\) is defined at every step.
JUSTIFIED: Inductively, \(R_k\) contains \(r\), is closed under \(f\), and all its vertices reach \(r\). If no non-root leaf existed, predecessor iteration in the finite non-root set would produce an \(f\)-cycle away from \(r\), contradicting reachability to \(r\).

10. Deleting the chosen encoding leaf preserves closure under \(f\) and reachability to \(r\).
JUSTIFIED: Since \(a_k\) is a leaf and \(f(a_k)\ne a_k\), no vertex of \(R_k\) maps to \(a_k\); hence no remaining orbit to \(r\) can be forced through \(a_k\).

11. After \(n-2\) encoding removals, the last non-root vertex \(b\) satisfies \(f(b)=r\).
JUSTIFIED: The remaining set is \(\{r,b\}\), it is closed under \(f\), \(f(r)=r\), and \(b\) reaches \(r\); the only possible image consistent with reachability is \(r\).

12. For every word \(w\in[n]^{n-2}\), the decoding algorithm has a valid least absent non-root element at each step.
JUSTIFIED: At step \(k\), \(R_k\setminus\{r\}\) has \(n-k\) elements while the suffix \(w_k,\ldots,w_{n-2}\) has length \(n-k-1\), so some element is absent; leastness uses the order on \([n]\).

13. The decoding assignment \(f(a_k)=w_k\) is legitimate.
JUSTIFIED: The chosen \(a_k\) is absent from the suffix containing \(w_k\), so \(w_k\ne a_k\); if \(w_k\) had been removed earlier as \(a_j\), then \(a_j\) would have appeared in its own forbidden suffix.

14. The decoded function belongs to \(\mathcal A_{n,r}\).
JUSTIFIED: The proof assigns increasing removal indices: for every \(v\ne r\), \(f(v)\) has strictly larger index, while \(f(r)=r\); hence all non-root vertices reach \(r\) and no non-root cycle exists.

15. For an encoded valid function, a remaining non-root vertex is an \(R_k\)-leaf iff it is absent from the remaining suffix.
JUSTIFIED: If it appears as some \(w_j=f(a_j)\), a still-present vertex maps to it. Conversely, a non-leaf preimage cannot be \(r\) or the final \(b\), since both map to \(r\), so it is some later \(a_j\).

16. \(\Psi(\Phi(f))=f\) for every \(f\in\mathcal A_{n,r}\).
JUSTIFIED: By Step 15, encoding and decoding choose the same least vertex at each stage, assign the same image value, remove the same vertex, and share the terminal assignments \(f(b)=r\), \(f(r)=r\).

17. \(\Phi(\Psi(w))=w\) for every \(w\in[n]^{n-2}\).
JUSTIFIED: In the decoded function, \(a_k\) is a leaf because it is absent from the suffix; every smaller non-root remaining vertex appears in the suffix and has a still-present preimage, so encoding removes \(a_k\) and records \(w_k\).

18. For \(n\ge2\), \(|\mathcal A_{n,r}|=n^{n-2}\).
JUSTIFIED: Steps 12-17 establish mutually inverse maps \(\mathcal A_{n,r}\leftrightarrow[n]^{n-2}\); finite word counting gives \(n^{n-2}\) words.

19. \(A_n=\bigsqcup_{r\in[n]}A_{n,r}\).
JUSTIFIED: A function with a unique cyclic vertex has exactly one such vertex \(r\in[n]\), and membership in \(A_{n,r}\) is exactly the assertion that \(r\) is that unique vertex; distinct roots give disjoint classes.

20. \(|A_n|=n^{n-1}\) for every positive integer \(n\).
JUSTIFIED: For \(n=1\), Step 8 gives one favorable function. For \(n\ge2\), Steps 18 and 19 give \(n\) disjoint classes each of size \(n^{n-2}\), so \(n\cdot n^{n-2}=n^{n-1}\).

21. The target probability is \(1/n\).
JUSTIFIED: Combining Steps 4 and 20 gives \(\Pr(A_n)=n^{n-1}/n^n\); since \(n>0\), elementary exponent arithmetic gives \(n^{n-1}/n^n=1/n\), including \(n=1\).

3. Unfilled gaps

- None.

4. Disallowed-premise check

- None.

5. Scope check

The proof establishes the full target statement for every positive integer \(n\). The case \(n=1\) is handled separately in the fixed-root count and then included in the final count; the case \(n\ge2\) is handled by the fixed-root bijection and disjoint-union assembly. No restriction, omitted case, omitted sub-statement, or weaker statement remains.

6. Coupling inventory

Definitions/notation/assumptions from the cleaned skeleton PDF or TeX file actually used: 6.

- \(n\) is a positive integer.
- \([n]=\{1,2,\ldots,n\}\), including its finite order for least-element choices.
- A function \(f:[n]\to[n]\) and the finite set of all such functions.
- The elementary uniform finite probability convention for a uniformly chosen function.
- The definition of \(G_f\) with vertex set \([n]\) and directed edges \((i,f(i))\).
- The definition of cyclic vertex as a vertex belonging to a cycle of \(G_f\).

Allowed formal skeleton statements used beyond definitions/notation/assumptions (statements in the Allowed list, appearing before the target): 0.

- None.

Disallowed skeleton statements cited (the target itself, anything equivalent to / stronger than / downstream of it, or anything appearing after it): 0.

- None.

Approved Source Ledger facts used: 0.

- None.

Standard-background facts the core argument relies on:

- Finite multiplication principle for tuples and words.
- Finite pigeonhole principle.
- Existence of a least element in a nonempty finite subset of \([n]\).
- Elementary finite predecessor-iteration/repetition reasoning.
- Finite disjoint-union counting.
- Elementary exponent arithmetic and cancellation for positive integers.

Is the core argument carried mainly by standard background? no. The load-bearing fixed-root count is carried by an explicit proof-internal encoding/decoding bijection; standard background supplies only finite-set and arithmetic mechanics.

7. Blueprint and subproof consistency

- Proof Blueprint present? YES
- Subclaim graph present? YES
- [KEY STEP] present? YES
- Did the final proof follow the blueprint? YES
- Blueprint smuggling issue? NO
- Did any S1-S5 subproof leave a needed subclaim unsolved? NO

8. Web-source confirmation

no web sources used

9. Controller-facing summary

Non-fillable gaps present? NO
Fillable-only gaps present? NO
Disallowed premises present? NO
Omitted case / weaker statement present? NO
Allowed formal skeleton statements used beyond definitions: 0 + []
Disallowed skeleton statements cited: 0 + []
Approved Source Ledger facts used: 0 + []
Standard-background-heavy? NO
Blueprint present? YES
[KEY STEP] present? YES
Blueprint smuggling issue? NO
Final proof follows blueprint? YES
Web-source issue? NO
Candidate guidance seed, if any: None
