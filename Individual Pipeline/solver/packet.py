"""Prompt payload shared by the standalone solver and its LLM client."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptPacket:
    """Complete system and user messages for one solver role call."""

    role: str
    system: str
    user: str
