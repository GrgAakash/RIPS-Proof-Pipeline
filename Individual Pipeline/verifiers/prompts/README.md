# Verifier prompt views

This directory contains generated views for the Problem Statement Verifier,
Verifier A, Verifier B, Verifier C, Composer A, and Final Checker. The canonical
source remains
[`Prompt Packet/Prompts.md`](../../../Prompt%20Packet/Prompts.md).

The standalone verifier API runner loads the A/B/C and Composer A views in this
directory at runtime. The integrated S0-S6 runner instead extracts all roles,
including the Problem Statement Verifier, from its selected canonical packet.

Do not edit these files directly. From the repository root, use:

```bash
python prompt_sync.py --write
python prompt_sync.py --check
```
