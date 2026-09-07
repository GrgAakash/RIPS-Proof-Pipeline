claim_id:
SL1
proof_location:
Final proof, Steps 1 and 4.
claim_or_fact_used:
The notation \([n]\), the function space \(\mathcal F_n\), the directed graph \(G_f\), and the meaning of cyclic vertex.
source_status: provided definition / notation / assumption.
cited_label_or_name:
Allowed support definitions.
exact_statement_used:
\([n]=\{1,\ldots,n\}\); \(n\) is a positive integer; \(G_f\) has vertex set \([n]\) and directed edges \((i,f(i))\); a cyclic vertex is a vertex belonging to a cycle of \(G_f\).
hypotheses_or_conditions_needed:
\(n\) is a positive integer and \(f:[n]\to[n]\).
where_hypotheses_are_checked:
Standing assumption and Step 1 definition of \(\mathcal F_n\).
strength_used:
Definitions only.
notes:
No excluded graph-tree correspondence is used.

claim_id:
SL2
proof_location:
Final proof, Step 1.
claim_or_fact_used:
The set of all functions \([n]\to[n]\) has cardinality \(n^n\).
source_status: standard background fact; proved inside the current proof.
cited_label_or_name:
Tuple encoding of finite functions; finite multiplication principle.
exact_statement_used:
The map \(f\mapsto(f(1),\ldots,f(n))\) is a bijection from \(\mathcal F_n\) to \([n]^n\), and \(|[n]^n|=n^n\).
hypotheses_or_conditions_needed:
The domain and codomain both have \(n\) elements.
where_hypotheses_are_checked:
Step 1 and the notation \([n]=\{1,\ldots,n\}\).
strength_used:
Exact denominator count.
notes:
This is the S1 denominator argument reproduced inside S6.

claim_id:
SL3
proof_location:
Final proof, Steps 1 and 5.
claim_or_fact_used:
Uniform finite probability equals favorable count divided by sample-space count.
source_status: allowed supporting statement.
cited_label_or_name:
Uniform finite probability convention.
exact_statement_used:
A uniform random function is chosen uniformly from the finite set of all functions \([n]\to[n]\), so the probability of \(A_n\subseteq\mathcal F_n\) is \(|A_n|/|\mathcal F_n|\).
hypotheses_or_conditions_needed:
\(\mathcal F_n\) is finite and \(A_n\subseteq\mathcal F_n\).
where_hypotheses_are_checked:
\(\mathcal F_n\) is finite by SL2; \(A_n\) is defined as a subset of \(\mathcal F_n\) in Step 1.
strength_used:
Only the probability conversion.
notes:
No probability distribution beyond the supplied uniform convention is used.

claim_id:
SL4
proof_location:
Final proof, Step 2.
claim_or_fact_used:
Every forward orbit of a function on a finite set eventually enters a directed cycle.
source_status: standard background fact; proved inside the current proof.
cited_label_or_name:
Finite pigeonhole principle and first-repetition cycle construction.
exact_statement_used:
Among \(f^0(x),\ldots,f^n(x)\), two iterates are equal; choosing the first repeated index gives a directed cycle in \(G_f\).
hypotheses_or_conditions_needed:
\([n]\) has \(n\) elements and all iterates remain in \([n]\).
where_hypotheses_are_checked:
Step 2.
strength_used:
Existence of an eventual directed cycle for each orbit.
notes:
This is the S2 orbit argument reproduced inside S6.

claim_id:
SL5
proof_location:
Final proof, Step 2.
claim_or_fact_used:
If \(G_f\) has unique cyclic vertex \(r\), then \(f(r)=r\), and every vertex reaches \(r\).
source_status: proved inside the current proof.
cited_label_or_name:
Unique cyclic vertex structure.
exact_statement_used:
The cycle containing \(r\) must be the one-vertex loop at \(r\); every eventual orbit cycle must be that same loop.
hypotheses_or_conditions_needed:
\(r\) is the unique cyclic vertex of \(G_f\).
where_hypotheses_are_checked:
Step 2 assumes the unique-cyclic-vertex condition before applying the conclusion.
strength_used:
Fixedness of \(r\) and reachability of \(r\) from all vertices.
notes:
No enumeration is hidden in this structural statement.

claim_id:
SL6
proof_location:
Final proof, Step 3, encoding well-definedness.
claim_or_fact_used:
At every encoding step, a non-root leaf exists in the remaining set.
source_status: proved inside the current proof.
cited_label_or_name:
Finite predecessor contradiction.
exact_statement_used:
If every non-root remaining vertex had an incoming edge from another remaining vertex, iterating a chosen predecessor map inside the finite non-root set would produce a directed cycle outside \(r\).
hypotheses_or_conditions_needed:
\(R_k\) is finite, contains \(r\), is closed under \(f\), and every element of \(R_k\) reaches \(r\).
where_hypotheses_are_checked:
Step 3 induction for the encoding.
strength_used:
Existence of the canonical removable leaf.
notes:
This is part of S3's fixed-root proof, expanded in S6.

claim_id:
SL7
proof_location:
Final proof, Step 3, encoding and terminal step.
claim_or_fact_used:
Deleting a selected leaf preserves closure and reachability; after \(n-2\) deletions the last non-root vertex maps to \(r\).
source_status: proved inside the current proof.
cited_label_or_name:
Closure after leaf deletion and two-vertex terminal step.
exact_statement_used:
Because no remaining vertex maps to the deleted leaf, \(f(R_{k+1})\subseteq R_{k+1}\); with final remaining set \(\{r,b\}\), closure and reachability force \(f(b)=r\).
hypotheses_or_conditions_needed:
The selected \(a_k\) is an \(R_k\)-leaf, \(f(a_k)\ne a_k\), and the induction hypotheses hold.
where_hypotheses_are_checked:
Step 3.
strength_used:
Well-defined encoding and final inverse comparison.
notes:
No Cayley formula or rooted-tree count is imported.

claim_id:
SL8
proof_location:
Final proof, Step 3, decoding construction.
claim_or_fact_used:
The decoding algorithm is well-defined for every word in \([n]^{n-2}\).
source_status: proved inside the current proof.
cited_label_or_name:
Suffix length count and parent-remains check.
exact_statement_used:
At step \(k\), some non-root remaining vertex is absent from a suffix of length \(n-k-1\); the letter \(w_k\) is neither the chosen vertex nor a previously removed vertex.
hypotheses_or_conditions_needed:
\(n\ge2\), \(1\le k\le n-2\), and the previous decoding choices.
where_hypotheses_are_checked:
Step 3.
strength_used:
Defines a function \(f:[n]\to[n]\) from each word.
notes:
This is the explicit inverse construction from S3, reproduced in S6.

claim_id:
SL9
proof_location:
Final proof, Step 3, decoded function verification.
claim_or_fact_used:
Every decoded function has \(r\) as its unique cyclic vertex.
source_status: proved inside the current proof.
cited_label_or_name:
Strictly increasing removal index.
exact_statement_used:
For every non-root vertex \(v\), the decoded value \(f(v)\) has strictly larger index, while \(f(r)=r\); hence all non-root orbits reach \(r\) and no non-root cycle exists.
hypotheses_or_conditions_needed:
The decoded edge assignments and the terminal assignments \(f(b)=r\), \(f(r)=r\).
where_hypotheses_are_checked:
Step 3.
strength_used:
Shows \(\Psi(w)\in\mathcal A_{n,r}\).
notes:
This proves membership directly.

claim_id:
SL10
proof_location:
Final proof, Step 3, inverse proof.
claim_or_fact_used:
The encoding and decoding maps are mutual inverses.
source_status: proved inside the current proof.
cited_label_or_name:
Leaf-suffix equivalence and decoded least-leaf property.
exact_statement_used:
For an encoded valid function, a remaining non-root vertex is a leaf exactly when it is absent from the remaining suffix; for a decoded function, the selected absent least vertex is exactly the least remaining leaf.
hypotheses_or_conditions_needed:
Encoding closure, terminal \(f(b)=r\), decoding choice rule, and decoded assignments.
where_hypotheses_are_checked:
Step 3 inverse arguments.
strength_used:
Establishes the bijection \(\mathcal A_{n,r}\cong[n]^{n-2}\).
notes:
This is the load-bearing fixed-root bijection.

claim_id:
SL11
proof_location:
Final proof, Step 3, final fixed-root count.
claim_or_fact_used:
There are \(n^{n-2}\) words of length \(n-2\) over \([n]\).
source_status: standard background fact.
cited_label_or_name:
Finite word count.
exact_statement_used:
For each of \(n-2\) positions there are \(n\) choices, so the word count is \(n^{n-2}\).
hypotheses_or_conditions_needed:
\([n]\) has \(n\) elements and \(n\ge2\).
where_hypotheses_are_checked:
Step 3 assumes \(n\ge2\) for the bijection.
strength_used:
Converts the bijection to \(|\mathcal A_{n,r}|=n^{n-2}\).
notes:
This is elementary finite multiplication.

claim_id:
SL12
proof_location:
Final proof, Step 4.
claim_or_fact_used:
The favorable event is the pairwise disjoint union of fixed-root events.
source_status: proved inside the current proof.
cited_label_or_name:
Unique-element unpacking and disjointness.
exact_statement_used:
\(A_n=\bigsqcup_{r\in[n]}A_{n,r}\), because a graph with a unique cyclic vertex has exactly one such vertex \(r\), and that \(r\) cannot be two distinct elements.
hypotheses_or_conditions_needed:
The definitions of \(A_n\), \(A_{n,r}\), and uniqueness.
where_hypotheses_are_checked:
Step 4.
strength_used:
Permits summing the fixed-root counts over \(r\).
notes:
This is the S4 assembly argument reproduced inside S6.

claim_id:
SL13
proof_location:
Final proof, Steps 4 and 5.
claim_or_fact_used:
Finite disjoint-union counting and elementary exponent arithmetic.
source_status: standard background fact.
cited_label_or_name:
Finite disjoint-union count; elementary arithmetic.
exact_statement_used:
For pairwise disjoint finite sets, the cardinality of the union is the sum of the cardinalities; \(n\cdot n^{n-2}=n^{n-1}\) for \(n\ge2\), \(1=1^{1-1}\), and \(n^{n-1}/n^n=1/n\).
hypotheses_or_conditions_needed:
The sets \(A_{n,r}\) are finite and pairwise disjoint; \(n\) is positive.
where_hypotheses_are_checked:
Finiteness follows from \(\mathcal F_n\) finite; disjointness is proved in Step 4; \(n\) is a standing positive integer.
strength_used:
The total favorable count and final probability simplification.
notes:
No unsupported imported enumeration is used.
