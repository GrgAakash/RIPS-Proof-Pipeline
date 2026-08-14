# Solver Prompt Views

These files are generated from the canonical packets in `Prompt Packet/`.
Do not edit them directly.

- `no_internet/`: S0, S1-S5, and S6 prompts for closed-book solver roles.
- `full_internet/`: S0, S1-S5, and S6 prompts with hosted-search instructions.
- `source_gate/`: restricted-web Skeleton Source Generator and Verifier prompts.

After editing a canonical packet, regenerate and verify all component views:

```bash
python prompt_sync.py --write
python prompt_sync.py --check
```
