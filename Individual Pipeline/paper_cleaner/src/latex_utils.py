"""LaTeX text-processing utilities: comments, macros, figure placeholders,
reference scanning, sectioning.

An internal helper module shared by step1/step2/step4/step7.
"""
from __future__ import annotations

import re
from typing import Optional


# ------------------------------------------------------------------- Comments

def strip_comments(tex: str) -> str:
    """Delete from % to end of line (skipping \\%), preserving newlines (§4.1 item 5)."""
    out_lines = []
    for line in tex.split("\n"):
        i, cut = 0, None
        while i < len(line):
            c = line[i]
            if c == "\\":
                i += 2
                continue
            if c == "%":
                cut = i
                break
            i += 1
        out_lines.append(line if cut is None else line[:cut])
    return "\n".join(out_lines)


# --------------------------------------------------------------- Brace matching

def read_brace_group(text: str, i: int) -> Optional[tuple[str, int]]:
    """text[i] must be '{'; returns (group contents, position one past the
    closing brace), or None if the brace is unmatched."""
    if i >= len(text) or text[i] != "{":
        return None
    depth, j = 0, i
    while j < len(text):
        c = text[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1:j], j + 1
        j += 1
    return None


_DEF_HEAD_RE = re.compile(
    r"\\(?:(?:re)?newcommand\*?|providecommand\*?|(?:re)?newenvironment\*?"
    r"|def)\s*(?:\{\s*\\?[A-Za-z@*]+\s*\}|\\[A-Za-z@]+)"
    r"(?:\s*\[[^\]]*\]|#\d)*")


def mask_definition_bodies(tex: str) -> str:
    """Blank out macro/environment DEFINITION bodies, length-preserving.

    A preamble shorthand like \\newcommand{\\be}{\\begin{equation}} otherwise
    leaks a literal \\begin delimiter into the environment walker, which can
    pair it with a far-away real \\end and swallow half the paper into one
    phantom env (observed on 1709.09195: a 208k-char "equation" holding 120
    labels, corrupting the label map and unlinking every deferred proof).
    Interiors become spaces (newlines kept), so every downstream position
    stays valid; document-body text is untouched."""
    out = list(tex)
    for m in _DEF_HEAD_RE.finditer(tex):
        i = m.end()
        nbodies = 2 if "environment" in m.group(0) else 1
        for _ in range(nbodies):
            while i < len(tex) and tex[i] in " \t\n":
                i += 1
            grp = read_brace_group(tex, i)
            if grp is None:
                break
            _, j = grp
            for k in range(i + 1, j - 1):
                if out[k] != "\n":
                    out[k] = " "
            i = j
    return "".join(out)


def braces_balanced(text: str) -> bool:
    depth, i = 0, 0
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    return depth == 0


# ------------------------------------------------------------------- Macros

MACRO_DEF_RE = re.compile(
    r"\\(newcommand|renewcommand|providecommand|def|DeclareMathOperator)\b\*?")


class MacroDef:
    def __init__(self, name: str, n_args: int, body: str, raw: str,
                 simple: bool):
        self.name = name          # without the backslash
        self.n_args = n_args
        self.body = body
        self.raw = raw            # the original definition line (used when writing macros.tex)
        self.simple = simple


def collect_macros(preamble: str) -> list[MacroDef]:
    """Collect \\newcommand \\renewcommand \\def \\DeclareMathOperator from the preamble."""
    macros: list[MacroDef] = []
    for m in MACRO_DEF_RE.finditer(preamble):
        kind = m.group(1)
        i = m.end()
        start = m.start()
        # command name: \def\cmd... or \newcommand{\cmd}
        while i < len(preamble) and preamble[i] in " \t":
            i += 1
        name = None
        if i < len(preamble) and preamble[i] == "{":
            grp = read_brace_group(preamble, i)
            if not grp:
                continue
            inner, i = grp
            inner = inner.strip()
            if inner.startswith("\\"):
                name = inner[1:]
        elif i < len(preamble) and preamble[i] == "\\":
            j = i + 1
            while j < len(preamble) and (preamble[j].isalpha() or preamble[j] == "@"):
                j += 1
            name = preamble[i + 1:j]
            i = j
        if not name:
            continue
        n_args, has_default, simple = 0, False, True
        if kind == "def":
            # \def\cmd#1#2{body}: the # parameter string
            params = ""
            while i < len(preamble) and preamble[i] != "{":
                params += preamble[i]
                i += 1
            n_args = params.count("#")
            if params.strip() and not re.fullmatch(r"(#\d)+", params.strip()):
                simple = False          # a \def with delimited parameters does not count as a simple macro
        else:
            while i < len(preamble) and preamble[i] in " \t":
                i += 1
            if i < len(preamble) and preamble[i] == "[":
                j = preamble.find("]", i)
                if j > 0:
                    n_args = int(preamble[i + 1:j]) if preamble[i + 1:j].isdigit() else 0
                    i = j + 1
            while i < len(preamble) and preamble[i] in " \t":
                i += 1
            if i < len(preamble) and preamble[i] == "[":   # optional default argument -> not simple
                j = preamble.find("]", i)
                has_default = True
                if j > 0:
                    i = j + 1
        while i < len(preamble) and preamble[i] in " \t":
            i += 1
        grp = read_brace_group(preamble, i)
        if not grp:
            continue
        body, end = grp
        if kind == "DeclareMathOperator":
            body = r"\operatorname{" + body + "}"
        raw = preamble[start:end]
        if has_default or "\\if" in body:
            simple = False
        macros.append(MacroDef(name, n_args, body, raw, simple))
    return macros


def mark_expandable(macros: list[MacroDef]) -> None:
    """Do not expand those whose right-hand side contains other custom macros (§4.1 6b)."""
    names = {m.name for m in macros}
    pat = re.compile(r"\\([A-Za-z@]+)")
    for m in macros:
        if not m.simple:
            continue
        for used in pat.findall(m.body):
            if used in names and used != m.name:
                m.simple = False
                break


def _replace_macro_once(text: str, m: MacroDef) -> tuple[str, int]:
    """Replace \\name calls in text once; returns (new text, replacement count)."""
    pat = re.compile(r"\\" + re.escape(m.name) + r"(?![A-Za-z@])")
    out, pos, count = [], 0, 0
    while True:
        mo = pat.search(text, pos)
        if not mo:
            out.append(text[pos:])
            break
        out.append(text[pos:mo.start()])
        i = mo.end()
        if m.n_args == 0:
            out.append(m.body)
            pos = i
            count += 1
            continue
        args, j, ok = [], i, True
        for _ in range(m.n_args):
            while j < len(text) and text[j] in " \t\n":
                j += 1
            grp = read_brace_group(text, j)
            if not grp:
                ok = False
                break
            arg, j = grp
            args.append(arg)
        if not ok:
            out.append(text[mo.start():i])       # arguments incomplete, keep as-is
            pos = i
            continue
        body = m.body
        for k, a in enumerate(args, 1):
            body = body.replace(f"#{k}", a)
        out.append(body)
        pos = j
        count += 1
    return "".join(out), count


def expand_simple_macros(text: str, macros: list[MacroDef],
                         max_rounds: int = 5) -> str:
    """Fixed-point expansion over the body (at most max_rounds passes),
    expanding simple macros only."""
    expandable = [m for m in macros if m.simple]
    for _ in range(max_rounds):
        total = 0
        for m in expandable:
            text, n = _replace_macro_once(text, m)
            total += n
        if total == 0:
            break
    return text


# --------------------------------------------------------------- Figure placeholders

FIGURE_ENVS = ("tikzpicture", "figure", "figure*", "pspicture", "wrapfigure")


def replace_figure_envs(tex: str) -> tuple[str, int]:
    """Replace each figure environment wholesale with [FIGURE-<n>], n
    incrementing across the document (§4.1 item 7)."""
    n = 0
    for env in FIGURE_ENVS:
        pat = re.compile(
            r"\\begin\{" + re.escape(env) + r"\}.*?\\end\{" + re.escape(env) + r"\}",
            re.DOTALL)
        while True:
            mo = pat.search(tex)
            if not mo:
                break
            n += 1
            tex = tex[:mo.start()] + f"[FIGURE-{n}]" + tex[mo.end():]
    return tex, n


# --------------------------------------------------------------- Reference scan

REF_CMD_RE = re.compile(r"\\(?:ref|eqref|cref|Cref|autoref|vref)\{([^}]*)\}")
# \hyperref[label]{text} carries its label in BRACKETS — papers that number
# assumptions as \hyperref[AS0]{AS0} were invisible to the whole ref machinery
# (2510.03923: 27 such references, every assumption edge lost)
HYPERREF_RE = re.compile(r"\\hyperref\[([^\]]*)\]")
CITE_RE = re.compile(r"\\cite[tp]?\*?(?:\[[^\]]*\])*\{([^}]*)\}")
LABEL_RE = re.compile(r"\\label\{([^}]*)\}")


def scan_refs(text: str) -> list[str]:
    """Return the labels referenced in the text (order-preserving dedup), with cref comma expansion."""
    seen, out = set(), []
    for mo in REF_CMD_RE.finditer(text):
        for lab in mo.group(1).split(","):
            lab = lab.strip()
            if lab and lab not in seen:
                seen.add(lab)
                out.append(lab)
    for mo in HYPERREF_RE.finditer(text):
        lab = mo.group(1).strip()
        if lab and lab not in seen:
            seen.add(lab)
            out.append(lab)
    return out


def scan_cites(text: str) -> list[str]:
    seen, out = set(), []
    for mo in CITE_RE.finditer(text):
        for key in mo.group(1).split(","):
            key = key.strip()
            if key and key not in seen:
                seen.add(key)
                out.append(key)
    return out


# ----------------------------------------------------------------- Sectioning/segmentation

SECTION_RE = re.compile(
    r"\\(?P<kind>section|appendix)\b(?P<star>\*)?", re.MULTILINE
)


def section_positions(tex: str) -> list[tuple[int, str]]:
    """Return [(start position, section_id)]; sections after \\appendix are labeled A, B, C, ....

    section 0 = from \\begin{document} to the first \\section (including the abstract/intro preamble).
    """
    marks: list[tuple[int, str]] = []
    sec_no, in_appendix, app_no = 0, False, 0
    for mo in SECTION_RE.finditer(tex):
        if mo.group("kind") == "appendix":
            in_appendix = True
            continue
        if mo.group("star"):
            continue
        if in_appendix:
            app_no += 1
            sid = chr(ord("A") + app_no - 1)
        else:
            sec_no += 1
            sid = str(sec_no)
        marks.append((mo.start(), sid))
    return marks


def section_of(pos: int, marks: list[tuple[int, str]]) -> str:
    cur = "0"
    for p, sid in marks:
        if p <= pos:
            cur = sid
        else:
            break
    return cur


def split_paragraph_chunks(text: str, cap: int) -> list[str]:
    """Split into <=cap chunks along paragraph boundaries (a single paragraph
    exceeding cap is hard-split)."""
    paras = re.split(r"\n\s*\n", text)
    chunks, cur = [], ""
    for p in paras:
        piece = (p + "\n\n")
        if len(cur) + len(piece) <= cap:
            cur += piece
            continue
        if cur:
            chunks.append(cur)
            cur = ""
        while len(piece) > cap:                 # rare: a single paragraph exceeds cap
            chunks.append(piece[:cap])
            piece = piece[cap:]
        cur = piece
    if cur.strip():
        chunks.append(cur)
    return [c for c in chunks if c.strip()]


def extract_env_block(tex: str, env: str, start: int = 0) -> Optional[tuple[int, int, str]]:
    """Find \\begin{env}...\\end{env} (handling same-name nesting), returning (start, end, body)."""
    begin_pat = re.compile(r"\\begin\{" + re.escape(env) + r"\}")
    end_pat = re.compile(r"\\(begin|end)\{" + re.escape(env) + r"\}")
    mo = begin_pat.search(tex, start)
    if not mo:
        return None
    depth, pos = 1, mo.end()
    while depth:
        m2 = end_pat.search(tex, pos)
        if not m2:
            return None
        depth += 1 if m2.group(1) == "begin" else -1
        pos = m2.end()
        if depth == 0:
            return mo.start(), pos, tex[mo.end():m2.start()]
    return None
