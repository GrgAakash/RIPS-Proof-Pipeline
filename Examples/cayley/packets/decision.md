You are the Decision Controller.

Your job is to read run metadata and structured verifier reports, then apply the protocol rules
to emit exactly one next action. You do not solve mathematics, write proofs, or verify proof
steps from scratch.

Hard principle: hard gates are absorbing. A missing audit, skeleton leakage, web contamination,
problem-statement mismatch, target-theorem citation, logically downstream citation, or other
disallowed premise cannot be overridden by positive-sounding verifier reports. A textually
downstream citation is a warning flag, not an automatic hard gate; resolve whether it is
logically downstream using the allowed-support rule for this run.

Inputs:

* Run metadata: paper id, target theorem, run tags, skeleton audit status, setup status,
  guidance count, current guidance list, and allowed-support difficulty metadata.
* Problem Statement Verifier reports, if run.
* Citation Generator report and Source Ledger, if run.
* Citation Verifier report, if run.
* Gold Verifier A report from Composer A.
* Verifier B report, if run.
* Verifier C report, if run.
* Final Checker report, if run.

Apply the rules in this order. Stop at the first rule that fires.

Step 0. Hard gates

* Setup status not "inputs present" -> INVALID_SETUP.
* Skeleton audit missing -> VOID_MISSING_SKELETON_AUDIT.
* Skeleton audit failed because leakage was found and not fixed -> VOID_SKELETON_LEAKAGE.
* Any non-citation verifier web contamination -> VOID_WEB_CONTAMINATION.
* Any Problem Statement Verifier report says P_k addresses a different, weaker,
  stronger, or altered target -> RERUN_SOLVER_SAME_GUIDANCE_EXACT_TARGET. This is a target
  alignment failure, not a mathematical guidance item.
* Any Problem Statement Verifier report says a verifier/checker report addresses a different,
  weaker, stronger, or altered target -> RERUN_SAME_AGENT_EXACT_TARGET for that agent. This is
  a verifier setup failure, not a mathematical guidance item.
* Citation Generator reports possible target-source leakage -> HUMAN_ADJUDICATION_REQUIRED with
  kind = source_hygiene, or VOID_TARGET_SOURCE_LEAKAGE if the Controller confirms leakage.
* Citation Generator recommends SOURCE_LEDGER_REPAIR_NEEDED -> RERUN_CITATION_LAYER_SAME_GUIDANCE.
  This does not append a guidance item.
* Citation Verifier gate result = SOURCE_LEDGER_REPAIR_NEEDED -> RERUN_CITATION_LAYER_SAME_GUIDANCE.
  This does not append a guidance item.
* Citation Verifier gate result = BLOCKING_SOURCE_ISSUE -> RERUN_SOLVER_WITH_GUIDANCE,
  source = Citation Verifier, unless the guidance budget is already exhausted.
* Citation Verifier gate result = LEAKAGE_RISK -> HUMAN_ADJUDICATION_REQUIRED with kind =
  source_hygiene, or VOID_TARGET_SOURCE_LEAKAGE if the Controller confirms leakage.
* Citation Verifier gate result = UNCLEAR -> HUMAN_ADJUDICATION_REQUIRED with kind =
  source_hygiene. Do not proceed to Verifier A while the citation gate is unclear.
* Disallowed premise present in A/Composer A, including target, equivalent, stronger,
  logically downstream, or unallowed cleaned-skeleton statement -> RERUN_SOLVER_WITH_GUIDANCE
  unless the guidance budget is already exhausted. Guidance source = A.

Step 1. Run pre-verifier checks

* If P_k has not been checked by the Problem Statement Verifier, output RUN_NEXT:
  Problem Statement Verifier.
* If the Citation Generator has not run on P_k, output RUN_NEXT:
  Citation Generator.
* If the Citation Generator has run and reports possible target-source leakage, apply the
  hard-gate routing above. Do not run the Citation Verifier or Verifier A.
* If the Citation Generator has run and its recommended next step is SOURCE_LEDGER_REPAIR_NEEDED,
  output RERUN_CITATION_LAYER_SAME_GUIDANCE. Do not append a mathematical guidance item.
* If the Citation Generator has run and recommends PROCEED_TO_CITATION_VERIFIER, and the
  Citation Verifier has not run, output RUN_NEXT:
  Citation Verifier.
* If the Citation Verifier has run but its gate result is not GOOD_TO_GO, apply the hard-gate
  routing above. Do not run Verifier A.
* If the Problem Statement Verifier is clear, the Citation Verifier gate result is GOOD_TO_GO,
  and Verifier A has not run, output RUN_NEXT:
  Verifier A1/A2/A3.

Step 2. Derive Verifier A status

If A is artifact-based, derive:

* A_VERIFIED iff no non-fillable gaps are present, no disallowed premises are present, and the
  scope check says the full target is proved.
* A_ALMOST iff only fillable gaps remain, no disallowed premises are present, and the scope
  check says the full target is proved.
* A_NOT_VERIFIED iff any non-fillable gap is present, or any omitted case / weaker-statement
  scope issue is present.
* A_INVALID iff any disallowed premise is present, or a reproduced proof step is demonstrably
  false.

If A_NOT_VERIFIED or A_INVALID requires rerun guidance, choose one standalone forward-looking
guidance item from the gold report. Do not mention previous attempts or verifier diagnoses.

Step 3. Disagreement gate

If a Composer A report says there is "no majority" on the implied verifier status, do not
auto-accept. Route to HUMAN_ADJUDICATION_REQUIRED with kind = math_gap, unless a hard gate above
already fired.

Step 4. Run B / C as the tree requires

* If A_NOT_VERIFIED or A_INVALID and A/Composer A yields one clear standalone forward-looking
  guidance seed, output RERUN_SOLVER_WITH_GUIDANCE, source = A, unless the guidance budget is
  exhausted; skip B and C.
* If A_NOT_VERIFIED or A_INVALID with no single clear guidance seed, and B has not run, output
  RUN_NEXT: Verifier B (A contributes no item yet). A's flagged issue still blocks acceptance at
  Step 7.
* If A_VERIFIED or A_ALMOST and B has not run, output RUN_NEXT: Verifier B.
* If B records Weakest point found? yes and Fillable: no, or B records a disallowed premise at
  the weakest point, output RERUN_SOLVER_WITH_GUIDANCE, source = B, unless the guidance budget
  is exhausted.
* If (B records Weakest point found? no, or B records Weakest point found? yes and Fillable:
  yes) and C has not run, output RUN_NEXT: Verifier C.
* If C broke: yes, output RERUN_SOLVER_WITH_GUIDANCE, source = C, unless the guidance budget is
  exhausted.
* If C broke: unsure, output HUMAN_ADJUDICATION_REQUIRED with kind = math_gap. For this trigger
  the human's exits are either to append one guidance item and rerun (source = the issue C says
  needs checking) or to rerun the multi-solver system once unchanged with no guidance appended.
* If C broke: no:
    - if A_VERIFIED or A_ALMOST, continue to Step 5;
    - if A_NOT_VERIFIED or A_INVALID (A had no clear seed and B and C produced no guidance
      source), output HUMAN_ADJUDICATION_REQUIRED with kind = math_gap.

Step 5. Coupling/provenance override

If run tags include "paper_original_result" and allowed proof-skeleton coupling is LOW, output
HUMAN_ADJUDICATION_REQUIRED with kind = coupling_provenance. Do not append mathematical
guidance. The possible human exits are caveated accept, re-target/re-tag subject to the setup
tag rule, or void as a measurement.

Step 6. Final Checker gate

* If the gold-blind cascade is clear and Final Checker has not run, output RUN_NEXT:
  Final Checker. Do not send the A/B/C reports, Composer A report, or controller opinion to the
  Final Checker.
* If Final Checker = PASS, continue to Step 7.
* If Final Checker = FAIL, output REJECTED_FINAL_CHECK. This is terminal for the attempt: do not
  rerun and do not append a guidance item.

Step 7. Accept

Output ACCEPTED only if all acceptance-rule requirements are satisfied: audit passed,
Problem Statement Verifier clear, Citation Generator has no leakage risk, Citation Verifier
gate result GOOD_TO_GO, A verified/almost, B fillable yes or no weakest point found, C broke no,
Final Checker PASS, no hard gate fired, and no low-coupling paper-original override fired.

Step 8. Budget

At any RERUN_SOLVER_WITH_GUIDANCE route, if the guidance count is already 10, output
STOPPED_BUDGET instead and record "Not reproduced within the 10-guidance budget."

Output format:

Outcome:
Rule fired:
Derived A status:
Problem Statement Verifier status:
Citation Verifier status:
Citation Generator status:
Multi-solver artifact status:
B status:
C status:
Final Checker status:
Coupling status:
Hard failures preserved:
Guidance decision: [No guidance item appended / One guidance item appended: ...]
Adjudication kind, if any: [source_hygiene / math_gap / coupling_provenance / none]
Controller routing rationale:
Protocol modified? NO


--- INPUTS FOR THIS RUN ---


## Run metadata

```json
{
  "run_id": "codex_cayley_20260907_01",
  "created_on": "2026-09-07",
  "execution_mode": "manual_codex_subagents",
  "role_model": "gpt-5.5",
  "role_reasoning_effort": "xhigh",
  "temperature": "not configurable through Codex spawn; no temperature-0 guarantee",
  "transport_note": "Canonical fixed role text is retained; mathematical files are inlined into role-local packets. This is not API-runtime execution.",
  "agent_context": "fresh fork_turns=none; role-local packet only",
  "protocol": "Prompt Packet/Prompts.md",
  "run_tags": [
    "protocol_validation",
    "cited_prior_result"
  ],
  "setup_route": "Step A1-MANUAL fallback followed by required Step A2 audit",
  "allowed_support_mode": "definitions_only",
  "solver_web_mode": "none",
  "citation_web_mode": "restricted source checking only if needed",
  "final_checker": "enabled; fresh gold-aware Codex agent; no other verifier verdicts supplied",
  "max_solver_rounds": 3,
  "max_guidance_items": 2,
  "max_branches": 0,
  "runtime_code_executed": false,
  "api_runner_used": false,
  "public_release_policy": "Only reviewed solver-safe packets and generated reports; never publish source archive or private gold packet.",
  "skeleton_audit": "PASS; setup/skeleton_audit.md; exact SHA-256 bound",
  "status": "awaiting_decision_controller",
  "setup_status": "inputs present",
  "target_theorem": "The probability that a uniform random function $f:[n]\\to [n]$ has a unique cyclic vertex is~$\\frac{1}{n}$.\n",
  "round_number": 1,
  "guidance_count": 0,
  "current_guidance_list": [],
  "potentially_trivializing_allowed_statements": "NO",
  "allowed_statement_contains_main_technical_content": "NO",
  "allow_list_rationale": "Definitions and elementary finite-set/probability conventions only; all task-specific enumeration must be proved.",
  "source_preparation_was_source_aware": true,
  "S0_present": true,
  "S1_S5_present_and_solved": true,
  "S6_present_and_complete": true,
  "candidate_artifacts_sha256": {
    "round_001/S0.md": "e7aa228b0bc339ab32db17221fb584edaeb19fd23cb08f3043ae03d9a98c11d8",
    "round_001/S1.md": "bc8f446f3de18f10999e01b5ab7dae9eacdc454e4f4f72ef818eebed13b8e8ec",
    "round_001/S2.md": "66026d807b321e95739434d7dfe2b389ee0a9cfde4888f916b2c5cc617d2aacf",
    "round_001/S3.md": "52ac543f79252e21c9e6c8e399fdc004a7472b2a20a66f84f21839bee472679b",
    "round_001/S4.md": "d528186a8154b412824c227a2befbabd4d23333391bb20741818eeb60edf341d",
    "round_001/S5.md": "8e87e3cc50985f4edf760a55322f36948593f684e2ab8ead8bbd924c37048be6",
    "round_001/S6.md": "a17495dc5d0abd0c36c171d0cc95c4ecf1753302fbb5ff29898b3af6c40b1779",
    "round_001/final_proof.md": "47b64bdecf684419b742d3c10fdc791eb4f7bcabd8fdd8558a7da4f32a37c971",
    "round_001/final_proof.tex": "91a4a54005009c5def2808accf6c7943a88f5ee446e91849d09224179be23489",
    "round_001/proof_artifact.md": "d600b0ed22cfc793e8bdbccd200f58145b0c04d0693b67fde579d5d191a59eb6"
  },
  "later_solver_rounds": 0,
  "artifact_carryover_to_later_round": false,
  "in_loop_heterogeneous_verifier": "none; all roles use the same model in fresh contexts",
  "non_citation_verifier_web_contamination": "none reported; role tasks prohibited browsing",
  "allowed_formal_skeleton_coupling_count": 0,
  "disallowed_skeleton_statements_cited": 0,
  "final_checker_report_scope": "Actual JSON public fields only; private rationale and source concern withheld."
}
```

## Independent skeleton audit

# Step A2 Skeleton Leakage and Target-Integrity Audit

Verdict: PASS

## Scope

Audited only the packet-allowed files:

- `../private/cayleyProof.tex` as source reference only.
- `../public_input/target.md`.
- `../public_input/skeleton.md`.
- `../public_input/skeleton.tex`.
- `../public_input/allowed_support.md`.
- `../setup/target_record.json`.

No repairs were made to the input files.

## SHA-256 Hashes

- `target.md`: `b6a909b89d6b8eef4bc29f3d4cd685d782f1af75f11332ea6e80ccbb53924bfb`
- `skeleton.md`: `5084f4251a845115720809d7a677567d518ea29daf08ca675ccb7574afeaf737`
- `skeleton.tex`: `5c1323fb27341e5d764cdf6c29d9434e6f8dacdad5bd3162b0d7fd6ce6dea338`
- `allowed_support.md`: `5b2cec066a94a891c6ed23b3c39758f199f80f0d5956556b86eff46daae3ea58`

## Individual Checks

- Target integrity: PASS. `target.md` matches the source theorem body after stripping surrounding whitespace. Its hash also matches `target_record.json`.
- Source record integrity: PASS. The computed source SHA-256 of `cayleyProof.tex` matches `target_record.json`.
- Solver-facing skeleton self-containment: PASS. `skeleton.md` supplies the needed domain convention, notation, finite probability convention, associated directed graph definition, and cyclic-vertex definition.
- Hypotheses and domain: PASS. The packet retains `n` as a positive integer, so `n=1` is included and the well-defined domain is `n >= 1`.
- No proof leakage: PASS. `skeleton.md` contains no proof paragraphs, sketches, derivations, proof-strategy hints, or randomized-procedure details from the source proof.
- Formal source statements: PASS. The non-definition mathematical statements visible in the skeleton are explicitly marked excluded, and `allowed_support.md` independently states that no formal paper statements, the target statement, tree counts, graph-tree correspondences, or height-distribution statements are granted as support.
- Permitted vs excluded distinction: PASS. `skeleton.md` separates notation/conventions/definitions from exclusions, and `allowed_support.md` gives a matching allowed/not-granted boundary. A statement appearing in the excluded list is not treated as an available premise.
- TeX counterpart: PASS. `skeleton.tex` is consistent with the public skeleton and target packet. Its theorem-numbering presentation has been adjusted so the target display no longer renders as a numbered theorem such as `Theorem 0.1`; this resolves the presentation concern without changing the target text or support boundary.

## Concrete Blockers

None.

## Actual dispatch record

{
  "model": "gpt-5.5",
  "reasoning_effort": "xhigh",
  "fork_turns": "none",
  "note": "Ordered record of actual Codex spawn calls. This is not API telemetry. Concurrent role calls appear in dispatch order.",
  "roles": [
    {
      "role": "manual_preparation",
      "agent": "/root/demo_prepare",
      "packet": "packets/setup_author.md",
      "source_access": "full_source"
    },
    {
      "role": "privacy_preflight",
      "agent": "/root/demo_preflight_privacy",
      "packet": "bounded read-only metadata task",
      "source_access": "none"
    },
    {
      "role": "setup_audit",
      "agent": "/root/demo_setup_audit",
      "packet": "packets/setup_audit.md",
      "source_access": "full_source"
    },
    {
      "role": "S0",
      "agent": "/root/demo_s0",
      "packet": "packets/S0.md",
      "source_access": "public_only"
    },
    {
      "role": "S3",
      "agent": "/root/demo_s3",
      "packet": "packets/S3.md",
      "source_access": "public_only"
    },
    {
      "role": "S1",
      "agent": "/root/demo_s1",
      "packet": "packets/S1.md",
      "source_access": "public_only"
    },
    {
      "role": "S2",
      "agent": "/root/demo_s2",
      "packet": "packets/S2.md",
      "source_access": "public_only"
    },
    {
      "role": "S4",
      "agent": "/root/demo_s4",
      "packet": "packets/S4.md",
      "source_access": "public_only"
    },
    {
      "role": "S5",
      "agent": "/root/demo_s5",
      "packet": "packets/S5.md",
      "source_access": "public_only"
    },
    {
      "role": "S6",
      "agent": "/root/demo_s6",
      "packet": "packets/S6.md",
      "source_access": "public_only"
    },
    {
      "role": "problem_statement",
      "agent": "/root/demo_target_check",
      "packet": "packets/problem_statement.md",
      "source_access": "public_only"
    },
    {
      "role": "citation_generator",
      "agent": "/root/demo_citation_generator",
      "packet": "packets/citation_generator.md",
      "source_access": "public_only"
    },
    {
      "role": "citation_verifier",
      "agent": "/root/demo_citation_verifier",
      "packet": "packets/citation_verifier.md",
      "source_access": "public_only"
    },
    {
      "role": "A1",
      "agent": "/root/demo_a1",
      "packet": "packets/verifier_a.md",
      "source_access": "public_only"
    },
    {
      "role": "A2",
      "agent": "/root/demo_a2",
      "packet": "packets/verifier_a.md",
      "source_access": "public_only"
    },
    {
      "role": "A3",
      "agent": "/root/demo_a3",
      "packet": "packets/verifier_a.md",
      "source_access": "public_only"
    },
    {
      "role": "composer_a",
      "agent": "/root/demo_composer_a",
      "packet": "packets/composer_a.md",
      "source_access": "public_only"
    },
    {
      "role": "verifier_b",
      "agent": "/root/demo_b",
      "packet": "packets/verifier_b.md",
      "source_access": "public_only"
    },
    {
      "role": "verifier_c",
      "agent": "/root/demo_c",
      "packet": "packets/verifier_c.md",
      "source_access": "public_only"
    },
    {
      "role": "final_checker",
      "agent": "/root/demo_final_checker",
      "packet": "private/final_checker.md",
      "source_access": "full_source_and_reference_proof"
    }
  ]
}

## Controller stage log

# Manual controller log

Execution: user requested Codex subagents, GPT-5.5 xhigh. No API runner and no pipeline-code edits. Fresh role-local agents use fork_turns=none. Canonical no-internet packet: Prompt Packet/Prompts.md.

## Setup

- Selected arXiv:2306.12918v1, its unnumbered Theorem in the source TeX. The exact theorem is the random-function equivalent of Cayley's formula, not a paraphrased tree-count statement.
- Tags fixed before solving: protocol_validation, cited_prior_result. This is a classical theorem demonstration, not a novelty or contamination benchmark.
- Controller extracted the exact target and privately retained its source proof; source spans and SHA-256 hashes are recorded in setup/target_record.json.
- Route: documented Step A1-MANUAL fallback. Neither Paper Cleaner nor Mini Python model runtime is executed.
- Support: definitions_only. No paper result or equivalent tree count is available as an assumed lemma.
- Allowed-support difficulty metadata: potentially trivializing allowed statements NO; allowed statements containing the target's main technical content NO. Rationale: only definitions and elementary finite counting/probability are granted; the enumeration and inverse construction must be proved. The conditional "if YES" justification is not applicable.
- Bounds: at most 3 solver rounds, 2 guidance items, no lemma branches. No mathematical guidance initially.
- demo_prepare: fresh GPT-5.5 xhigh agent, packet packets/setup_author.md, source-aware manual proof stripping.
- demo_preflight_privacy: fresh read-only GPT-5.5 xhigh agent. Transport and Git/private boundaries passed; S0 remains BLOCKED until a passing exact-file Step A2 audit is recorded. Git exclusion is Outputs/.gitignore:1:*.
- Sampling-temperature control is not exposed by Codex spawn. The protocol's temperature-0 Final Checker setting therefore cannot be guaranteed; this manual demonstration will disclose that boundary.

## Setup gate decision

- demo_setup_audit independently returned PASS and no blockers. The controller rechecked the exact target/skeleton/support hashes against its report before dispatch.
- TeX presentation was corrected to preserve the source's unnumbered Theorem and compiled/rendered successfully. No mathematical input was altered by that formatting fix. The final TeX hash is included in the audit.
- Section 3 grants are empty: pre-solver external-grant source checking is not applicable, not a skipped failed gate.
- S0 may now run on the hash-bound public packet, with no guidance. Key-first scheduling is mandatory.

## Solver round

- demo_s0 completed from packets/S0.md. The repository's read-only prompt parser identifies exactly five assignments and key_solver_id S3.
- S0 uses only the public skeleton, target, support rule and empty guidance. Its plan is not a mathematical premise.
- Dispatched demo_s3 from packets/S3.md. S1, S2, S4, S5 and S6 remain unstarted until S3's section-3 failure output is solved.
- All fixed solver prompts are extracted from the no-internet canonical packet. Artifact assembly uses local Python text/hash helpers only, not API clients or runtime orchestration.
- demo_s3 completed with the exact section-3 marker failure_output_type: solved. The read-only report parser confirms solved=true. This is the key-solver scheduling gate, not an independent mathematical-verifier verdict.
- Key gate passed: release S1, S2, S4 and S5. They receive their own assignments and S0 only, not the S3 response or any verifier result. Concurrency is bounded by the available Codex slots.
- demo_s1, demo_s2, demo_s4, and demo_s5 returned solved. All five parsed outputs have solved=true and setup_failure=false. S4/S5 may cite required current-round subclaims conditionally; S6 must discharge them using the actually supplied subproofs.
- Dispatched fresh demo_s6 with the exact public input, S0 and all five outputs. No private source, audit findings, controller log, or reference proof is supplied.

## Candidate and target gate

- S6 returned failure_output_type: solved. The parser confirms complete=true. Required proof, source-ledger, checklist and no-web sections were extracted by their exact markers.
- P contains S0, S1-S5, S6, and the actually submitted standalone LaTeX proof. Each component and the assembled artifact have recorded hashes. No branch proofs exist.
- Dispatched fresh demo_target_check for exact-target alignment. Citation and mathematical review have not yet started.
- demo_target_check returned MATCH, parsed problem_statement_match=yes. It explicitly checked the positive-integer domain, uniform distribution, unique-cyclic-vertex event, and 1/n conclusion in the submitted representations.
- The submitted LaTeX compiled to a two-page PDF with no overfull/underfull warnings. Both pages were visually inspected; no clipping or layout defects were found. Compilation/rendering is artifact QA, not mathematical verification.
- Dispatched fresh demo_citation_generator on the unchanged P and source ledger. It has no original source/bibliography or reference-proof access; only restricted source checking is allowed.
- Citation Generator completed: ledger complete YES, internet NO, leakage NO, unsupported sources NO, suspicious background NO, next step PROCEED_TO_CITATION_VERIFIER. All required summary fields parsed successfully.
- Dispatched fresh demo_citation_verifier on the same P, with the generated ledger and unchanged public packet.
- The optional encoding illustration was prepared after solving and was not supplied to any role. Light/dark and desktop/mobile renders have no text clipping or overlap. It illustrates the S6 construction, not an additional proof premise.

## Mathematical verifier cascade

- Citation Verifier returned GOOD_TO_GO. All source-issue flags are NO, ledger present YES, parse status OK, internet NO, no citation repair and no guidance. Source-hygiene gates permit A.
- Dispatched A1/A2/A3 as independent fresh GPT-5.5 xhigh agents on the identical packets/verifier_a.md file. They receive no sibling reports, controller opinion or reference proof. Composer A remains unstarted until all three artifacts are available.
- All three A reports are now complete: no non-fillable or fillable-only gaps, no disallowed premises, no scope omission, no web issue, no blueprint smuggling, and no guidance seed. Allowed formal-statement coupling count is 0; definitions/conventions are used, and the central bijection is proved internally.
- Dispatched fresh Composer A on those three reports only, without the original proof, target, skeleton, source, or controller opinion. B remains unstarted until the merged report is examined for routing.
- Composer A has no gaps or disallowed premises, scope full, no challenged/unaligned steps, and all reports imply the same controller verdict. Derived A status: VERIFIED. The only inventory difference is whether two elementary definitions are grouped; it does not change the allowed formal-statement coupling count of 0 or any verdict.
- Canonical A-to-B route applies. Dispatched fresh Verifier B on unchanged P and public inputs with citation evidence, but no A/Composer A reports or controller opinion.
- B returned Weakest point found? no, Missing claim None, Fillable not applicable. Its separate disallowed-premise check says None; the weakest-point disallowed field is not applicable because no vulnerable claim was found. No web sources were used. This is the canonical B-clear route, not a filled mathematical gap.
- Dispatched fresh Verifier C on unchanged P and public inputs with citation evidence. It does not receive A, Composer A, B, controller opinions, or private source material.
- C returned broke: no and no disallowed premise; no web sources were used. Its main attack tested the key leaf/suffix equivalence and was closed by the proof's existing terminal-root argument. No repair or new guidance was needed.
- Gold-blind cascade is clear. Allowed formal-skeleton coupling is 0, but the setup-time tags are protocol_validation and cited_prior_result, not paper_original_result; the low-coupling original-result override does not fire.
- Dispatched fresh privileged Final Checker with only the target, public prefix/support, unchanged P, original source, reference proof and empty guidance. No A/B/C, Composer A, citation verdicts, controller opinion, or run-tag metadata is supplied to this role. Its private output stays under private/.
- Final Checker sampling temperature remains unconfigurable in Codex, as disclosed before solving. A later PASS would be a manual Codex checker result, not evidence of an exact temperature-0 API-runtime execution.

## Final checker and controller review

- The Final Checker returned strict JSON: decision PASS, failure_category none. Its sanitized diagnosis accepts the internal fixed-root encoding/decoding, the n=1 endpoint, and the disjoint-union/probability conclusion. The private rationale and source concern remain private; only public fields are released.
- Candidate hashes were rechecked and are unchanged. The Final Checker packet was mechanically checked to include the actual candidate, gold proof, and full source, and not to include any A/Composer A/B/C or citation report.
- The fresh Decision Controller will receive run metadata, source/difficulty boundaries, the passing hash-bound audit, actual stage log/dispatch record, reports, and canonical routing rules. It is not asked to re-prove the theorem.

## Relevant decision tree


================================================================
Primary protocol map: FlowChart.md is the main operational view of the protocol. This
DECISION TREE block is the synchronized textual companion for exact acceptance and routing
details; if FlowChart.md and this block disagree, pause and reconcile them before running.

Round k. Run the multi-solver blueprint system:
  * S0(skeleton, target, guidance list H_k) -> blueprint.
  * S0 designates exactly one key solver K in S1-S5. Run K first.
  * K passes exactly when its existing S1-S5 failure output is `solved`; no separate referee or
    verifier is added at this gate.
  * If K does not pass, apply the existing controller priority to K's single failure output,
    including an eligible branch or one guidance item, skip the other four solvers and S6, and
    return to fresh S0.
  * Only if K passes do the remaining four S1-S5 solvers run their assigned subclaims.
  * S6 composes S0 + S1-S5 into final candidate artifact P_k.
P_k includes the S0 blueprint, S1-S5 subproblem outputs, and S6 composed proof for verifier
inspection, but none of those artifacts are shown to the next Solver round except through one
explicitly counted guidance item.

Pre-run validity gate:
  * If no passing skeleton leakage audit is recorded, void the run as
    "void_missing_skeleton_audit" and do not run or score the Solver.
  * If proof leakage is found in the skeleton and not fixed, void the run as
    "void_skeleton_leakage" and do not run or score the Solver.

Pre-verifier target and citation/source gates:
  * Run the Problem Statement Verifier on P_k. Check the S6 composed proof and note any
    S0/S1-S5 artifact that changes the target. If it says the proof addresses a different,
    weaker, stronger, or altered target, rerun the multi-solver system with the exact same
    guidance list and a corrected target packet. Do not append a mathematical guidance item.
  * Run the Citation Generator on P_k to produce a Source Ledger before Verifier A.
  * If the Citation Generator reports possible target-source leakage, stop the cascade and route
    to source-hygiene adjudication or void the run if leakage is confirmed.
  * If the Citation Generator recommends SOURCE_LEDGER_REPAIR_NEEDED, repair or rerun the
    citation layer with the same guidance list. Do not append a mathematical guidance item.
  * Run the Citation Verifier on the Source Ledger before Verifier A. The verification cascade
    may proceed only if the Citation Verifier returns Citation gate result = GOOD_TO_GO.
  * If the Citation Verifier returns SOURCE_LEDGER_REPAIR_NEEDED, repair or rerun the citation
    layer with the same guidance list. Do not append a mathematical guidance item.
  * If the Citation Verifier returns BLOCKING_SOURCE_ISSUE, use its candidate guidance seed
    as the guidance source unless the guidance budget is exhausted.
  * If the Citation Verifier returns LEAKAGE_RISK, stop the cascade and route to source-hygiene
    adjudication or void the run if leakage is confirmed.
  * If the Citation Verifier returns UNCLEAR, do not proceed to Verifier A; route to
    source-hygiene adjudication or rerun the Citation Verifier with the same inputs.
  * The Problem Statement Verifier may also be run on any verifier/checker report. If it says
    that report verifies or attacks the wrong target, rerun that same agent with the exact
    target. Do not append a mathematical guidance item.

Required Verifier A ensemble:
  * Run Verifier A independently as A1/A2/A3 in fresh chats using the same verifier prompt and
    inputs. Then run Composer A on the A reports only. Treat the Composer A gold report as A for
    verdict derivation, coupling, disagreement, and routing.
  * Compatibility requirement: A1/A2/A3 must all use the current artifact-based Step C Verifier A
    prompt with the same proof, target theorem, skeleton, allowed supporting statements, and
    guidance list. Composer A then merges those artifact reports.
  * Composer A does not see the proof, skeleton, target theorem, or allowed supporting
    statements. It merges verifier evidence only.
  * If A is artifact-based and does not output a verdict word, the Decision Controller derives
    VERIFIED / ALMOST VERIFIED / NOT VERIFIED / INVALID from gaps, disallowed premises, scope,
    and demonstrably false reproduced steps.

After the Problem Statement Verifier is clear, the Citation Generator reports no leakage risk,
and the Citation Verifier returns GOOD_TO_GO, run Verifier A1/A2/A3 on (skeleton, target, H_k,
P_k), then run Composer A and derive A's status from the Composer A gold report:
  * A = VERIFIED or ALMOST VERIFIED -> run B.
  * A = NOT VERIFIED or INVALID and A/Composer A provides one clear candidate guidance seed
    -> candidate guidance = A's seed; skip B and C; append one item; fresh multi-solver run.
  * A = NOT VERIFIED or INVALID but no single clear candidate guidance seed is available
    -> run B (A contributes no item yet) or route to math-gap adjudication if B/C are not
       sufficient to identify one issue.

Run Verifier B on (skeleton, target, H_k, P_k) when reached:
  * B records Weakest point found? yes and Fillable: no (or a disallowed premise at the
    weakest point) -> blocking; candidate guidance = a standalone item formed from B's
    missing claim; skip C; append one item; fresh multi-solver run.
  * B records Weakest point found? no, or B records Weakest point found? yes and Fillable: yes
    -> run C.

Run Verifier C on (skeleton, target, H_k, P_k) when reached:
  * C broke: no     -> gold-blind cascade is clear; proceed to the coupling override, then the
                       Final Checker gate (accept only if the acceptance rule below holds).
  * C broke: yes    -> candidate guidance = a standalone item formed from C's failing point;
                       append one item; fresh multi-solver run.
  * C broke: unsure -> math-gap adjudication: decide from what C says needs checking, or rerun
                       the multi-solver system once unchanged.

A-vs-rest disagreement: if A = NOT VERIFIED/INVALID but B and C are clear, do NOT auto-accept.
Use A's flagged issue as the guidance source (or adjudicate manually), then rerun.

Proof-skeleton coupling override:
  * If the run tags include "paper_original_result" and Verifier A reports LOW
    proof-skeleton coupling, do NOT auto-accept even if A/B/C otherwise pass.
    Route to COUPLING/PROVENANCE ADJUDICATION (not math-gap adjudication): a human
    chooses exactly one of
       - ACCEPT (caveated): the proof is mathematically correct but has LOW skeleton
         coupling, so it is recorded as ACCEPTED with the caveat "weak evidence for
         skeleton-guided reproduction";
       - RE-TARGET / RE-TAG: choose a different target, or correct the run tags if the
         tagging was wrong (subject to the setup-time tag rule in Operating Rule 9);
       - VOID the run as a measurement.
    Do NOT append a mathematical guidance item in this case: there is no mathematical
    gap to fix, and any "use skeleton statement X" guidance would steer the Solver toward
    the intended proof and contaminate the measurement. Record the coupling concern and
    the chosen outcome in the log.

Final Checker gate (privileged, gold-aware; runs only when the gold-blind cascade is clear and
no coupling override fired):
  * Run the Final Checker on (target, public prefix, candidate proof, gold proof, source,
    released guidance). It does NOT see the A/B/C reports, the Composer gold report, or this
    controller's opinion.
  * Final Checker = PASS -> ACCEPTED.
  * Final Checker = FAIL -> REJECTED at final check. TERMINAL for the attempt: do not rerun and
    do NOT append a guidance item (the Final Checker is a truth judge, not a hint generator).
    Record failure_category, the private rationale, and the sanitized public reason. Round
    status = "rejected_final_check".
  * A proof that cleared the gold-blind cascade but FAILS here is a logged FALSE-ACCEPT of the
    A/B/C cascade; flag it so the cascade's production false-accept rate can be counted.

Three kinds of adjudication (keep them distinct):
  * Source-hygiene adjudication: triggered by Citation Generator leakage risk, Citation
    Verifier LEAKAGE_RISK, Citation Verifier UNCLEAR, or a source issue that needs Controller
    review. The human/controller resolves whether the run should be voided, whether the citation
    layer should be rerun with the same inputs, or whether the issue is a substantive source
    issue selected as the one guidance item.
  * Math-gap adjudication: triggered by an A/B/C-flagged mathematical issue (e.g., C broke:
    unsure, A-vs-rest disagreement, or a blocking B with fillable: no). The human picks the
    single best-supported issue as the one guidance item, then reruns the multi-solver system. This path
    normally appends exactly one guidance item (subject to the stopping rule); the one exception
    is a C broke: unsure trigger, where the human may instead rerun the multi-solver system
    once unchanged with no guidance appended.
  * Coupling/provenance adjudication: triggered ONLY by the coupling override above. The
    human never appends a guidance item; the exits are caveated accept, re-target/re-tag,
    or void (see above).

Selecting the one item when several findings exist (guidance is formed from the chosen finding's
missing claim):
  1. Prefer a hard violation: a disallowed premise or substantive source issue from the
     Citation Verifier, or A reporting an omitted case or a step that is demonstrably false.
  2. Otherwise a blocking finding: A non-fillable gap, B fillable: no, or C broke: yes.
  3. Tie -> Citation Verifier before A before B before C.

Acceptance rule (record explicitly in the log):
  ACCEPT iff  Problem Statement Verifier reports no target mismatch for P_k
         AND  Citation Generator reports no target-source leakage
         AND  Citation Verifier gate result is GOOD_TO_GO
         AND  A (derived from the artifact report) has no non-fillable gap, no disallowed
              premise, and full scope
         AND  (B records Weakest point found? no, or B records Weakest point found? yes and
              Fillable: yes)
         AND  B records no disallowed premise
         AND  C broke: no, no disallowed premise
         AND  a passing skeleton leakage audit is recorded
         AND  NOT (run tags include "paper_original_result" AND allowed proof-skeleton coupling
              is LOW)
         AND  the Final Checker returns PASS.
  The gold-blind cascade (A/B/C) clearing is necessary but NOT sufficient: a cleared cascade
  sends the candidate to the Final Checker, whose PASS is the final acceptance authority and
  whose FAIL is a terminal rejection (no rerun).

Standing limitation for the controller log: citation verification audits the proof artifact,
not the model's internal memory. A citation-clean proof may still have benefited from memorized
training data. GOOD_TO_GO means source hygiene is acceptable; it does not certify
non-leakage, originality, or independence from memorized sources.

Stopping rule: at most 10 guidance items. If H_k already has 10 and the proof is not
accepted, stop and record "Not reproduced within the 10-guidance budget."

================================================================

## Problem Statement Verifier

1. Target restatement

The supplied target theorem is: for every positive integer \(n\), if \(f:[n]\to[n]\) is chosen uniformly from the finite set of all functions \([n]\to[n]\), then the probability that the associated directed graph \(G_f\), with edges \((i,f(i))\), has exactly one cyclic vertex is \(\frac{1}{n}\).

2. Statement addressed by the checked output

The checked Solver proof addresses the statement that, for every positive integer \(n\), a uniform random function \(f:[n]\to[n]\) has a unique cyclic vertex in its associated directed graph \(G_f\) with probability \(1/n\). It also gives the equivalent enumeration that exactly \(n^{n-1}\) functions \(f:[n]\to[n]\) have a unique cyclic vertex.

3. Alignment check

MATCH - the checked output addresses the same target theorem.

4. Evidence

The solver's target decomposition states: "Prove that, for a uniformly chosen function \(f:[n]\to[n]\), the event that \(G_f\) has exactly one cyclic vertex has probability \(1/n\)." Its conclusion to prove is
\[
\Pr\bigl(\{f:[n]\to[n]\colon G_f\text{ has a unique cyclic vertex}\}\bigr)=\frac1n.
\]
The submitted standalone LaTeX theorem states: "Let \(n\) be a positive integer. The probability that a uniform random function \(f:[n]\to[n]\) has a unique cyclic vertex in its associated directed graph \(G_f\) is \(1/n\)." These match the supplied target's domain, distribution, event, and conclusion.

5. Controller-facing summary

Artifact role checked:
Solver proof

Problem statement match? YES

Actual statement addressed:
For every positive integer \(n\), a uniformly chosen function \(f:[n]\to[n]\) has a unique cyclic vertex in \(G_f\) with probability \(1/n\).

Mismatch type, if any: none

Recommended controller action: continue


## Citation Generator and Source Ledger

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


## Citation Verifier

# 1. Source Ledger present?

YES. The controller-facing Citation Generator Source Ledger appears after the submitted standalone LaTeX proof under the heading "Citation Generator Source Ledger", with entries CG-SL1 through CG-SL23.

# 2. Source inventory

## provided definitions / notation / assumptions

- CG-SL1: Notation \([n]\), the standing assumption that \(n\) is positive, the function space \(\mathcal F_n\), the associated directed graph \(G_f\), and the definition of cyclic vertex. Used in the final proof opening paragraph and Steps 1, 2, and 4.

## allowed supporting statements

- CG-SL4: Uniform finite probability convention: a uniform random function is chosen uniformly from the finite function set, so event probability is favorable count divided by sample-space count. Used in final proof Steps 1 and 5.

## additional mathematical guidance items

- None. The packet states that no additional mathematical guidance is supplied.

## standard background facts

- CG-SL3: Elementary multiplication principle for the tuple count \(|[n]^n|=n^n\). Used in final proof Step 1.
- CG-SL5: Finite pigeonhole principle. Used in final proof Step 2 to obtain a repeated iterate.
- CG-SL19: Elementary finite word count: there are \(n^{n-2}\) words of length \(n-2\) over \([n]\). Used in final proof Step 3.
- CG-SL21: Finite disjoint-union counting. Used in final proof Step 4.
- CG-SL23: Elementary exponent arithmetic and cancellation, including \(n^{n-1}/n^n=1/n\). Used in final proof Step 5.

## proved inside the current proof

- CG-SL2: Tuple encoding \(f\mapsto(f(1),\ldots,f(n))\) is a bijection from \(\mathcal F_n\) to \([n]^n\). Used in final proof Step 1.
- CG-SL6: First-repetition cycle construction in a finite forward orbit. Used in final proof Step 2.
- CG-SL7: Unique-cyclic-vertex structure: the unique cyclic vertex \(r\) is fixed, and every vertex reaches \(r\). Used in final proof Step 2 and then in Step 3.
- CG-SL8: The \(n=1\) fixed-root case. Used in final proof Step 3 and Step 4.
- CG-SL9: Internal fixed-root encoding construction. Used in final proof Step 3.
- CG-SL10: Existence of a non-root \(R_k\)-leaf at each encoding step. Used in final proof Step 3.
- CG-SL11: Deleting the selected leaf preserves closure and reachability. Used in final proof Step 3.
- CG-SL12: Two-vertex terminal step \(f(b)=r\). Used in final proof Step 3.
- CG-SL13: Suffix length count for the decoding choice. Used in final proof Step 3.
- CG-SL14: Parent-remains check for the decoding assignment. Used in final proof Step 3.
- CG-SL15: The decoded function belongs to \(\mathcal A_{n,r}\). Used in final proof Step 3.
- CG-SL16: Leaf-suffix equivalence for an encoded valid function. Used in final proof Step 3.
- CG-SL17: Decoded least-leaf property. Used in final proof Step 3.
- CG-SL18: \(\Phi\) and \(\Psi\) are mutual inverses, giving the fixed-root bijection. Used in final proof Step 3.
- CG-SL20: \(A_n\) is the pairwise disjoint union of the fixed-root events \(A_{n,r}\). Used in final proof Step 4.
- CG-SL22: Assembly of the total favorable count \(|A_n|=n^{n-1}\), with \(n=1\) handled separately. Used in final proof Step 4 and Step 5.

## external cited sources

- None.

## unsupported or unclear sources

- None.

# 3. Source accuracy check

| Ledger entry | Mark | Check |
|---|---|---|
| CG-SL1 | ACCURATE | The definitions and notation appear in the supplied packet and allowed support list, and the proof uses them only as definitions. |
| CG-SL2 | ACCURATE | The tuple-encoding bijection is proved directly in Step 1. |
| CG-SL3 | ACCURATE | The multiplication principle is genuinely elementary finite-set counting and is used only for \(|[n]^n|=n^n\). |
| CG-SL4 | ACCURATE | The uniform finite probability convention is explicitly supplied and is used at the stated strength. |
| CG-SL5 | ACCURATE | The finite pigeonhole principle is standard elementary finite-set reasoning and the hypotheses are visible. |
| CG-SL6 | ACCURATE | The first-repetition cycle construction is proved in Step 2 from the directed-edge definition. |
| CG-SL7 | ACCURATE | The fixedness of \(r\) and reachability of \(r\) are proved in Step 2 under the unique-cyclic-vertex hypothesis. |
| CG-SL8 | ACCURATE | The one-point fixed-root case is proved directly in Step 3. |
| CG-SL9 | ACCURATE | The encoding construction is introduced internally, and its needed well-definedness is accounted for in CG-SL10 and CG-SL11. |
| CG-SL10 | ACCURATE | The non-root leaf existence argument is supplied in Step 3 using finite predecessor iteration and reachability to \(r\). |
| CG-SL11 | ACCURATE | Closure and reachability after leaf deletion are proved in Step 3 and are not imported. |
| CG-SL12 | ACCURATE | The terminal fact \(f(b)=r\) is proved from closure, \(f(r)=r\), and reachability. |
| CG-SL13 | ACCURATE | The suffix-length existence argument is elementary finite counting and is stated in the decoding construction. |
| CG-SL14 | ACCURATE | The proof checks both \(w_k\ne a_k\) and that \(w_k\) has not been removed earlier. |
| CG-SL15 | ACCURATE | The decoded function is shown to have only the loop at \(r\) by the increasing-index argument. |
| CG-SL16 | ACCURATE | The leaf-suffix equivalence is proved in the \(\Psi(\Phi(f))=f\) argument. |
| CG-SL17 | ACCURATE | The decoded least-leaf property is proved in the \(\Phi(\Psi(w))=w\) argument. |
| CG-SL18 | ACCURATE | The mutual-inverse conclusion follows from the two inverse checks in Step 3. |
| CG-SL19 | ACCURATE | The finite word count is elementary multiplication and is used only after the bijection is established. |
| CG-SL20 | ACCURATE | The disjoint-union decomposition is proved directly from uniqueness and the definitions of \(A_n\) and \(A_{n,r}\). |
| CG-SL21 | ACCURATE | Finite disjoint-union counting is standard background and its hypotheses are checked by Step 4. |
| CG-SL22 | ACCURATE | The total favorable count is assembled inside Step 4 from the proved fixed-root count and disjoint union. |
| CG-SL23 | ACCURATE | The exponent arithmetic and cancellation are elementary and require only \(n>0\), which is a standing assumption. |

No Source Ledger entry is overstrengthened, misquoted, assigned the wrong source status, missing a visible hypothesis check, not found, or unclear.

# 4. Missing source entries

None. The ledger accounts for the load-bearing definitions, finite-probability conversion, finite-set background facts, orbit-structure facts, fixed-root encoding/decoding proof, disjoint-union assembly, and final arithmetic. The ordinary least-element choices in finite subsets are covered within the encoding and decoding well-definedness entries and do not require an external source.

# 5. Disallowed source check

None. The proof does not cite or use the target theorem, an equivalent imported theorem, Cayley's formula, the excluded rooted-tree correspondence, the excluded height-distribution statement, or any external source. The fixed-root count is target-level load-bearing material, but it is proved inside the current proof rather than imported as a source.

# 6. Internet/source-check report

Internet used? NO

Sources checked:
None.

URLs or references checked:
None.

Any source inaccessible? NO

Possible target-source leakage encountered? NO

# 7. Controller-facing summary

Citation gate result: GOOD_TO_GO

Source Ledger present? YES

Missing source entries present? NO

Disallowed sources present? NO

Overstrengthened or misquoted sources present? NO

Suspicious standard-background claims present? NO

External source issue present? NO

Citation-only repair needed? NO

Substantive source issue present? NO

Candidate guidance seed, if any: None


## Composer A gold report

# Composer A gold Verifier A evidence report

## 1. Gold step status

1. ALL-ACCEPTED: Definitions of \(\mathcal F_n=\{f:[n]\to[n]\}\) and \(A_n=\{f\in\mathcal F_n:G_f\text{ has a unique cyclic vertex}\}\). Reports: A1 step 1, A2 step 1, A3 step 1.

2. ALL-ACCEPTED: The map \(f\mapsto(f(1),\ldots,f(n))\) is a bijection from \(\mathcal F_n\) to \([n]^n\). Reports: A1 step 2, A2 step 2, A3 step 2.

3. ALL-ACCEPTED: \(|\mathcal F_n|=n^n\). Reports: A1 step 3, A2 step 3, A3 step 3.

4. ALL-ACCEPTED: \(\Pr(A_n)=|A_n|/n^n\). Reports: A1 step 4, A2 step 4, A3 step 4.

5. ALL-ACCEPTED: Every forward orbit eventually repeats and enters a directed cycle. Reports: A1 step 5, A2 steps 5-6, A3 step 5.

6. ALL-ACCEPTED: If \(G_f\) has unique cyclic vertex \(r\), then \(f(r)=r\). Reports: A1 step 6, A2 step 7, A3 step 6.

7. ALL-ACCEPTED: If \(G_f\) has unique cyclic vertex \(r\), then every vertex reaches \(r\). Reports: A1 step 6, A2 step 8, A3 step 7.

8. ALL-ACCEPTED: For fixed \(r\), the class \(\mathcal A_{n,r}\) is defined as the functions for which \(r\) is the unique cyclic vertex. Reports: A2 step 9; A1 and A3 use this class in their fixed-root count ledgers without raising any concern.

9. ALL-ACCEPTED: For \(n=1\), the fixed-root count is \(|\mathcal A_{1,1}|=1\). Reports: A1 step 7, A2 step 10, A3 step 8.

10. ALL-ACCEPTED: For \(n\ge2\), the leaf-removal encoding \(\Phi:\mathcal A_{n,r}\to[n]^{n-2}\) is defined by repeatedly removing the least non-root \(R_k\)-leaf and recording \(w_k=f(a_k)\). Reports: A1 step 8, A2 step 11, A3 step 9.

11. ALL-ACCEPTED: A non-root \(R_k\)-leaf exists at each encoding step. Reports: A1 step 9, A2 step 12, A3 step 9.

12. ALL-ACCEPTED: Deleting the chosen encoding leaf preserves closure under \(f\) and reachability to \(r\). Reports: A1 step 10, A2 step 13, A3 step 10.

13. ALL-ACCEPTED: After \(n-2\) removals, the final non-root vertex \(b\) satisfies \(f(b)=r\). Reports: A1 step 10, A2 step 14, A3 step 11.

14. ALL-ACCEPTED: The decoding algorithm can choose the least non-root remaining element absent from the suffix \(w_k,\ldots,w_{n-2}\). Reports: A1 step 11, A2 step 15, A3 step 12.

15. ALL-ACCEPTED: The decoding assignment \(f(a_k)=w_k\) is legitimate. Reports: A1 step 12, A2 step 16, A3 step 13.

16. ALL-ACCEPTED: The decoded function lies in \(\mathcal A_{n,r}\). Reports: A1 step 13, A2 step 17, A3 step 14.

17. ALL-ACCEPTED: For an encoded valid function, a non-root remaining vertex is an \(R_k\)-leaf iff it is absent from the remaining suffix. Reports: A1 step 14, A2 step 18, A3 step 15.

18. ALL-ACCEPTED: \(\Psi(\Phi(f))=f\) for every \(f\in\mathcal A_{n,r}\). Reports: A1 step 15, A2 step 19, A3 step 16.

19. ALL-ACCEPTED: \(\Phi(\Psi(w))=w\) for every \(w\in[n]^{n-2}\). Reports: A1 step 16, A2 step 20, A3 step 17.

20. ALL-ACCEPTED: \(\Phi\) is a bijection and \(|\mathcal A_{n,r}|=n^{n-2}\) for \(n\ge2\). Reports: A1 step 17, A2 step 21, A3 step 18.

21. ALL-ACCEPTED: \(A_n=\bigsqcup_{r\in[n]}A_{n,r}\). Reports: A1 step 18, A2 step 22, A3 step 19.

22. ALL-ACCEPTED: \(|A_n|=n^{n-1}\) for every positive integer \(n\). Reports: A1 step 19, A2 step 23, A3 step 20.

23. ALL-ACCEPTED: \(\Pr(A_n)=1/n\). Reports: A1 step 20, A2 step 24, A3 step 21.

No CHALLENGED steps.

No UNALIGNED steps.

## 2. Gold unfilled gaps (union)

Empty list.

## 3. Gold disallowed premises (union)

Empty list.

## 4. Gold scope check

full

## 5. Gold coupling inventory

Allowed formal skeleton statements used beyond definitions/notation/assumptions: 0; none.

Disallowed skeleton statements cited: 0; none.

Standard-background-heavy? NO.

## 6. Disagreement map

Step/gap disagreement: none. All three reports marked all addressed proof steps justified and listed no unfilled gaps.

Fillability disagreement: none. No report raised a gap, so no fillability disagreement appears.

Disallowed-premise disagreement: none. All three reports listed no disallowed premises.

Scope disagreement: none. All three reports said the full target statement was established for every positive integer \(n\), with \(n=1\) and \(n\ge2\) covered.

Coupling-count disagreement: none for the required coupling inventory categories. All three reports listed 0 allowed formal skeleton statements used beyond definitions/notation/assumptions, 0 disallowed skeleton statements cited, and Standard-background-heavy? NO. A non-verdict inventory difference appears only in definitions/notation/assumptions counted from the cleaned skeleton: A1 counted 6, A2 counted 7, and A3 counted 6.

Same controller verdict across reports: all agree. Each run's report, on its own, would imply the same controller verdict: no non-fillable gaps, no fillable-only gaps, no disallowed premises, no omitted case or weaker statement, no web-source issue, and candidate guidance seed None.

## 7. Web-source roll-up

Empty list.

## 8. Gold Verifier A evidence report for the Decision Controller

Non-fillable gaps present? NO

Fillable-only gaps present? NO

Disallowed premises present? NO

Omitted case / weaker statement present? NO

Allowed formal skeleton statements used beyond definitions: 0 + []

Disallowed skeleton statements cited: 0 + []

Standard-background-heavy? NO

Web-source issue? NO

Same issue recurring across reports? NO

Candidate guidance seed, if any: None


## Verifier B

1. Weakest point

No weakest point found.

2. Why this is the weakest point

Every load-bearing step inspected in the composed S6 proof is justified from the allowed definitions, elementary finite-set/probability background, or arguments proved inside the proposed proof. The fixed-root enumeration, which is the only nontrivial part under the definitions-only support policy, is expanded by an explicit leaf-removal encoding, a decoding algorithm, and mutual-inverse checks. The proof does not import Cayley's formula, the rooted-tree correspondence, the target theorem, or any external source.

3. Weakest point location

unclear / not applicable

4. Source status of the vulnerable claim

Not applicable: no vulnerable claim found. The inspected load-bearing inputs are definitions or notation explicitly available in the cleaned skeleton PDF or TeX file, the allowed uniform finite probability convention, standard background, and claims introduced and proved inside the proposed proof.

5. Issue type

Not applicable: no issue found.

6. What must be proved to close it (the missing claim)

None.

7. Fillable?

fillable: not applicable - no weakest point is found.

8. Disallowed-premise check

None.

9. Web-source confirmation

no web sources used

Final summary format:

Weakest point found? no
Weakest point (step + claim, or "None"): None
Weakest point location (inside key step / outside key step / blueprint / S1-S5 / no key step / unclear / not applicable): unclear / not applicable
Source status: not applicable; no vulnerable claim found
Missing claim, or "None": None
Fillable: not applicable
Disallowed premise at the weakest point? not applicable


## Verifier C

1. Most serious possible failure point

The most serious possible failure point is the leaf-suffix equivalence in the [KEY STEP] fixed-root enumeration. This equivalence is what makes the Prufer-style encoding and decoding choose the same removed vertices; if it fails, the claimed bijection \(\mathcal A_{n,r}\cong [n]^{n-2}\) is not established, and the numerator count \(n^{n-1}\) loses its only nontrivial support.

2. Exact location

Final proof, Step 3, inverse proof:

\[
y\text{ is an }R_k\text{-leaf}
\quad\Longleftrightarrow\quad
y\text{ does not occur among }w_k,\ldots,w_{n-2}.
\]

The vulnerable transition is the converse direction:

"Conversely, if \(y\) is not an \(R_k\)-leaf, choose \(z\in R_k\setminus\{y\}\) with \(f(z)=y\). Since \(y\ne r\), this \(z\) cannot be \(r\); and from the terminal observation above it cannot be the final non-root vertex \(b\), because \(f(b)=r\). Thus \(z=a_j\) for some \(j\ge k\), and \(w_j=f(a_j)=y\)."

3. Attack location

inside [KEY STEP]

4. Source status of the vulnerable claim

introduced and proved inside the proposed proof; standard background; definition or notation explicitly available in the cleaned skeleton PDF or TeX file

5. Why the proof could fail there

The attack is that "not an \(R_k\)-leaf" only says some still-present vertex \(z\ne y\) maps to \(y\). To justify that \(y\) appears in the remaining code suffix, the proof must rule out all still-present vertices other than future removed vertices \(a_j\), \(j\ge k\), as possible sources of this edge. In particular, it must rule out the root \(r\) and the final unremoved non-root vertex \(b\), and it must know that every other still-present non-root vertex is one of the future \(a_j\)'s. If \(b\) could map to \(y\ne r\), then \(y\) could fail to be a leaf without appearing as any recorded suffix letter, so the encoding and decoding algorithms might choose different vertices.

The proof supplies the needed checks. It previously proves in the encoding induction that after the \(n-2\) removals the final remaining set is \(\{r,b\}\), with \(f(r)=r\) and \(f(b)=r\). Therefore neither \(r\) nor \(b\) can be the chosen source \(z\) for an edge to \(y\ne r\). Since \(z\in R_k\), \(z\) also cannot be an already removed vertex. Hence \(z\) must be one of the future removed vertices \(a_j\) with \(j\ge k\), so \(y=w_j\) does occur in the suffix. This closes the apparent gap.

6. Did it break?

broke: no - the attack does not succeed; the proof is robust at this point because the terminal fact \(f(b)=r\), the root identity \(f(r)=r\), and the description of \(R_k\) after prior removals together force any remaining non-root predecessor of \(y\ne r\) to be a future removed vertex whose image is recorded in the suffix.

7. Disallowed-premise check

Empty. The attacked point does not rely on the target theorem, an equivalent or stronger statement, a textually downstream cleaned-skeleton statement, a cleaned-skeleton statement not in the allowed list, or an external fact. The fixed-root count is load-bearing, but it is proved inside the proposed proof rather than imported as a premise.

8. Three most delicate points

1. Leaf existence during encoding. To certify it, check that the predecessor map \(p\) is defined entirely on \(R_k\setminus\{r\}\), and that a cycle of \(p\) really gives a directed cycle for \(f\) outside \(r\). The proof checks this using \(f(r)=r\), finite repetition, and reachability to \(r\).

2. Decoding parent-remains check. To certify it, check that each letter \(w_k\) has not already been removed and is not equal to the vertex \(a_k\) currently being removed. The proof checks this from the suffix-avoidance rule: \(a_k\) is absent from the suffix containing \(w_k\), and an earlier removed \(a_j\) was absent from its own suffix, which also would have contained \(w_k\) if \(w_k=a_j\).

3. Mutual inverse proof for the fixed-root code. To certify it, check both directions: for an encoded valid function, leaves are exactly vertices absent from the remaining suffix; for a decoded word, the chosen absent least vertex is exactly the least remaining leaf. The proof supplies both checks and uses only finite-set reasoning plus facts already proved in the key step.

9. Web-source confirmation

no web sources used

Final summary format:

Most serious attack (step + claim): Step 3 [KEY STEP], the claim that for \(y\in R_k\setminus\{r\}\), \(y\) is an \(R_k\)-leaf if and only if \(y\) does not occur among \(w_k,\ldots,w_{n-2}\).
Attack location (inside key step / outside key step / blueprint / S1-S5 / no key step / unclear / not applicable): inside key step
Broke: no
If broke, the false claim or failing step:
If unsure, exact check needed to decide:
Source status: introduced and proved inside the proposed proof; standard background; definition or notation explicitly available in the cleaned skeleton PDF or TeX file
Disallowed premise at the attacked point? no


## Final Checker public report

{
  "decision": "PASS",
  "failure_category": "none",
  "public_diagnosis": [
    "The proof is acceptable: it supplies an internal fixed-root enumeration by an explicit encoding and decoding, handles n=1, then uses only disjoint-union counting and finite uniform probability arithmetic to obtain the target probability."
  ]
}

Decision Controller outcome -> controller-log round status (use this when filling the log):
  * ACCEPTED                                               -> accepted
  * RERUN_SOLVER_WITH_GUIDANCE                             -> rejected_with_guidance
  * RERUN_SOLVER_SAME_GUIDANCE_EXACT_TARGET                 -> non-terminal target-alignment rerun; no guidance item
  * RERUN_CITATION_LAYER_SAME_GUIDANCE                     -> non-terminal source-ledger repair/rerun; no guidance item
  * RERUN_SAME_AGENT_EXACT_TARGET                           -> non-terminal verifier/checker rerun; no guidance item
  * REJECTED_FINAL_CHECK                                   -> rejected_final_check
  * HUMAN_ADJUDICATION_REQUIRED, kind = math_gap           -> math_gap_adjudication
  * HUMAN_ADJUDICATION_REQUIRED, kind = source_hygiene -> source_hygiene_adjudication
  * HUMAN_ADJUDICATION_REQUIRED, kind = coupling_provenance -> coupling_provenance_adjudication,
        then the human's chosen exit sets the final logged status:
          caveated accept -> accepted_caveated_low_coupling
          re-target/re-tag -> retargeted
          void as a measurement -> (record the void reason)
  * INVALID_SETUP                                          -> void_setup_failure
  * VOID_MISSING_SKELETON_AUDIT                            -> void_missing_skeleton_audit
  * VOID_SKELETON_LEAKAGE                                  -> void_skeleton_leakage
  * VOID_TARGET_SOURCE_LEAKAGE                             -> void_target_source_leakage
  * VOID_WEB_CONTAMINATION                                 -> void_web_contamination
  * STOPPED_BUDGET                                         -> stopped_budget_reached
  * RUN_NEXT: Problem Statement Verifier / Citation Generator / Citation Verifier /
    Verifier A1/A2/A3 / Verifier B / Verifier C / Final Checker -> non-terminal; no round status yet
Note: the Decision Controller never emits a caveated accept itself. Low-coupling paper-original
runs route to HUMAN_ADJUDICATION_REQUIRED (coupling_provenance); the human's exit determines the
final logged status.
