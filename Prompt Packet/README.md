# Prompt Packet

This folder contains the human-readable prompt protocol for the RIPS proof-reconstruction workflow.

The prompt packet is the specification for the agent roles and controller routing. Local paper inputs and run artifacts live under repository-level `Inputs/` and `Outputs/` and remain ignored by Git.

## What This Protocol Does

The workflow asks a proof-blind solver system to reconstruct a proof from a cleaned public skeleton, then routes the proposed proof artifact through independent verification roles before any final acceptance. The primary setup path now creates one target-scoped package with Paper Cleaner Mini, independently audits its exact hash, verifies every Section 3 external grant, and deterministically exports the solver inputs. The older full-paper manual skeleton path remains an explicit fallback.

The current protocol uses:

1. **Multi-solver system**: S0 creates a proof blueprint, S1-S5 solve assigned subclaims, and S6 composes the final candidate artifact `P_k`.
2. **Problem Statement Verifier**: checks that `P_k`, and any verifier report that needs checking, addresses the exact target theorem.
3. **Citation Generator**: uses restricted internet source checking to build a Source Ledger for the proof artifact.
4. **Citation Verifier**: uses restricted internet source checking to verify the Source Ledger; A1/A2/A3 do not run until it returns `GOOD_TO_GO`.
5. **Verifier A1/A2/A3**: three independent full-proof audits that check gaps, disallowed premises, scope coverage, and proof-skeleton coupling.
6. **Composer A**: merges the three A reports into one controller-facing evidence report without inventing new mathematical evidence.
7. **Verifier B**: identifies the single weakest point, or reports that no weakest point was found.
8. **Verifier C**: adversarially tries to break the proof.
9. **Decision Controller**: applies routing rules, guidance-budget rules, hard gates, and acceptance conditions.
10. **Final Checker**: privileged gold-aware referee that runs only after the proof-blind cascade clears.
11. **Prompt Assembler**: fills fixed prompt templates with the current target, allowed statements, guidance list, and proposed proof.

## Folder Contents

This folder is organized as:

```text
Prompt Packet/
  README.md
  Prompts.md
  PromptsWithFullInternet.md
  FlowChart.md
  QnAforPrompts.md
```

File roles:

- `Prompts.md`: canonical full prompt packet and decision tree.
- `PromptsWithFullInternet.md`: internet-enabled solver packet variant.
- `FlowChart.md`: primary operational map of the protocol.
- `QnAforPrompts.md`: design notes explaining why the protocol is structured this way.

## Current Design Choices

- Verifier A is a required three-run ensemble: A1, A2, and A3.
- Paper Cleaner Mini is the primary target-specific setup path. Its exported
  package is labeled `target_scoped_proof_informed`; it must not be described
  as experimentally identical to the fallback full-paper proof-stripped
  skeleton.
- A Mini package reaches S0 only after a hash-matching independent audit and,
  when Section 3 is nonempty, a restricted-web Skeleton Source Generator and
  Skeleton Source Verifier return exact grant coverage and `GOOD_TO_GO`.
- Deterministic export writes the native `target.md`, `skeleton.md`,
  `allowed_support.md`, zero-byte `guidance.md`, optional `bibliography.bib`,
  and `setup_manifest.json` contract. Gold proof and full source are omitted by
  default and never enter S0-S6 prompts.
- S0/S1-S5/S6 artifacts are current-round-only and are not carried into later Solver rounds except through one counted guidance item.
- An accepted branch releases only an `E###` statement, independently verified status, permission to use it without reproof, and its use location as that counted item. Its proof body and branch history remain sealed from later Solvers. Deterministic final assembly hash-checks and attaches the full proof, including nested branch proofs transitively, before citation and A/B/C verification.
- The Problem Statement Verifier, Citation Generator, and Citation Verifier run before the A/B/C cascade; the Citation Verifier must return `GOOD_TO_GO` before Verifier A1/A2/A3 run.
- Citation Generator, Citation Verifier, and the pre-solver Skeleton Source gate are internet-enabled only for restricted source checking. `Prompts.md` keeps S0-S6 no-internet; `PromptsWithFullInternet.md` enables source-supported solver browsing. Verifier A/B/C remain no-internet in both modes.
- Citation reports are controller-visible only and are not carried into later Solver rounds except through one counted guidance item.
- Composer A merges A1/A2/A3 reports before the Decision Controller derives A's status.
- Verifiers can see the existing mathematical guidance list, but they do not append guidance.
- Guidance generation is centralized through the Decision Controller and Prompt Assembler.
- Solver roles (S0/S1-S5/S6), Problem Statement Verifier, Citation Generator, Citation Verifier, Verifier A/B/C, and Final Checker are LLM roles.
- Prompt assembly, logging, guidance-budget checks, and eventually Decision Controller routing should become deterministic code where possible.
- S6 returns one response, but its prompt requires machine-readable markers (for example `<!-- BEGIN_SOURCE_LEDGER --> ... <!-- END_SOURCE_LEDGER -->`) around the Final proof, Source Ledger, Completion checklist, and Web-source confirmation sections. Deterministic code (`Individual Pipeline/solver/s6_artifacts.py`) splits the saved `S6.md` into `candidate_final_proof.md`, `source_ledger.md`, `completion_checklist.md`, and `web_source_confirmation.md`, falling back to the section headings for older outputs. `Individual Pipeline/solver/sealed_proofs.py` then produces `final_proof.md`; downstream citation and proof verifiers receive that assembled proof.
