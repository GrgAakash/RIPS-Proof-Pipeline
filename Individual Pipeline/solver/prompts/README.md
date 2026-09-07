# Solver prompt views

These files are generated review views of the canonical packets under
[`Prompt Packet/`](../../../Prompt%20Packet/README.md). Do not edit them
directly.

- `no_internet/`: S0, S1-S5, and S6 prompts for closed-book solver roles.
- `full_internet/`: S0, S1-S5, and S6 prompts with hosted-search instructions.
- `source_gate/`: restricted-web Skeleton Source Generator and Verifier prompts.

After editing a canonical packet, run the following from the repository root:

```bash
python prompt_sync.py --write
python prompt_sync.py --check
```
