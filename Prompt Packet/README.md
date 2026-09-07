# Prompt protocol

This directory contains the human-readable specification for the RIPS
proof-reconstruction workflow.

## Start here

| Document | Role |
|---|---|
| [`FlowChart.md`](FlowChart.md) | Two-layer operational map: implemented runtime routes plus clearly marked manual/standalone protocol extensions |
| [`Prompts.md`](Prompts.md) | Canonical role contracts for closed-book S0-S6 |
| [`PromptsWithFullInternet.md`](PromptsWithFullInternet.md) | Canonical role contracts for source-supported S0-S6 |

`FlowChart.md` answers **what runs next** and labels whether an edge is executed
by the integrated Python runtime or belongs to the fuller manual protocol. The
selected prompt packet answers **what each role sees and must return**. The
terminal `state.json` status records what the integrated runtime actually did.

## Protocol at a glance

| Stage | Responsibility | Internet policy |
|---|---|---|
| Paper Cleaner Steps 1–5 | Retrieve and index the whole paper, trace dependencies, and select source-backed target IDs | API-backed; full paper available to cleaner roles |
| Paper Cleaner Mini | Build a target-scoped public packet from the source paper | API-backed; full paper available to cleaner roles |
| Independent package audit | Recheck the exact package and frozen target hashes | no solver access |
| Skeleton Source Generator/Verifier | Verify every Section 3 external grant | restricted source checking |
| S0 | Create the blueprint and select one key solver | packet-dependent |
| S1-S5 | Solve assigned proof obligations | packet-dependent |
| S6 | Compose one candidate proof and source ledger | packet-dependent |
| Problem Statement Verifier | Check that the artifact addresses the exact target | no browsing |
| Citation Generator/Verifier | Build and validate the source ledger | restricted source checking |
| A1/A2/A3 + Composer A | Independently audit the complete proof, then merge reports | no browsing |
| Verifier B | Identify the single weakest point | no browsing |
| Verifier C | Adversarially attempt to break the proof | no browsing |
| Decision Controller | Apply deterministic routing, budgets, and stop rules | code, not an LLM role |
| Coupling/provenance adjudication | Handle LOW-coupling paper-original cases in the full protocol | standalone verifier or human; not integrated into the S0-S6 runtime |
| Controller Audit | Optionally check a persisted controller decision against the protocol | external/manual; no browsing |
| Final Checker | Privileged gold-aware referee after the cascade clears, when private material is present | no browsing; isolated private input |

## Internet modes

| Behavior | `Prompts.md` | `PromptsWithFullInternet.md` |
|---|---:|---:|
| S0-S6 hosted search | No | Yes |
| Pre-solver Section 3 source gate | Restricted | Restricted |
| Post-S6 citation gate | Restricted | Restricted |
| A/B/C verifier browsing | No | No |
| Final Checker browsing | No | No |

Do not enable solver web search while loading `Prompts.md`, and do not describe
`PromptsWithFullInternet.md` as closed-book.

## Information boundaries

- S0-S6 receive the exact target, public skeleton, allowed support, and counted
  guidance—not the target's reference proof.
- Current-round solver artifacts are not silently carried into later rounds.
  Only one controller-approved guidance item crosses that boundary.
- An accepted branch releases its statement, status, permission to use it, and
  use location. Its proof body remains sealed until deterministic final
  assembly.
- Citation and verifier reports are controller-visible; they do not become an
  uncounted solver hint channel.
- When private material is present, the Final Checker sees privileged reference
  material but not the A/B/C reports or controller opinion. Without that
  material, the integrated runtime can report only `accepted_cascade_only`.

These boundaries are part of the experimental contract, not editorial advice.

## Principal artifacts

S6 uses machine-readable markers so deterministic code can separate:

- `candidate_final_proof.md`;
- `source_ledger.md`;
- `completion_checklist.md`;
- `web_source_confirmation.md` when applicable.

Accepted branch proofs are hash-checked and attached by
`Individual Pipeline/solver/sealed_proofs.py` before citation and mathematical
verification. The downstream roles receive the assembled `final_proof.md`.

## Editing and synchronization

Only the two canonical packets are edited by hand. The review-friendly files
under component `prompts/` directories are generated views.

From the repository root:

```bash
python prompt_sync.py --write
python prompt_sync.py --check
```

The check must report that all component views are current. Protocol changes
should also be reflected in `FlowChart.md` and, when they affect user-facing
behavior, the root and component READMEs.

## Interpretation rule

A candidate proof, a proof that passed only part of the cascade, a
cascade-accepted proof, and a private-checker-accepted proof are different
outcomes. Report the terminal controller status and name the gates that
actually ran.
