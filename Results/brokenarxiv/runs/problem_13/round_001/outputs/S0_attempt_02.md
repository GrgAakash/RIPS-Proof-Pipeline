1. Target decomposition

target_label: T

target_type: Hasse principle / rational point existence theorem.

main_goal: Prove that the stated local solubility and Brauer-triviality hypotheses force \(X(K)\neq \varnothing\).

variables_and_parameters:
\(K\) is a number field; \(v\) ranges over all places of \(K\); \(K_v\) is the completion; \(G=\mathrm{SL}_n\); \(X\) is a \(K\)-homogeneous space of \(G\); \(\bar H\) is a finite nilpotent geometric stabilizer of \(X_{\bar K}\).

conclusion_to_prove:
\(X(K)\neq\varnothing\).

2. Available tools

tool: Local solubility hypothesis  
source_status: assumption  
exact_statement_or_fact: For every place \(v\) of \(K\), \(X(K_v)\neq\varnothing\).  
intended_role_in_proof: Choose an adelic point \((x_v)_v\in X(\mathbb A_K)\).

tool: Constant unramified algebraic Brauer hypothesis  
source_status: assumption  
exact_statement_or_fact:
\[
\ker(\operatorname{Br}_{nr}(X)\to \operatorname{Br}_{nr}(X_{\bar K}))
=\operatorname{im}(\operatorname{Br}(K)\to \operatorname{Br}(X)).
\]
intended_role_in_proof: Show every algebraic unramified Brauer class evaluates like a constant class.

tool: Global reciprocity for \(\operatorname{Br}(K)\)  
source_status: standard background fact  
exact_statement_or_fact: For \(\beta\in \operatorname{Br}(K)\),
\[
\sum_v \operatorname{inv}_v(\beta_{K_v})=0.
\]
intended_role_in_proof: Prove that the chosen adelic point is orthogonal to the algebraic unramified Brauer group.

tool: Specialness of \(\mathrm{SL}_n\)  
source_status: standard background fact  
exact_statement_or_fact: For every field \(F/K\), \(H^1(F,\mathrm{SL}_n)=1\).  
intended_role_in_proof: Convert neutrality of the Springer obstruction into an actual \(F\)-rational point.

tool: Springer/Giraud obstruction class for homogeneous spaces with finite stabilizer  
source_status: proved inside the current proof  
exact_statement_or_fact: To \(X\) one attaches a finite \(K\)-kernel/link \(L_X\) and a class \(\eta_X\in H^2(K,L_X)\); local points neutralize \(\eta_{X,K_v}\), and \(X(K)\neq\varnothing\) follows from global neutrality because \(H^1(K,\mathrm{SL}_n)=1\).  
intended_role_in_proof: Reformulate rational-point existence as a global neutrality problem.

tool: Characteristic central series of finite nilpotent groups  
source_status: standard background fact  
exact_statement_or_fact: A finite nilpotent group has a finite central series by characteristic subgroups with finite abelian quotients.  
intended_role_in_proof: Make the stabilizer/link reducible by induction through abelian central quotients.

tool: Poitou-Tate duality for finite Galois modules over number fields  
source_status: standard background fact  
exact_statement_or_fact: For a finite Galois module \(A\), global obstruction classes with trivial local images are detected by dual finite-module cohomology via the Poitou-Tate pairing.  
intended_role_in_proof: Detect each abelian lifting obstruction by dual Brauer-type classes.

tool: Abelian obstruction/Brauer pairing calculation  
source_status: proved inside the current proof  
exact_statement_or_fact: At each central abelian quotient step, the Poitou-Tate obstruction to lifting local neutralizations equals the Brauer-Manin evaluation of the corresponding algebraic unramified Brauer class.  
intended_role_in_proof: Use Brauer orthogonality to kill all successive lifting obstructions.

3. Subclaim support graph

id: SC1  
statement: The hypotheses imply \(X(\mathbb A_K)^{\operatorname{Br}_{nr,alg}}\neq\varnothing\), where \(\operatorname{Br}_{nr,alg}(X)=\ker(\operatorname{Br}_{nr}(X)\to \operatorname{Br}_{nr}(X_{\bar K}))\).  
uses_prior_subclaims: none  
purpose: Remove the Brauer obstruction using the constantness assumption.  
status: must be proved in final proof.  
suggested_solver: S1.

id: SC2  
statement: \(X\) has an associated finite Springer obstruction class \(\eta_X\), locally neutral at every \(v\); moreover, global neutrality of \(\eta_X\) implies \(X(K)\neq\varnothing\).  
uses_prior_subclaims: none  
purpose: Translate rational points into a global cohomological neutrality problem.  
status: must be proved in final proof.  
suggested_solver: S2.

id: SC3  
statement: The finite nilpotent stabilizer link of \(X\) admits a Galois-compatible central filtration with finite abelian quotients, and neutrality of \(\eta_X\) can be tested by successively solving the corresponding abelian lifting problems.  
uses_prior_subclaims: SC2  
purpose: Reduce the nonabelian nilpotent obstruction to abelian obstruction steps.  
status: must be proved in final proof.  
suggested_solver: S3.

id: SC4  
statement: For each abelian central step, the obstruction to passing from local neutral liftings to a global neutral lifting is exactly detected by the algebraic unramified Brauer-Manin pairing.  
uses_prior_subclaims: SC1, SC3  
purpose: Show Brauer orthogonality annihilates every obstruction in the induction.  
status: must be proved in final proof.  
suggested_solver: S4.

id: SC5  
statement: If \(X(\mathbb A_K)^{\operatorname{Br}_{nr,alg}}\neq\varnothing\), then \(\eta_X\) is globally neutral, hence \(X(K)\neq\varnothing\).  
uses_prior_subclaims: SC2, SC3, SC4  
purpose: Assemble the nilpotent induction and conclude the target theorem from SC1.  
status: must be proved in final proof.  
suggested_solver: S5.

4. Hardest step prediction

hardest_step_id: SC4

hardest_step_description: Identifying the abelian lifting obstruction with the evaluation of algebraic unramified Brauer classes. This requires matching the cohomological obstruction from a central finite abelian quotient with the Brauer-Manin pairing via finite-module global duality.

risk_if_wrong: The proof would only show absence of a visible Brauer obstruction, not that the Springer obstruction is globally neutral. That would leave a gap between local solubility and \(K\)-rational solubility.

how_final_proof_should_handle_it: Work one central abelian quotient at a time. Define the obstruction class precisely, verify it is locally trivial, identify its Poitou-Tate duals with the relevant algebraic unramified Brauer classes, and prove equality between the duality pairing and the Brauer evaluation sum.

5. Failure-mode checks

circularity_check: Do not cite the target theorem or a black-box Hasse principle for nilpotent stabilizers. The local-global statement must be obtained through SC2-SC5.

full_theorem_check: The proof must conclude \(X(K)\neq\varnothing\), not merely nonemptiness of a Brauer-Manin set.

source_check: No external paper-specific results are allowed. Deep task-specific ingredients are listed as subclaims to be proved inside the current proof.

hypothesis_check: The number-field hypothesis is needed for global reciprocity and Poitou-Tate duality. The group \(G=\mathrm{SL}_n\) is needed for \(H^1(K,G)=1\). Nilpotence is needed for the central-series induction.

notation_check: The kernel in the Brauer hypothesis is the algebraic unramified Brauer group. Evaluations must be made only for Brauer classes that are regular/unramified at the local points.

standard_background_check: Permitted standard facts should be limited to global reciprocity, \(H^1(F,\mathrm{SL}_n)=1\), finite nilpotent central series, and Poitou-Tate duality for finite Galois modules, with hypotheses explicitly checked.

6. Subproblem assignment table

S1: Prove SC1. Starting from local points \((x_v)\), show every algebraic unramified Brauer class is pulled back from \(\operatorname{Br}(K)\), hence its adelic invariant sum is zero by global reciprocity.

S2: Prove SC2. Construct the Springer/Giraud obstruction class for \(X\), prove local points give local neutralizations, and prove that global neutrality gives a \(K\)-point using \(H^1(K,\mathrm{SL}_n)=1\).

S3: Prove SC3. Build a Galois-compatible characteristic central filtration of the finite nilpotent geometric stabilizer and formulate the successive abelian lifting problems for the obstruction class.

S4: Prove SC4. For one finite abelian central quotient, identify the global lifting obstruction through Poitou-Tate duality and prove that its pairing equals the relevant algebraic unramified Brauer-Manin evaluation.

S5: Prove SC5 and assemble T. Induct over the filtration from S3, use S4 and the orthogonality from S1 at each step, obtain global neutrality, then invoke S2 to get \(X(K)\neq\varnothing\).

7. Web-source confirmation

no web sources used