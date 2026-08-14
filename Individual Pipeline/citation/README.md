# Citation Gate

This package implements the Citation Generator, Citation Verifier, and their
deterministic gate. The solver runs it after S6 and before the Verifier A/B/C
cascade.

Runtime artifacts are written under:

```text
Outputs/<run-name>/solver/<problem>/round_NNN/citation_gate/
```

The package contains executable code, not the citation reports produced by a
run.

Generated, review-friendly copies of both role prompts live in `prompts/`.
Their source of truth is `Prompt Packet/`; regenerate them from the repository
root with `python prompt_sync.py --write`.
