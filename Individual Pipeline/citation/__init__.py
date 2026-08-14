"""Citation Generator and Citation Verifier runtime.

The package is used both by the standalone ``verifier`` command and by the
integrated S0-S6 solver pipeline.
"""

from .gate import run_citation_gate
from .models import CitationGateDecision, CitationGeneratorReport, CitationVerifierReport
from .prompts import CitationPromptTemplates

__all__ = [
    "CitationGateDecision",
    "CitationGeneratorReport",
    "CitationPromptTemplates",
    "CitationVerifierReport",
    "run_citation_gate",
]
