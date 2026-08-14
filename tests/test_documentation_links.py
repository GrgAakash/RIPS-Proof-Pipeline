from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAP = ROOT / "SOURCE_MAP.md"
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


class DocumentationLinkTests(unittest.TestCase):
    def test_every_source_map_link_resolves(self) -> None:
        broken: list[str] = []
        for raw_target in MARKDOWN_LINK_RE.findall(
                SOURCE_MAP.read_text(encoding="utf-8-sig")):
            target = unquote(raw_target.strip().strip("<>")).split("#", 1)[0]
            if not target or SCHEME_RE.match(target):
                continue
            if not (SOURCE_MAP.parent / target).exists():
                broken.append(raw_target)

        self.assertEqual(broken, [], f"broken SOURCE_MAP.md links: {broken}")


if __name__ == "__main__":
    unittest.main()
