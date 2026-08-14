"""Prompt-copy drift tests for local verifier prompt templates."""

from __future__ import annotations

import unittest

from verifiers.prompt_sync import LOCAL_PROMPTS, SECTIONS, expected_prompts


class PromptCopyDriftTests(unittest.TestCase):
    def test_local_prompt_copies_match_prompts_md_sections(self) -> None:
        expected_prompts_by_name = expected_prompts()
        for file_name in SECTIONS:
            with self.subTest(file_name=file_name):
                expected = expected_prompts_by_name[file_name]
                actual = (LOCAL_PROMPTS / file_name).read_text(encoding="utf-8-sig")
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
