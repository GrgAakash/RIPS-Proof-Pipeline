<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../docs/rips-proof-mark-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="../docs/rips-proof-mark.png">
    <img src="../docs/rips-proof-mark.png" width="132" alt="RIPS Proof Pipeline project mark">
  </picture>
</p>

<h1 align="center">PromptRIPS Protocol Flow</h1>

<p align="center">
  <strong>Operational order, evidence gates, rerun paths, and terminal outcomes.</strong>
</p>

<p align="center">
  <a href="../README.md">Project home</a> ·
  <a href="README.md">Prompt protocol</a> ·
  <a href="Prompts.md">No-internet packet</a> ·
  <a href="PromptsWithFullInternet.md">Source-supported packet</a>
</p>

[![RIPS Proof Pipeline overview](../docs/pipeline-overview.svg)](../README.md#how-the-pipeline-works)

> 🧭 **Reading guide:** Start with the one-minute table, then open the
> integrated-runtime map for the exact automated route. Dashed arrows in the
> later diagrams are manual or standalone-protocol paths; the integrated
> `solver/` runtime does not execute them automatically.

## Protocol in one minute

| Phase | What happens | Live implementation boundary |
|---:|---|---|
| **1. Prepare** | Paper Cleaner selects the target; Mini builds and audits the public packet; the Section 3 source gate runs when needed | arXiv wrappers prepare Steps 1-5; `run-cleaner-solver` starts from that prepared paper and enforces Mini/audit/source gates; hand-authored `run-open-problem` inputs bypass setup gates |
| **2. Reconstruct** | S0 plans and selects one key solver; that solver must pass before the other four S1-S5 roles and S6 run | automated by `solver/orchestrator.py` |
| **3. Validate sources** | Problem Statement Verifier checks the exact target; Citation Generator/Verifier check the source ledger | automated before mathematical verification |
| **4. Review mathematics** | A1/A2/A3 review independently; Composer A merges; B finds the weakest point; C attacks it | automated with conservative human-review exits for malformed or contradictory reports |
| **5. Decide** | The deterministic controller accepts, reruns, branches, requests human review, stops, or invokes the private Final Checker | public-only runs can reach `accepted_cascade_only`; private runs require Final Checker PASS for `accepted` |
| **6. Extend or audit** | Coupling/provenance adjudication and Controller Audit remain available in the written protocol | coupling exists in the standalone verifier package; Controller Audit is external/manual, not invoked by the integrated runtime |

### Authority boundary

- [Prompts.md](Prompts.md) and
  [PromptsWithFullInternet.md](PromptsWithFullInternet.md) define the role
  contracts and full manual protocol.
- `Individual Pipeline/solver/*.py` defines what the integrated command-line
  runtime actually executes.
- A persisted controller decision is **auditable**, but it is not
  **independently audited** unless a separate Controller Audit is run.
- The terminal `state.json` status and the gates that actually ran are the
  authoritative result of an automated run.

## Choose a view

<details>
<summary><strong>1. Integrated runtime map</strong> — exact automated order and exits</summary>

This is the route executed by `python -m solver run-open-problem`. Setup gates
are guaranteed only when the input bundle came through `run-cleaner-solver`.
Both prompt packets use the key-solver-first schedule shown below.

```mermaid
flowchart TD
    classDef input fill:#f6f8fa,stroke:#8b949e,color:#24292f;
    classDef agent fill:#eaf4ff,stroke:#4b8fd8,color:#0b2545;
    classDef verifier fill:#fff7e6,stroke:#d99000,color:#332000;
    classDef controller fill:#f1f8f4,stroke:#2da44e,color:#12361f;
    classDef decision fill:#ffffff,stroke:#8b949e,color:#24292f;
    classDef terminal fill:#fdeeee,stroke:#d1242f,color:#3b0d0d;
    classDef record fill:#f6f8fa,stroke:#8b949e,color:#24292f,stroke-dasharray:4 3;

    inputs["Prepared or hand-authored<br/>solver inputs"]:::input
    s0["S0 Blueprint<br/>selects key solver K"]:::agent
    key["Run K first"]:::agent
    keyGate{"K solved?"}:::decision
    rest["Run remaining four<br/>S1-S5 solvers"]:::agent
    s6["S6 Composer"]:::agent
    complete{"Complete candidate?"}:::decision
    assemble["Deterministic final assembly<br/>attach hash-checked branch proofs"]:::controller

    solverRoute{"Solver controller route"}:::decision
    branch["Open bounded recursive branch"]:::controller
    branchResult{"Branch result"}:::decision
    reconsider["Reconsider failure pool<br/>without another branch"]:::controller

    psv["Problem Statement Verifier"]:::verifier
    target{"Exact target?"}:::decision
    citeG["Citation Generator"]:::verifier
    cgGate{"Generator result"}:::decision
    citeV["Citation Verifier"]:::verifier
    cvGate{"Citation gate"}:::decision
    repair["Citation-only repair<br/>same proof and same H_k"]:::controller
    attempts{"Attempts remain?"}:::decision
    exhausted{"Prior no-guidance rerun<br/>already recorded?"}:::decision

    runCascade{"Run A/B/C cascade?"}:::decision
    skipGold{"Private gold proof present?"}:::decision
    a["A1/A2/A3 in parallel"]:::verifier
    composer["Composer A"]:::verifier
    aGate{"Derived A route"}:::decision
    b["Verifier B"]:::verifier
    bGate{"Readable B route"}:::decision
    c["Verifier C"]:::verifier
    cGate{"Readable C route"}:::decision

    private{"Private gold proof present?"}:::decision
    finalCheck["Final Checker<br/>isolated and gold-aware"]:::verifier
    finalGate{"Final Checker output"}:::decision
    accepted(["accepted"]):::terminal
    cascadeOnly(["accepted_cascade_only<br/>not privately checked"]):::terminal
    rejected(["rejected_final_check<br/>terminal, no rerun"]):::terminal

    guidance["Append exactly one<br/>counted guidance item"]:::controller
    budget{"Guidance budget<br/>already exhausted?"}:::decision
    retrySame["Rerun S0 with same H_k<br/>no guidance appended"]:::controller
    roundLimit{"Maximum rounds reached<br/>before another round?"}:::decision
    human["needs_human_review<br/>with adjudication kind"]:::terminal
    stopped(["stopped_budget"]):::terminal
    maxStopped(["stopped_max_rounds"]):::terminal
    persisted["Controller decision and artifacts persisted<br/>auditable; not automatically audited"]:::record

    inputs --> s0 --> key --> keyGate
    s0 -->|"setup failure / leakage marker"| human
    keyGate -->|"yes"| rest --> s6 --> complete
    keyGate -->|"no"| solverRoute
    complete -->|"no"| solverRoute
    complete -->|"yes"| assemble --> psv --> target

    solverRoute -->|"branch lemma"| branch --> branchResult
    branchResult -->|"proved or conservatively disproved"| guidance
    branchResult -->|"inconclusive"| reconsider --> solverRoute
    solverRoute -->|"forbidden-route or ordinary-hint item"| guidance
    solverRoute -->|"no usable item: first occurrence"| retrySame
    solverRoute -->|"repeated no-useful result / setup issue"| human

    target -->|"yes"| citeG --> cgGate
    target -->|"no: first occurrence"| retrySame
    target -->|"unclear or repeated no"| human
    cgGate -->|"proceed"| citeV --> cvGate
    cgGate -->|"ledger repair"| repair
    cgGate -->|"leakage / unclear"| human
    cvGate -->|"GOOD_TO_GO"| runCascade
    runCascade -->|"yes"| a
    runCascade -->|"no"| skipGold
    skipGold -->|"yes"| finalCheck
    skipGold -->|"no"| human
    cvGate -->|"ledger repair"| repair
    cvGate -->|"blocking issue + seed"| guidance
    cvGate -->|"leakage / unclear / no seed"| human
    repair --> attempts
    attempts -->|"yes"| citeG
    attempts -->|"no"| exhausted
    exhausted -->|"no"| retrySame
    exhausted -->|"yes"| human

    a --> composer --> aGate
    aGate -->|"VERIFIED / ALMOST"| b
    aGate -->|"NOT VERIFIED / INVALID, no seed"| b
    aGate -->|"blocking + one seed"| guidance
    aGate -->|"no majority"| human
    b --> bGate
    bGate -->|"clean, readable, no disallowed premise"| c
    bGate -->|"blocking + stated missing claim"| guidance
    bGate -->|"contradictory / unreadable / no seed"| human
    c --> cGate
    cGate -->|"broke yes + failing point"| guidance
    cGate -->|"broke no + A clear + no disallowed premise"| private
    cGate -->|"unsure / unreadable / no failing point / disallowed / A blocked"| human

    private -->|"no"| cascadeOnly
    private -->|"yes"| finalCheck --> finalGate
    finalGate -->|"PASS"| accepted
    finalGate -->|"FAIL"| rejected
    finalGate -->|"unparseable"| human

    guidance --> budget
    budget -->|"yes"| stopped
    budget -->|"no"| roundLimit
    retrySame --> roundLimit
    roundLimit -->|"no"| s0
    roundLimit -->|"yes"| maxStopped

    accepted -.-> persisted
    cascadeOnly -.-> persisted
    rejected -.-> persisted
    human -.-> persisted
    stopped -.-> persisted
    maxStopped -.-> persisted
```

</details>

<details>
<summary><strong>2. Setup and branch detail</strong> — enforced and optional entry paths</summary>

Solid arrows are enforced by the integrated wrapper or solver runtime. Dashed
arrows are recommended manual safeguards or prompt-protocol operations.

```mermaid
flowchart TD
    classDef input fill:#f6f8fa,stroke:#8b949e,color:#24292f;
    classDef step fill:#eaf4ff,stroke:#4b8fd8,color:#0b2545;
    classDef audit fill:#fff7e6,stroke:#d99000,color:#332000;
    classDef decision fill:#ffffff,stroke:#8b949e,color:#24292f;
    classDef guidance fill:#f1f8f4,stroke:#2da44e,color:#12361f;
    classDef manual fill:#fffaf0,stroke:#d0a85c,color:#3b2b00,stroke-dasharray:4 3;
    classDef terminal fill:#fdeeee,stroke:#d1242f,color:#3b0d0d;

    entry{"Input route"}:::decision
    paper["arXiv ID or URL"]:::input
    upstream["Paper Cleaner Steps 1-5<br/>download, index, select"]:::step
    mini["Paper Cleaner Mini<br/>target-scoped package"]:::step
    audit["Independent package audit<br/>exact target and SHA-256"]:::audit
    auditGate{"Audit passes?"}:::decision
    sourceNeed{"External Section 3 grants?"}:::decision
    source["Skeleton Source Generator<br/>and Verifier"]:::audit
    sourceGate{"GOOD_TO_GO?"}:::decision
    export["Deterministic solver bundle export"]:::step
    hand["Hand-authored target.md<br/>and skeleton.md/.tex"]:::input
    manualAudit["Recommended external audit<br/>not enforced by run-open-problem"]:::manual
    stopSetup(["Stop before solver"]):::terminal
    runtime["Integrated S0-S6 runtime"]:::step

    failure["Key solver or composed-proof failure"]:::input
    priority{"Highest-priority usable finding"}:::decision
    branchable{"Branch eligible and<br/>within depth/count/budget?"}:::decision
    recursive["Run bounded recursive pipeline"]:::step
    result{"Branch terminal result"}:::decision
    proved["Accepted branch: seal proof body<br/>release E### statement only"]:::guidance
    disproved["Conservatively disproved:<br/>release counted warning"]:::guidance
    inconclusive["Reconsider parent failure pool<br/>with branching disabled"]:::guidance
    parent["Append at most one item<br/>and restart parent at S0"]:::step
    noItem{"Repeated no-guidance<br/>result?"}:::decision
    retry["Restart parent at S0<br/>with unchanged H_k"]:::step
    review(["needs_human_review"]):::terminal

    entry -->|"recommended wrapper"| paper --> upstream --> mini --> audit --> auditGate
    auditGate -->|"fail / stale / missing"| stopSetup
    auditGate -->|"pass"| sourceNeed
    sourceNeed -->|"no"| export
    sourceNeed -->|"yes"| source --> sourceGate
    sourceGate -->|"yes"| export --> runtime
    sourceGate -->|"no / unclear / leakage"| stopSetup

    entry -->|"direct CLI"| hand --> runtime
    paper -.->|"manual full-paper fallback"| hand
    hand -.->|"recommended safeguard"| manualAudit
    manualAudit -.->|"if accepted"| runtime

    failure --> priority
    priority -->|"forbidden-route item"| parent
    priority -->|"branch lemma"| branchable
    priority -->|"ordinary-hint item"| parent
    priority -->|"no useful item"| noItem
    branchable -->|"yes"| recursive --> result
    result -->|"proved"| proved --> parent
    result -->|"disproved"| disproved --> parent
    result -->|"inconclusive"| inconclusive --> priority
    branchable -->|"no: reconsider lower-priority findings"| inconclusive
    noItem -->|"no"| retry --> runtime
    noItem -->|"yes"| review
    parent --> runtime
```

</details>

## Protocol-only extensions and guidance selection

The next view deliberately separates paths that the integrated runtime executes
from paths that still require the standalone verifier package or a human
operator.

<details>
<summary><strong>3. Manual extensions and one-item policy</strong> — no hidden automation</summary>

```mermaid
flowchart TD
    classDef runtime fill:#eaf4ff,stroke:#4b8fd8,color:#0b2545;
    classDef manual fill:#fffaf0,stroke:#d0a85c,color:#3b2b00,stroke-dasharray:4 3;
    classDef decision fill:#ffffff,stroke:#8b949e,color:#24292f;
    classDef result fill:#f1f8f4,stroke:#2da44e,color:#12361f;
    classDef terminal fill:#fdeeee,stroke:#d1242f,color:#3b0d0d;

    cClear["A/B/C cascade clear"]:::runtime
    routeMode{"Controller surface"}:::decision
    finalMode["Private/gold decision<br/>then Final Checker when available"]:::runtime
    coupling{"paper_original_result<br/>and LOW coupling?"}:::decision
    couplingAdj["Coupling/provenance adjudication<br/>no mathematical guidance"]:::manual
    caveat(["Caveated accept"]):::terminal
    retag(["Re-target or re-tag"]):::terminal
    void(["Void measurement"]):::terminal

    outcomes["Any persisted controller outcome"]:::runtime
    audit["Optional external Controller Audit<br/>not invoked by integrated runtime"]:::manual

    firstBlock["Integrated runtime:<br/>first blocking stage reached"]:::runtime
    autoSeed{"One mechanically supported seed?"}:::decision
    one["Append exactly one item"]:::result
    human["Human adjudication"]:::manual
    candidates["Findings available to human"]:::manual
    hard{"Any hard violation?"}:::decision
    blocking{"Any blocking finding?"}:::decision
    chooseHard["Use hard violation"]:::result
    chooseOrder["Tie order:<br/>Citation Verifier, A, B, C"]:::result
    unchanged["No item; unchanged rerun<br/>only where protocol permits"]:::result

    cClear --> routeMode
    routeMode -->|"integrated runtime"| finalMode
    routeMode -.->|"standalone verifier / manual protocol"| coupling
    coupling -->|"yes"| couplingAdj
    coupling -->|"no"| finalMode
    couplingAdj --> caveat
    couplingAdj --> retag
    couplingAdj --> void

    outcomes -.->|"if separately requested"| audit

    firstBlock --> autoSeed
    autoSeed -->|"yes"| one
    autoSeed -->|"no or ambiguous"| human --> candidates
    candidates --> hard
    hard -->|"yes"| chooseHard
    hard -->|"no"| blocking
    blocking -->|"yes"| chooseOrder
    blocking -->|"no"| unchanged
```

</details>

## Operational invariants

| Rule | Boundary that must remain true |
|---|---|
| **Fresh contexts** | Solver and verifier roles run in fresh temporary chats; only controller-approved counted guidance crosses rounds. |
| **Key solver first** | S0 designates one key solver; the other four S1-S5 roles and S6 wait until it reports `solved`. |
| **One-item state** | At most one guidance item is appended per ordinary rerun; target and citation repairs do not create mathematical guidance. |
| **Citation-only repair** | Source-ledger repair retries the citation layer on the same proof and same `H_k` before any unchanged full solver rerun. |
| **Sealed branch proofs** | Later solvers receive the accepted statement and permission, not the branch proof body; deterministic assembly releases the hash-checked proof only at the end. |
| **Source before mathematics** | Target and citation/source gates clear before A1/A2/A3 run. |
| **Controller owns outcomes** | Model roles report structured findings; deterministic routing and the recorded terminal status determine the workflow outcome. |
| **Final Checker isolation** | When private material is present, the gold-aware Final Checker runs last without internet or verifier/controller opinions; FAIL is terminal and malformed output requires human review. |
| **Public-only boundary** | Without private gold material, a clear cascade ends as `accepted_cascade_only`, never `accepted` or “privately checked.” |
| **Audit semantics** | Runtime decisions are persisted for audit. Controller Audit and coupling/provenance adjudication are not automatic integrated-runtime stages. |

<details>
<summary><strong>Full protocol notes</strong> — implementation and interpretation rules</summary>

### Full protocol notes

- This file separates the integrated runtime from the fuller manual protocol. The DECISION TREE
  block in Prompts.md remains the authority for manual role contracts; the integrated-runtime
  map above follows the checked-in Python controller. Do not present a manual-only edge as an
  automated stage.
- Every Solver and Verifier run is a fresh temporary chat (Markovian); the only state carried
  forward into a later Solver prompt is the cumulative guidance list. S0, S1-S5, and S6 are
  internal current-round solver chats. Their blueprint/subproof/composition artifacts may be
  inspected by verifiers for that round, but they are not carried into the next Solver round
  except through one explicitly counted guidance item.
- An accepted branch contributes one guidance item labeled E###: exact statement, independently
  verified status, permission to use without reproof, and use location. Its proof body, failed
  attempts, solver history, and verifier reports stay out of every later Solver prompt. After S6,
  deterministic code verifies the sealed proof hash and attaches the proof to the final artifact;
  nested accepted branch proofs are already included transitively. Missing or changed sealed
  artifacts stop before citation and proof verification.
- The Solver system is S0 blueprint, S1-S5 subproblem solvers, and S6 composer. S0 designates
  exactly one key solver in S1-S5; that solver runs first, and the other four plus S6 are skipped
  when it does not report `solved`. After a complete S6 result, the final-only assembler produces
  verifier-facing P_k by attaching any sealed accepted-branch proofs.
- Paper Cleaner Mini is the primary setup path. It produces a
  `target_scoped_proof_informed` package, which is a stronger and more targeted input condition
  than the manual full-paper skeleton fallback. Deterministic code, not another LLM, maps its
  audited seven sections to the solver input files.
- For a new public paper, the primary mathematical input is one arXiv ID or
  arxiv.org URL. The existing Paper Cleaner performs only Steps 1-5 to
  download and flatten the source, index statements and proofs, analyze
  dependencies, and select `mains` plus `hardest`. Its older package and
  verification stages do not run; Paper Cleaner Mini owns package generation.
- `Prompts.md` keeps Solver chats no-internet; `PromptsWithFullInternet.md` runs S0-S6 in
  source-supported internet mode. Verifier A/B/C remain no-internet in both modes. The Skeleton
  Source Generator/Verifier and post-proof Citation Generator/Verifier are restricted-internet
  source-checking roles.
- The Problem Statement Verifier checks that candidate artifact P_k addresses the exact target.
  In the integrated runtime, a clear first mismatch reruns S0-S6 unchanged; a repeated mismatch
  or an `UNCLEAR` report requires human target-alignment review. No path appends mathematical
  guidance for a target repair. The manual protocol may also apply this check to verifier or
  checker reports.
- Citation Generator creates a Source Ledger and Citation Verifier checks source hygiene before
  Verifier A runs. Both citation roles may use internet access only for source checking: common
  theorem names, standard background facts, textbook-level references, named inequalities,
  named identities, exact statements of cited theorems, and whether a claimed standard result is
  actually standard. They must not search for the target theorem, target label, original target
  source, target proof, distinctive target phrases, or any original proof or solution.
- Verifier A1/A2/A3 do not run until Citation Verifier returns GOOD_TO_GO and no citation-role
  leakage risk is present. Source-ledger repair first reruns the Citation Generator/Verifier layer
  on the same proof and same H_k, up to the configured attempt limit. An exhausted first repair
  result triggers an unchanged full solver rerun; a repeated no-guidance result requires human
  source-hygiene review. A substantive source issue can become the one guidance item.
- Citation Generator and Citation Verifier reports are controller-visible only. They are not
  passed to future Solver runs except through one explicitly counted standalone guidance item.
- A recorded passing skeleton audit bound to the exact skeleton SHA-256 is a hard gate for the
  recommended `run-cleaner-solver` path. Missing, failed, or hash-stale audit results stop that
  path before Solver scoring; a nonempty Section 3 additionally requires a GOOD_TO_GO source
  gate. The lower-level `run-open-problem` command accepts hand-authored inputs and does not
  enforce these setup records, so those inputs must not be described as cleaner-audited.
- Run interpretation is a set of tags, not a single label. For example, a run can be both
  `protocol_validation` and `cited_prior_result`.
- Run tags are fixed at setup before the Solver runs; they must not be edited based on verifier
  output. In particular, the `paper_original_result` tag may not be dropped after seeing the
  coupling assessment.
- In the current Prompts.md, Verifier A1/A2/A3 are artifact-based. They report gaps, disallowed premises, scope coverage,
  false reproduced steps, allowed coupling, and disallowed citations. They do not emit the final
  verdict word, confidence, seriousness, or "obvious and decisive" label.
- The Decision Controller derives Verifier A's status from Composer A's gold report from the required A1/A2/A3 ensemble.
- Verifier B and C are also field-based: B reports whether a weakest point was found plus
  `fillable: yes/no/not applicable`; C reports the attack plus `broke: yes/no/unsure`. Neither emits severity,
  seriousness, confidence, or a verdict word; the Decision Controller routes on fillable/broke.
- The Final Checker is a privileged, gold-aware LLM referee that runs LAST when private gold
  material is present. It sees the gold proof and source but NOT verifier reports, Composer
  output, or controller opinion, and runs with no internet at temperature 0. PASS = `accepted`;
  FAIL = terminal `rejected_final_check` with no rerun or guidance item; malformed output requires
  human review. Without private gold, a clear cascade ends as `accepted_cascade_only`, which is
  not a private correctness certification.
- Composer A is required for the current Verifier A layer. It sees only the Verifier A reports, not the proof, skeleton,
  target theorem, or allowed supporting statements. It preserves every issue any A run flagged and
  surfaces disagreement instead of majority-voting problems away.
- Disallowed skeleton citations are violations. They are recorded separately and do not count as
  positive proof-skeleton coupling.
- The full prompt protocol and standalone verifier package can compute proof-skeleton coupling.
  For paper-original targets, LOW allowed coupling routes there to coupling/provenance
  adjudication even if A/B/C otherwise pass. The integrated S0-S6 runtime does not currently load
  this metadata or execute that override; its diagram therefore marks the edge as non-automatic.
- Coupling/provenance adjudication has exits only: caveated accept, re-target/re-tag, or void. It
  does not append mathematical guidance, because there is no math gap to fix and guidance toward a
  skeleton statement would steer the Solver.
- Training-data leakage and unbounded "standard background" are treated as the same
  provenance-risk problem; the coupling check is the controller-level mitigation.
- Out-of-loop feedback from another model or a human is protocol review, not in-loop
  heterogeneous verification. To affect acceptance, a different model or human checkpoint must run
  inside the verifier cascade with the same structured fields.
- Solver chats see their assigned solver packet(s). Verifier chats see their verifier packet,
  which includes proposed proof artifact P_k and is therefore built only after final assembly.
  The manual Prompt Assembler prepares ready-to-paste packets; the integrated runtime renders
  those prompts dynamically. Verifiers do not see the operating rules, decision tree, controller
  log, paper metadata, or arXiv URL.
- The accept/reject combination, one-item selection, and stopping rule live in deterministic
  controller code for integrated runs and in the external controller log for manual runs; they do
  not live in any Solver or Verifier prompt.
- Controller Audit is an optional independent check of whether the Decision Controller followed
  the protocol. The integrated runtime persists every controller decision but does not invoke the
  Controller Audit role. If that role is run externally, record its result without relabeling a
  merely persisted decision as independently audited.
- This chart shows the controller-level loop. The run log should still record the paper ID,
  target theorem, run tags, target scope, skeleton filenames and checksum, skeleton audit and
  pre-solver external-grant gate status,
  solver output, verifier outputs, Composer A output, derived A status, allowed coupling,
  disallowed citations, Decision Controller outcome, Controller Audit result if separately run, web-source audit,
  acceptance decision, and any appended guidance item.

</details>
