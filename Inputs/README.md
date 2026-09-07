# Local inputs

Keep prepared papers, solver packets, and verifier inputs here. Git ignores
generated files; only the guides and placeholders are tracked.

| Directory | Purpose | Guide |
|---|---|---|
| `paper_cleaner_input/` | Prepared paper source and Steps 1-5 evidence | [`paper_cleaner_input/README.md`](paper_cleaner_input/README.md) |
| `solver_input/` | Audited or hand-authored theorem packets | [`solver_input/README.md`](solver_input/README.md) |
| `verifier_input/` | Optional files for standalone verifier commands | [`verifier_input/README.md`](verifier_input/README.md) |

Typical integrated layout:

```text
paper_cleaner_input/<paper-id>/
solver_input/<run-name>/solver_input/
verifier_input/
```

These folders may contain paper text and private reference proofs. Keep API
keys out of them, and check what you have permission to share before publishing
any extracted text.

The [command guide](../Commands/README.md) shows how to prepare these inputs.
