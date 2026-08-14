"""Step 1: source fetch (§4). arXiv main route + OCR fallback.

Outputs: source/flat.tex (or flat.md), source/macros.tex, source/meta.json.
"""
from __future__ import annotations

import gzip
import io
import random
import re
import shutil
import subprocess
import tarfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

from .common import Rejected, RunContext
from .latex_utils import (collect_macros, expand_simple_macros, mark_expandable,
                          replace_figure_envs, strip_comments)
from .schemas import Meta
from .tar_compat import UnsafeArchiveError, extract_data

STEP = "step1"

# ---------------------------------------------------- §4.3 field_baseline table lookup

FIELD_MAP = {
    "math.AC": "commutative algebra", "math.AG": "algebraic geometry",
    "math.AP": "analysis of PDEs", "math.AT": "algebraic topology",
    "math.CA": "classical analysis", "math.CO": "combinatorics",
    "math.CT": "category theory", "math.CV": "complex analysis",
    "math.DG": "differential geometry", "math.DS": "dynamical systems",
    "math.FA": "functional analysis", "math.GM": "mathematics",
    "math.GN": "general topology", "math.GR": "group theory",
    "math.GT": "geometric topology", "math.HO": "mathematics",
    "math.IT": "information theory", "math.KT": "K-theory and homological algebra",
    "math.LO": "mathematical logic", "math.MG": "metric geometry",
    "math.MP": "mathematical physics", "math-ph": "mathematical physics",
    "math.NA": "numerical analysis", "math.NT": "number theory",
    "math.OA": "operator algebras", "math.OC": "optimization and control theory",
    "math.PR": "probability theory", "math.QA": "quantum algebra",
    "math.RA": "rings and algebras", "math.RT": "representation theory",
    "math.SG": "symplectic geometry", "math.SP": "spectral theory",
    "math.ST": "mathematical statistics", "stat.TH": "mathematical statistics",
    "cs.LG": "learning theory", "stat.ML": "learning theory",
    "cs.DM": "discrete mathematics", "cs.CC": "computational complexity",
    "cs.IT": "information theory", "cs.DS": "algorithms",
    "quant-ph": "quantum information theory",
}


def field_baseline_of(category: str, categories: list[str] | None = None) -> str:
    """Union of the primary+secondary category mappings, always suffixed with
    "the paper's own subject area" (§4.3).

    The suffix lets 4a/4c treat standard material from the paper's own field as
    known -- the category table cannot cover cross-disciplinary topics (such as
    an optimal-transport paper under math.OC). Pure table lookup, zero LLM.
    """
    seen, parts = set(), []
    for cat in [category] + list(categories or []):
        mapped = FIELD_MAP.get(cat)
        if mapped and mapped not in seen:
            seen.add(mapped)
            parts.append(mapped)
    if not parts:
        return "graduate-level knowledge of the paper's own subject area"
    return ("graduate-level " + ", ".join(parts)
            + ", and the paper's own subject area")


# ------------------------------------------------------------------ network layer

def _http_get(url: str, retries: int = 3, timeout: int = 60) -> bytes:
    last = None
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=timeout,
                             headers={"User-Agent": "paper-cleaner/2.3"})
            if r.status_code == 200:
                return r.content
            last = f"HTTP {r.status_code}"
        except requests.RequestException as e:
            last = repr(e)
        time.sleep(2 * (attempt + 1))
    raise Rejected("download_error", f"{url}: {last}")


ATOM = "{http://www.w3.org/2005/Atom}"


def fetch_arxiv_meta(ctx: RunContext, arxiv_id: str) -> Meta:
    xml_bytes = _http_get(f"https://export.arxiv.org/api/query?id_list={arxiv_id}")
    root = ET.fromstring(xml_bytes)
    entry = root.find(f"{ATOM}entry")
    title, published, category = "", "", ""
    categories: list[str] = []
    if entry is not None:
        title = re.sub(r"\s+", " ", (entry.findtext(f"{ATOM}title") or "")).strip()
        published = (entry.findtext(f"{ATOM}published") or "")[:10]
        cat_el = entry.find("{http://arxiv.org/schemas/atom}primary_category")
        if cat_el is not None:
            category = cat_el.get("term", "")
        categories = [c.get("term", "") for c in entry.findall(f"{ATOM}category")]
    return Meta(paper_id=ctx.paper_id, title=title, paper_date=published,
                primary_category=category, categories=categories,
                field_baseline=field_baseline_of(category, categories),
                source_type="latex")


# ---------------------------------------------------------------- source unpacking

def _sniff_and_unpack(ctx: RunContext, blob: bytes) -> str:
    """Expand the e-print content into source/raw/; return 'tex' | 'pdf'."""
    raw_dir = ctx.path("source/raw")
    if blob[:4] == b"%PDF":
        (raw_dir / "paper.pdf").write_bytes(blob)
        return "pdf"
    if blob[:2] == b"\x1f\x8b":
        blob = gzip.decompress(blob)
        if blob[:4] == b"%PDF":
            (raw_dir / "paper.pdf").write_bytes(blob)
            return "pdf"
    try:
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:*") as tf:
            extract_data(tf, raw_dir)
        return "tex"
    except UnsafeArchiveError as exc:
        raise Rejected("unsafe_archive", str(exc)) from exc
    except (tarfile.TarError, ValueError):
        pass
    (raw_dir / "main.tex").write_bytes(blob)      # neither PDF nor tar: a bare single .tex
    return "tex"


def _find_main_tex(raw_dir: Path) -> Path | None:
    """§4.1 item 3: the main file must contain \\documentclass; if several
    candidates, prefer those with \\begin{document} and take the largest."""
    cands = []
    for p in raw_dir.rglob("*.tex"):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "\\documentclass" in text:
            cands.append((p, "\\begin{document}" in text, p.stat().st_size))
    if not cands:
        return None
    with_doc = [c for c in cands if c[1]]
    pool = with_doc or cands
    return max(pool, key=lambda c: c[2])[0]


# ------------------------------------------------------------------- flatten

INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]*)\}")


LATEXPAND_MISS_RE = re.compile(r"(?i)not found|cannot open|no such file")


def _flatten_own(path: Path, base: Path, depth: int = 0,
                 missing: list[str] | None = None) -> str:
    if depth > 10:
        raise Rejected("input_recursion", str(path))
    text = path.read_text(encoding="utf-8", errors="replace")

    def repl(mo: re.Match) -> str:
        name = mo.group(1).strip()
        cand = base / name
        if not cand.suffix:
            cand = cand.with_suffix(".tex")
        if not cand.exists():
            if missing is not None:              # dropped directive: the caller logs it —
                missing.append(name)             # a lost appendix file otherwise only shows
            return ""                            # up as "theorems without proofs" downstream
        return _flatten_own(cand, base, depth + 1, missing)

    return INPUT_RE.sub(repl, text)


def flatten(main_tex: Path, raw_dir: Path,
            missing: list[str] | None = None) -> str:
    if shutil.which("latexpand"):
        try:
            r = subprocess.run(
                ["latexpand", "--keep-comments", main_tex.name],
                cwd=main_tex.parent, capture_output=True, text=True, timeout=120)
            if r.returncode == 0 and r.stdout.strip():
                if missing is not None and r.stderr:
                    missing.extend(ln.strip()[:200]
                                   for ln in r.stderr.splitlines()
                                   if LATEXPAND_MISS_RE.search(ln))
                return r.stdout
        except (subprocess.SubprocessError, OSError):
            pass
    return _flatten_own(main_tex, main_tex.parent, missing=missing)


def _inline_bbl(tex: str, raw_dir: Path, main_stem: str) -> str:
    """Inline the .bbl at \\bibliography{...} (citation parsing needs \\bibitem)."""
    if "\\bibitem" in tex:
        return tex
    bbls = list(raw_dir.rglob("*.bbl"))
    preferred = [b for b in bbls if b.stem == main_stem]
    bbl = (preferred or bbls or [None])[0]
    if bbl is None:
        return tex
    content = bbl.read_text(encoding="utf-8", errors="replace")
    if "\\bibliography" in tex:
        return re.sub(r"\\bibliography\{[^}]*\}", lambda _: content, tex, count=1)
    return tex.replace("\\end{document}", content + "\n\\end{document}", 1)


# ---------------------------------------------------------------- OCR route

def _run_ocr(ctx: RunContext, pdf: Path) -> str:
    """Nougat / MinerU wrapper (§4.2); tool missing -> rejected."""
    if not ctx.cfg.ocr.enabled:
        raise Rejected("ocr_disabled", str(pdf))
    engine = ctx.cfg.ocr.engine
    out_dir = ctx.path("source/raw/ocr_out")
    out_dir.mkdir(parents=True, exist_ok=True)
    if engine == "nougat" and shutil.which("nougat"):
        ctx.progress(f"OCR (nougat) on {pdf.name} — may take many minutes")
        subprocess.run(["nougat", str(pdf), "-o", str(out_dir)],
                       capture_output=True, timeout=3600)
        mmds = list(out_dir.glob("*.mmd")) + list(out_dir.glob("*.md"))
        if mmds:
            return mmds[0].read_text(encoding="utf-8", errors="replace")
    if engine == "mineru" and shutil.which("magic-pdf"):
        subprocess.run(["magic-pdf", "-p", str(pdf), "-o", str(out_dir)],
                       capture_output=True, timeout=3600)
        mds = list(out_dir.rglob("*.md"))
        if mds:
            return mds[0].read_text(encoding="utf-8", errors="replace")
    raise Rejected("ocr_unavailable",
                   f"engine={engine} not installed or produced no output")


def _ocr_quality_gate(ctx: RunContext, md: str) -> None:
    """G2: sample formulas and parse their syntax (§4.2 item 2)."""
    from pylatexenc.latexwalker import LatexWalker
    formulas = re.findall(r"\$\$(.+?)\$\$", md, re.DOTALL) + \
        re.findall(r"(?<!\$)\$([^$]+)\$(?!\$)", md, re.DOTALL)
    formulas = [f for f in formulas if f.strip()]
    if not formulas:
        raise Rejected("ocr_quality", "no formulas found in OCR output")
    sample = random.Random(0).sample(formulas, min(50, len(formulas)))
    bad = 0
    for f in sample:
        try:
            LatexWalker(f, tolerant_parsing=False).get_latex_nodes()
        except Exception:
            bad += 1
    rate = bad / len(sample)
    ctx.log_event(event="ocr_quality", sampled=len(sample), unparseable=bad)
    if rate > ctx.cfg.ocr.max_unparseable_rate:
        raise Rejected("ocr_quality", f"unparseable rate {rate:.2f}")


def _ocr_route(ctx: RunContext, pdf: Path, meta: Meta) -> None:
    md = _run_ocr(ctx, pdf)
    _ocr_quality_gate(ctx, md)
    md, _ = replace_figure_envs(md)
    ctx.path("source/flat.md").write_text(md, encoding="utf-8")
    ctx.path("source/macros.tex").write_text("", encoding="utf-8")
    meta.source_type = "ocr"
    if not meta.field_baseline:
        meta.field_baseline = field_baseline_of("")
    ctx.write_json("source/meta.json", meta)


# ------------------------------------------------------------------- main entry

def ingest_local_tex(ctx: RunContext, tex_path: str,
                     primary_category: str = "") -> None:
    """Direct local .tex ingest (tests/offline): runs the same §4.1 items 4-8
    processing as the arXiv route."""
    ctx.step_name = STEP
    raw_dir = ctx.path("source/raw")
    main_tex = raw_dir / Path(tex_path).name
    shutil.copyfile(tex_path, main_tex)
    meta = Meta(paper_id=ctx.paper_id, title=Path(tex_path).stem,
                primary_category=primary_category,
                field_baseline=field_baseline_of(primary_category),
                source_type="latex")
    _process_tex(ctx, main_tex, raw_dir, meta)


def _process_tex(ctx: RunContext, main_tex: Path, raw_dir: Path,
                 meta: Meta) -> None:
    missing_inputs: list[str] = []
    tex = flatten(main_tex, raw_dir, missing_inputs)        # §4.1 item 4
    for name in missing_inputs:
        ctx.log_event(event="flatten_missing_input", name=name,
                      level="warning")
    tex = _inline_bbl(tex, raw_dir, main_tex.stem)
    tex = strip_comments(tex)                               # item 5

    body_start = tex.find("\\begin{document}")
    preamble = tex[:body_start] if body_start > 0 else ""
    body = tex[body_start:] if body_start > 0 else tex

    macros = collect_macros(preamble)                       # item 6
    mark_expandable(macros)
    ctx.path("source/macros.tex").write_text(               # 6a: write all verbatim
        "\n".join(m.raw for m in macros) + ("\n" if macros else ""),
        encoding="utf-8")
    body = expand_simple_macros(body, macros)               # 6b

    body, n_fig = replace_figure_envs(body)                 # item 7
    ctx.log_event(event="figures_replaced", count=n_fig)

    ctx.path("source/flat.tex").write_text(preamble + body, encoding="utf-8")
    ctx.write_json("source/meta.json", meta)
    ctx.log_event(event="step1_done", source_type=meta.source_type,
                  chars=len(preamble) + len(body), macros=len(macros),
                  missing_inputs=len(missing_inputs))


def run(ctx: RunContext, arxiv_id: str | None = None,
        pdf_path: str | None = None) -> None:
    ctx.step_name = STEP
    raw_dir = ctx.path("source/raw")

    if pdf_path:                                            # local PDF route
        dst = raw_dir / "paper.pdf"
        shutil.copyfile(pdf_path, dst)
        meta = Meta(paper_id=ctx.paper_id, title=Path(pdf_path).stem,
                    field_baseline=field_baseline_of(""), source_type="ocr")
        _ocr_route(ctx, dst, meta)
        return

    assert arxiv_id
    meta = fetch_arxiv_meta(ctx, arxiv_id)
    blob = _http_get(f"https://arxiv.org/e-print/{arxiv_id}")
    kind = _sniff_and_unpack(ctx, blob)

    if kind == "pdf":                                       # author uploaded only a PDF
        _ocr_route(ctx, raw_dir / "paper.pdf", meta)
        return

    main_tex = _find_main_tex(raw_dir)
    if main_tex is None:                                    # no main tex -> OCR
        pdfs = list(raw_dir.rglob("*.pdf"))
        if not pdfs:
            pdf_blob = _http_get(f"https://arxiv.org/pdf/{arxiv_id}")
            (raw_dir / "paper.pdf").write_bytes(pdf_blob)
            pdfs = [raw_dir / "paper.pdf"]
        _ocr_route(ctx, pdfs[0], meta)
        return

    _process_tex(ctx, main_tex, raw_dir, meta)
