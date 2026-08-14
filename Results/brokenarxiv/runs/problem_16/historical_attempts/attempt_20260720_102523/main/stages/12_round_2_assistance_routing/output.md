## 1. Post-Main Solver assessment

Bounded assistance is justified.

SS1 exposed one concrete bottleneck: the reverse inclusion in the local Nakayama valuation lemma is asserted via a “standard Nakayama cohomological argument” but not expanded. This is exactly one of the named critical risks, especially because the theorem’s proof depends on the precise ramification normalization
`e(L/L^H) N_{D/H}(Y^H)` and must handle nonnormal subgroups `H <= D`.

No broader assistance is needed. The global realization step and compact-kernel identification should remain for SS2 Defender review unless SS3’s output reveals a dependency gap.

## 5. Critical Claims Ledger updates/proposals

CL1 maximal compact kernel: leave for SS2 Defender.

CL2 valuation image not full `Y^D`: active risk, tied to SS3 assignment.

CL3 ramification normalization: active risk, tied to SS3 assignment.

CL4 global realization for subgroup terms including nonnormal `H`: leave for SS2 Defender after SS3 confirms local term shape.

CL5 norm valuation vs lattice trace: active risk, tied to SS3 assignment.

CL6 maximal compact notation: leave for SS2 Defender.

CL7 no strong approximation for tori: leave for SS2 Defender.

Proposed focused ledger item:
CL8 local Nakayama reverse inclusion: SS1’s proof currently cites a standard argument; SS3 must supply a self-contained proof or identify the exact missing hypothesis.

## 8. Subsolver execution plan

Add one Midfielder only.

SS3 should address the single bottleneck: prove or repair the local Nakayama valuation reverse inclusion for finite Galois local `L/F`, `D = Gal(L/F)`, and `D`-lattice `Y`, with valuation normalized by `nu_L(L^x)=Z`.

Required output from SS3:
- A standalone proof of  
  `nu_L((Y tensor L^x)^D) subset sum_{H<=D} e(L/L^H) N_{D/H}(Y^H)`.
- Explicit verification of the ramification factor `e(L/L^H)`.
- Explicit handling of nonnormal subgroups `H`.
- Clarify whether SS1’s boundary/corestriction sketch is valid as written or needs a corrected argument.

SS3 must not re-prove the full target theorem or work on global approximation.

## 9. Subsolver assignment table contiguous SS1, SS2, and any added SS#

| Solver | Role | Assignment |
|---|---|---|
| SS1 | Main Solver | Maintain full proof draft and integrate only bounded support if accepted. |
| SS2 | Defender | Audit final proof for CL1-CL7, especially global realization and compact subgroup claims. |
| SS3 | Midfielder | Supply the local Nakayama reverse-inclusion proof with ramification normalization and nonnormal subgroup handling. |

## 10. Web-source confirmation: no web sources used