from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from prompt_sync import COMPONENT_ROOT, _resolve_layout, expected_views, stale_views


class ComponentPromptViewTests(unittest.TestCase):
    def test_all_component_prompt_views_are_current(self) -> None:
        self.assertEqual(stale_views(), [])

    def test_expected_component_ownership(self) -> None:
        paths = set(expected_views())
        self.assertEqual(len(paths), 16)
        self.assertTrue(any(path.startswith("solver/prompts/") for path in paths))
        self.assertTrue(any(path.startswith("citation/prompts/") for path in paths))
        self.assertTrue(any(path.startswith("verifiers/prompts/") for path in paths))
        for relative in ("paper_cleaner/prompts", "paper_cleaner_mini/prompts"):
            prompt_dir = COMPONENT_ROOT / relative
            with self.subTest(prompt_dir=relative):
                self.assertTrue(prompt_dir.is_dir())
                self.assertTrue(any(path.is_file() for path in prompt_dir.iterdir()))

    def test_only_solver_prompts_have_mode_specific_views(self) -> None:
        paths = set(expected_views())
        no_internet = {
            path.removeprefix("solver/prompts/no_internet/")
            for path in paths
            if path.startswith("solver/prompts/no_internet/")
        }
        full_internet = {
            path.removeprefix("solver/prompts/full_internet/")
            for path in paths
            if path.startswith("solver/prompts/full_internet/")
        }
        self.assertEqual(no_internet, full_internet)
        self.assertEqual(no_internet, {"s0.md", "s1_s5_subproblem.md", "s6.md"})

    def test_installed_layout_uses_environment_packet(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            module_root = root / "site-packages"
            install_prefix = root / "venv"
            module_root.mkdir()
            (install_prefix / "Prompt Packet").mkdir(parents=True)

            component_root, packet_root = _resolve_layout(module_root, install_prefix)

            self.assertEqual(component_root, module_root)
            self.assertEqual(packet_root, install_prefix / "Prompt Packet")


if __name__ == "__main__":
    unittest.main()
