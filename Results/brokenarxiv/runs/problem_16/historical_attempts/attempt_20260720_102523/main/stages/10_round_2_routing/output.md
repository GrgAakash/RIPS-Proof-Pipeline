1. Target normalization

Let `F = Q_p`. For a Q-torus `T`, prove:

`T(F) = T(Z_p) T(Q)`,

where `T(Z_p)` is the maximal compact subgroup of `T(F)`.

Normalized equivalent goal for Main Solver:

Show the natural map

`T(Q) -> T(F) / T(Z_p)`

is surjective.

Use a finite Galois splitting field `K/Q` for `T`; locally choose a finite Galois extension `L/F` splitting `T_F`. Let `Y = X_*(T_L)` be the cocharacter lattice with local decomposition group action. The likely route is to translate `T(F)/T(Z_p)` into a valuation lattice and prove every local valuation class is realized by a rational point.

2. Task-adaptive proof obligations

Main Solver must establish, not assume:

- Define the valuation map for a split torus over `L`:
  `nu_L : T(L) = Y tensor L^x -> Y`, normalized by `nu_L(pi_L)=1`.
- Identify `T(F)` with `(Y tensor L^x)^D`, where `D = Gal(L/F)` after choosing a local Galois splitting extension.
- Identify `T(Z_p)` as the kernel of the induced valuation map on `T(F)`.
- Reduce the theorem to surjectivity of the valuation image of `T(Q)` onto `nu_L(T(F))`.
- Prove or invoke as an internal subclaim the supplied guidance statement:
  every element of `nu_L((Y tensor L^x)^D)` lies in
  `sum_{H <= D} e(L/L^H) N_{D/H}(Y^H)`.
- For each subgroup `H <= D` and `y in Y^H`, construct a rational point whose local valuation contribution is `e(L/L^H) N_{D/H}(y)`.
- Justify the global-to-local construction without hidden strong approximation beyond standard facts: likely using rational numbers with prescribed `p`-adic valuation and units elsewhere, and norm maps from finite field extensions tied to subtori or induced tori.
- Check ramification normalization carefully: local valuations, norm valuations, and the factor `e(L/L^H)` must match exactly.

3. Available tools

Allowed:

- Standard definitions of algebraic tori, cocharacter lattices, splitting fields, local fields, maximal compact subgroups.
- Standard valuation facts for finite extensions of local fields.
- Standard Galois descent for split tori.
- Standard induced torus / norm torus formalism if proved or clearly reduced inside the solution.
- Weak approximation on number fields only if stated as standard background and used narrowly to construct elements with prescribed valuation at a finite set of places.
- The supplied local Nakayama valuation reverse-inclusion statement as a required internal target/subclaim, not as an already-proved theorem.

Not allowed:

- External citations.
- Web search.
- Prior attempt memory.
- Any theorem equivalent to or downstream from the target theorem.
- Certifying the target via an unstated strong approximation theorem for tori.

4. Subclaim support graph

`C0`: Choose global Galois splitting field and local decomposition data.

`C1`: Local valuation model:
`T(F)/T(Z_p) ≅ nu_L((Y tensor L^x)^D)`.

Depends on: definitions, local splitting, maximal compact identification.

`C2`: Local Nakayama reverse inclusion:
`nu_L((Y tensor L^x)^D) subset sum_H e(L/L^H) N_{D/H}(Y^H)`.

Depends on: guidance item 1; Main Solver must prove or explicitly isolate proof.

`C3`: For each generator term `e(L/L^H) N_{D/H}(y)`, there exists `q in T(Q)` with that local valuation.

Depends on: global realization of local decomposition subgroup/subfield, induced subtorus/norm construction, weak approximation/norm valuation calculation.

`C4`: Additivity/multiplicativity combines generator terms into one rational point.

Depends on: group law and valuation homomorphism.

`C5`: Given arbitrary `t in T(F)`, choose `q in T(Q)` with same valuation; then `t q^{-1} in T(Z_p)`.

Depends on: `C1-C4`.

Final target follows from `C5`.

5. Critical Claims Ledger

- `CL1`: `T(Z_p) = ker(nu_L on T(F))`. Risk: for nonsplit tori this requires correct invariant interpretation.
- `CL2`: The valuation image is not simply `Y^D`; it is `nu_L((Y tensor L^x)^D)`. Risk: false simplification.
- `CL3`: The Nakayama inclusion must use `e(L/L^H)` with the stated normalization. Risk: inverse or missing ramification factor.
- `CL4`: Local subgroup terms must be globally realizable by rational points. Risk: assuming local data automatically globalizes.
- `CL5`: Norm valuation computation must match cocharacter norm `N_{D/H}`. Risk: confusing field norm and lattice trace.
- `CL6`: Maximal compact subgroup terminology must match the kernel of all rational characters’ absolute-value maps. Risk: model-dependent notation `T(Z_p)`.
- `CL7`: No appeal to the target theorem under another name, such as unrestricted strong approximation for tori.

6. Key-step and Main Solver selection

Key step selected for SS1 Main Solver:

Build the valuation-lattice proof around `C1-C3`, with particular focus on converting the local Nakayama generators into actual global rational points.

Reason for selecting one Main Solver now:

The proof is tightly coupled: local valuation normalization, Galois lattice algebra, and global point construction must be integrated coherently. Splitting these before seeing the first attempt risks incompatible normalizations.

SS1 Main Solver owns the complete proof attempt and must return:

- full proof draft;
- explicit statement of each internal lemma used;
- uncertain_steps;
- help_requests;
- proposed_board_updates.

7. Failure-mode checks

Defender must later test:

- Does the proof accidentally assume the theorem for induced tori or subtori?
- Does the global construction work for arbitrary Q-tori, not only split or quasi-split tori?
- Are the local and global splitting fields aligned correctly at the prime over `p`?
- Are all subgroup terms `H <= D` handled, including non-normal `H`?
- Is `L^H/F` used correctly when `H` is not normal?
- Is the ramification index `e(L/L^H)` placed in the correct direction?
- Does the proof identify the maximal compact subgroup canonically enough?
- Is weak approximation used only in a standard, defensible form?
- Are products of constructed rational points still in `T(Q)` and do their valuations add as claimed?

8. Subsolver execution plan with exactly SS1 Main Solver and SS2 Defender initially

SS1 Main Solver:

Produce the first full proof attempt. Do not skip the local Nakayama proof route. If a step is standard, state the exact standard fact and verify it is not equivalent to the target. Mark any gap rather than concealing it.

SS2 Defender:

Wait until SS1 returns the integrated proof. Then attack the proof line by line, prioritizing `CL1-CL7`, ramification normalization, and the global realization of local valuation generators. Defender must not supply a replacement final solution unless requested later by Manager.

No Midfielders or Attackers are launched in this routing pass.

9. Subsolver assignment table exactly SS1 and SS2

| ID | Role | Status | Assignment | Output Required |
|---|---|---:|---|---|
| SS1 | Main Solver | Active first | Construct complete proof of `T(Q_p)=T(Z_p)T(Q)` using valuation lattice reduction and the supplied Nakayama route. | Proof draft, uncertain_steps, help_requests, proposed_board_updates |
| SS2 | Defender | Queued last | Attack SS1’s integrated proof for hidden assumptions, normalization errors, and unsupported global realization claims. | Defect report with severity and precise challenged claims |

10. Web-source confirmation

No web, internet, files, APIs, Python, prior task history, or external sources were used.