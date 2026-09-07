Source Ledger

claim_id:
CG-SL1
proof_location:
Final proof, opening paragraph and Steps 1, 2, 4.
claim_or_fact_used:
The notation \([n]\), the standing assumption on \(n\), the function space \(\mathcal F_n\), the associated directed graph \(G_f\), and the definition of cyclic vertex.
candidate_source_status:
provided definition / notation / assumption
candidate_source_label_or_name:
Provided mathematical packet, Sections 1, 2, and 4; Allowed Support list.
exact_statement_needed:
\([n]=\{1,2,\ldots,n\}\); \(n\) is a positive integer; a function \(f:[n]\to[n]\) has associated directed graph \(G_f\) with vertex set \([n]\) and directed edges \((i,f(i))\); a vertex is cyclic if it belongs to a cycle of \(G_f\).
hypotheses_or_conditions_needed:
\(n\) is a positive integer and \(f:[n]\to[n]\).
where_hypotheses_are_checked:
The final proof begins with \(n\) fixed as in the theorem and defines \(\mathcal F_n=\{f:[n]\to[n]\}\).
strength_used_by_proof:
Definitions and notation only.
source_check_status:
VERIFIED
source_evidence:
Packet Sections 1, 2, and 4 state the notation, standing assumption, directed graph construction, and cyclic-vertex definition; the Allowed Support list repeats these as allowed without proof.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL2
proof_location:
Final proof, Step 1.
claim_or_fact_used:
The map \(f\mapsto(f(1),\ldots,f(n))\) is a bijection from \(\mathcal F_n\) to \([n]^n\).
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Tuple encoding of a finite function.
exact_statement_needed:
Values on the finite domain \([n]\) determine a function \(f:[n]\to[n]\), and every \(n\)-tuple in \([n]^n\) determines such a function.
hypotheses_or_conditions_needed:
The domain is exactly \([n]=\{1,\ldots,n\}\), and all tuple coordinates lie in the codomain \([n]\).
where_hypotheses_are_checked:
Step 1 defines \(\mathcal F_n\) and uses the supplied notation for \([n]\).
strength_used_by_proof:
Transfers the sample-space cardinality problem from functions to \(n\)-tuples.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 1, by saying that the values \(f(1),\ldots,f(n)\) determine \(f\), and every \(n\)-tuple in \([n]^n\) determines such a function.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL3
proof_location:
Final proof, Step 1.
claim_or_fact_used:
\(|[n]^n|=n^n\), hence \(|\mathcal F_n|=n^n\).
candidate_source_status:
standard background fact
candidate_source_label_or_name:
Elementary multiplication principle for finite choices.
exact_statement_needed:
If a word or tuple has \(m\) positions and each position has \(n\) possible values, then there are \(n^m\) such tuples; here \(m=n\).
hypotheses_or_conditions_needed:
\([n]\) has \(n\) elements and there are \(n\) tuple coordinates.
where_hypotheses_are_checked:
Packet notation gives \([n]=\{1,\ldots,n\}\), and Step 1 uses \(n\)-tuples.
strength_used_by_proof:
Gives the denominator count \(n^n\) for the uniform sample space.
source_check_status:
NOT_APPLICABLE
source_evidence:
Genuinely elementary finite-set counting allowed by the Allowed Support list.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL4
proof_location:
Final proof, Steps 1 and 5.
claim_or_fact_used:
For a uniform finite probability space, the probability of an event is its cardinality divided by the sample-space cardinality.
candidate_source_status:
allowed supporting statement
candidate_source_label_or_name:
Uniform finite probability convention.
exact_statement_needed:
A uniform random function is chosen uniformly from the finite set of all functions \([n]\to[n]\), so \(\Pr(A_n)=|A_n|/|\mathcal F_n|\) for \(A_n\subseteq\mathcal F_n\).
hypotheses_or_conditions_needed:
\(\mathcal F_n\) is finite and \(A_n\subseteq\mathcal F_n\).
where_hypotheses_are_checked:
Step 1 proves \(|\mathcal F_n|=n^n\), and \(A_n\) is defined as a subset of \(\mathcal F_n\).
strength_used_by_proof:
Converts the enumeration of favorable functions into the desired probability.
source_check_status:
VERIFIED
source_evidence:
Packet Section 1 states the elementary finite probability convention, and the Allowed Support list permits the uniform finite probability convention.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL5
proof_location:
Final proof, Step 2.
claim_or_fact_used:
The finite pigeonhole principle gives a repeated value among \(f^0(x),f^1(x),\ldots,f^n(x)\).
candidate_source_status:
standard background fact
candidate_source_label_or_name:
Finite pigeonhole principle.
exact_statement_needed:
If \(n+1\) objects lie in an \(n\)-element set, then two of the objects are equal.
hypotheses_or_conditions_needed:
The iterates \(f^0(x),\ldots,f^n(x)\) all lie in the \(n\)-element set \([n]\).
where_hypotheses_are_checked:
Step 2 fixes \(f:[n]\to[n]\) and \(x\in[n]\), so all iterates remain in \([n]\).
strength_used_by_proof:
Provides the first repetition needed to construct an eventual directed cycle.
source_check_status:
NOT_APPLICABLE
source_evidence:
Elementary finite-set reasoning permitted by the Allowed Support list.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL6
proof_location:
Final proof, Step 2.
claim_or_fact_used:
A first repeated value in a forward orbit determines a directed cycle in \(G_f\).
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
First-repetition cycle construction.
exact_statement_needed:
If \(b>0\) is minimal with \(f^a(x)=f^b(x)\) for some \(a<b\), then \(f^a(x),f^{a+1}(x),\ldots,f^{b-1}(x)\) are pairwise distinct and the directed edges close them into a cycle.
hypotheses_or_conditions_needed:
\(f:[n]\to[n]\), \(x\in[n]\), and a repeated pair of iterates \(f^a(x)=f^b(x)\) with \(a<b\).
where_hypotheses_are_checked:
Step 2 obtains the repeated pair from CG-SL5 and chooses the minimal repeated index \(b\).
strength_used_by_proof:
Shows every forward orbit eventually enters a directed cycle.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 2, using the directed edges \((i,f(i))\).
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL7
proof_location:
Final proof, Step 2.
claim_or_fact_used:
If \(G_f\) has a unique cyclic vertex \(r\), then \(f(r)=r\) and every vertex reaches \(r\) after finitely many iterations.
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Unique-cyclic-vertex structure.
exact_statement_needed:
The cycle containing \(r\) has no vertex other than \(r\), so it is the loop at \(r\); every eventual orbit cycle consists of cyclic vertices, so under uniqueness it must be the same loop at \(r\).
hypotheses_or_conditions_needed:
\(r\) is the unique cyclic vertex of \(G_f\).
where_hypotheses_are_checked:
Step 2 explicitly assumes the unique-cyclic-vertex condition before applying the conclusion.
strength_used_by_proof:
Supplies the fixed root and reachability facts used in the fixed-root enumeration.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 2.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL8
proof_location:
Final proof, Step 3, \(n=1\) paragraph.
claim_or_fact_used:
For \(n=1\), the fixed-root class has exactly one function and that function has unique cyclic vertex \(1\).
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
One-point fixed-root case.
exact_statement_needed:
The only function \([1]\to[1]\) sends \(1\) to \(1\), giving the single loop at \(1\), so \(|\mathcal A_{1,1}|=1\).
hypotheses_or_conditions_needed:
\(n=1\), hence \([1]=\{1\}\) and \(r=1\).
where_hypotheses_are_checked:
Step 3 handles the case \(n=1\) separately.
strength_used_by_proof:
Provides the endpoint fixed-root count.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 3.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL9
proof_location:
Final proof, Step 3, definition of \(\mathcal A_{n,r}\), \(R\)-leaves, and the encoding map \(\Phi\).
claim_or_fact_used:
The fixed-root class and the leaf-removal encoding are valid internal constructions.
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Internal fixed-root encoding construction.
exact_statement_needed:
For \(f\in\mathcal A_{n,r}\), recursively choose the least non-root \(R_k\)-leaf, record \(w_k=f(a_k)\), and remove \(a_k\).
hypotheses_or_conditions_needed:
\(n\ge2\), \(r\in[n]\), \(f\in\mathcal A_{n,r}\), and the existence of a suitable \(R_k\)-leaf at each step.
where_hypotheses_are_checked:
Step 3 fixes \(r\), defines \(\mathcal A_{n,r}\), assumes \(n\ge2\), and then proves well-definedness in CG-SL10 and CG-SL11.
strength_used_by_proof:
Defines the code map \(\Phi:\mathcal A_{n,r}\to[n]^{n-2}\).
source_check_status:
NOT_APPLICABLE
source_evidence:
Construction introduced and checked inside Final proof, Step 3.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL10
proof_location:
Final proof, Step 3, encoding well-definedness paragraph.
claim_or_fact_used:
At every encoding step, a non-root \(R_k\)-leaf exists.
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Finite predecessor contradiction.
exact_statement_needed:
If no non-root \(R_k\)-leaf existed, choosing a predecessor for every non-root remaining vertex and iterating inside the finite non-root set would produce a directed cycle outside \(r\), contradicting reachability to \(r\).
hypotheses_or_conditions_needed:
\(R_k\) is finite, contains \(r\), is closed under \(f\), and every element of \(R_k\) reaches \(r\).
where_hypotheses_are_checked:
Step 3 establishes these as the induction hypotheses for encoding, initially from CG-SL7.
strength_used_by_proof:
Ensures the encoding can choose a canonical removable vertex at every step.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 3.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL11
proof_location:
Final proof, Step 3, encoding induction after choosing \(a_k\).
claim_or_fact_used:
Deleting the selected leaf preserves closure under \(f\) and reachability of \(r\).
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Closure after leaf deletion.
exact_statement_needed:
Since no remaining vertex maps to \(a_k\), deleting \(a_k\) preserves \(f(R_{k+1})\subseteq R_{k+1}\); remaining paths to \(r\) cannot pass through \(a_k\).
hypotheses_or_conditions_needed:
\(a_k\) is an \(R_k\)-leaf, \(f(R_k)\subseteq R_k\), every element of \(R_k\) reaches \(r\), and \(a_k\ne r\).
where_hypotheses_are_checked:
Step 3 uses the definition of \(R_k\)-leaf and the induction hypotheses.
strength_used_by_proof:
Maintains the encoding induction through \(n-2\) removals.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 3.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL12
proof_location:
Final proof, Step 3, terminal encoding paragraph.
claim_or_fact_used:
After \(n-2\) removals, the last non-root vertex \(b\) satisfies \(f(b)=r\).
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Two-vertex terminal step.
exact_statement_needed:
When \(R_{n-1}=\{r,b\}\), closure of \(R_{n-1}\), \(f(r)=r\), and reachability of \(b\) to \(r\) force \(f(b)=r\).
hypotheses_or_conditions_needed:
The encoding induction has left exactly \(\{r,b\}\), with closure and reachability preserved.
where_hypotheses_are_checked:
Step 3 after completing the encoding removals.
strength_used_by_proof:
Used in the inverse-map proof and in identifying the terminal edge.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 3.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL13
proof_location:
Final proof, Step 3, decoding construction.
claim_or_fact_used:
At each decoding step, a least non-root remaining element absent from the current suffix exists.
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Suffix length count.
exact_statement_needed:
At step \(k\), the set \(R_k\setminus\{r\}\) has \(n-k\) elements while the suffix \(w_k,\ldots,w_{n-2}\) has length \(n-k-1\), so some non-root remaining element is absent from the suffix.
hypotheses_or_conditions_needed:
\(n\ge2\), \(1\le k\le n-2\), and exactly one non-root vertex has been removed at each earlier step.
where_hypotheses_are_checked:
Step 3 defines the decoding algorithm after assuming \(n\ge2\).
strength_used_by_proof:
Makes the decoding choice rule well-defined.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 3, using finite counting.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL14
proof_location:
Final proof, Step 3, decoding construction.
claim_or_fact_used:
The assigned value \(w_k\) is a valid image in \(R_k\setminus\{a_k\}\), so the decoding defines a function \(f:[n]\to[n]\).
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Parent-remains check.
exact_statement_needed:
\(w_k\ne a_k\) because \(a_k\) is absent from the suffix containing \(w_k\), and \(w_k\) was not removed earlier because an earlier removed vertex was absent from the earlier suffix containing \(w_k\).
hypotheses_or_conditions_needed:
The decoding choice rule for each \(a_j\) and the current suffix \(w_j,\ldots,w_{n-2}\).
where_hypotheses_are_checked:
Step 3, immediately after defining \(f(a_k)=w_k\).
strength_used_by_proof:
Ensures all decoded edge assignments are legitimate.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 3.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL15
proof_location:
Final proof, Step 3, decoded function verification.
claim_or_fact_used:
The decoded function belongs to \(\mathcal A_{n,r}\).
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Strictly increasing removal-index argument.
exact_statement_needed:
For every \(v\ne r\), the decoded value \(f(v)\) has strictly larger assigned index than \(v\); hence repeated iteration reaches \(r\), while \(f(r)=r\), so the only directed cycle is the loop at \(r\).
hypotheses_or_conditions_needed:
The decoding construction, the terminal assignments \(f(b)=r\), \(f(r)=r\), and the index assignment to removed vertices, \(b\), and \(r\).
where_hypotheses_are_checked:
Step 3 after defining the decoding map.
strength_used_by_proof:
Shows \(\Psi:[n]^{n-2}\to\mathcal A_{n,r}\).
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 3.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL16
proof_location:
Final proof, Step 3, proof that \(\Psi(\Phi(f))=f\).
claim_or_fact_used:
For an encoded valid function, a remaining non-root vertex is an \(R_k\)-leaf exactly when it is absent from the remaining code suffix.
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Leaf-suffix equivalence.
exact_statement_needed:
For \(y\in R_k\setminus\{r\}\), \(y\) is an \(R_k\)-leaf if and only if \(y\) does not occur among \(w_k,\ldots,w_{n-2}\).
hypotheses_or_conditions_needed:
The encoding construction, closure of remaining sets, the terminal fact \(f(b)=r\), and \(y\ne r\).
where_hypotheses_are_checked:
Step 3 inverse proof for an arbitrary \(f\in\mathcal A_{n,r}\).
strength_used_by_proof:
Shows the decoder chooses the same vertices and reconstructs \(f\).
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 3.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL17
proof_location:
Final proof, Step 3, proof that \(\Phi(\Psi(w))=w\).
claim_or_fact_used:
For a decoded word, the encoding algorithm removes the same vertices and records the same letters.
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Decoded least-leaf property.
exact_statement_needed:
At step \(k\), the decoded \(a_k\) has no incoming edge from remaining vertices, while every smaller non-root remaining vertex occurs in the suffix and therefore has an incoming edge from a still-present vertex.
hypotheses_or_conditions_needed:
The decoding choice rule, decoded edge assignments, and the definitions of \(R_k\)-leaf and suffix.
where_hypotheses_are_checked:
Step 3 inverse proof for an arbitrary \(w\in[n]^{n-2}\).
strength_used_by_proof:
Shows the encoder recovers the original word \(w\).
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 3.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL18
proof_location:
Final proof, Step 3, conclusion of the fixed-root enumeration.
claim_or_fact_used:
\(\Phi\) and \(\Psi\) are mutual inverses, so \(\mathcal A_{n,r}\) is in bijection with \([n]^{n-2}\).
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Mutual inverse proof for the fixed-root coding maps.
exact_statement_needed:
\(\Psi(\Phi(f))=f\) for every \(f\in\mathcal A_{n,r}\), and \(\Phi(\Psi(w))=w\) for every \(w\in[n]^{n-2}\).
hypotheses_or_conditions_needed:
The well-defined encoding, well-defined decoding, leaf-suffix equivalence, and decoded least-leaf property.
where_hypotheses_are_checked:
Step 3 establishes these before concluding the bijection.
strength_used_by_proof:
Establishes the load-bearing fixed-root bijection without importing a tree correspondence or Cayley's formula.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 3.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL19
proof_location:
Final proof, Step 3, final paragraph.
claim_or_fact_used:
There are \(n^{n-2}\) words of length \(n-2\) over \([n]\).
candidate_source_status:
standard background fact
candidate_source_label_or_name:
Finite word count by the multiplication principle.
exact_statement_needed:
For each of \(n-2\) positions there are \(n\) choices from \([n]\), so the number of words is \(n^{n-2}\).
hypotheses_or_conditions_needed:
\([n]\) has \(n\) elements and \(n\ge2\).
where_hypotheses_are_checked:
Packet notation gives the alphabet size, and Step 3 is in the \(n\ge2\) case.
strength_used_by_proof:
Converts the fixed-root bijection into \(|\mathcal A_{n,r}|=n^{n-2}\).
source_check_status:
NOT_APPLICABLE
source_evidence:
Genuinely elementary finite-set counting allowed by the Allowed Support list.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL20
proof_location:
Final proof, Step 4.
claim_or_fact_used:
The favorable event \(A_n\) is the pairwise disjoint union of the fixed-root events \(A_{n,r}\), \(r\in[n]\).
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Unique-element unpacking and disjointness.
exact_statement_needed:
\(A_n=\bigsqcup_{r\in[n]}A_{n,r}\), because a function with a unique cyclic vertex has exactly one such vertex \(r\in[n]\), and a unique vertex cannot be two distinct elements.
hypotheses_or_conditions_needed:
The definitions of \(A_n\), \(A_{n,r}\), and uniqueness of the cyclic vertex.
where_hypotheses_are_checked:
Step 4 defines \(A_{n,r}\) and proves both inclusions and disjointness.
strength_used_by_proof:
Permits summing fixed-root counts over possible roots.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 4.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL21
proof_location:
Final proof, Step 4.
claim_or_fact_used:
The cardinality of a finite disjoint union is the sum of the cardinalities of its parts.
candidate_source_status:
standard background fact
candidate_source_label_or_name:
Finite disjoint-union counting.
exact_statement_needed:
If a finite family of sets is pairwise disjoint, then the cardinality of its union equals the sum of the cardinalities of the sets.
hypotheses_or_conditions_needed:
The family \(\{A_{n,r}:r\in[n]\}\) is finite and pairwise disjoint.
where_hypotheses_are_checked:
Finiteness follows from \([n]\) being finite; pairwise disjointness is proved in Step 4.
strength_used_by_proof:
Combines the fixed-root counts into the total favorable count.
source_check_status:
NOT_APPLICABLE
source_evidence:
Genuinely elementary finite-set counting allowed by the Allowed Support list.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL22
proof_location:
Final proof, Step 4.
claim_or_fact_used:
The total favorable count is \(|A_n|=n^{n-1}\), with the \(n=1\) case handled separately.
candidate_source_status:
proved inside the current proof
candidate_source_label_or_name:
Assembly from fixed-root counts.
exact_statement_needed:
For \(n=1\), \(|A_n|=1=1^{1-1}\); for \(n\ge2\), \(|A_n|=\sum_{r\in[n]}n^{n-2}=n\cdot n^{n-2}=n^{n-1}\).
hypotheses_or_conditions_needed:
The fixed-root count from Step 3, the disjoint-union statement from CG-SL20, finite disjoint-union counting, and elementary exponent arithmetic.
where_hypotheses_are_checked:
Step 4 treats \(n=1\) and \(n\ge2\) separately and invokes the already-proved fixed-root count.
strength_used_by_proof:
Provides the numerator for the final probability calculation.
source_check_status:
NOT_APPLICABLE
source_evidence:
Proved directly in Final proof, Step 4, using CG-SL8, CG-SL18, CG-SL19, CG-SL20, and CG-SL21.
internet_used:
NO
url_or_reference_checked:
None.

claim_id:
CG-SL23
proof_location:
Final proof, Step 5.
claim_or_fact_used:
\(\frac{n^{n-1}}{n^n}=\frac1n\) for positive \(n\).
candidate_source_status:
standard background fact
candidate_source_label_or_name:
Elementary exponent arithmetic and cancellation.
exact_statement_needed:
For a positive integer \(n\), \(n^n=n\cdot n^{n-1}\), so \(n^{n-1}/n^n=1/n\); in the endpoint \(n=1\), this gives \(1/1=1\).
hypotheses_or_conditions_needed:
\(n\) is a positive integer, so the denominator is nonzero.
where_hypotheses_are_checked:
Standing assumption gives \(n>0\), and the \(n=1\) count was handled in Step 4.
strength_used_by_proof:
Completes the final probability identity.
source_check_status:
NOT_APPLICABLE
source_evidence:
Elementary arithmetic allowed by the Allowed Support list.
internet_used:
NO
url_or_reference_checked:
None.

Citation Generator summary:
Source inventory complete? YES
Source Ledger complete? YES
All source locations verified? NOT_APPLICABLE
Internet used? NO
Possible target-source leakage encountered? NO
Unsupported or unclear sources present? NO
Suspicious standard-background claims present? NO
External sources checked:
None
Recommended next step: PROCEED_TO_CITATION_VERIFIER
