"""LLM clients and deterministic mocks for the citation gate."""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request

from .models import LLMResponse, PromptPacket


class MockLLMClient:
    """Deterministic offline client for smoke tests and audits."""

    def __init__(self, model: str = "mock-citation-model") -> None:
        self.model = model
        self.calls: list[dict] = []

    def complete(self, prompt: PromptPacket, metadata: dict) -> LLMResponse:
        self.calls.append({"role": prompt.role, **metadata})
        return LLMResponse(mock_citation_response(prompt.role, metadata), self.model)


def mock_citation_response(role: str, metadata: dict) -> str:
    """Return one deterministic citation-role response for offline pipelines."""

    if role == "citation_generator":
        return _mock_citation_generator(metadata)
    if role == "citation_verifier":
        return _mock_citation_verifier(metadata)
    if role == "citation_reformat":
        return _mock_citation_reformat(metadata)
    return ""


class OpenAICompatibleClient:
    """Tiny stdlib OpenAI-compatible client for standalone live runs."""

    def __init__(
        self,
        *,
        model: str,
        base_url: str,
        api_key: str | None,
        temperature: float = 0.0,
        timeout_seconds: int = 120,
        max_tokens: int | None = None,
        web_search: bool = False,
        require_web_search: bool = False,
        web_search_context_size: str | None = None,
    ) -> None:
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.temperature = temperature
        self.timeout_seconds = timeout_seconds
        self.max_tokens = max_tokens
        self.web_search = web_search
        self.require_web_search = require_web_search
        self.web_search_context_size = web_search_context_size

    def complete(self, prompt: PromptPacket, metadata: dict) -> LLMResponse:
        if not self.api_key:
            raise RuntimeError("API key is required for --client openai")
        if self.web_search:
            return self._complete_responses(prompt)
        return self._complete_chat_completions(prompt)

    def _complete_chat_completions(self, prompt: PromptPacket) -> LLMResponse:
        payload: dict = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
        }
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        request = urllib.request.Request(
            url=f"{self.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds, context=ssl.create_default_context()) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            exc.read()
            raise RuntimeError(f"OpenAI-compatible API error {exc.code}: response body omitted") from exc
        text = data["choices"][0]["message"]["content"]
        return LLMResponse(text=text, model=str(data.get("model", self.model)))

    def _complete_responses(self, prompt: PromptPacket) -> LLMResponse:
        tool: dict = {"type": "web_search"}
        if self.web_search_context_size is not None:
            tool["search_context_size"] = self.web_search_context_size
        payload: dict = {
            "model": self.model,
            "input": [
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
            "tools": [tool],
        }
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        if self.max_tokens is not None:
            payload["max_output_tokens"] = self.max_tokens
        if self.require_web_search:
            payload["tool_choice"] = "required"
        request = urllib.request.Request(
            url=f"{self.base_url.rstrip('/')}/responses",
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds, context=ssl.create_default_context()) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            exc.read()
            raise RuntimeError(f"OpenAI Responses API error {exc.code}: response body omitted") from exc
        return LLMResponse(text=_extract_responses_text(data), model=str(data.get("model", self.model)))


def _extract_responses_text(data: dict) -> str:
    output_text = data.get("output_text")
    if isinstance(output_text, str):
        return output_text
    chunks: list[str] = []
    for item in data.get("output", []):
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if not isinstance(content, dict):
                continue
            text = content.get("text")
            if isinstance(text, str):
                chunks.append(text)
    if chunks:
        return "\n".join(chunks)
    raise RuntimeError("OpenAI Responses API response did not contain output text")


def _mock_citation_generator(metadata: dict) -> str:
    scenario = str(metadata.get("citation_scenario", "all_supported"))
    if scenario == "malformed_summary_routes_unclear":
        return "This response intentionally omits the controller summary."
    if scenario == "target_source_leakage":
        next_step, leakage, complete, unsupported, suspicious = (
            "MANUAL_REVIEW_FOR_LEAKAGE",
            "YES",
            "NO",
            "UNCLEAR",
            "UNCLEAR",
        )
    elif scenario == "source_ledger_repair_needed":
        next_step, leakage, complete, unsupported, suspicious = (
            "SOURCE_LEDGER_REPAIR_NEEDED",
            "NO",
            "NO",
            "YES",
            "NO",
        )
    else:
        next_step, leakage, complete, unsupported, suspicious = (
            "PROCEED_TO_CITATION_VERIFIER",
            "NO",
            "YES",
            "NO",
            "NO",
        )
    return f"""# Source Ledger

claim_id: C1
proof_location: Mock proof sentence 1
claim_or_fact_used: The proof uses only allowed public-prefix facts.
candidate_source_status: allowed supporting statement
candidate_source_label_or_name: mock public prefix
exact_statement_needed: Toy statement already present in the public packet.
hypotheses_or_conditions_needed: None beyond the target setup.
where_hypotheses_are_checked: Public packet.
strength_used_by_proof: Exact statement.
source_evidence: The mock source is supplied by the toy benchmark packet.
internet_used: NO
url_or_reference_checked: None

Citation Generator summary:
Source Ledger complete: {complete}
Internet used: NO
Possible target-source leakage encountered: {leakage}
Unsupported or unclear sources present: {unsupported}
Suspicious standard-background claims present: {suspicious}
External sources checked: None
Recommended next step: {next_step}
"""


def _mock_citation_verifier(metadata: dict) -> str:
    scenario = str(metadata.get("citation_scenario", "all_supported"))
    if scenario == "malformed_summary_routes_unclear":
        return "This malformed verifier output has no summary fields."
    if scenario == "blocking_source_issue":
        gate, missing, external, repair, substantive = "BLOCKING_SOURCE_ISSUE", "YES", "YES", "NO", "YES"
        guidance = "Add a valid source or proof for the mock load-bearing claim."
    elif scenario == "source_ledger_repair_needed":
        gate, missing, external, repair, substantive, guidance = (
            "SOURCE_LEDGER_REPAIR_NEEDED",
            "YES",
            "NO",
            "YES",
            "NO",
            "None",
        )
    elif scenario == "target_source_leakage":
        gate, missing, external, repair, substantive, guidance = (
            "LEAKAGE_RISK",
            "UNCLEAR",
            "YES",
            "NO",
            "UNCLEAR",
            "None",
        )
    else:
        gate, missing, external, repair, substantive, guidance = "GOOD_TO_GO", "NO", "NO", "NO", "NO", "None"
    return f"""# Citation Verifier Report

Controller-facing summary
Citation gate result: {gate}
Source Ledger present: YES
Missing source entries present: {missing}
Disallowed sources present: NO
Overstrengthened or misquoted sources present: NO
Suspicious standard-background claims present: NO
External source issue present: {external}
Citation-only repair needed: {repair}
Substantive source issue present: {substantive}
Candidate guidance seed, if any: {guidance}
"""


def _mock_citation_reformat(metadata: dict) -> str:
    if str(metadata.get("citation_scenario", "all_supported")) == "malformed_summary_routes_unclear":
        return "Still malformed."
    if metadata.get("reformat_for") == "citation_verifier":
        return _mock_citation_verifier({**metadata, "citation_scenario": "all_supported"})
    return _mock_citation_generator({**metadata, "citation_scenario": "all_supported"})
