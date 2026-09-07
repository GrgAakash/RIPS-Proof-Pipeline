# Local inputs

This directory is the private working surface for paper preparation, solver
packets, and standalone verifier inputs. Generated content is ignored by Git;
only contracts and placeholder files belong in the repository.

| Directory | Purpose | Detailed contract |
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

> [!CAUTION]
> Inputs may contain third-party paper text, reference proofs, and private
> source material. Never commit API keys or generated input directories, and
> review redistribution rights before sharing any extracted paper content.

Use the repository-level [`Commands/`](../Commands/README.md) wrappers to
populate these directories safely.
