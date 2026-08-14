**1. Composition Map / Critical Claim Statuses**

- Target theorem status: not proved.
- Local valuation reverse inclusion: not proved.
- Transfer-generation kernel statement: not proved.
- Alternative route: none supplied.
- Final equality `T(Q_p)=T(Z_p)T(Q)`: not established.
- Maximal compact claim for `T(Z_p)`: not established as part of a complete proof.

**2. Main Solver Authorship And Proof-Reference Audit**

- Main Solver artifact is explicitly `Unsolved`.
- `main_solver_proof_key:false`.
- Main Solver does not present a complete proof and identifies the required local transfer-generation/Nakayama-type step as unresolved.
- Defender accepts the blocker diagnosis and reports no hidden accepted proof remains.
- No Main Solver proof is accepted or used as final.

**3. Final Manager Failure Output YAML**

```yaml
answer_status: UNRESOLVED
manager_acceptance_key: false
main_solver_proof_complete: false
main_solver_proof_used_as_final: false
failure_output_type: stopped_budget_reached
status: "Not reproduced within the 3-guidance-round budget"
```

**4. Source Ledger Markers**

```yaml
source_ledger:
  used_sources:
    - current_user_message_only
  excluded_sources:
    - prior_task_history
    - web_or_internet
    - api_keys
    - python
    - files
```

**5. Background / Assumptions Markers**

```yaml
background_assumptions:
  allowed_support: definitions_and_notation_only
  disallowed_support:
    - prior_formal_theorem_equivalent
    - downstream_theorem
    - named_Nakayama_or_Tate_Nakayama_citation_without_proof
    - unproved_transfer_generation_theorem
```

**6. Completion Checklist Markers**

```yaml
completion_checklist:
  target_theorem_accepted: false
  critical_local_claim_proved: false
  proof_reference_audit_passed: false
  defender_objection_resolved: false
  final_status_recorded: true
```

**7. Web-Source Confirmation Markers**

```yaml
web_source_confirmation:
  web_used: false
  internet_used: false
  web_confirmation_performed: false
  reason: "User explicitly prohibited web/internet use."
```