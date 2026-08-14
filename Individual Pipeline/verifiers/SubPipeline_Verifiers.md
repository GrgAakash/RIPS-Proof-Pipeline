# SubPipeline: Verifiers

This visual maps the standalone verifier subpipeline. It shows where the current verifier cascade ends and what the real next protocol step should be.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"background": "#F6FBFF", "fontFamily": "Inter, Segoe UI, Arial", "fontSize": "24px", "primaryTextColor": "#F8FAFC", "primaryBorderColor": "#071A33", "lineColor": "#071A33", "edgeLabelBackground": "#F6FBFF"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 52, "rankSpacing": 62, "curve": "basis", "padding": 20}}}%%
flowchart TB
    title["SubPipeline: Verifiers"]
    input["Input proof package<br/>target + allowed statements + proof + skeleton_ref"]

    ensemble["Verifier A ensemble<br/>A1 + A2 + A3 independent runs"]
    composer["Composer A<br/>merges A reports only<br/>blind to proof, target, skeleton, allowed statements"]
    acheck["A routing check<br/>disallowed premise / no majority / A status / guidance seed"]

    b["Verifier B<br/>single weakest point report<br/>weakest_point + source_status + missing_claim + fillable"]
    bcheck["B routing check<br/>fillable + disallowed premise at weakest point"]
    c["Verifier C<br/>adversarial break report<br/>attack + source_status + broke + failing/unsure field"]
    ccheck["C routing check<br/>broke: yes / no / unsure"]

    arerun["Rerun solver from S0<br/>source: A"]
    aadj["Math-gap adjudication<br/>no majority or unresolved A"]
    brerun["Rerun solver from S0<br/>source: B"]
    crerun["Rerun solver from S0<br/>source: C"]
    cadj["Math-gap adjudication<br/>C unsure or A unresolved"]
    finalgate["Final Checker gate<br/>A/B/C cascade clear"]
    artifacts["Saved run record<br/>prompt-shaped raw outputs<br/>parsed JSON with B/C fields<br/>summary.json"]

    title --> input
    input --> ensemble
    ensemble --> composer
    composer --> acheck

    acheck -->|"disallowed premise<br/>or clear A guidance"| arerun
    acheck -->|"no majority"| aadj
    acheck -->|"A clear, or A issue<br/>without seed"| b

    b --> bcheck
    bcheck -->|"fillable: no<br/>or disallowed premise"| brerun
    bcheck -->|"no weakest point<br/>or fillable: yes"| c

    c --> ccheck
    ccheck -->|"broke: yes"| crerun
    ccheck -->|"broke: no + A clean"| finalgate
    ccheck -->|"broke: unsure<br/>or unresolved A"| cadj

    arerun --> artifacts
    aadj --> artifacts
    brerun --> artifacts
    crerun --> artifacts
    cadj --> artifacts
    finalgate --> artifacts

    classDef mono fill:#0B3B68,stroke:#071A33,stroke-width:3px,color:#F8FAFC;
    class title,input,ensemble,composer,acheck,b,bcheck,c,ccheck,arerun,aadj,brerun,crerun,cadj,finalgate,artifacts mono;

    linkStyle default stroke:#071A33,stroke-width:2.5px;
```



## How To Read This Map

This is a map-style diagram. The curved arrows show which boxes correspond to which outcomes.

`STOPPED_*` statuses in `summary.json` mean the current verifier cascade ended at that stage. They do not necessarily mean the whole experiment stopped forever.

The real next move is recorded in:

```text
protocol_next_step
rerun_starts_at
current_cascade_action
```

Examples:

```json
{
  "status": "STOPPED_AFTER_B",
  "protocol_action": "RERUN_SOLVER_WITH_GUIDANCE",
  "protocol_source": "B",
  "protocol_next_step": "FRESH_MULTI_SOLVER_RUN_FROM_S0",
  "rerun_starts_at": "S0_BLUEPRINT",
  "current_cascade_action": "END_CURRENT_VERIFIER_CASCADE"
}
```

This means B ended the current verifier cascade, but the real next protocol step is a fresh solver rerun from S0.

```json
{
  "status": "COMPLETED_C_CLEAN",
  "protocol_next_step": "FINAL_CHECKER_GATE",
  "current_cascade_action": "CASCADE_CLEAR"
}
```

This means A/B/C cleared and the next real protocol step is the Final Checker gate.