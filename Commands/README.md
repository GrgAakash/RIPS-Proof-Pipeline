# Commands

The scripts resolve the repository root from their own location, so they can
be called from any working directory.

- `prepare_paper_input.sh`: prepare one arXiv paper through upstream Step 5.
- `run_no_internet.sh`: run the integrated pipeline with closed-book S0-S6.
- `run_full_internet.sh`: run the integrated pipeline with hosted search for
  S0-S6.
- `run_mini_from_arxiv.sh`: run only the optional Mini cleaner and audit.

Required environment values:

- Preparation and Mini: `OPENAI_API_KEY`, `ARXIV`.
- Integrated runs: `OPENAI_API_KEY`, `PAPER_ID`, `TARGET_ID`.

Common optional values are `MODEL`, `RUN_NAME`, `RUN_TAG`, `SOLVER_WORKERS`,
`SOLVER_DELAY_SECONDS`, `MAX_ROUNDS`, `MAX_BRANCH_DEPTH`, `MAX_BRANCHES`,
`CITATION_MODEL`, `CITATION_MAX_ATTEMPTS`, and
`CITATION_WEB_SEARCH_CONTEXT_SIZE`. `INCLUDE_PRIVATE_FINAL_CHECKER` defaults to
`1`; set it to `0` to omit the private gold proof and full source from the
prepared solver bundle. When it is enabled, the command checks that the
selected target has an extractable proof before starting the paid Mini cleaner
stages.

Example:

```bash
PAPER_ID=2606.16585 \
TARGET_ID=stmt-a83f71c209d4 \
MAX_ROUNDS=3 \
  ./Commands/run_no_internet.sh
```

These are API-backed commands. The offline test suite does not require an API
key and should be used for ordinary regression checks.
