1. **Support Admission Decision**

SS3: **ADMIT, partial only.**

Do not admit CL8 as proved. Admit SS3’s concrete solved partial result: the easy containment
`sum_H e(L/L^H) N_{D/H}(Y^H) subset im(nu_L)`
including its checks of the ramification factor and nonnormal subgroup handling. Also admit the obstruction note: the reverse inclusion remains unsolved and needs the promised Nakayama-style transfer-generation theorem.

```yaml
approved_support_ids:
  - SS3.partial_easy_containment
  - SS3.ramification_factor_check
  - SS3.nonnormal_H_easy_direction_check
  - SS3.unsolved_obstruction_identification
rejected_support_ids:
  - SS3.CL8_reverse_inclusion_proved
admission_rationale: >
  SS3 explicitly does not prove the assigned reverse inclusion
  im(nu_L) subset sum_H e(L/L^H)N_{D/H}(Y^H).
  Its proved content is compatible with Main Solver's draft but only covers
  the opposite/easy containment and supporting bookkeeping. The artifact
  correctly identifies the missing ingredient as a Nakayama-style
  transfer-generation theorem for arbitrary D-lattices Y, so CL8 should
  remain marked unsolved unless Main Solver supplies that argument.
```

2. **Proposed Board Updates**

- Mark `CL8 local reverse inclusion` as **UNSOLVED / needs expansion**.
- Add solved partial: `easy containment transfer sum subset im(nu_L)` verified.
- Add solved bookkeeping: ramification factor `e(L/L^H)` and nonnormal `H` handling are acceptable for the easy direction.
- Add required next step: prove the Nakayama-style transfer-generation theorem giving the reverse inclusion for arbitrary `D`-lattices `Y`.

3. **Web-Source Confirmation**

No web sources used.