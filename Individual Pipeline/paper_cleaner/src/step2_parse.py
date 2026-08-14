"""Step 2: structural parsing (§5, purely procedural, no LLM).

Input: source/flat.tex (OCR route: flat.md, parsed with the Markdown regex set).
Output: index/statements.v1.json, index/label_map.json, index/orphan_proofs.json.
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

from .common import RunContext, sha256_text
from .gates import g1_min_statements
from .latex_utils import (LABEL_RE, mask_definition_bodies, scan_cites,
                          scan_refs, section_of, section_positions,
                          strip_comments)
from .schemas import Citation, Meta, Statement, StatementsIndex
from .target_integrity import source_statement_id

STEP = "step2"

# §5.1 environment-name allowlist (alias -> canonical env_type)
ENV_ALIASES = {
    "theorem": "theorem", "thm": "theorem", "mainthm": "theorem",
    "claim": "theorem", "fact": "theorem", "result": "theorem",
    "observation": "theorem",
    "lemma": "lemma", "lem": "lemma",
    "proposition": "proposition", "prop": "proposition",
    "corollary": "corollary", "cor": "corollary",
    "definition": "definition", "defn": "definition", "dfn": "definition",
    "assumption": "assumption", "hypothesis": "assumption",
    "remark": "remark", "rem": "remark",
    "example": "example",
    "equation": "equation", "align": "equation", "multline": "equation",
    "gather": "equation",
}
EQUATION_ENVS = {"equation", "align", "multline", "gather"}
THEOREM_LIKE = {"theorem", "lemma", "proposition", "corollary"}
TAG_RE = re.compile(r"\\tag\*?\{([^}]*)\}")


# Papers frequently give theorem environments project-specific names, e.g.
# ``\newtheorem{thmO}{Theorem}`` and then use ``\begin{thmO}``.  A fixed
# allowlist silently loses those statements.  Discover the standard amsthm
# declaration forms before walking the document and map their printed titles
# (or, secondarily, their environment-name prefixes) to our canonical types.
NEW_THEOREM_RE = re.compile(
    r"\\newtheorem\s*\*?\s*"
    r"\{(?P<env>[A-Za-z@][A-Za-z0-9@:_*.-]*)\}\s*"
    r"(?:\[[^\]]*\]\s*)?"
    r"\{(?P<title>[^{}]*)\}"
    r"(?:\s*\[[^\]]*\])?",
    re.IGNORECASE,
)

DECLARED_TITLE_TYPES = (
    (re.compile(r"\b(?:theorem|claim|fact|result|observation)\b", re.I), "theorem"),
    (re.compile(r"\blemma\b", re.I), "lemma"),
    (re.compile(r"\bproposition\b", re.I), "proposition"),
    (re.compile(r"\bcorollary\b", re.I), "corollary"),
    (re.compile(r"\b(?:definition|notation)\b", re.I), "definition"),
    (re.compile(r"\b(?:assumption|hypothesis|axiom|condition)\b", re.I), "assumption"),
    (re.compile(r"\b(?:remark|note|conjecture|question|problem)\b", re.I), "remark"),
    (re.compile(r"\bexample\b", re.I), "example"),
)

DECLARED_ENV_PREFIX_TYPES = (
    ("theorem", "theorem"), ("thm", "theorem"), ("theo", "theorem"),
    ("claim", "theorem"), ("fact", "theorem"), ("result", "theorem"),
    ("observation", "theorem"), ("obs", "theorem"),
    ("lemma", "lemma"), ("lem", "lemma"),
    ("proposition", "proposition"), ("prop", "proposition"),
    ("corollary", "corollary"), ("cor", "corollary"),
    ("definition", "definition"), ("defn", "definition"), ("def", "definition"),
    ("assumption", "assumption"), ("ass", "assumption"), ("hyp", "assumption"),
    ("remark", "remark"), ("rem", "remark"), ("note", "remark"),
    ("conjecture", "remark"), ("conj", "remark"),
    ("question", "remark"), ("problem", "remark"),
    ("example", "example"), ("ex", "example"),
)


def _plain_declaration_title(title: str) -> str:
    """Reduce a simple printed theorem title to searchable plain text."""

    title = re.sub(r"\\[A-Za-z@]+\*?", " ", title)
    return re.sub(r"[^A-Za-z]+", " ", title).strip()


def _canonical_declared_type(env_name: str, title: str) -> tuple[str, str]:
    """Return ``(canonical_type, inference_source)`` for one declaration."""

    plain_title = _plain_declaration_title(title)
    for pattern, canonical in DECLARED_TITLE_TYPES:
        if pattern.search(plain_title):
            return canonical, "title"

    normalized_env = env_name.lower().rstrip("*")
    for prefix, canonical in DECLARED_ENV_PREFIX_TYPES:
        if normalized_env.startswith(prefix):
            return canonical, "environment_name"

    # ``\newtheorem`` itself says that the construct is theorem-like.  Keep an
    # unfamiliar/localized title instead of silently dropping it, and log the
    # fallback so a human can audit unusual declarations.
    return "theorem", "newtheorem_fallback"


def _declared_theorem_aliases(tex: str) -> list[tuple[str, str, str, str]]:
    """Return ``(environment, canonical, title, source)`` declarations."""

    declarations = []
    for match in NEW_THEOREM_RE.finditer(strip_comments(tex)):
        env_name = match.group("env")
        title = match.group("title").strip()
        canonical, source = _canonical_declared_type(env_name, title)
        declarations.append((env_name.lower(), canonical, title, source))
    return declarations


@dataclass
class RawEnv:
    env_type: str            # canonical name
    starred: bool
    pos: int                 # \begin start
    end: int                 # after \end
    body: str                # environment body verbatim (content after the optional argument)
    display_name: str
    section: str
    latex_label: str


@dataclass
class RawProof:
    pos: int
    end: int
    body: str
    of_text: str             # optional-argument source text, e.g. "Proof of Theorem 2.1"
    section: str


def _split_opt_arg(body: str) -> tuple[str, str]:
    """The [ ... ] optional argument at the start of body -> (display_name, remaining body)."""
    s = body.lstrip()
    if not s.startswith("["):
        return "", body
    depth, i = 0, 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == "]" and depth == 0:
            return s[1:i].strip(), s[i + 1:]
        i += 1
    return "", body


def _walk_envs(tex: str) -> list:
    """pylatexenc node tree -> all environment nodes (including nested)."""
    from pylatexenc.latexwalker import LatexEnvironmentNode, LatexWalker
    lw = LatexWalker(tex, tolerant_parsing=True)
    nodes, _, _ = lw.get_latex_nodes()
    found = []

    def rec(nodelist):
        for nd in nodelist or []:
            if nd is None:
                continue
            if isinstance(nd, LatexEnvironmentNode):
                found.append(nd)
                rec(nd.nodelist)
            elif hasattr(nd, "nodelist") and nd.nodelist:
                rec(nd.nodelist)
            elif hasattr(nd, "nodeargd") and nd.nodeargd and \
                    getattr(nd.nodeargd, "argnlist", None):
                for a in nd.nodeargd.argnlist:
                    if a is not None and hasattr(a, "nodelist") and a.nodelist:
                        rec(a.nodelist)
    rec(nodes)
    return found


# Labeled list-item assumptions: \item\label{AS0} \textbf{AS0.} <text> — a
# common ML/applied-math pattern where assumptions live in a bare itemize
# instead of a theorem-like env (2510.03923: AS0/AS1 were invisible to the
# whole pipeline, every reference to them unresolvable). The bold short tag
# is required, so ordinary labeled list items (proof steps, enumerations)
# do not match.
ITEM_ASSUMPTION_RE = re.compile(
    r"\\item\s*(?:\\label\{(?P<lab1>[^}]*)\}\s*)?"
    r"\\textbf\{\s*\(?(?P<tag>[A-Z]{1,3}\d{0,2})[.)]?\s*\}"
    r"\s*(?:\\label\{(?P<lab2>[^}]*)\})?"
    r"(?P<body>.*?)(?=\\item\b|\\end\{(?:itemize|enumerate|description)\})",
    re.DOTALL)


def _extract_item_assumptions(tex: str, marks, taken: list[tuple[int, int]]
                              ) -> list[RawEnv]:
    out = []
    for mo in ITEM_ASSUMPTION_RE.finditer(tex):
        if any(a <= mo.start() < b for a, b in taken):
            continue                    # inside a captured env: not standalone
        lab = mo.group("lab1") or mo.group("lab2") or ""
        tag = mo.group("tag")
        body = f"\\textbf{{{tag}.}} " + mo.group("body").strip()
        env = RawEnv("assumption", False, mo.start(), mo.end(), body,
                     "", section_of(mo.start(), marks), lab)
        out.append(env)
    return out


def _extract_latex(tex: str, ctx: RunContext | None = None
                   ) -> tuple[list[RawEnv], list[RawProof]]:
    aliases = dict(ENV_ALIASES)
    for env_name, canonical, title, source in _declared_theorem_aliases(tex):
        aliases[env_name] = canonical
        if ctx is not None:
            ctx.log_event(event="theorem_environment_alias",
                          environment=env_name, canonical=canonical,
                          title=title[:100], inference_source=source,
                          level=("warning" if source == "newtheorem_fallback"
                                 else "info"))

    # macro/env definition bodies must not contribute \begin/\end delimiters
    # to the walker (length-preserving mask, so every position stays valid)
    tex = mask_definition_bodies(tex)
    marks = section_positions(tex)
    envs, proofs = [], []
    for nd in _walk_envs(tex):
        name_raw = nd.environmentname
        name = name_raw.rstrip("*").lower()
        starred = name_raw.endswith("*")
        full = tex[nd.pos:nd.pos + nd.len]
        mo_b = re.match(r"\\begin\{[^}]*\}", full)
        mo_e = re.search(r"\\end\{[^}]*\}\s*$", full)
        if not (mo_b and mo_e):
            continue
        inner = full[mo_b.end():mo_e.start()]
        sec = section_of(nd.pos, marks)
        if name == "proof":
            of_text, body = _split_opt_arg(inner)
            proofs.append(RawProof(nd.pos, nd.pos + nd.len, body.strip(),
                                   of_text, sec))
            continue
        if name not in aliases:
            continue
        canon = aliases[name]
        display, body = _split_opt_arg(inner)
        tag = None
        if canon == "equation":
            display, body = "", inner            # in math envs, [ is content, not an optional arg
            tag = TAG_RE.search(inner)
            if not LABEL_RE.search(inner) and not tag:
                continue                          # only capture if it has \label or \tag (§5.1)
        lab = LABEL_RE.search(body)
        envs.append(RawEnv(canon, starred, nd.pos, nd.pos + nd.len,
                           body.strip(), display, sec,
                           lab.group(1) if lab else ""))
    # _walk_envs recurses into environment bodies, so a labeled equation nested
    # inside a theorem-like env is (intentionally) captured as its own entry too
    taken = [(e.pos, e.end) for e in envs] + [(p.pos, p.end) for p in proofs]
    envs += _extract_item_assumptions(tex, marks, taken)
    return envs, proofs


# ------------------------------------------------------------- OCR second set of regexes

MD_STMT_RE = re.compile(
    r"\*\*(Theorem|Lemma|Proposition|Corollary|Definition|Assumption|Remark|"
    r"Example|Claim)\s*([A-Za-z0-9.]*)\s*\.?\*\*", re.IGNORECASE)
# Loose superset of MD_STMT_RE: bold headers that LOOK like statement heads but
# fail the strict pattern (extra space, trailing "(Main)", odd punctuation) —
# each one is a statement the OCR route silently loses, so log it.
MD_STMT_LOOSE_RE = re.compile(
    r"\*\*\s*(?:Theorem|Lemma|Proposition|Corollary|Definition|Assumption|"
    r"Remark|Example|Claim)\b[^*\n]{0,80}?\*\*", re.IGNORECASE)
MD_PROOF_RE = re.compile(r"(?:\*\*?|_)Proof(?:\s+of\s+([^.*_]+))?\.?(?:\*\*?|_)",
                         re.IGNORECASE)
MD_SECTION_RE = re.compile(r"^#{1,3}\s*(?:(\d+)|([A-Z]))[.\s]", re.MULTILINE)
QED_RE = re.compile(r"(∎|□|\$\\square\$|\\qed|\\blacksquare)")


def _extract_markdown(ctx: RunContext,
                      md: str) -> tuple[list[RawEnv], list[RawProof]]:
    marks = [(m.start(), m.group(1) or m.group(2))
             for m in MD_SECTION_RE.finditer(md)]
    stmt_hits = list(MD_STMT_RE.finditer(md))
    strict_starts = {m.start() for m in stmt_hits}
    for m in MD_STMT_LOOSE_RE.finditer(md):
        if m.start() not in strict_starts:
            ctx.log_event(event="md_stmt_unmatched", header=m.group(0)[:100],
                          pos=m.start(), level="warning")
    proof_hits = list(MD_PROOF_RE.finditer(md))
    boundaries = sorted([m.start() for m in stmt_hits] +
                        [m.start() for m in proof_hits] + [len(md)])

    def until_next(start: int) -> int:
        nxt = [b for b in boundaries if b > start]
        blank = md.find("\n\n", start)
        cands = [b for b in (nxt[0] if nxt else len(md), ) ]
        end = cands[0]
        if 0 < blank < end:
            end = blank
        return end

    envs, proofs = [], []
    for m in stmt_hits:
        end = until_next(m.end())
        canon = ENV_ALIASES.get(m.group(1).lower(), "theorem")
        envs.append(RawEnv(canon, False, m.start(), end,
                           md[m.end():end].strip(), "",
                           section_of(m.start(), marks), ""))
        envs[-1].display_name = ""
        if m.group(2):
            envs[-1].body = md[m.end():end].strip()
    for m in proof_hits:
        qed = QED_RE.search(md, m.end())
        nxt = [b for b in boundaries if b > m.start()]
        end = min(qed.end() if qed else len(md), nxt[0] if nxt else len(md))
        proofs.append(RawProof(m.start(), end, md[m.end():end].strip(),
                               (f"Proof of {m.group(1).strip()}"
                                if m.group(1) else ""),
                               section_of(m.start(), marks)))
    return envs, proofs


# ---------------------------------------------------------------- assemble index

def build_index(ctx: RunContext, tex: str, meta: Meta) -> tuple[StatementsIndex, dict]:
    if meta.source_type == "ocr":
        envs, proofs = _extract_markdown(ctx, tex)
    else:
        envs, proofs = _extract_latex(tex, ctx=ctx)
    envs.sort(key=lambda e: e.pos)
    proofs.sort(key=lambda p: p.pos)

    # Statement identity is source-backed and opaque. In particular, never
    # emulate TeX counters here: theorem environments may share/reset/nest
    # counters in ways a structural parser cannot reproduce safely.
    statements: list[Statement] = []
    used_ids: set[str] = set()
    label_counts = Counter(
        env.latex_label.strip() for env in envs if env.latex_label.strip()
    )
    source_file = ("source/flat.md" if meta.source_type == "ocr"
                   else "source/flat.tex")
    for e in envs:
        sid = source_statement_id(
            paper_id=ctx.paper_id, env_type=e.env_type,
            statement_tex=e.body, latex_label=e.latex_label,
            used_ids=used_ids,
            duplicate_label=label_counts[e.latex_label.strip()] > 1)
        used_ids.add(sid)
        source_slice = tex[e.pos:e.end]
        source_verified = bool(e.body and e.body in source_slice)
        if not source_verified:
            ctx.log_event(event="statement_source_unverified", statement=sid,
                          pos=e.pos, level="warning")
        statements.append(Statement(
            id=sid, env_type=e.env_type,
            latex_label=e.latex_label, display_name=e.display_name,
            section=e.section, order_index=0, statement_tex=e.body,
            statement_sha256=sha256_text(e.body), source_file=source_file,
            source_start=e.pos, source_end=e.end,
            source_sha256=sha256_text(source_slice),
            source_verified=source_verified,
            proof_tex=None, proof_location="omitted", mechanical_refs=[],
            uses_figure="[FIGURE-" in e.body, added_by="parser"))

    # ID collision detection (§5.2): a duplicate is a program bug
    ids = [s.id for s in statements]
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, f"duplicate statement ids: {sorted(dup)}"

    for oi, s in enumerate(statements):
        s.order_index = oi

    # Ambiguous labels are removed from the resolution map. Failing closed is
    # safer than binding a proof or dependency to whichever duplicate appeared
    # first in source order.
    label_map = _unambiguous_label_map(ctx, statements)

    # proof pairing (§5.4)
    pos_sorted = sorted(zip(statements, envs), key=lambda t: t[1].pos)
    orphans: list[RawProof] = []
    for p in proofs:
        paired = _pair_proof(p, pos_sorted, label_map, tex)
        if paired is None:
            orphans.append(p)
            continue
        target, pairing = paired
        if target.proof_tex is not None:
            orphans.append(p)
            ctx.log_event(event="duplicate_proof_for_statement",
                          statement=target.id, pos=p.pos, level="warning")
            continue
        proof_slice = tex[p.pos:p.end]
        target.proof_tex = p.body
        target.proof_location = (f"appendix:{p.section}"
                                 if p.section.isalpha() else "inline")
        target.proof_sha256 = sha256_text(p.body)
        target.proof_source_file = source_file
        target.proof_source_start = p.pos
        target.proof_source_end = p.end
        target.proof_source_sha256 = sha256_text(proof_slice)
        target.proof_source_verified = bool(p.body and p.body in proof_slice)
        target.proof_pairing = pairing
        if not target.proof_source_verified:
            ctx.log_event(event="proof_source_unverified", statement=target.id,
                          pos=p.pos, level="warning")
        if "[FIGURE-" in p.body:
            target.uses_figure = True
    for p in orphans:
        ctx.log_event(event="orphan_proof", pos=p.pos, of=p.of_text[:80],
                      level="warning")

    # mechanical_refs (§5.3)
    for s in statements:
        refs: list[str] = []
        for text in (s.statement_tex, s.proof_tex or ""):
            for lab in scan_refs(text):
                if lab in label_map:
                    if label_map[lab] not in refs:
                        refs.append(label_map[lab])
                else:
                    ctx.log_event(event="unknown_label", label=lab, stmt=s.id)
            for key in scan_cites(text):
                if f"cite:{key}" not in refs:
                    refs.append(f"cite:{key}")
        s.mechanical_refs = refs

    citations = _parse_bibliography(tex)
    macros_tex = ctx.path("source/macros.tex").read_text(encoding="utf-8") \
        if ctx.path("source/macros.tex").exists() else ""
    index = StatementsIndex(schema_version=2, paper_id=ctx.paper_id,
                            macros_tex=macros_tex,
                            global_context=[], statements=statements,
                            citations=citations)
    orphan_records = [{"pos": p.pos, "end": p.end, "of_text": p.of_text,
                       "body": p.body, "section": p.section}
                      for p in orphans]
    return index, {"orphan_proofs": orphan_records}


PROOF_HEADING_RE = re.compile(r"[Pp]roofs?\s+of\s+([^\n]{1,160})")


def _pair_proof(p: RawProof, pos_sorted, label_map: dict, tex: str):
    """Pair by explicit source label, then strict source adjacency.

    Printed theorem numbers are deliberately ignored: without evaluating the
    document's TeX counters they are not reliable identifiers.
    """
    stmts = [(s, e) for s, e in pos_sorted]
    if p.of_text:
        labeled = resolve_hint(p.of_text, stmts, label_map)
        if labeled is not None:
            return labeled, "explicit-label"
        # An explicit but unresolved "Proof of ..." title must never fall
        # through to adjacency: it may name a different theorem.
        return None

    # The immediately preceding theorem-like source environment is safe when
    # only whitespace separates it from the proof. Non-theorem environments
    # are skipped so nested labeled equations do not shadow their host.
    prev = None
    for s, e in stmts:
        if e.end <= p.pos and s.env_type in THEOREM_LIKE:
            prev = (s, e)
        elif e.pos >= p.pos:
            break
    if prev and tex[prev[1].end:p.pos].strip() == "":
        return prev[0], "adjacent"
    # A \paragraph{Proof of Theorem~\ref{X}.} / \subsection{Proof of ...}
    # heading followed by an argument-less proof environment. Only an explicit
    # unambiguous source label resolves the hint.
    window_start = prev[1].end if prev else max(0, p.pos - 400)
    window = tex[max(window_start, p.pos - 400):p.pos]
    hits = list(PROOF_HEADING_RE.finditer(window))
    if hits:
        labeled = resolve_hint(hits[-1].group(1), stmts, label_map)
        if labeled is not None:
            return labeled, "explicit-heading-label"
    return None


def resolve_hint(hint: str, stmts, label_map: dict):
    """Resolve ``Proof of ...`` only through an explicit source reference.

    Reused by step3's proof_links (§6.3 item 4). stmts elements may be (Statement, RawEnv)
    or Statement.
    """
    def unwrap(x):
        return x[0] if isinstance(x, tuple) else x

    from .latex_utils import scan_refs
    for lab in scan_refs(hint):                     # \ref \cref \Cref \autoref
        sid = label_map.get(lab)
        if sid:
            for x in stmts:
                # a "Proof of ..." can only belong to a theorem-like entry;
                # a label resolving elsewhere is a corrupted-map artifact
                if unwrap(x).id == sid \
                        and unwrap(x).env_type in THEOREM_LIKE:
                    return unwrap(x)
    return None


def _unambiguous_label_map(
    ctx: RunContext, statements: list[Statement]
) -> dict[str, str]:
    owners: dict[str, str] = {}
    ambiguous: set[str] = set()
    for statement in statements:
        labels = list(LABEL_RE.findall(statement.statement_tex))
        if statement.latex_label and statement.latex_label not in labels:
            labels.insert(0, statement.latex_label)
        for label in labels:
            previous = owners.setdefault(label, statement.id)
            if previous != statement.id:
                ambiguous.add(label)
                ctx.log_event(event="label_collision", label=label,
                              kept=previous, dropped=statement.id,
                              level="warning")
    for label in ambiguous:
        owners.pop(label, None)
    return owners


BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}")


def _parse_bibliography(tex: str) -> list[Citation]:
    hits = list(BIBITEM_RE.finditer(tex))
    out = []
    end_bib = tex.find("\\end{thebibliography}")
    for i, m in enumerate(hits):
        stop = hits[i + 1].start() if i + 1 < len(hits) else \
            (end_bib if end_bib > m.end() else len(tex))
        out.append(Citation(key=m.group(1).strip(),
                            raw_bib=tex[m.start():stop].strip()))
    return out


def run(ctx: RunContext) -> None:
    ctx.step_name = STEP
    meta = ctx.read_model("source/meta.json", Meta)
    src = ctx.path("source/flat.md" if meta.source_type == "ocr"
                   else "source/flat.tex")
    tex = src.read_text(encoding="utf-8")
    index, extras = build_index(ctx, tex, meta)
    g1_min_statements(ctx, index)                    # G1
    ctx.write_json("index/statements.v1.json", index)
    label_map = _unambiguous_label_map(ctx, index.statements)
    ctx.write_json("index/label_map.json", label_map)
    ctx.write_json("index/orphan_proofs.json", extras["orphan_proofs"])
    ctx.log_event(event="step2_done", statements=len(index.statements),
                  labels=len(label_map), citations=len(index.citations),
                  orphan_proofs=len(extras["orphan_proofs"]))
