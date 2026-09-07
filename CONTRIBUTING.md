# Contributing

Contributions that improve correctness, reproducibility, documentation, or
offline test coverage are welcome. This is research software: changes should
preserve the distinction between a generated candidate, a verifier-cascade
result, a private-checker result, and a formally proved theorem.

## Before opening an issue

- Check the [command guide](Commands/README.md) and
  [documentation map](SOURCE_MAP.md).
- Search existing issues for the same failure or documentation gap.
- Remove API keys, private gold proofs, restricted paper text, personal paths,
  and privileged Final Checker details from anything you attach.

For a run failure, include the command, Python version, selected prompt packet,
solver internet mode, terminal `state.json` status, and the smallest relevant
error excerpt. Do not upload an entire ignored run directory by default.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[pipeline]'
```

Run the offline checks before submitting a change:

```bash
python3 -B prompt_sync.py --check
PYTHONPATH='Individual Pipeline' \
  python3 -B -m unittest discover -s tests -p 'test*.py'
```

These checks do not make paid API calls. Install `.[pipeline]` for the full
suite; otherwise the target-integrity test module is skipped. CI installs
these dependencies and should run without skips.

## Documentation and prompt changes

- Edit canonical role text only in `Prompt Packet/Prompts.md` or
  `Prompt Packet/PromptsWithFullInternet.md`.
- Regenerate component prompt views with `python3 prompt_sync.py --write`.
- Keep `Prompt Packet/FlowChart.md`, the component READMEs, and the runtime
  behavior aligned.
- Link to real repository artifacts; do not promise supplements or reports that
  are not present.
- Treat `Examples/cayley/` as an archived run: keep raw role outputs unchanged.
  Its offline tests check file hashes, recorded gates, and the private-file
  boundary. Improve the guide without silently rewriting the evidence.
- After changing result tables or `Results/paper_reproduction/subjects.json`,
  regenerate the figures and subject lists with
  `python3 -B docs/build_results_charts.py --write`; offline tests check for drift.
- Rebuild the paired subject comparison with
  `python3 -B docs/build_paired_results.py --write`. Match exact paper/target
  identifiers; add a renumbering alias only when supported by statement-level
  evidence. Keep unresolved labels out of paired totals, not in the failure count.

## Pull-request checklist

- [ ] The change has one clear purpose.
- [ ] Offline tests and prompt synchronization pass.
- [ ] New or moved public documentation links are covered by the link test.
- [ ] No credentials, private inputs, generated run directories, or local
      absolute paths are included.
- [ ] Mathematical and evaluation claims match the evidence actually present.
- [ ] Any user-visible workflow change is reflected in the relevant README and
      flow chart.

## Licensing

The project owners have not yet selected an open-source license. Until they do,
public visibility does not grant permission to reuse or redistribute the code.
Prospective contributors should contact the maintainers if licensing terms
affect their contribution.
