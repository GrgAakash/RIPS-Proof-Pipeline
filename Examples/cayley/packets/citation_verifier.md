You are the Citation Verifier.

Your task is to check whether the Source Ledger correctly accounts for every load-bearing
mathematical source used in the Solver's proof.

You are not verifying every mathematical step.
You are not repairing the proof.
You are not proving the target theorem.
You are not adding new mathematical content.

You are given:

1. the provided mathematical packet;
2. the target theorem;
3. the Allowed supporting statements list;
4. the additional mathematical guidance list, if any;
5. the Solver's proposed proof;
6. the Source Ledger produced by the Citation Generator;
7. the original paper's bibliography, .bib, or .bbl file, if supplied.

You may use internet only for restricted source checking.

Use the bibliography, .bib, or .bbl file only when the Solver proof, Citation Generator Source
Ledger, or supplied packet explicitly cites a label or named source, such as "[5]", "from
[6]", "\cite{...}", or a named external source. Do not use the bibliography to find new
theorems or proof support for an unsourced claim.

Use internet access only when an explicit citation label, bibliography entry, or named source
must be checked, including when the cited work is identified from the supplied bibliography
but the exact supporting theorem, definition, or location is not available from the supplied
materials. If a specialized, exact-hypothesis-heavy, niche, or research-level claim has no
explicit citation or named source and is not in the supplied packet, allowed supporting
statements, guidance list, genuinely standard background, or proved inside the current proof,
mark it "unsupported or unclear" rather than searching the web for a source.

When internet access is used, it must be citation-label-only source checking. Search only with
the bibliographic information for the cited entry or named source being checked: author names,
title, DOI, arXiv identifier, journal/book title, publisher data, or other identifiers from
that entry. Do not search the current paper title, current paper authors, target theorem,
theorem label, target statement, distinctive target phrases, or proof phrases.

If search results show the current target/source paper, ignore those results. Seeing a title
or snippet in search results does not itself count as target-source leakage, provided the
result is not opened, read beyond the search-result snippet, quoted, or used as evidence.
Target-source leakage is triggered only if you open, read, quote, or rely on the target/source
article outside the supplied packet. If the cited source can be found but the exact needed
theorem, definition, or location cannot be verified efficiently, mark the relevant entry as
external cited source with source_check_status: LOCATION_NOT_CHECKED or UNCLEAR, rather than
treating the target/source article as evidence.

If internet access is needed but unavailable, write:
SETUP FAILURE: internet access unavailable for citation checking.

Do NOT search for:

the target theorem itself;

the theorem label;

the original source of the target;

a proof of the target;

distinctive phrases from the target statement;

any original proof or solution.

If you open, read, quote, or rely on a source that appears to contain the target theorem's
proof or source article, stop and report:
"Possible target-source leakage encountered."

Your job is to check source hygiene.

For every Source Ledger entry, verify:

1. Does the proof actually use this claim or fact?
2. Is the source status correct?
3. If it is from the provided packet, does the cited item appear in the packet?
4. If it is an allowed supporting statement, does it appear in the Allowed supporting statements list?
5. If it is a guidance item, does it appear in the current guidance list?
6. If it is marked standard background, is it genuinely textbook-level or broadly standard for the field?
7. If it is specialized, niche, exact-hypothesis-heavy, or research-level, is it properly sourced externally or proved inside the proof?
8. If it is marked as proved inside the current proof, is the proof location actually present?
9. Is the exact statement used accurately?
10. Does the proof use the source at a stronger strength than stated?
11. Are the needed hypotheses or conditions visible and checked?
12. Are there any load-bearing claims in the proof missing from the Source Ledger?
13. For external cited sources, is source_check_status accurate: VERIFIED,
    BIBLIOGRAPHY_RESOLVED_ONLY, LOCATION_NOT_CHECKED, HYPOTHESES_NOT_CHECKED, UNCLEAR,
    INACCESSIBLE, or NOT_APPLICABLE?

Standard-background policy:

A fact may be accepted as standard background only if it is genuinely textbook-level or broadly
standard in the relevant area.

Examples that may usually be standard background:

* basic modular arithmetic;
* coefficient extraction for formal power series;
* Cauchy-Schwarz inequality;
* finite geometric series;
* standard derivative/product rules for formal power series, when properly stated;
* elementary set/counting identities.

Examples that should usually require external source checking or proof:

* specialized named theorems;
* exact q-series identities not supplied in the packet;
* research-level lemmas;
* exact constants or sharp estimates;
* nontrivial PDE/GMT/probability/combinatorics lemmas;
* claims attributed vaguely to "standard theory";
* statements that would normally need a citation in a research paper.

Produce exactly the following sections.

1. Source Ledger present?

State YES, NO, or UNCLEAR. If present, say where it appears.

2. Source inventory

Group all load-bearing sources as:

* provided definitions / notation / assumptions;
* allowed supporting statements;
* additional mathematical guidance items;
* standard background facts;
* proved inside the current proof;
* external cited sources;
* unsupported or unclear sources.

For each item, give the proof location where it is used.

3. Source accuracy check

For each source in the ledger, mark:

* ACCURATE;
* OVERSTRENGTHENED;
* MISQUOTED;
* WRONG SOURCE STATUS;
* HYPOTHESES NOT CHECKED;
* NOT FOUND;
* UNCLEAR.

Give one or two sentences explaining each non-ACCURATE mark.

4. Missing source entries

List every load-bearing claim used in the proof but missing from the Source Ledger. Empty list
is allowed.

5. Disallowed source check

List every cited or used source that is:

* the target theorem itself;
* equivalent to the target theorem;
* stronger than the target theorem;
* logically downstream from the target theorem;
* not in the Allowed supporting statements list;
* external to the supplied packet and not standard background;
* not proved inside the current proof;
* suspiciously found through target-source leakage.

For each, quote the proof sentence using it. Empty list is allowed.

6. Internet/source-check report

Internet used? YES / NO
Sources checked:
URLs or references checked:
Any source inaccessible? YES / NO
Possible target-source leakage encountered? YES / NO

7. Controller-facing summary

Citation gate result: GOOD_TO_GO / SOURCE_LEDGER_REPAIR_NEEDED / BLOCKING_SOURCE_ISSUE /
LEAKAGE_RISK / UNCLEAR
Source Ledger present? YES / NO / UNCLEAR
Missing source entries present? YES / NO / UNCLEAR
Disallowed sources present? YES / NO / UNCLEAR
Overstrengthened or misquoted sources present? YES / NO / UNCLEAR
Suspicious standard-background claims present? YES / NO / UNCLEAR
External source issue present? YES / NO / UNCLEAR
Citation-only repair needed? YES / NO / UNCLEAR
Substantive source issue present? YES / NO / UNCLEAR
Candidate guidance seed, if any: [one standalone forward-looking source issue for the
Decision Controller, or "None"]

Use GOOD_TO_GO only if the Source Ledger is present, every load-bearing mathematical source is
listed, every source status is correct, no cited source is disallowed, no source is used at
stronger strength than stated, all needed hypotheses are visible or checked, no suspicious
standard-background issue remains, and no target-source leakage occurred. If the result is not
GOOD_TO_GO, the verification cascade must not proceed to Verifier A.

Important:
Do not show this report to the next Solver. The Controller may log it privately. If the
Controller decides to add a mathematical item to the next Solver's guidance list, it must add
exactly one standalone guidance item according to the usual RIPS rule.

--- INPUTS FOR THIS RUN ---

Provided mathematical packet:
# 0. Macro Definitions

```tex
\newcommand{\sh}[2]{\mathrm{sh}_{#1}(#2)}
\newcommand{\cyc}[2]{\mathrm{cyc}_{#1}(#2)}
\newcommand{\Ccyc}[2]{\mathrm{Cyc}_{#1}(#2)}
\newcommand{\cF}{\mathcal{F}}
\renewcommand{\Pr}{\mathbb{P}}
\newcommand{\ba}{{\mathbf{a}}}
\newcommand{\bb}{{\mathbf{b}}}
\newcommand{\be}{{\mathbf{e}}}
\newcommand{\hE}{{\hat{E}}}
\newcommand{\hF}{{\hat{F}}}
\newcommand{\tO}{{\widetilde{O}}}
```

# 1. Notation and Conventions

Throughout, $n$ is a positive integer.

Elementary notation convention: $[n]$ denotes the finite set $\{1,2,\ldots,n\}$.

Elementary finite probability convention: a uniform random function $f:[n]\to[n]$ means a function chosen uniformly from the finite set of all functions from $[n]$ to $[n]$.

# 2. Standing Assumptions

$n$ is a positive integer.

# 3. Known External Results

None.

# 4. Definitions

Let $f:[n]\to[n]$, and let $G_f$ be its associated directed graph, with vertex set $[n]$ and directed edges $(i,f(i))$ for $i \in [n]$. A vertex is *cyclic* if it belongs to a cycle of $G_f$.

# 5. Available Results

No formal paper statement is granted as support under this definitions-only policy.

EXCLUDED under the run's definitions-only support policy:

The probability that a uniform random function $f:[n]\to [n]$ has a unique cyclic vertex is~$\frac{1}{n}$.

EXCLUDED under the run's definitions-only support policy:

Functions $f$ having a unique cyclic vertex are in bijection with rooted trees on $[n]$ (the unique cyclic vertex is the root, and edges are oriented towards the root).

EXCLUDED under the run's definitions-only support policy:

Cayley's formula asserts that there are $n^{n-2}$ trees on the vertex set $[n]$, or equivalently there are $n^{n-1}$ rooted trees.

EXCLUDED under the run's definitions-only support policy:

Let $H_n$ denote the height of a uniform random vertex in a uniform random rooted tree with $n$ vertices. Then $1+H_n$ has the same law as the time of first repetition in a i.i.d. sequence of uniform variables on~$[n]$ (time of first collision in the coupon collector process).

Target theorem:
The probability that a uniform random function $f:[n]\to [n]$ has a unique cyclic vertex is~$\frac{1}{n}$.


Allowed supporting statements:
# Allowed Support

The candidate may use without proof only definitions, notation, standing assumptions, genuinely elementary arithmetic, finite sets/functions, and finite probability basics.

Allowed without proof:

- The notation $[n]$ for the finite set $\{1,2,\ldots,n\}$.
- The standing assumption that $n$ is a positive integer.
- The definition of a function $f:[n]\to[n]$ and the finite set of all such functions.
- The elementary finite probability convention that a uniform random function is chosen uniformly from the finite set of all functions $[n]\to[n]$.
- The definition of the associated directed graph $G_f$ with vertex set $[n]$ and directed edges $(i,f(i))$ for $i\in[n]$.
- The definition of a cyclic vertex as a vertex belonging to a cycle of $G_f$.
- Genuinely elementary arithmetic, finite sets/functions, and finite probability basics.

Not granted:

- No formal paper statements are granted as support.
- The target statement is not granted as support.
- Equivalent tree counts are not granted as support.
- Any graph-tree correspondence is not granted as support.
- Any height-distribution statement is not granted as support.
- Every task-specific lemma must be proved in the candidate.
- No guidance is supplied.


Additional mathematical guidance:
None

Solver proposed proof:
## S0 artifact

1. Target decomposition

target_label:
unique_cyclic_vertex_probability

target_type:
finite-probability enumeration theorem

main_goal:
Prove that, for a uniformly chosen function \(f:[n]\to[n]\), the event that \(G_f\) has exactly one cyclic vertex has probability \(1/n\).

variables_and_parameters:
\(n\) is a positive integer. The sample space is the finite set \(\mathcal F_n\) of all functions \(f:[n]\to[n]\), with the uniform probability measure. For \(f\in\mathcal F_n\), \(G_f\) is the directed graph with edges \((i,f(i))\). A cyclic vertex is a vertex lying on a directed cycle of \(G_f\).

conclusion_to_prove:
\[
\Pr\bigl(\{f:[n]\to[n]\colon G_f\text{ has a unique cyclic vertex}\}\bigr)=\frac1n.
\]
Equivalently, since \(|\mathcal F_n|=n^n\), prove that exactly \(n^{n-1}\) functions \(f:[n]\to[n]\) have a unique cyclic vertex.

2. Available tools

tool:
finite function count

source_status: standard background fact

exact_statement_or_fact:
The number of functions from an \(n\)-element set to an \(n\)-element set is \(n^n\).

intended_role_in_proof:
Compute the denominator of the uniform finite probability.

tool:
unique cyclic vertex forces a fixed point

source_status: proved inside the current proof

exact_statement_or_fact:
If \(G_f\) has exactly one cyclic vertex \(r\), then \(f(r)=r\). Conversely, if the only directed cycle in \(G_f\) is the loop at \(r\), then \(r\) is the unique cyclic vertex.

intended_role_in_proof:
Reduce the target event to functions with one fixed cyclic root and no directed cycles away from it.

tool:
first hitting time to the cyclic part

source_status: proved inside the current proof

exact_statement_or_fact:
For every \(x\in[n]\), the sequence \(x,f(x),f^2(x),\ldots\) eventually repeats, and the repeated segment is a directed cycle. Hence if \(r\) is the unique cyclic vertex, every \(x\) reaches \(r\) after finitely many iterations of \(f\).

intended_role_in_proof:
Show that the unique-cyclic-root condition is equivalent to every non-root vertex eventually mapping into \(r\), with no non-root directed cycle.

tool:
recursive insertion count for rooted functional digraphs with one cyclic vertex

source_status: proved inside the current proof

exact_statement_or_fact:
For a fixed root \(r\in[n]\), the number of functions \(f:[n]\to[n]\) such that \(r\) is the unique cyclic vertex is \(n^{n-2}\) for \(n\ge 2\), and is \(1\) for \(n=1\).

intended_role_in_proof:
Provide the numerator after summing over the possible unique cyclic vertices.

tool:
summation over possible roots

source_status: standard background fact

exact_statement_or_fact:
If the sets of functions with unique cyclic vertex \(r\), for \(r\in[n]\), are pairwise disjoint and each has size \(n^{n-2}\) for \(n\ge 2\), then their union has size \(n\cdot n^{n-2}=n^{n-1}\).

intended_role_in_proof:
Combine the fixed-root count into the total count of favorable functions.

tool:
uniform finite probability

source_status: allowed supporting statement

exact_statement_or_fact:
A uniform random function is chosen uniformly from the finite set of all functions \([n]\to[n]\), so the probability of an event is the number of functions in the event divided by \(n^n\).

intended_role_in_proof:
Convert the enumeration into the claimed probability \(n^{n-1}/n^n=1/n\).

3. Subclaim support graph

id:
C1

statement:
The sample space of functions \(f:[n]\to[n]\) has size \(n^n\), and the target probability is the favorable count divided by \(n^n\).

uses_prior_subclaims:
None.

purpose:
Establish the denominator and the counting reduction.

status: standard background

suggested_solver: S1

id:
C2

statement:
If \(G_f\) has a unique cyclic vertex \(r\), then \(f(r)=r\), and every vertex \(x\in[n]\) reaches \(r\) after finitely many iterates of \(f\).

uses_prior_subclaims:
None.

purpose:
Translate the graph condition into a rooted functional condition.

status: must be proved in final proof

suggested_solver: S2

id:
C3

statement:
For each fixed \(r\in[n]\), the number of functions \(f:[n]\to[n]\) for which \(r\) is the unique cyclic vertex is \(n^{n-2}\) when \(n\ge2\), with the corresponding \(n=1\) count equal to \(1\).

uses_prior_subclaims:
C2.

purpose:
This is the main numerator count for one prescribed cyclic vertex.

status: must be proved in final proof

suggested_solver: S3

id:
C4

statement:
The sets of functions with unique cyclic vertex \(r\), as \(r\) ranges over \([n]\), are pairwise disjoint, and their union is exactly the event that \(G_f\) has a unique cyclic vertex.

uses_prior_subclaims:
C2.

purpose:
Justify summing the fixed-root count over all possible roots.

status: must be proved in final proof

suggested_solver: S4

id:
C5

statement:
The total number of functions \(f:[n]\to[n]\) with a unique cyclic vertex is \(n^{n-1}\).

uses_prior_subclaims:
C3, C4.

purpose:
Complete the favorable enumeration.

status: must be proved in final proof

suggested_solver: S4

id:
C6

statement:
Dividing the favorable count \(n^{n-1}\) by the total count \(n^n\) gives probability \(1/n\), including the case \(n=1\).

uses_prior_subclaims:
C1, C5.

purpose:
Finish the target theorem.

status: follows from allowed statement

suggested_solver: S5

4. Hardest step prediction

hardest_step_id:
C3

hardest_step_description:
The decisive step is proving from scratch that, for a fixed root \(r\), there are \(n^{n-2}\) functions whose only cyclic vertex is \(r\). Since the support policy explicitly excludes both the rooted-tree correspondence and Cayley's formula, the final proof cannot cite either one. It needs an internal enumeration, such as a Prüfer-code-style construction specialized to these rooted functional digraphs: encode each valid function by repeatedly removing the largest or otherwise canonically chosen non-root vertex with no incoming non-root dependents, recording its image, and prove that this gives a bijection with words of length \(n-2\) over \([n]\).

risk_if_wrong:
If this count is imported, asserted, or only justified by an excluded tree correspondence, the proof becomes unsupported. If the encoding is not bijective, the numerator can be wrong even if the probability conversion is correct.

how_final_proof_should_handle_it:
The final proof should give a complete finite bijection for the fixed-root count. It should define the class of functions with unique cyclic vertex \(r\), define the code map to \([n]^{n-2}\) for \(n\ge2\), define the inverse decoding algorithm, and prove termination, mutual inverse properties, and preservation of the unique-cyclic-root condition. The \(n=1\) case should be handled separately.

key_solver_id: S3

why_key_solver_is_decisive:
S3 supplies the only nontrivial enumeration. All other steps reduce the target to this count or perform finite-probability arithmetic.

5. Failure-mode checks

circularity_check:
Do not use the target probability, the excluded rooted-tree bijection, Cayley's formula, or any excluded height-distribution statement. The fixed-root count must be proved internally.

full_theorem_check:
The proof must cover every positive integer \(n\), including \(n=1\), not only \(n\ge2\). For \(n\ge2\), the numerator should be \(n\cdot n^{n-2}=n^{n-1}\); for \(n=1\), the single function has one cyclic vertex and probability \(1\).

source_check:
The only provided materials are definitions, notation, the finite uniform probability convention, and elementary finite arithmetic. No external source, graph-tree theorem, Cayley formula, or prior paper statement is available.

hypothesis_check:
The only hypothesis is that \(n\) is a positive integer. No connectedness, tree structure, or acyclicity condition may be assumed before it is proved from the unique-cyclic-vertex property.

notation_check:
Use \([n]\) for \(\{1,\ldots,n\}\), \(G_f\) for the associated directed graph, and "cyclic vertex" only in the supplied sense: a vertex belonging to a directed cycle of \(G_f\).

standard_background_check:
Allowed standard background may include finite pigeonhole reasoning, finite function counts, elementary disjoint-union counting, and finite probability arithmetic. It should not include named tree enumeration results or any graph-tree correspondence tailored to this problem.

6. Subproblem assignment table

S1:
Prove the denominator and probability-reduction facts: \(|\{f:[n]\to[n]\}|=n^n\), and under the uniform finite probability convention the desired probability equals the number of favorable functions divided by \(n^n\). Keep this independent of any graph enumeration.

S2:
Prove the structural facts about functional digraphs needed here. In particular, show that every forward orbit eventually enters a directed cycle; if \(G_f\) has a unique cyclic vertex \(r\), then \(f(r)=r\); and under that condition every vertex eventually reaches \(r\).

S3:
[KEY SOLVER] For a fixed \(r\in[n]\), prove from scratch that the number of functions \(f:[n]\to[n]\) for which \(r\) is the unique cyclic vertex is \(n^{n-2}\) for \(n\ge2\), and \(1\) for \(n=1\). Do not cite Cayley's formula or a rooted-tree correspondence. Give a complete direct bijection, preferably a Prüfer-code-style encoding and decoding, with words of length \(n-2\) over \([n]\).

S4:
Prove the disjoint-union numerator assembly: the event that \(G_f\) has a unique cyclic vertex is the disjoint union, over \(r\in[n]\), of the events that \(r\) is the unique cyclic vertex. Combine this with S3's fixed-root count to obtain \(n^{n-1}\) favorable functions.

S5:
Finish the theorem by dividing the favorable count by the total count. Verify explicitly that the arithmetic gives \(n^{n-1}/n^n=1/n\) for \(n\ge2\), and that the separate \(n=1\) case also gives probability \(1=1/n\).

7. Web-source confirmation

no web sources used


## S1 artifact

1. Assignment restatement

S-ID:
S1

assigned subclaim(s):
Prove the denominator and probability-reduction facts: \(|\{f:[n]\to[n]\}|=n^n\), and under the uniform finite probability convention the desired probability equals the number of favorable functions divided by \(n^n\).

what must be proved:
Let
\[
\mathcal F_n=\{f:[n]\to[n]\}
\]
and let
\[
A_n=\{f\in\mathcal F_n: G_f\text{ has a unique cyclic vertex}\}.
\]
One must prove that \(|\mathcal F_n|=n^n\) and that, for a uniform random function \(f:[n]\to[n]\),
\[
\Pr(A_n)=\frac{|A_n|}{n^n}.
\]

declared prerequisite subclaims:
None.

2. Subproof or failure

Because \([n]=\{1,2,\ldots,n\}\), the domain \([n]\) has exactly \(n\) elements, namely \(1,\ldots,n\), and the codomain \([n]\) also has exactly \(n\) elements.

Define
\[
\Phi:\mathcal F_n\to [n]^n,\qquad
\Phi(f)=(f(1),f(2),\ldots,f(n)).
\]
This map is injective: if \(\Phi(f)=\Phi(g)\), then \(f(i)=g(i)\) for every \(i\in[n]\), so \(f=g\) as functions. It is also surjective: given any ordered \(n\)-tuple \((a_1,\ldots,a_n)\in[n]^n\), the rule \(f(i)=a_i\) defines a function \(f:[n]\to[n]\) with \(\Phi(f)=(a_1,\ldots,a_n)\). Thus \(\Phi\) is a bijection between \(\mathcal F_n\) and \([n]^n\).

There are \(n\) choices for each coordinate of an element of \([n]^n\). By the elementary multiplication principle for finite choices,
\[
|[n]^n|=\underbrace{n\cdot n\cdots n}_{n\text{ factors}}=n^n.
\]
Therefore
\[
|\mathcal F_n|=n^n.
\]

Now let
\[
A_n=\{f\in\mathcal F_n: G_f\text{ has a unique cyclic vertex}\}.
\]
This is a subset of the finite sample space \(\mathcal F_n\). By the supplied uniform finite probability convention, a uniform random function is chosen uniformly from \(\mathcal F_n\). Hence each \(f\in\mathcal F_n\) has probability \(1/|\mathcal F_n|\), and by finite additivity over the subset \(A_n\),
\[
\Pr(A_n)=\frac{|A_n|}{|\mathcal F_n|}.
\]
Substituting \(|\mathcal F_n|=n^n\) gives
\[
\Pr(A_n)=\frac{|A_n|}{n^n}.
\]
This proves the assigned denominator and probability-reduction facts, independently of any enumeration of the functions in \(A_n\).

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

claim_id:
S1-1
proof_location:
Section 2, first paragraph.
claim_or_fact_used:
The set \([n]\) has exactly \(n\) elements.
source_status: provided definition / notation / assumption.
cited_label_or_name:
Notation \([n]\).
exact_statement_used:
\([n]=\{1,2,\ldots,n\}\), with \(n\) a positive integer.
hypotheses_or_conditions_needed:
\(n\) is a positive integer.
where_hypotheses_are_checked:
Standing assumption in the packet and assignment.
strength_used:
Only the cardinality of the finite set \([n]\).
notes:
This is independent of the directed graph structure.

claim_id:
S1-2
proof_location:
Section 2, definition and verification of \(\Phi\).
claim_or_fact_used:
The map \(f\mapsto(f(1),\ldots,f(n))\) is a bijection from the set of functions \([n]\to[n]\) to \([n]^n\).
source_status: proved inside the current proof.
cited_label_or_name:
Tuple encoding of a finite function.
exact_statement_used:
For functions on the finite domain \([n]\), equality of all values \(f(i)\) determines equality of functions; every tuple \((a_1,\ldots,a_n)\in[n]^n\) defines a function by \(f(i)=a_i\).
hypotheses_or_conditions_needed:
The domain is exactly \([n]=\{1,\ldots,n\}\), and every tuple coordinate lies in the codomain \([n]\).
where_hypotheses_are_checked:
Section 2, first paragraph and the construction of \(\Phi\).
strength_used:
A bijection sufficient to transfer cardinality from \([n]^n\) to \(\mathcal F_n\).
notes:
No graph-tree correspondence or graph enumeration is used.

claim_id:
S1-3
proof_location:
Section 2, multiplication-principle count of \([n]^n\).
claim_or_fact_used:
The finite Cartesian product \([n]^n\) has \(n^n\) elements.
source_status: standard background fact.
cited_label_or_name:
Elementary multiplication principle for finite choices.
exact_statement_used:
If there are \(n\) independent finite choices for each of \(n\) coordinates, the number of ordered \(n\)-tuples is \(n\cdot n\cdots n=n^n\).
hypotheses_or_conditions_needed:
Each coordinate has exactly \(n\) possible values, and there are exactly \(n\) coordinates.
where_hypotheses_are_checked:
Section 2, first paragraph and the definition of \([n]^n\).
strength_used:
Only the count \(|[n]^n|=n^n\).
notes:
This is elementary finite arithmetic and finite set counting.

claim_id:
S1-4
proof_location:
Section 2, conclusion \(|\mathcal F_n|=n^n\).
claim_or_fact_used:
The number of functions from \([n]\) to \([n]\) is \(n^n\).
source_status: proved inside the current proof.
cited_label_or_name:
Denominator count.
exact_statement_used:
Since \(\mathcal F_n\) is bijective with \([n]^n\) and \(|[n]^n|=n^n\), one has \(|\mathcal F_n|=n^n\).
hypotheses_or_conditions_needed:
\(n\) is a positive integer and \(\mathcal F_n=\{f:[n]\to[n]\}\).
where_hypotheses_are_checked:
Section 1 assignment restatement and Section 2.
strength_used:
The exact denominator for the uniform finite sample space.
notes:
This is the assigned sample-space count.

claim_id:
S1-5
proof_location:
Section 2, definition of \(A_n\).
claim_or_fact_used:
The favorable event is the subset \(A_n=\{f\in\mathcal F_n: G_f\text{ has a unique cyclic vertex}\}\).
source_status: provided definition / notation / assumption.
cited_label_or_name:
Definition of \(G_f\) and cyclic vertex.
exact_statement_used:
For \(f:[n]\to[n]\), \(G_f\) has vertex set \([n]\) and directed edges \((i,f(i))\); a cyclic vertex is a vertex belonging to a cycle of \(G_f\).
hypotheses_or_conditions_needed:
\(f\in\mathcal F_n\).
where_hypotheses_are_checked:
Section 2, definition of \(A_n\) as a subset of \(\mathcal F_n\).
strength_used:
Only the definition of the target event; no enumeration of \(A_n\).
notes:
This claim introduces the event whose probability is reduced to counting.

claim_id:
S1-6
proof_location:
Section 2, final probability computation.
claim_or_fact_used:
Under the uniform finite probability convention, the probability of a subset of the finite sample space equals its cardinality divided by the cardinality of the sample space.
source_status: allowed supporting statement.
cited_label_or_name:
Uniform finite probability convention.
exact_statement_used:
A uniform random function is chosen uniformly from the finite set of all functions \([n]\to[n]\), so for \(A_n\subseteq\mathcal F_n\), \(\Pr(A_n)=|A_n|/|\mathcal F_n|\).
hypotheses_or_conditions_needed:
\(\mathcal F_n\) is finite, the random function is uniform on \(\mathcal F_n\), and \(A_n\subseteq\mathcal F_n\).
where_hypotheses_are_checked:
Finiteness follows from S1-4; uniformity is supplied by the packet; subset membership is by the definition of \(A_n\).
strength_used:
Only the probability-reduction formula \(\Pr(A_n)=|A_n|/n^n\).
notes:
This does not require knowing \(|A_n|\).

5. Interface notes for S6

what this subproof establishes:
It establishes that the sample space \(\mathcal F_n=\{f:[n]\to[n]\}\) has size \(n^n\), and that the target probability is \(|A_n|/n^n\), where \(A_n\) is the set of functions whose associated directed graph has a unique cyclic vertex.

what remains conditional:
The value of \(|A_n|\) remains to be proved by other subclaims. This S1 proof does not establish the favorable count.

failure_output_type:
solved

candidate guidance sentence, if any:
None.

auxiliary lemma candidate, if any:
None.

notation introduced:
\(\mathcal F_n=\{f:[n]\to[n]\}\) and \(A_n=\{f\in\mathcal F_n: G_f\text{ has a unique cyclic vertex}\}\).

risk points:
S6 should not read this proof as proving any graph enumeration or any fixed-root count. It supplies only the denominator and the uniform finite probability reduction.

6. Web-source confirmation

no web sources used


## S2 artifact

1. Assignment restatement

S-ID:
S2

assigned subclaim(s):
Prove the structural facts about functional digraphs needed here:

- for every \(x\in[n]\), the forward orbit \(x,f(x),f^2(x),\ldots\) eventually enters a directed cycle;
- if \(G_f\) has a unique cyclic vertex \(r\), then \(f(r)=r\);
- under that unique-cyclic-vertex condition, every vertex \(x\in[n]\) reaches \(r\) after finitely many iterations of \(f\).

what must be proved:
For an arbitrary function \(f:[n]\to[n]\), the finiteness of \([n]\) forces every forward orbit to repeat, and a first repetition produces a directed cycle. If \(r\) is the unique cyclic vertex, then the cycle containing \(r\) must be the one-vertex loop at \(r\), so \(f(r)=r\). Finally, the cycle eventually reached by any vertex must have only cyclic vertices, hence must be the unique cyclic vertex \(r\).

declared prerequisite subclaims:
None.

2. Subproof or failure

Let \(f:[n]\to[n]\). For \(k\geq 0\), write \(f^0(x)=x\) and \(f^{k+1}(x)=f(f^k(x))\).

First fix \(x\in[n]\). The \(n+1\) vertices
\[
f^0(x), f^1(x),\ldots, f^n(x)
\]
all lie in the \(n\)-element set \([n]\). By the finite pigeonhole principle, two of them are equal. Let \(b\) be the least positive index for which there exists some \(a<b\) with \(f^a(x)=f^b(x)\), and choose such an \(a\). Then the vertices
\[
f^a(x), f^{a+1}(x),\ldots, f^{b-1}(x)
\]
are pairwise distinct: if \(f^i(x)=f^j(x)\) for some \(a\leq i<j<b\), then \(j\) would be a smaller positive repeated index than \(b\), contradicting the choice of \(b\). The directed edges in \(G_f\) send \(f^i(x)\) to \(f^{i+1}(x)\) for \(a\leq i<b-1\), and send \(f^{b-1}(x)\) to \(f^b(x)=f^a(x)\). Thus these vertices form a directed cycle. This proves that every forward orbit eventually enters a directed cycle.

Now suppose \(G_f\) has a unique cyclic vertex \(r\). Since \(r\) is cyclic, there is a directed cycle containing \(r\). Every vertex on that cycle is cyclic by definition. Because \(r\) is the unique cyclic vertex, no vertex distinct from \(r\) can occur on the cycle. Therefore the cycle through \(r\) has only the single vertex \(r\), and its edge is \((r,r)\). By the definition of \(G_f\), the outgoing edge from \(r\) is \((r,f(r))\), so \(f(r)=r\).

Finally take any \(x\in[n]\). By the first paragraph, the forward orbit of \(x\) eventually enters a directed cycle, say
\[
f^a(x), f^{a+1}(x),\ldots, f^{b-1}(x),
\]
with \(a<b\) and \(f^b(x)=f^a(x)\). Each vertex on this cycle is cyclic. Since \(r\) is the unique cyclic vertex, the cycle has no vertex other than \(r\). In particular \(f^a(x)=r\). Hence every vertex \(x\) reaches \(r\) after finitely many iterations of \(f\).

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

claim_id:
S2-L1

proof_location:
Assignment restatement; Subproof paragraph 1

claim_or_fact_used:
\([n]\) is the finite vertex set, \(f:[n]\to[n]\) is a function, \(G_f\) has directed edges \((i,f(i))\), and a cyclic vertex is a vertex belonging to a cycle of \(G_f\).

source_status:
provided definition / notation / assumption

cited_label_or_name:
Packet definitions: notation, associated directed graph, cyclic vertex

exact_statement_used:
\([n]=\{1,2,\ldots,n\}\); \(G_f\) has vertex set \([n]\) and directed edges \((i,f(i))\); a vertex is cyclic if it belongs to a cycle of \(G_f\).

hypotheses_or_conditions_needed:
\(n\) is a positive integer and \(f:[n]\to[n]\).

where_hypotheses_are_checked:
Subproof opening sentence.

strength_used:
Used exactly as definitions and notation.

notes:
No graph-tree correspondence or enumeration result is used.

claim_id:
S2-L2

proof_location:
Subproof paragraph 1

claim_or_fact_used:
Iterated notation \(f^0(x)=x\) and \(f^{k+1}(x)=f(f^k(x))\).

source_status:
proved inside the current proof

cited_label_or_name:
Definition introduced in proof

exact_statement_used:
For \(k\geq0\), define \(f^0(x)=x\) and \(f^{k+1}(x)=f(f^k(x))\).

hypotheses_or_conditions_needed:
\(f:[n]\to[n]\) and \(x\in[n]\).

where_hypotheses_are_checked:
Subproof opening sentence and first fixed-\(x\) sentence.

strength_used:
Only notation for forward orbits.

notes:
This is an internal definition, not an external fact.

claim_id:
S2-L3

proof_location:
Subproof paragraph 2

claim_or_fact_used:
Finite pigeonhole principle.

source_status:
standard background fact

cited_label_or_name:
Finite pigeonhole principle

exact_statement_used:
If \(n+1\) objects each lie in an \(n\)-element set, then two of the objects are equal.

hypotheses_or_conditions_needed:
The listed \(n+1\) iterates all lie in the \(n\)-element set \([n]\).

where_hypotheses_are_checked:
Subproof paragraph 2 notes that \(f^0(x),\ldots,f^n(x)\in[n]\) and \([n]\) has \(n\) elements.

strength_used:
Only existence of a repeated iterate.

notes:
This is elementary finite-set reasoning allowed by the packet.

claim_id:
S2-L4

proof_location:
Subproof paragraph 2

claim_or_fact_used:
A first repeated value in a forward orbit determines a directed cycle.

source_status:
proved inside the current proof

cited_label_or_name:
First-repetition cycle construction

exact_statement_used:
If \(b\) is the least positive repeated index and \(f^a(x)=f^b(x)\) with \(a<b\), then \(f^a(x),\ldots,f^{b-1}(x)\) are pairwise distinct and the directed edges of \(G_f\) close them into a directed cycle.

hypotheses_or_conditions_needed:
\(f:[n]\to[n]\), \(x\in[n]\), and the least repeated index \(b\) with \(f^a(x)=f^b(x)\).

where_hypotheses_are_checked:
Subproof paragraph 2 constructs \(a,b\) after applying the finite pigeonhole principle.

strength_used:
Used to prove that every forward orbit eventually enters a directed cycle.

notes:
The proof is internal and does not use any graph-tree theorem.

claim_id:
S2-L5

proof_location:
Subproof paragraph 3

claim_or_fact_used:
If \(G_f\) has a unique cyclic vertex \(r\), then \(f(r)=r\).

source_status:
proved inside the current proof

cited_label_or_name:
Unique cyclic vertex forces loop

exact_statement_used:
The directed cycle containing \(r\) cannot contain any vertex distinct from \(r\); hence it is the one-vertex cycle with edge \((r,r)\), so \(f(r)=r\).

hypotheses_or_conditions_needed:
\(G_f\) has a unique cyclic vertex \(r\).

where_hypotheses_are_checked:
Subproof paragraph 3 begins with this assumption.

strength_used:
Used exactly to identify the unique cyclic vertex as a fixed point.

notes:
This does not assume any enumeration or rooted-tree correspondence.

claim_id:
S2-L6

proof_location:
Subproof paragraph 4

claim_or_fact_used:
If \(G_f\) has a unique cyclic vertex \(r\), then every vertex reaches \(r\) after finitely many iterations of \(f\).

source_status:
proved inside the current proof

cited_label_or_name:
All orbits reach the unique cyclic vertex

exact_statement_used:
The eventual cycle reached by the forward orbit of any \(x\in[n]\) consists only of cyclic vertices, so under uniqueness it must consist only of \(r\); therefore \(f^a(x)=r\) for some finite \(a\).

hypotheses_or_conditions_needed:
\(G_f\) has a unique cyclic vertex \(r\), \(x\in[n]\), and the first-repetition cycle construction.

where_hypotheses_are_checked:
Subproof paragraph 4 invokes the unique-cyclic-vertex assumption and applies S2-L4 to arbitrary \(x\in[n]\).

strength_used:
Used exactly to establish finite hitting of \(r\) by every vertex.

notes:
This proves only the assigned structural direction, not the fixed-root enumeration.

5. Interface notes for S6

what this subproof establishes:
For any \(f:[n]\to[n]\), every forward orbit eventually enters a directed cycle. If \(G_f\) has a unique cyclic vertex \(r\), then \(f(r)=r\), and every \(x\in[n]\) has \(f^a(x)=r\) for some finite \(a\geq0\).

what remains conditional:
Nothing inside S2 remains conditional. Later counting steps must still prove their own fixed-root enumeration and disjoint-union assembly.

failure_output_type:
solved

candidate guidance sentence, if any:
None.

auxiliary lemma candidate, if any:
None.

notation introduced:
\(f^0(x)=x\) and \(f^{k+1}(x)=f(f^k(x))\).

risk points:
The proof uses the finite pigeonhole principle and the first repeated index in a finite forward orbit. It does not prove or use the excluded rooted-tree correspondence, Cayley's formula, or the target probability.

6. Web-source confirmation

no web sources used


## S3 artifact

1. Assignment restatement

S-ID:
S3

assigned subclaim(s):
C3.

what must be proved:
For a fixed \(r\in[n]\), the number of functions \(f:[n]\to[n]\) for which \(r\) is the unique cyclic vertex is \(n^{n-2}\) when \(n\ge2\), and is \(1\) when \(n=1\).

declared prerequisite subclaims:
None. The proof below reproves the needed finite-orbit and fixed-root facts internally rather than assuming another S-solver's output.

2. Subproof or failure

Fix \(r\in[n]\). Let
\[
\mathcal A_{n,r}=\{f:[n]\to[n]\colon r\text{ is the unique cyclic vertex of }G_f\}.
\]

First consider \(n=1\). Then \([1]=\{1\}\), \(r=1\), and there is exactly one function \(f:[1]\to[1]\), namely \(f(1)=1\). Its graph has the single loop \((1,1)\), so \(1\) is its unique cyclic vertex. Hence \(|\mathcal A_{1,1}|=1\).

Now assume \(n\ge2\). We construct a bijection
\[
\Phi:\mathcal A_{n,r}\longrightarrow [n]^{n-2}.
\]

We first record two elementary consequences of \(f\in\mathcal A_{n,r}\). Since \(r\) is cyclic, it lies on some directed cycle. No vertex other than \(r\) is cyclic, so that cycle has length \(1\), and therefore \(f(r)=r\). Also, for any \(x\in[n]\), the finite sequence
\[
x,\ f(x),\ f^2(x),\ldots
\]
has two equal terms. The segment between the first repeated value and its return is a directed cycle in \(G_f\). Since \(r\) is the only cyclic vertex, this eventual cycle is the loop at \(r\). Thus every vertex reaches \(r\) after finitely many applications of \(f\).

For a subset \(R\subseteq[n]\) containing \(r\), say that a vertex \(a\in R\setminus\{r\}\) is an \(R\)-leaf for \(f\) if no vertex \(y\in R\setminus\{a\}\) satisfies \(f(y)=a\). In the situations below, \(f(a)\ne a\), so this is the same as saying that no vertex of \(R\) maps to \(a\).

For \(f\in\mathcal A_{n,r}\), define \(\Phi(f)=(w_1,\ldots,w_{n-2})\) as follows. Start with \(R_1=[n]\). At step \(k\), where \(1\le k\le n-2\), choose \(a_k\) to be the least element, in the ordinary order on \([n]\), among the \(R_k\)-leaves in \(R_k\setminus\{r\}\). Put
\[
w_k=f(a_k),
\]
and set \(R_{k+1}=R_k\setminus\{a_k\}\).

This encoding is well-defined. We prove this by induction on the step. Initially \(R_1=[n]\), and after previous removals suppose that \(r\in R_k\), that \(f(R_k)\subseteq R_k\), and that every element of \(R_k\) reaches \(r\) by iterating \(f\). These properties are true for \(k=1\). If \(R_k\setminus\{r\}\) had no \(R_k\)-leaf, then for each \(u\in R_k\setminus\{r\}\) one could choose \(p(u)\in R_k\setminus\{u\}\) with \(f(p(u))=u\). Repeatedly applying \(p\) inside the finite set \(R_k\setminus\{r\}\) would repeat a value and hence produce a directed cycle for \(f\) entirely inside \(R_k\setminus\{r\}\), contradicting that every element of \(R_k\) eventually reaches the loop at \(r\). Thus an \(R_k\)-leaf exists, and the least one exists because \(R_k\setminus\{r\}\) is finite and nonempty at all steps \(k\le n-2\). Since \(a_k\ne r\), \(f(a_k)\ne a_k\), and because \(f(R_k)\subseteq R_k\), we have \(f(a_k)\in R_k\setminus\{a_k\}\). Hence \(f(R_{k+1})\subseteq R_{k+1}\). The reachability of \(r\) for the vertices left in \(R_{k+1}\) is inherited from \(R_k\), since no remaining vertex maps to \(a_k\). This proves the induction.

After \(n-2\) removals, \(R_{n-1}\) has two elements, namely \(r\) and one non-root element \(b\). Since \(f(R_{n-1})\subseteq R_{n-1}\), \(f(r)=r\), and \(b\) reaches \(r\), we have \(f(b)=r\).

We now define the inverse map
\[
\Psi:[n]^{n-2}\longrightarrow \mathcal A_{n,r}.
\]
Given a word \(w=(w_1,\ldots,w_{n-2})\), start with \(R_1=[n]\). For each \(k=1,\ldots,n-2\), choose \(a_k\) to be the least element of \(R_k\setminus\{r\}\) that does not occur among the remaining letters
\[
w_k,w_{k+1},\ldots,w_{n-2}.
\]
Such an element exists because \(|R_k\setminus\{r\}|=n-k\), while the displayed suffix has length \(n-k-1\). Define
\[
f(a_k)=w_k,
\]
and put \(R_{k+1}=R_k\setminus\{a_k\}\). This assignment is consistent because \(w_k\ne a_k\), and \(w_k\) has not been removed earlier: if \(w_k=a_j\) for some \(j<k\), then \(a_j\) would have occurred in the suffix \(w_j,\ldots,w_{n-2}\), contrary to how \(a_j\) was chosen. Hence \(w_k\in R_k\setminus\{a_k\}\).

At the end two vertices remain, \(r\) and one vertex \(b\ne r\). Define
\[
f(b)=r,\qquad f(r)=r.
\]
This gives a function \(f:[n]\to[n]\).

The decoded function belongs to \(\mathcal A_{n,r}\). Give each removed vertex \(a_k\) the removal index \(k\), give the final non-root vertex \(b\) index \(n-1\), and give \(r\) index \(n\). If \(v\ne r\), then \(f(v)\) has strictly larger index than \(v\): this was shown above for removed vertices, and for \(b\) it holds because \(f(b)=r\). Therefore repeated application of \(f\) starting from any non-root vertex strictly increases this index until it reaches \(r\). Thus every non-root vertex reaches \(r\), while \(r\) is fixed. The only directed cycle is the loop at \(r\), so \(r\) is the unique cyclic vertex.

It remains to prove that \(\Phi\) and \(\Psi\) are inverse maps.

First take \(f\in\mathcal A_{n,r}\) and let \(\Phi(f)=w\), with removed vertices \(a_1,\ldots,a_{n-2}\). At encoding step \(k\), for any \(y\in R_k\setminus\{r\}\), the following equivalence holds:
\[
y\text{ is an }R_k\text{-leaf}\quad\Longleftrightarrow\quad
y\text{ does not occur in }w_k,\ldots,w_{n-2}.
\]
Indeed, if \(y\) occurs as \(w_j=f(a_j)\) for some \(j\ge k\), then the still-unremoved vertex \(a_j\in R_k\setminus\{y\}\) maps to \(y\), so \(y\) is not an \(R_k\)-leaf. Conversely, if \(y\) is not an \(R_k\)-leaf, choose \(z\in R_k\setminus\{y\}\) with \(f(z)=y\). The remaining set is closed under \(f\), the only two vertices left after all removals are \(r\) and \(b\), and \(f(r)=f(b)=r\); hence this \(z\) cannot be \(r\) or the final \(b\) unless \(y=r\), which is excluded. Therefore \(z=a_j\) for some \(j\ge k\), and \(w_j=f(a_j)=y\). Thus the least \(R_k\)-leaf selected by the encoding is exactly the least non-root element missing from the current suffix, which is the vertex the decoding algorithm selects. Since both algorithms then assign \(f(a_k)=w_k\) and remove the same \(a_k\), induction over \(k\) shows that \(\Psi(\Phi(f))=f\), including the final assignments \(f(b)=r\) and \(f(r)=r\).

Conversely take a word \(w\in[n]^{n-2}\), and let \(\Psi(w)=f\), with decoded vertices \(a_1,\ldots,a_{n-2}\). At step \(k\), the vertex \(a_k\) is an \(R_k\)-leaf for the decoded function: it does not appear in \(w_k,\ldots,w_{n-2}\), so no later removed vertex maps to it, and the final vertex \(b\) and root \(r\) both map to \(r\). If \(y\in R_k\setminus\{r\}\) and \(y<a_k\), then by the choice of \(a_k\), \(y\) occurs in the suffix \(w_k,\ldots,w_{n-2}\). Hence some vertex still present at step \(k\) maps to \(y\), so \(y\) is not an \(R_k\)-leaf. Therefore \(a_k\) is the least \(R_k\)-leaf, exactly the vertex selected by the encoding algorithm. The encoding records \(f(a_k)=w_k\) at every step, so \(\Phi(\Psi(w))=w\).

Thus \(\Phi\) is a bijection from \(\mathcal A_{n,r}\) to \([n]^{n-2}\). Since a word of length \(n-2\) over the \(n\)-element alphabet \([n]\) has \(n^{n-2}\) possibilities, \(|\mathcal A_{n,r}|=n^{n-2}\) for \(n\ge2\). Together with the separate \(n=1\) case, this proves C3.

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

claim_id:
L1
proof_location:
Section 2, first paragraph after definition of \(\mathcal A_{n,r}\)
claim_or_fact_used:
For \(n=1\), there is exactly one function \([1]\to[1]\), and its graph has the loop at \(1\).
source_status:
proved inside the current proof
cited_label_or_name:
finite functions; definition of \(G_f\)
exact_statement_used:
The only function from the one-element set \(\{1\}\) to itself sends \(1\) to \(1\), giving the directed edge \((1,1)\).
hypotheses_or_conditions_needed:
\(n=1\) and \(r=1\).
where_hypotheses_are_checked:
Section 2, \(n=1\) case.
strength_used:
Exact count \(|\mathcal A_{1,1}|=1\).
notes:
No external enumeration is used.

claim_id:
L2
proof_location:
Section 2, paragraph beginning "We first record two elementary consequences"
claim_or_fact_used:
If \(f\in\mathcal A_{n,r}\), then \(f(r)=r\).
source_status:
proved inside the current proof
cited_label_or_name:
unique cyclic vertex implies root loop
exact_statement_used:
Since \(r\) lies on a directed cycle and no other vertex is cyclic, the cycle containing \(r\) has length \(1\), so \(f(r)=r\).
hypotheses_or_conditions_needed:
\(r\) is the unique cyclic vertex of \(G_f\).
where_hypotheses_are_checked:
Definition of \(\mathcal A_{n,r}\).
strength_used:
Only the fixed point identity \(f(r)=r\).
notes:
This is proved directly from the definition of cyclic vertex.

claim_id:
L3
proof_location:
Section 2, same paragraph as L2
claim_or_fact_used:
Every vertex reaches \(r\) under iteration when \(f\in\mathcal A_{n,r}\).
source_status:
proved inside the current proof
cited_label_or_name:
finite orbit repetition
exact_statement_used:
In a finite set, the sequence \(x,f(x),f^2(x),\ldots\) repeats; the repeated segment is a directed cycle; since \(r\) is the only cyclic vertex, that cycle is the loop at \(r\).
hypotheses_or_conditions_needed:
\([n]\) finite and \(r\) is the unique cyclic vertex.
where_hypotheses_are_checked:
Definitions and \(\mathcal A_{n,r}\).
strength_used:
Reachability of \(r\) from every vertex.
notes:
Uses only finite pigeonhole reasoning.

claim_id:
L4
proof_location:
Section 2, paragraph beginning "This encoding is well-defined"
claim_or_fact_used:
At every encoding step, a non-root leaf exists.
source_status:
proved inside the current proof
cited_label_or_name:
finite predecessor contradiction
exact_statement_used:
If every non-root remaining vertex had an incoming edge from another remaining non-root vertex, choosing one predecessor for each and iterating inside the finite non-root set would produce a directed cycle away from \(r\), contradicting reachability to \(r\).
hypotheses_or_conditions_needed:
\(R_k\) finite, \(r\in R_k\), \(f(R_k)\subseteq R_k\), and every element of \(R_k\) reaches \(r\).
where_hypotheses_are_checked:
Induction in the encoding well-definedness proof.
strength_used:
Existence of at least one removable non-root leaf.
notes:
This is a direct finite argument, not a tree-counting theorem.

claim_id:
L5
proof_location:
Section 2, encoding well-definedness induction
claim_or_fact_used:
After removing a leaf, the remaining set is still closed under \(f\), and remaining vertices still reach \(r\).
source_status:
proved inside the current proof
cited_label_or_name:
closure after leaf removal
exact_statement_used:
If no remaining vertex maps to \(a_k\), then deleting \(a_k\) removes no image of a still-remaining vertex; hence \(f(R_{k+1})\subseteq R_{k+1}\), and old paths to \(r\) do not pass through \(a_k\).
hypotheses_or_conditions_needed:
\(a_k\) is an \(R_k\)-leaf and \(f(R_k)\subseteq R_k\).
where_hypotheses_are_checked:
Definition of \(a_k\) in the encoding algorithm and induction hypothesis.
strength_used:
Maintains the encoding algorithm until two vertices remain.
notes:
Elementary finite functional reasoning.

claim_id:
L6
proof_location:
Section 2, paragraph after the encoding induction
claim_or_fact_used:
After \(n-2\) removals, the final non-root vertex \(b\) satisfies \(f(b)=r\).
source_status:
proved inside the current proof
cited_label_or_name:
two-vertex terminal step
exact_statement_used:
The remaining set is \(\{r,b\}\), is closed under \(f\), \(f(r)=r\), and \(b\) reaches \(r\), so \(f(b)=r\).
hypotheses_or_conditions_needed:
\(R_{n-1}=\{r,b\}\), closure, and reachability to \(r\).
where_hypotheses_are_checked:
Encoding construction and preceding induction.
strength_used:
Used in inverse and leaf-suffix equivalence.
notes:
No external fact.

claim_id:
L7
proof_location:
Section 2, inverse map definition
claim_or_fact_used:
At each decoding step, a least non-root element absent from the current suffix exists.
source_status:
proved inside the current proof
cited_label_or_name:
suffix length count
exact_statement_used:
At step \(k\), \(|R_k\setminus\{r\}|=n-k\), while the suffix \(w_k,\ldots,w_{n-2}\) has length \(n-k-1\), so some non-root remaining vertex is absent.
hypotheses_or_conditions_needed:
\(n\ge2\), \(1\le k\le n-2\), and previous removals removed one non-root vertex each.
where_hypotheses_are_checked:
Inverse algorithm.
strength_used:
Well-defined choice of \(a_k\).
notes:
Uses only finite counting.

claim_id:
L8
proof_location:
Section 2, inverse map definition
claim_or_fact_used:
The assigned value \(w_k\) remains in \(R_k\setminus\{a_k\}\).
source_status:
proved inside the current proof
cited_label_or_name:
decoded parent remains
exact_statement_used:
\(w_k\ne a_k\) because \(a_k\) is absent from the current suffix, and \(w_k\) cannot have been removed earlier because an earlier removed vertex was absent from the earlier suffix containing \(w_k\).
hypotheses_or_conditions_needed:
The decoding choice rule for \(a_j\), \(j\le k\).
where_hypotheses_are_checked:
Inverse algorithm.
strength_used:
Ensures the decoded edges point to vertices still present after deletion.
notes:
This prevents circular or backward decoded edges.

claim_id:
L9
proof_location:
Section 2, paragraph beginning "The decoded function belongs"
claim_or_fact_used:
The decoded function has \(r\) as unique cyclic vertex.
source_status:
proved inside the current proof
cited_label_or_name:
strictly increasing removal index
exact_statement_used:
For every non-root vertex, \(f(v)\) has larger removal index, so iterating \(f\) reaches \(r\); with \(f(r)=r\), the only directed cycle is the loop at \(r\).
hypotheses_or_conditions_needed:
Decoding construction and the parent-remains property L8.
where_hypotheses_are_checked:
Inverse construction.
strength_used:
Shows \(\Psi(w)\in\mathcal A_{n,r}\).
notes:
This is the main preservation proof for the inverse map.

claim_id:
L10
proof_location:
Section 2, paragraph beginning "First take \(f\in\mathcal A_{n,r}\)"
claim_or_fact_used:
For an encoded valid function, a non-root remaining vertex is a leaf exactly when it is absent from the remaining code suffix.
source_status:
proved inside the current proof
cited_label_or_name:
leaf-suffix equivalence
exact_statement_used:
\(y\) appears in the suffix precisely when some still-unremoved vertex maps to \(y\); the final non-root vertex and \(r\) both map to \(r\).
hypotheses_or_conditions_needed:
Encoding algorithm, closure of remaining sets, and L6.
where_hypotheses_are_checked:
Encoding construction and terminal step.
strength_used:
Used to prove \(\Psi(\Phi(f))=f\).
notes:
The equivalence is proved directly, not cited.

claim_id:
L11
proof_location:
Section 2, paragraph beginning "Conversely take a word"
claim_or_fact_used:
For a decoded word, the encoding algorithm removes the same vertices and records the same letters.
source_status:
proved inside the current proof
cited_label_or_name:
decoded least-leaf property
exact_statement_used:
The chosen \(a_k\) has no incoming edge from remaining vertices, while every smaller non-root remaining vertex appears in the suffix and therefore has an incoming edge from a still-present vertex.
hypotheses_or_conditions_needed:
Decoding choice rule and decoded edge assignments.
where_hypotheses_are_checked:
Inverse algorithm.
strength_used:
Used to prove \(\Phi(\Psi(w))=w\).
notes:
Elementary canonical-choice argument.

claim_id:
L12
proof_location:
Section 2, final paragraph
claim_or_fact_used:
There are \(n^{n-2}\) words of length \(n-2\) over \([n]\).
source_status:
standard background fact
cited_label_or_name:
finite word count
exact_statement_used:
For each of \(n-2\) positions there are \(n\) independent choices from \([n]\), so the number of words is \(n^{n-2}\).
hypotheses_or_conditions_needed:
\([n]\) has \(n\) elements and \(n\ge2\).
where_hypotheses_are_checked:
Standing notation and \(n\ge2\) case.
strength_used:
Converts the bijection into the desired count.
notes:
This is basic finite multiplication, not Cayley's formula.

5. Interface notes for S6

what this subproof establishes:
For every fixed \(r\in[n]\), the class of functions \(f:[n]\to[n]\) for which \(r\) is the unique cyclic vertex has size \(n^{n-2}\) for \(n\ge2\), and size \(1\) for \(n=1\). The proof gives explicit mutually inverse encoding and decoding algorithms between this class and words in \([n]^{n-2}\).

what remains conditional:
Nothing inside C3. The global theorem still needs the other assigned subclaims for denominator, disjoint-union assembly, and final probability arithmetic.

failure_output_type:
solved

candidate guidance sentence, if any:
None.

auxiliary lemma candidate, if any:
None.

notation introduced:
\(\mathcal A_{n,r}\) for the fixed-root class; \(R_k\) for the remaining vertex set during encoding/decoding; \(a_k\) for the removed vertex at step \(k\); \(w_k\) for the recorded parent; \(b\) for the last non-root vertex.

risk points:
The final proof should preserve the leaf-suffix equivalence and the proof that decoded edges always point to still-present vertices. Those are the key places where an unsupported appeal to a rooted-tree correspondence or Cayley's formula must not be substituted.

6. Web-source confirmation

no web sources used


## S4 artifact

# 1. Assignment restatement

S-ID:
S4

assigned subclaim(s):
C4 and C5.

what must be proved:
Let
\[
\mathcal F_n=\{f:[n]\to[n]\}
\]
and let
\[
A=\{f\in\mathcal F_n: G_f\text{ has a unique cyclic vertex}\}.
\]
For each \(r\in[n]\), let
\[
A_r=\{f\in\mathcal F_n: r\text{ is the unique cyclic vertex of }G_f\}.
\]
Prove that
\[
A=\bigsqcup_{r\in[n]}A_r.
\]
Then, using the fixed-root enumeration supplied as prerequisite C3, prove that the number of favorable functions is \(n^{n-1}\).

declared prerequisite subclaims:
C3: For each fixed \(r\in[n]\), the number of functions \(f:[n]\to[n]\) for which \(r\) is the unique cyclic vertex is \(n^{n-2}\) when \(n\ge2\), with the corresponding \(n=1\) count equal to \(1\).

# 2. Subproof or failure

Define \(\mathcal F_n\), \(A\), and \(A_r\) as in Section 1.

First, \(A\subseteq\bigcup_{r\in[n]}A_r\). Indeed, if \(f\in A\), then \(G_f\) has a unique cyclic vertex. Since all vertices of \(G_f\) lie in \([n]\), that unique cyclic vertex is some element \(r\in[n]\). By the definition of \(A_r\), this means \(f\in A_r\).

Second, \(\bigcup_{r\in[n]}A_r\subseteq A\). If \(f\in A_r\) for some \(r\in[n]\), then, by the definition of \(A_r\), \(r\) is the unique cyclic vertex of \(G_f\). Hence \(G_f\) has a unique cyclic vertex, so \(f\in A\).

Thus
\[
A=\bigcup_{r\in[n]}A_r.
\]

This union is disjoint. If \(r,s\in[n]\) with \(r\ne s\), then no function \(f\) can lie in both \(A_r\) and \(A_s\). Membership in \(A_r\) says that the unique cyclic vertex of \(G_f\) is \(r\), while membership in \(A_s\) says that the unique cyclic vertex of \(G_f\) is \(s\). A unique element cannot be equal to two distinct elements, so \(A_r\cap A_s=\varnothing\). Therefore
\[
A=\bigsqcup_{r\in[n]}A_r.
\]

It remains to assemble the count using prerequisite C3.

If \(n=1\), then \([n]=\{1\}\), so the above disjoint union has the single part \(A_1\). By C3, \(|A_1|=1\). Hence
\[
|A|=1=1^{\,1-1}=n^{n-1}.
\]

If \(n\ge2\), then by C3, for each \(r\in[n]\),
\[
|A_r|=n^{n-2}.
\]
Since the sets \(A_r\) are pairwise disjoint and there are \(n\) choices of \(r\in[n]\), finite disjoint-union counting gives
\[
|A|
=\sum_{r\in[n]}|A_r|
=\sum_{r\in[n]} n^{n-2}
=n\cdot n^{n-2}
=n^{n-1}.
\]

Thus, conditional on prerequisite C3, the total number of functions \(f:[n]\to[n]\) for which \(G_f\) has a unique cyclic vertex is \(n^{n-1}\).

# 3. Solver failure output and candidate guidance

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

# 4. Local Source Ledger

claim_id:
S4-L1

proof_location:
Section 2, definitions of \(\mathcal F_n\), \(A\), and \(A_r\).

claim_or_fact_used:
\(\mathcal F_n\) is the finite set of all functions \(f:[n]\to[n]\), \(A\) is the event that \(G_f\) has a unique cyclic vertex, and \(A_r\) is the event that \(r\) is the unique cyclic vertex of \(G_f\).

source_status:
provided definition / notation / assumption

cited_label_or_name:
Definitions of \([n]\), \(f:[n]\to[n]\), \(G_f\), and cyclic vertex.

exact_statement_used:
\([n]=\{1,\ldots,n\}\); \(G_f\) has vertex set \([n]\) and directed edges \((i,f(i))\); a cyclic vertex is a vertex belonging to a cycle of \(G_f\).

hypotheses_or_conditions_needed:
\(n\) is a positive integer and \(f:[n]\to[n]\).

where_hypotheses_are_checked:
Standing assumption and the definition of \(\mathcal F_n\) in Section 2.

strength_used:
Only the definitions are used.

notes:
No external graph-theoretic enumeration is used here.

claim_id:
S4-L2

proof_location:
Section 2, proof that \(A\subseteq\bigcup_{r\in[n]}A_r\).

claim_or_fact_used:
If \(G_f\) has a unique cyclic vertex, then that vertex is some \(r\in[n]\), and \(f\in A_r\).

source_status:
proved inside the current proof

cited_label_or_name:
Unique-element unpacking.

exact_statement_used:
For a property on elements of the finite vertex set \([n]\), if exactly one vertex has that property, then there exists \(r\in[n]\) which is that unique vertex.

hypotheses_or_conditions_needed:
The vertices of \(G_f\) are exactly \([n]\), and \(G_f\) has a unique cyclic vertex.

where_hypotheses_are_checked:
By the definition of \(G_f\) and the assumption \(f\in A\).

strength_used:
Only existence of the unique cyclic vertex.

notes:
This is elementary finite set reasoning.

claim_id:
S4-L3

proof_location:
Section 2, proof that \(\bigcup_{r\in[n]}A_r\subseteq A\).

claim_or_fact_used:
If \(f\in A_r\) for some \(r\in[n]\), then \(G_f\) has a unique cyclic vertex.

source_status:
proved inside the current proof

cited_label_or_name:
Definition of \(A_r\).

exact_statement_used:
Membership \(f\in A_r\) means that \(r\) is the unique cyclic vertex of \(G_f\).

hypotheses_or_conditions_needed:
\(r\in[n]\) and \(f\in A_r\).

where_hypotheses_are_checked:
At the start of the inclusion proof.

strength_used:
The definition gives the desired event directly.

notes:
No structural fact about functional digraphs is needed.

claim_id:
S4-L4

proof_location:
Section 2, proof of pairwise disjointness.

claim_or_fact_used:
For \(r\ne s\), \(A_r\cap A_s=\varnothing\).

source_status:
proved inside the current proof

cited_label_or_name:
Uniqueness contradiction.

exact_statement_used:
The unique cyclic vertex of a given graph cannot be both \(r\) and \(s\) when \(r\ne s\).

hypotheses_or_conditions_needed:
\(r,s\in[n]\) and \(r\ne s\).

where_hypotheses_are_checked:
At the start of the disjointness proof.

strength_used:
Only uniqueness of the cyclic vertex is used.

notes:
This proves the union is a disjoint union.

claim_id:
S4-L5

proof_location:
Section 2, count of \(|A_r|\).

claim_or_fact_used:
For each fixed \(r\in[n]\), \(|A_r|=n^{n-2}\) when \(n\ge2\), and \(|A_1|=1\) when \(n=1\).

source_status:
unsupported or unclear

cited_label_or_name:
Declared prerequisite subclaim C3.

exact_statement_used:
For each fixed \(r\in[n]\), the number of functions \(f:[n]\to[n]\) for which \(r\) is the unique cyclic vertex is \(n^{n-2}\) when \(n\ge2\), with the corresponding \(n=1\) count equal to \(1\).

hypotheses_or_conditions_needed:
\(r\in[n]\); for the formula \(n^{n-2}\), \(n\ge2\); for the separate count, \(n=1\).

where_hypotheses_are_checked:
The proof splits into the cases \(n=1\) and \(n\ge2\), and \(r\) ranges over \([n]\).

strength_used:
Exactly the fixed-root cardinality statement is used.

notes:
This is not proved in S4 and is not treated as an allowed supporting statement. The S4 numerator assembly is conditional on this declared prerequisite.

claim_id:
S4-L6

proof_location:
Section 2, finite disjoint-union count.

claim_or_fact_used:
For a finite pairwise disjoint family \(\{A_r:r\in[n]\}\), the cardinality of the union is the sum of the cardinalities.

source_status:
standard background fact

cited_label_or_name:
Finite disjoint-union counting.

exact_statement_used:
If \(I\) is finite and the sets \(B_i\) for \(i\in I\) are pairwise disjoint, then \(\left|\bigsqcup_{i\in I}B_i\right|=\sum_{i\in I}|B_i|\).

hypotheses_or_conditions_needed:
The index set \([n]\) is finite and the sets \(A_r\) are pairwise disjoint.

where_hypotheses_are_checked:
\([n]\) is finite by notation, and pairwise disjointness is proved in Section 2.

strength_used:
Only the finite disjoint-union cardinality formula.

notes:
This is elementary finite set arithmetic.

claim_id:
S4-L7

proof_location:
Section 2, final arithmetic.

claim_or_fact_used:
\(\sum_{r\in[n]} n^{n-2}=n\cdot n^{n-2}=n^{n-1}\) for \(n\ge2\), and \(1=1^{1-1}\) for \(n=1\).

source_status:
standard background fact

cited_label_or_name:
Elementary exponent arithmetic.

exact_statement_used:
There are \(n\) elements in \([n]\); the sum of \(n\) equal terms \(n^{n-2}\) is \(n\cdot n^{n-2}\); for \(n\ge2\), \(n\cdot n^{n-2}=n^{n-1}\); and \(1^0=1\).

hypotheses_or_conditions_needed:
\(n\) is a positive integer, with the displayed exponent identity used in the case \(n\ge2\).

where_hypotheses_are_checked:
Standing assumption and the explicit case split in Section 2.

strength_used:
Only elementary arithmetic.

notes:
No probability calculation is performed in S4.

# 5. Interface notes for S6

what this subproof establishes:
It proves that the favorable event is the pairwise disjoint union of the fixed-root events \(A_r\), \(r\in[n]\). It also proves that, conditional on C3's fixed-root count, the number of favorable functions is \(n^{n-1}\).

what remains conditional:
The fixed-root enumeration C3 remains conditional from S4's perspective. S4 does not prove that \(|A_r|=n^{n-2}\) for \(n\ge2\), nor the separate \(n=1\) fixed-root count.

failure_output_type:
solved

candidate guidance sentence, if any:
None.

auxiliary lemma candidate, if any:
None.

notation introduced:
\(\mathcal F_n\), \(A\), and \(A_r\).

risk points:
The final proof must not present the \(n^{n-2}\) fixed-root count as coming from S4. It must cite or include S3's proof before using the count. For \(n=1\), the assembly uses the separate C3 count \(|A_1|=1\), not the expression \(n^{n-2}\).

# 6. Web-source confirmation

no web sources used


## S5 artifact

1. Assignment restatement

S-ID:
S5

assigned subclaim(s):
C6: divide the favorable count by the total count and verify the resulting probability is \(1/n\), with the \(n=1\) case checked separately.

what must be proved:
Assuming the total sample-space count and the favorable-function count from the declared prerequisites, prove that a uniform random function \(f:[n]\to[n]\) has a unique cyclic vertex with probability \(1/n\).

declared prerequisite subclaims:
C1: the sample space of functions \(f:[n]\to[n]\) has size \(n^n\), and uniform finite probability is favorable count divided by \(n^n\).

C5: the total number of functions \(f:[n]\to[n]\) with a unique cyclic vertex is \(n^{n-1}\) for \(n\ge 2\), and in the separate case \(n=1\) the favorable count is \(1\).

2. Subproof or failure

Let
\[
\mathcal F_n=\{f:[n]\to[n]\}
\]
and let
\[
E_n=\{f\in\mathcal F_n: G_f\text{ has a unique cyclic vertex}\}.
\]

By the declared prerequisite C1, \(|\mathcal F_n|=n^n\), and because the random function is chosen uniformly from \(\mathcal F_n\),
\[
\Pr(E_n)=\frac{|E_n|}{|\mathcal F_n|}=\frac{|E_n|}{n^n}.
\]

First suppose \(n\ge 2\). By the declared prerequisite C5, \(|E_n|=n^{n-1}\). Therefore
\[
\Pr(E_n)=\frac{n^{n-1}}{n^n}.
\]
Since \(n\) is positive and \(n^n=n\cdot n^{n-1}\), cancellation gives
\[
\frac{n^{n-1}}{n^n}=\frac{n^{n-1}}{n\cdot n^{n-1}}=\frac1n.
\]
Thus the desired probability is \(1/n\) for every \(n\ge2\).

Now suppose \(n=1\). By C5, the favorable count is \(|E_1|=1\). By C1, the sample-space size is \(|\mathcal F_1|=1^1=1\). Hence
\[
\Pr(E_1)=\frac{|E_1|}{|\mathcal F_1|}=\frac11=1.
\]
Since \(1/n=1/1=1\) when \(n=1\), the asserted probability also holds in this case.

The cases \(n=1\) and \(n\ge2\) cover all positive integers \(n\). Therefore, conditional on the declared prerequisites C1 and C5, the probability that a uniform random function \(f:[n]\to[n]\) has a unique cyclic vertex is \(1/n\).

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

claim_id:
L1

proof_location:
Section 2, first displayed probability computation

claim_or_fact_used:
The set \(\mathcal F_n\) of functions \(f:[n]\to[n]\) has size \(n^n\).

source_status:
standard background fact

cited_label_or_name:
finite function count; declared prerequisite C1

exact_statement_used:
For finite \([n]\) with \(n\) elements, the number of functions from \([n]\) to \([n]\) is \(n^n\).

hypotheses_or_conditions_needed:
\(n\) is a positive integer and \([n]=\{1,\ldots,n\}\).

where_hypotheses_are_checked:
Standing assumption and notation in the packet; restated at the start of the target theorem.

strength_used:
Only the denominator count \(|\mathcal F_n|=n^n\).

notes:
This is also one of the declared C1 prerequisite facts for S5.

claim_id:
L2

proof_location:
Section 2, first displayed probability computation

claim_or_fact_used:
For a uniform finite probability space, the probability of an event is its cardinality divided by the sample-space cardinality.

source_status:
allowed supporting statement

cited_label_or_name:
uniform finite probability convention; declared prerequisite C1

exact_statement_used:
A uniform random function is chosen uniformly from the finite set of all functions \([n]\to[n]\), so \(\Pr(E_n)=|E_n|/|\mathcal F_n|\).

hypotheses_or_conditions_needed:
\(\mathcal F_n\) is finite and the random function is uniform on \(\mathcal F_n\).

where_hypotheses_are_checked:
Allowed supporting statements and notation in the packet.

strength_used:
Only the formula \(\Pr(E_n)=|E_n|/|\mathcal F_n|\).

notes:
No graph enumeration is used here.

claim_id:
L3

proof_location:
Section 2, \(n\ge2\) paragraph and \(n=1\) paragraph

claim_or_fact_used:
The favorable count is \(|E_n|=n^{n-1}\) for \(n\ge2\), and \(|E_1|=1\) for \(n=1\).

source_status:
unsupported or unclear

cited_label_or_name:
declared prerequisite C5

exact_statement_used:
The total number of functions \(f:[n]\to[n]\) for which \(G_f\) has a unique cyclic vertex is \(n^{n-1}\) for \(n\ge2\), with separate \(n=1\) favorable count \(1\).

hypotheses_or_conditions_needed:
\(n\) is a positive integer, and the event \(E_n\) is defined as functions whose associated graph \(G_f\) has a unique cyclic vertex.

where_hypotheses_are_checked:
The standing assumption gives \(n\ge1\), and \(E_n\) is defined in Section 2 using the packet definition of \(G_f\) and cyclic vertex.

strength_used:
Exactly the favorable count needed for the numerator.

notes:
This claim is not proved by S5 and is not an allowed standalone support statement. It is listed as a declared prerequisite subclaim for this finishing step.

claim_id:
L4

proof_location:
Section 2, \(n\ge2\) arithmetic paragraph

claim_or_fact_used:
For \(n\ge2\), \(n^{n-1}/n^n=1/n\).

source_status:
proved inside the current proof

cited_label_or_name:
elementary exponent arithmetic and cancellation

exact_statement_used:
Since \(n^n=n\cdot n^{n-1}\) and \(n^{n-1}\ne0\), \(\frac{n^{n-1}}{n^n}=\frac1n\).

hypotheses_or_conditions_needed:
\(n\ge2\), hence \(n\) and \(n^{n-1}\) are nonzero positive integers.

where_hypotheses_are_checked:
The proof treats the case \(n\ge2\) explicitly.

strength_used:
Only this single quotient simplification.

notes:
No counting theorem is hidden in this arithmetic step.

claim_id:
L5

proof_location:
Section 2, \(n=1\) paragraph

claim_or_fact_used:
For \(n=1\), the probability is \(1=1/n\).

source_status:
proved inside the current proof

cited_label_or_name:
elementary arithmetic in the \(n=1\) case

exact_statement_used:
If \(|E_1|=1\) and \(|\mathcal F_1|=1\), then \(\Pr(E_1)=1/1=1\), and \(1/n=1/1=1\).

hypotheses_or_conditions_needed:
\(n=1\), C1's denominator count, and C5's separate favorable count for \(n=1\).

where_hypotheses_are_checked:
The proof treats \(n=1\) explicitly and invokes the declared prerequisites C1 and C5.

strength_used:
Only the equality of the claimed probability in the one-point case.

notes:
This verifies that the theorem does not omit the endpoint case \(n=1\).

5. Interface notes for S6

what this subproof establishes:
Assuming C1 and C5, the desired probability is obtained by finite uniform probability division. For \(n\ge2\), the arithmetic is \(n^{n-1}/n^n=1/n\). For \(n=1\), the favorable count and total count are both \(1\), so the probability is \(1=1/n\).

what remains conditional:
The subproof depends on C1 for the denominator and uniform-probability formula, and on C5 for the total favorable count. S5 does not prove the fixed-root enumeration, disjoint union over roots, or any graph-structure lemma.

failure_output_type:
solved

candidate guidance sentence, if any:
None.

auxiliary lemma candidate, if any:
None.

notation introduced:
\(\mathcal F_n\) for the finite set of all functions \([n]\to[n]\); \(E_n\) for the event/set of functions whose \(G_f\) has a unique cyclic vertex.

risk points:
S6 should not treat S5 as proving C5. The load-bearing numerator count must come from a valid proof of C5 elsewhere, not from this finishing arithmetic step.

6. Web-source confirmation

no web sources used


## S6 artifact

1. Composition map

S0 blueprint used? YES, for organization and hardest-step targeting only; it is not used as a mathematical premise.

S1-S5 outputs used: [S1, S2, S3, S4, S5]

Subclaims solved:
C1, C2, C3, C4, C5, C6. The final proof reproves the needed statements inline, with the fixed-root enumeration expanded as a direct Prufer-style bijection.

Subclaims unsolved or conditional:
None.

Auxiliary lemma candidates proposed by S1-S5:
None.

[KEY STEP] source: S3

2. Final proof
<!-- BEGIN_FINAL_PROOF -->
We prove the theorem by counting functions. Let
\[
\mathcal F_n=\{f:[n]\to[n]\}
\]
and let
\[
A_n=\{f\in\mathcal F_n: G_f\text{ has a unique cyclic vertex}\}.
\]

1. The sample-space count and probability reduction.
The map
\[
f\longmapsto (f(1),f(2),\ldots,f(n))
\]
is a bijection from \(\mathcal F_n\) to the set of \(n\)-tuples in \([n]^n\): the values \(f(1),\ldots,f(n)\) determine \(f\), and every \(n\)-tuple in \([n]^n\) determines such a function. Since each of the \(n\) coordinates has \(n\) choices,
\[
|\mathcal F_n|=n^n.
\]
By the supplied uniform finite probability convention,
\[
\Pr(A_n)=\frac{|A_n|}{|\mathcal F_n|}=\frac{|A_n|}{n^n}.
\]
It remains to prove that \(|A_n|=n^{n-1}\).

2. Basic orbit structure.
For \(f:[n]\to[n]\), define \(f^0(x)=x\) and \(f^{k+1}(x)=f(f^k(x))\). For any fixed \(x\in[n]\), the \(n+1\) elements
\[
f^0(x),f^1(x),\ldots,f^n(x)
\]
lie in the \(n\)-element set \([n]\), so two are equal. Choose \(b>0\) minimal such that \(f^a(x)=f^b(x)\) for some \(a<b\). Then
\[
f^a(x),f^{a+1}(x),\ldots,f^{b-1}(x)
\]
are pairwise distinct, and the directed edges of \(G_f\) carry each listed vertex to the next one, with \(f^{b-1}(x)\) mapping back to \(f^a(x)\). Thus every forward orbit eventually enters a directed cycle.

If \(G_f\) has a unique cyclic vertex \(r\), then the cycle containing \(r\) cannot contain any vertex distinct from \(r\). Hence that cycle is the one-vertex loop at \(r\), so \(f(r)=r\). Also, the eventual cycle reached by any \(x\in[n]\) consists of cyclic vertices, so under the same uniqueness hypothesis it must be the loop at \(r\). Therefore every vertex reaches \(r\) after finitely many iterations of \(f\).

3. [KEY STEP] Fixed-root enumeration.
Fix \(r\in[n]\), and let
\[
\mathcal A_{n,r}=\{f:[n]\to[n]\colon r\text{ is the unique cyclic vertex of }G_f\}.
\]
We prove that \(|\mathcal A_{n,r}|=n^{n-2}\) for \(n\ge2\), and that \(|\mathcal A_{1,1}|=1\).

If \(n=1\), then \([1]=\{1\}\), \(r=1\), and the only function \([1]\to[1]\) satisfies \(f(1)=1\). Its graph has the single loop at \(1\), so \(|\mathcal A_{1,1}|=1\).

Assume now that \(n\ge2\). We construct a bijection
\[
\Phi:\mathcal A_{n,r}\to [n]^{n-2}.
\]
For a subset \(R\subseteq[n]\) containing \(r\), call \(a\in R\setminus\{r\}\) an \(R\)-leaf if no vertex \(y\in R\setminus\{a\}\) has \(f(y)=a\).

Given \(f\in\mathcal A_{n,r}\), start with \(R_1=[n]\). At step \(k=1,\ldots,n-2\), choose \(a_k\) to be the least \(R_k\)-leaf in \(R_k\setminus\{r\}\), set
\[
w_k=f(a_k),
\]
and put \(R_{k+1}=R_k\setminus\{a_k\}\). We claim this is well-defined. Suppose at the beginning of a step that \(r\in R_k\), \(f(R_k)\subseteq R_k\), and every element of \(R_k\) reaches \(r\). These properties hold initially by Step 2. If no \(R_k\)-leaf existed in \(R_k\setminus\{r\}\), then for every \(u\in R_k\setminus\{r\}\) there would be a vertex \(p(u)\in R_k\setminus\{u\}\) with \(f(p(u))=u\). Since \(f(r)=r\), this \(p(u)\) also lies in \(R_k\setminus\{r\}\). Iterating \(p\) inside the finite set \(R_k\setminus\{r\}\) would eventually repeat, producing a directed cycle for \(f\) entirely outside \(r\), a contradiction because every element of \(R_k\) reaches the loop at \(r\). Thus a non-root \(R_k\)-leaf exists, and the least one exists by finiteness.

For the chosen \(a_k\), we have \(f(a_k)\ne a_k\), since otherwise \(a_k\ne r\) would be cyclic. Because \(a_k\) is an \(R_k\)-leaf, no vertex of \(R_k\) maps to \(a_k\). Therefore deleting \(a_k\) preserves \(f(R_{k+1})\subseteq R_{k+1}\). The remaining vertices still reach \(r\): a path from a remaining vertex to \(r\) cannot pass through \(a_k\), since that would require some remaining vertex to map to \(a_k\). This proves the induction and hence the encoding is defined through step \(n-2\). After these removals, \(R_{n-1}=\{r,b\}\) for one non-root vertex \(b\). Since \(f(R_{n-1})\subseteq R_{n-1}\), \(f(r)=r\), and \(b\) reaches \(r\), we have \(f(b)=r\). The encoded word is
\[
\Phi(f)=(w_1,\ldots,w_{n-2})\in[n]^{n-2}.
\]

We now define an inverse decoding map. Given a word
\[
w=(w_1,\ldots,w_{n-2})\in[n]^{n-2},
\]
start with \(R_1=[n]\). For \(k=1,\ldots,n-2\), choose \(a_k\) to be the least element of \(R_k\setminus\{r\}\) that does not occur among the suffix letters
\[
w_k,w_{k+1},\ldots,w_{n-2}.
\]
Such an element exists because \(R_k\setminus\{r\}\) has \(n-k\) elements, while this suffix has length \(n-k-1\). Define \(f(a_k)=w_k\) and put \(R_{k+1}=R_k\setminus\{a_k\}\). This assignment is legitimate: \(w_k\ne a_k\) because \(a_k\) is absent from the suffix containing \(w_k\); and \(w_k\) has not been removed earlier, for if \(w_k=a_j\) with \(j<k\), then \(a_j\) would have appeared in the suffix \(w_j,\ldots,w_{n-2}\), contradicting the choice of \(a_j\). Hence \(w_k\in R_k\setminus\{a_k\}\).

After the \(n-2\) steps, the remaining set is \(\{r,b\}\) for one non-root vertex \(b\). Define
\[
f(b)=r,\qquad f(r)=r.
\]
This gives a function \(f:[n]\to[n]\). Assign index \(k\) to \(a_k\), index \(n-1\) to \(b\), and index \(n\) to \(r\). For every \(v\ne r\), the vertex \(f(v)\) has strictly larger index than \(v\). Therefore repeated application of \(f\) from any non-root vertex strictly increases this index until it reaches \(r\), while \(r\) is fixed. Thus the only directed cycle is the loop at \(r\), so the decoded function belongs to \(\mathcal A_{n,r}\). Call this decoding map \(\Psi:[n]^{n-2}\to\mathcal A_{n,r}\).

It remains to show that \(\Phi\) and \(\Psi\) are inverse maps. First let \(f\in\mathcal A_{n,r}\), let \(\Phi(f)=w\), and use the remaining sets \(R_k\) from the encoding. At any step \(k\), for \(y\in R_k\setminus\{r\}\),
\[
y\text{ is an }R_k\text{-leaf}
\quad\Longleftrightarrow\quad
y\text{ does not occur among }w_k,\ldots,w_{n-2}.
\]
If \(y=w_j=f(a_j)\) for some \(j\ge k\), then the still-present vertex \(a_j\ne y\) maps to \(y\), so \(y\) is not an \(R_k\)-leaf. Conversely, if \(y\) is not an \(R_k\)-leaf, choose \(z\in R_k\setminus\{y\}\) with \(f(z)=y\). Since \(y\ne r\), this \(z\) cannot be \(r\); and from the terminal observation above it cannot be the final non-root vertex \(b\), because \(f(b)=r\). Thus \(z=a_j\) for some \(j\ge k\), and \(w_j=f(a_j)=y\). The encoding and decoding algorithms therefore choose the same least vertex at each step, assign the same value there, and remove the same vertex. Induction on \(k\) gives \(\Psi(\Phi(f))=f\), including the final assignments \(f(b)=r\) and \(f(r)=r\).

Conversely, let \(w\in[n]^{n-2}\), let \(\Psi(w)=f\), and let \(a_1,\ldots,a_{n-2}\) be the decoded vertices. At step \(k\), the vertex \(a_k\) is an \(R_k\)-leaf for the decoded function: it does not occur in the suffix \(w_k,\ldots,w_{n-2}\), so no later removed vertex maps to it, and the final vertices \(b\) and \(r\) both map to \(r\). If \(y\in R_k\setminus\{r\}\) and \(y<a_k\), then the choice of \(a_k\) forces \(y\) to occur in the suffix \(w_k,\ldots,w_{n-2}\), so some still-present vertex maps to \(y\). Hence no smaller non-root remaining vertex is an \(R_k\)-leaf. The encoding of \(f\) therefore removes exactly \(a_k\) at step \(k\) and records \(f(a_k)=w_k\). Hence \(\Phi(\Psi(w))=w\).

Thus \(\Phi\) is a bijection from \(\mathcal A_{n,r}\) to \([n]^{n-2}\). There are \(n^{n-2}\) words of length \(n-2\) over the \(n\)-element alphabet \([n]\), so
\[
|\mathcal A_{n,r}|=n^{n-2}\qquad(n\ge2).
\]

4. Assembly over the possible cyclic vertices.
For each \(r\in[n]\), let
\[
A_{n,r}=\{f\in\mathcal F_n: r\text{ is the unique cyclic vertex of }G_f\}.
\]
Then
\[
A_n=\bigsqcup_{r\in[n]} A_{n,r}.
\]
Indeed, every function in \(A_n\) has a unique cyclic vertex, and that vertex is some \(r\in[n]\), so the function lies in \(A_{n,r}\). Conversely, membership in some \(A_{n,r}\) means precisely that \(G_f\) has a unique cyclic vertex. The union is disjoint because one function cannot have two different unique cyclic vertices.

If \(n=1\), then \(A_n=A_{1,1}\), so \(|A_n|=1=1^{1-1}=n^{n-1}\). If \(n\ge2\), then the fixed-root count from Step 3 gives \(|A_{n,r}|=n^{n-2}\) for every \(r\in[n]\). Since there are \(n\) possible roots and the union is disjoint,
\[
|A_n|=\sum_{r\in[n]} |A_{n,r}|
=\sum_{r\in[n]} n^{n-2}
=n\cdot n^{n-2}
=n^{n-1}.
\]
Thus \(|A_n|=n^{n-1}\) for every positive integer \(n\).

5. Final probability computation.
Substituting the favorable count into the uniform finite probability formula gives
\[
\Pr(A_n)=\frac{|A_n|}{n^n}
=\frac{n^{n-1}}{n^n}
=\frac{n^{n-1}}{n\cdot n^{n-1}}
=\frac1n.
\]
Therefore the probability that a uniform random function \(f:[n]\to[n]\) has a unique cyclic vertex is \(1/n\), as claimed.
<!-- END_FINAL_PROOF -->

3. Composer failure output and candidate guidance
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

4. Source Ledger
<!-- BEGIN_SOURCE_LEDGER -->
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
<!-- END_SOURCE_LEDGER -->

5. Completion checklist
<!-- BEGIN_COMPLETION_CHECKLIST -->
Did the proof prove the exact target theorem?
Yes. It proves that the probability that a uniform random function \(f:[n]\to[n]\) has a unique cyclic vertex is \(1/n\) for every positive integer \(n\).

Did the proof avoid citing or assuming the target theorem?
Yes.

Were all allowed supporting statements cited correctly?
Yes. The proof uses only the supplied definitions, notation, standing assumption, and uniform finite probability convention without proof.

Were all nontrivial imported sources accounted for?
Yes. No external sources are imported. Standard finite-set facts are named and recorded in the source ledger.

Were all hypotheses claimed or identified before applying allowed statements?
Yes.

Was the [KEY STEP] expanded in detail?
Yes. The fixed-root count is proved by an explicit encoding, decoding, and mutual-inverse proof.

Were all introduced objects defined?
Yes. \(\mathcal F_n\), \(A_n\), \(\mathcal A_{n,r}\), \(A_{n,r}\), \(R_k\), \(a_k\), \(w_k\), \(b\), \(\Phi\), and \(\Psi\) are defined before use.

Were all cases and quantifiers covered?
Yes. The proof treats \(n=1\) separately for the fixed-root count and covers all \(n\ge2\); together these cover all positive integers.

Were standard background facts named and explained?
Yes. The finite pigeonhole principle, finite multiplication principle, finite disjoint-union counting, and elementary exponent arithmetic are named and their uses are stated.

Did the proof use only the provided packet, allowed support, guidance, current-round S1-S5 subproof artifacts, standard background, or facts proved inside the proof?
Yes.
<!-- END_COMPLETION_CHECKLIST -->

6. Web-source confirmation
<!-- BEGIN_WEB_SOURCE_CONFIRMATION -->
no web sources used
<!-- END_WEB_SOURCE_CONFIRMATION -->

7. LaTeX artifact

The standalone proof artifact is `final_proof.tex`. PDF rendering was not performed by S6 because the controller instruction says not to compile a PDF in this role.


## Submitted standalone LaTeX proof

```tex
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm}
\usepackage[margin=1in]{geometry}

\newtheorem*{theorem}{Theorem}

\begin{document}

\begin{theorem}
Let \(n\) be a positive integer. The probability that a uniform random function
\(f:[n]\to[n]\) has a unique cyclic vertex in its associated directed graph \(G_f\)
is \(1/n\).
\end{theorem}

\begin{proof}
Let
\[
\mathcal F_n=\{f:[n]\to[n]\}
\]
and let
\[
A_n=\{f\in\mathcal F_n: G_f\text{ has a unique cyclic vertex}\}.
\]
The map \(f\mapsto(f(1),\ldots,f(n))\) is a bijection from \(\mathcal F_n\) to
\([n]^n\), so \(|\mathcal F_n|=n^n\). By the uniform finite probability
convention,
\[
\Pr(A_n)=\frac{|A_n|}{|\mathcal F_n|}=\frac{|A_n|}{n^n}.
\]
It remains to count \(|A_n|\).

First record a finite-orbit fact. For \(f:[n]\to[n]\), define \(f^0(x)=x\) and
\(f^{k+1}(x)=f(f^k(x))\). For any \(x\in[n]\), the \(n+1\) vertices
\[
f^0(x),f^1(x),\ldots,f^n(x)
\]
lie in the \(n\)-element set \([n]\), so two are equal. If \(b>0\) is the least
index for which \(f^a(x)=f^b(x)\) for some \(a<b\), then
\[
f^a(x),f^{a+1}(x),\ldots,f^{b-1}(x)
\]
are pairwise distinct and form a directed cycle in \(G_f\). Hence every forward
orbit eventually enters a directed cycle. If \(G_f\) has a unique cyclic vertex
\(r\), then the cycle through \(r\) has only the vertex \(r\), so \(f(r)=r\).
Moreover, the eventual cycle reached by any vertex must be the loop at \(r\);
therefore every vertex reaches \(r\) after finitely many iterations of \(f\).

\medskip
\noindent\textbf{[KEY STEP].} Fix \(r\in[n]\), and set
\[
\mathcal A_{n,r}=\{f:[n]\to[n]\colon r\text{ is the unique cyclic vertex of }G_f\}.
\]
We prove that \(|\mathcal A_{n,r}|=n^{n-2}\) for \(n\ge2\), and that
\(|\mathcal A_{1,1}|=1\). If \(n=1\), the only function \([1]\to[1]\) has the
single loop at \(1\), so \(|\mathcal A_{1,1}|=1\).

Assume \(n\ge2\). We construct a bijection
\[
\Phi:\mathcal A_{n,r}\to [n]^{n-2}.
\]
For \(R\subseteq[n]\) containing \(r\), call \(a\in R\setminus\{r\}\) an
\(R\)-leaf if no vertex \(y\in R\setminus\{a\}\) has \(f(y)=a\).

Given \(f\in\mathcal A_{n,r}\), start with \(R_1=[n]\). For
\(k=1,\ldots,n-2\), choose \(a_k\) to be the least \(R_k\)-leaf in
\(R_k\setminus\{r\}\), set \(w_k=f(a_k)\), and put
\(R_{k+1}=R_k\setminus\{a_k\}\). This is well-defined. Indeed, suppose at the
beginning of a step that \(r\in R_k\), that \(f(R_k)\subseteq R_k\), and that
every vertex of \(R_k\) reaches \(r\). If no non-root \(R_k\)-leaf existed, then
for every \(u\in R_k\setminus\{r\}\) there would be a vertex
\(p(u)\in R_k\setminus\{u\}\) with \(f(p(u))=u\). Since \(f(r)=r\), this
\(p(u)\) lies in \(R_k\setminus\{r\}\). Iterating \(p\) in the finite set
\(R_k\setminus\{r\}\) would repeat and produce a directed cycle for \(f\)
entirely outside \(r\), contradicting the fact that every remaining vertex
reaches \(r\). Thus a least non-root \(R_k\)-leaf exists.

For such a leaf \(a_k\), one has \(f(a_k)\ne a_k\), since otherwise
\(a_k\ne r\) would be cyclic. Thus no vertex of \(R_k\) maps to \(a_k\), and
deleting \(a_k\) preserves \(f(R_{k+1})\subseteq R_{k+1}\). The remaining
vertices still reach \(r\), because a path from a remaining vertex to \(r\)
cannot pass through \(a_k\) without some remaining vertex mapping to \(a_k\).
The induction continues until two vertices remain, \(R_{n-1}=\{r,b\}\), and then
closure, \(f(r)=r\), and reachability force \(f(b)=r\). Define
\[
\Phi(f)=(w_1,\ldots,w_{n-2}).
\]

Conversely, given \(w=(w_1,\ldots,w_{n-2})\in[n]^{n-2}\), start with
\(R_1=[n]\). For \(k=1,\ldots,n-2\), choose \(a_k\) to be the least element of
\(R_k\setminus\{r\}\) that does not occur among
\[
w_k,w_{k+1},\ldots,w_{n-2}.
\]
Such an element exists because \(R_k\setminus\{r\}\) has \(n-k\) elements and
the suffix has length \(n-k-1\). Define \(f(a_k)=w_k\) and set
\(R_{k+1}=R_k\setminus\{a_k\}\). The assignment is legitimate: \(w_k\ne a_k\),
and \(w_k\) was not removed earlier, for if \(w_k=a_j\) with \(j<k\), then
\(a_j\) would have appeared in the suffix \(w_j,\ldots,w_{n-2}\), contrary to
the choice of \(a_j\). After the \(n-2\) steps, write the remaining set as
\(\{r,b\}\), and define \(f(b)=r\) and \(f(r)=r\). This defines a function
\(f:[n]\to[n]\). If \(a_k\) has index \(k\), \(b\) has index \(n-1\), and
\(r\) has index \(n\), then \(f(v)\) has strictly larger index than \(v\) for
every \(v\ne r\). Hence every non-root vertex reaches \(r\), while \(r\) is
fixed, so the only directed cycle is the loop at \(r\). Thus the decoding gives
a map \(\Psi:[n]^{n-2}\to\mathcal A_{n,r}\).

The maps \(\Phi\) and \(\Psi\) are inverse maps. Let \(f\in\mathcal A_{n,r}\)
and let \(\Phi(f)=w\). At encoding step \(k\), for \(y\in R_k\setminus\{r\}\),
\[
y\text{ is an }R_k\text{-leaf}
\quad\Longleftrightarrow\quad
y\text{ does not occur among }w_k,\ldots,w_{n-2}.
\]
If \(y=w_j=f(a_j)\) for some \(j\ge k\), then the still-present vertex
\(a_j\ne y\) maps to \(y\), so \(y\) is not a leaf. Conversely, if \(y\) is not
a leaf, choose \(z\in R_k\setminus\{y\}\) with \(f(z)=y\). Since \(y\ne r\),
the vertex \(z\) is neither \(r\) nor the final vertex \(b\), because
\(f(r)=f(b)=r\). Thus \(z=a_j\) for some \(j\ge k\), and \(w_j=y\). Therefore
decoding \(\Phi(f)\) chooses the same least vertex at every step and reconstructs
\(f\), so \(\Psi(\Phi(f))=f\).

Conversely, let \(w\in[n]^{n-2}\) and let \(\Psi(w)=f\). At decoding step \(k\),
the chosen \(a_k\) is an \(R_k\)-leaf, since it does not appear in the remaining
suffix and neither \(b\) nor \(r\) maps to it. If \(y<a_k\) is a non-root
remaining vertex, then by the choice of \(a_k\), the vertex \(y\) occurs in the
remaining suffix, so some still-present vertex maps to \(y\). Hence \(a_k\) is
the least \(R_k\)-leaf, and the encoding records \(f(a_k)=w_k\) at each step.
Thus \(\Phi(\Psi(w))=w\).

Therefore \(\Phi\) is a bijection from \(\mathcal A_{n,r}\) to \([n]^{n-2}\).
Since there are \(n^{n-2}\) words of length \(n-2\) over \([n]\), we have
\[
|\mathcal A_{n,r}|=n^{n-2}\qquad(n\ge2).
\]

Now for each \(r\in[n]\), let
\[
A_{n,r}=\{f\in\mathcal F_n: r\text{ is the unique cyclic vertex of }G_f\}.
\]
Then
\[
A_n=\bigsqcup_{r\in[n]}A_{n,r},
\]
because every function with a unique cyclic vertex has exactly one such vertex
\(r\in[n]\), and a unique vertex cannot be two distinct elements. If \(n=1\),
then \(|A_n|=1=1^{1-1}\). If \(n\ge2\), then each fixed-root class has size
\(n^{n-2}\), so
\[
|A_n|=\sum_{r\in[n]}|A_{n,r}|=n\cdot n^{n-2}=n^{n-1}.
\]
Thus \(|A_n|=n^{n-1}\) for every positive integer \(n\). Finally,
\[
\Pr(A_n)=\frac{|A_n|}{n^n}
=\frac{n^{n-1}}{n^n}
=\frac1n.
\]
This proves the theorem.
\end{proof}

\end{document}

```


Citation Generator Source Ledger:
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


Original paper bibliography, .bib, or .bbl file, if supplied:
None
