"""Config loading, run context, exceptions, and structured logging.

An internal helper module outside the plan's repo layout, shared by llm.py
and every step module to avoid circular imports.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# Live progress ticker (stderr). Structured logging always goes to
# logs/run.jsonl; this is the human-visible mirror of the interesting
# events, because a 30-minute silent run is undebuggable from the terminal.
# Disable with PAPER_CLEANER_PROGRESS=0.
PROGRESS_ON = os.environ.get("PAPER_CLEANER_PROGRESS", "1") != "0"

import yaml
from pydantic import BaseModel, Field, ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
PIPELINE_VERSION = "2.3"


# ------------------------------------------------------------------- Exceptions

class Rejected(Exception):
    """Rule-based rejection: the system deliberately abandons the whole paper per the rules."""

    def __init__(self, reason: str, detail: str = ""):
        super().__init__(f"{reason}: {detail}" if detail else reason)
        self.reason = reason
        self.detail = detail


class TaskFailed(Exception):
    """A single LLM task still fails after exhausting retries."""

    def __init__(self, task: str, detail: str = ""):
        super().__init__(f"llm task {task} failed: {detail}")
        self.task = task
        self.detail = detail


# ------------------------------------------------------------------- Config

class ModelsCfg(BaseModel):
    a0: str
    a1: str
    a2: str
    a3_ext: str
    a3_cmp: str = ""   # empty -> a4b-tier model (§9.3: comparison runs on the a4b tier)
    a4a: str
    a4b: str
    a4c: str
    a5: str = ""       # selection-rationale writer (human-read doc); empty -> a4b tier
    a6: str = ""       # package repairer (audit-tier model); empty -> a4a tier
    a7: str = ""       # appeal judge for would-be exclusions; empty -> a6 tier

    def for_task(self, task: str) -> str:
        if task == "a3_cmp" and not self.a3_cmp:
            return self.a4b
        if task == "a5" and not self.a5:
            return self.a4b
        if task == "a6" and not self.a6:
            return self.a4a
        if task == "a7" and not self.a7:
            return self.for_task("a6")
        return getattr(self, task)


class StandardCfg(BaseModel):
    temperature: float = 0


class ReasoningCfg(BaseModel):
    reasoning_effort: str = "medium"


class LlmCfg(BaseModel):
    standard: StandardCfg = Field(default_factory=StandardCfg)
    reasoning: ReasoningCfg = Field(default_factory=ReasoningCfg)
    max_output_tokens: dict[str, int] = Field(default_factory=dict)
    structured_outputs: bool = True
    validation_retries: int = 2
    network_retries: int = 5
    parallel: int = 8
    cache: bool = True


class PipelineCfg(BaseModel):
    granularity: str = "main-only"          # main-only | per-node
    policies: list[str] = Field(default_factory=lambda: ["dep-closure"])
    max_main_theorems: int = 5
    min_main_theorems: int = 3
    hardest_theorems: int = 2               # hardest picks beyond the mains (may overlap)
    max_verify_iters: int = 3
    min_proof_chars: int = 300
    package_char_cap: int = 300000
    repair_agent: bool = False              # A6: audit-tier repairer for would-be-excluded packages
    final_gate: bool = False                # audit-tier a4a re-check before a package ships (once per package)
    appeal: bool = False                    # A7: audit-tier appeal review before an exclusion is written (once per package)


class LimitsCfg(BaseModel):
    index_char_cap: int = 240000
    stmt_trunc_chars: int = 600
    section_chunk_chars: int = 120000


class OcrCfg(BaseModel):
    enabled: bool = True
    engine: str = "nougat"
    max_unparseable_rate: float = 0.10


class Config(BaseModel):
    provider: str = "openai"                # openai | azure
    models: ModelsCfg
    llm: LlmCfg = Field(default_factory=LlmCfg)
    pipeline: PipelineCfg = Field(default_factory=PipelineCfg)
    limits: LimitsCfg = Field(default_factory=LimitsCfg)
    ocr: OcrCfg = Field(default_factory=OcrCfg)


class ConfigError(Exception):
    pass


def load_config(path: str | Path) -> Config:
    try:
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        cfg = Config.model_validate(raw)
    except (OSError, yaml.YAMLError, ValidationError) as e:
        raise ConfigError(str(e)) from e
    if cfg.pipeline.min_main_theorems > cfg.pipeline.max_main_theorems:
        raise ConfigError(
            f"pipeline.min_main_theorems ({cfg.pipeline.min_main_theorems}) "
            f"> max_main_theorems ({cfg.pipeline.max_main_theorems})")
    return cfg


# ------------------------------------------------------------------- Utilities

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atomic_write_text(p: Path, text: str) -> None:
    """tmp + rename, so a crash mid-write never leaves a truncated JSON that
    kills the next checkpoint-resume."""
    tmp = p.with_name(f"{p.name}.{os.getpid()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)


# --------------------------------------------------------------- Run context

class RunContext:
    """Run context for a single paper: directories, config, logging."""

    def __init__(self, paper_id: str, cfg: Config, runs_dir: str | Path = "runs"):
        self.paper_id = paper_id
        self.cfg = cfg
        self.run_dir = Path(runs_dir) / paper_id
        self.prompts_dir = REPO_ROOT / "prompts"
        self.data_dir = REPO_ROOT / "data"
        for sub in ("source/raw", "index", "graph", "roles", "packages",
                    "cache", "logs"):
            (self.run_dir / sub).mkdir(parents=True, exist_ok=True)
        self.step_name = ""   # name of the current step, used for logging

    # ---- Paths and JSON IO
    def path(self, rel: str) -> Path:
        return self.run_dir / rel

    def read_json(self, rel: str) -> Any:
        return json.loads(self.path(rel).read_text(encoding="utf-8"))

    def write_json(self, rel: str, obj: Any) -> None:
        p = self.path(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(obj, BaseModel):
            text = obj.model_dump_json(indent=2, by_alias=True)
        else:
            text = json.dumps(obj, indent=2, ensure_ascii=False, default=_dump)
        atomic_write_text(p, text)

    def read_model(self, rel: str, model_cls):
        return model_cls.model_validate_json(self.path(rel).read_text(encoding="utf-8"))

    def prompt_text(self, task: str) -> str:
        return (self.prompts_dir / f"{task}.txt").read_text(encoding="utf-8")

    # ---- Live progress line (stderr, flushed; no artifact is touched)
    def progress(self, msg: str) -> None:
        if PROGRESS_ON:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[{ts}] {self.paper_id} {self.step_name or '-':<5} | {msg}",
                  file=sys.stderr, flush=True)

    # ---- Structured logging: logs/run.jsonl, one event per line
    def log_event(self, **kw) -> None:
        kw.setdefault("ts", now_iso())
        kw.setdefault("paper", self.paper_id)
        kw.setdefault("step", self.step_name)
        with open(self.path("logs/run.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(kw, ensure_ascii=False, default=str) + "\n")

    # ---- Append to excluded.json
    def add_excluded(self, target_id: str, policy: str, reason_code: str,
                     detail: str = "") -> None:
        p = self.path("excluded.json")
        items = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
        items.append({"target_id": target_id, "policy": policy,
                      "reason_code": reason_code, "detail": detail})
        atomic_write_text(p, json.dumps(items, indent=2, ensure_ascii=False))
        self.log_event(event="excluded", target=target_id, policy=policy,
                       reason=reason_code, detail=detail[:500])
        self.progress(f"✗ excluded {target_id} [{reason_code}] {detail[:70]}")


def _dump(o):
    if isinstance(o, BaseModel):
        return o.model_dump(by_alias=True)
    raise TypeError(f"not JSON serializable: {type(o)}")


# ---------------------------------------------------------------- State machine §1.1

class Status:
    """status.json wrapper: per-step done/skip bookkeeping + final state (§1.1)."""

    def __init__(self, ctx: RunContext):
        self.ctx = ctx
        p = ctx.path("status.json")
        if p.exists():
            self.data = json.loads(p.read_text(encoding="utf-8"))
        else:
            self.data = {"paper_id": ctx.paper_id, "steps": {},
                         "final_state": None, "reject_reason": None}

    def save(self) -> None:
        self.ctx.write_json("status.json", self.data)

    def done(self, step: str, input_hash: str) -> bool:
        rec = self.data["steps"].get(step)
        return bool(rec and rec.get("state") == "done"
                    and rec.get("input_hash") == input_hash)

    def mark_done(self, step: str, input_hash: str, **extra) -> None:
        self.data["steps"][step] = {"state": "done", "input_hash": input_hash,
                                    "finished_at": now_iso(), **extra}
        self.save()

    def finalize(self, state: str, reason: Optional[str] = None) -> None:
        self.data["final_state"] = state
        self.data["reject_reason"] = reason
        self.save()


def step_input_hash(ctx: RunContext, input_files: list[str],
                    config_keys: list[str], prompt_tasks: list[str]) -> str:
    """input_hash = sha256(input file contents + relevant config fields + prompt template contents)."""
    h = hashlib.sha256()
    for rel in input_files:
        p = ctx.path(rel)
        h.update(rel.encode())
        if p.exists():
            h.update(p.read_bytes())
    cfg_dump = ctx.cfg.model_dump()
    for key in config_keys:
        cur: Any = cfg_dump
        for part in key.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
            if cur is None:
                break
        h.update(f"{key}={canonical_json(cur)}".encode())
    for task in prompt_tasks:
        p = ctx.prompts_dir / f"{task}.txt"
        if p.exists():
            h.update(p.read_bytes())
    return "sha256:" + h.hexdigest()


class StepTimer:
    def __init__(self):
        self.t0 = time.monotonic()

    def ms(self) -> int:
        return int((time.monotonic() - self.t0) * 1000)
