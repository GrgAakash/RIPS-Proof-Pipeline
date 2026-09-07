# Prompt protocol

This directory explains how the proof workflow runs and contains the prompts
for each role.

## Start here

| Document | Role |
|---|---|
| [`FlowChart.md`](FlowChart.md) | What runs next, with Python-runtime and manual-only paths marked separately |
| [`Prompts.md`](Prompts.md) | Role prompts for S0-S6 without web search |
| [`PromptsWithFullInternet.md`](PromptsWithFullInternet.md) | Role prompts for S0-S6 with web search |

Start with the flow chart for the order of operations, then open a prompt to
see what that role receives and must return. For a completed Python run,
`state.json` records which steps actually ran.

## Protocol at a glance

| Stage | What it does | Access and execution |
|---|---|---|
| Paper Cleaner Steps 1–5 | Read the paper, identify statements and dependencies, and select targets | API-backed; full paper available to cleaner roles |
| Paper Cleaner Mini | Prepare the context for one theorem | API-backed; full paper available to cleaner roles |
| Independent package audit | Check the finished input and its file hashes | no solver access |
| Skeleton Source Generator/Verifier | Check sources for external results in Section 3 | restricted source checking |
| S0 | Make a plan and choose the key solver | packet-dependent |
| S1-S5 | Solve the assigned parts | packet-dependent |
| S6 | Write the candidate proof and list its sources | packet-dependent |
| Problem Statement Verifier | Check that the proof addresses the exact target | no browsing |
| Citation Generator/Verifier | List and check the sources used | restricted source checking |
| A1/A2/A3 + Composer A | Review the proof separately, then combine findings | no browsing |
| Verifier B | Identify the single weakest point | no browsing |
| Verifier C | Adversarially attempt to break the proof | no browsing |
| Decision Controller | Decide what runs next and enforce stopping rules | code in the integrated runtime; a separate controller role in manual runs |
| Coupling/provenance adjudication | Handle LOW-coupling paper-original cases in the full protocol | standalone verifier or human; not integrated into the S0-S6 runtime |
| Controller Audit | Check that the recorded decision follows the rules | external/manual; no browsing |
| Final Checker | Review the candidate against private reference material after earlier checks pass | no browsing; isolated private input |

## Internet modes

| Behavior | `Prompts.md` | `PromptsWithFullInternet.md` |
|---|---:|---:|
| S0-S6 hosted search | No | Yes |
| Key solver must finish with `solved` before the other four run | Yes | Yes |
| Pre-solver Section 3 source gate | Restricted | Restricted |
| Post-S6 citation gate | Restricted | Restricted |
| A/B/C verifier browsing | No | No |
| Final Checker browsing | No | No |

Do not enable solver web search while loading `Prompts.md`, and do not describe
`PromptsWithFullInternet.md` as closed-book.

## Information boundaries

- S0-S6 receive the target, prepared context, allowed supporting results, and
  recorded guidance. They do not receive the reference proof.
- A new solver round does not receive the previous round's outputs. At most one
  new, controller-approved guidance item is added between rounds.
- An accepted branch releases its statement, status, permission to use it, and
  use location. Its proof body remains sealed until deterministic final
  assembly.
- Citation and proof-review reports go to the controller, not directly to the
  next solver round.
- When private material is present, the Final Checker sees privileged reference
  material but not the A/B/C reports or controller opinion. Without that
  material, the integrated runtime can report only `accepted_cascade_only`.

Keep these inputs separate when running the protocol manually too.

## Principal artifacts

S6 marks sections of its response so code can save them as separate files:

- `candidate_final_proof.md`;
- `source_ledger.md`;
- `completion_checklist.md`;
- `web_source_confirmation.md` when applicable.

Accepted branch proofs are hash-checked and attached by
`Individual Pipeline/solver/sealed_proofs.py` before citation and mathematical
verification. The downstream roles receive the assembled `final_proof.md`.

## Editing and synchronization

Edit the two original prompt packets here. The copies under component
`prompts/` directories are generated from them.

From the repository root:

```bash
python prompt_sync.py --write
python prompt_sync.py --check
```

The check should report that all copies are current. When the workflow changes,
update `FlowChart.md` and the relevant READMEs too.

## Interpretation rule

A candidate, a partial review, a cascade-only pass, and a private Final Checker
pass mean different things. Report the saved final status and which reviews ran.
