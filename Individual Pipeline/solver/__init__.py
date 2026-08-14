"""Autonomous S0-S6 mathematical solver workflow.

This subpackage implements both canonical solver modes:

* ``Prompt Packet/Prompts.md`` runs S0-S6 without hosted web search.
* ``Prompt Packet/PromptsWithFullInternet.md`` gives source-supported web
  search to the solver roles selected by the protocol.

Both modes use the same autonomous pipeline:

* LLM roles (S0 blueprint, S1-S5 subproblem solvers, S6 composer, Verifier
  A1/A2/A3 + Composer A, Verifier B, Verifier C, Final Checker) do the
  mathematical judgment.
* Deterministic Python (the Decision Controller in ``controller.py``) does all
  routing: appending at most one guidance item per failed round, opening branch
  pipelines on candidate lemmas, walking the verifier cascade, and stopping on
  the 10-guidance budget.

This package is the solver workflow for hard and open mathematical problems.
"""
