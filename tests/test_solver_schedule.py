"""Exercise both canonical packets without model calls or network access."""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from citation.prompts import CitationPromptTemplates
from solver.agent_calls import AgentCaller
from solver.controller import ControllerConfig
from solver.mock import ScriptedMockClient
from solver.orchestrator import OpenProblemOrchestrator, OpenRunConfig, ProblemInputs
from solver.prompt_loader import PacketPrompts
from solver.run_store import OpenRunStore
from solver.schemas import (
    STATUS_ACCEPTED_CASCADE_ONLY,
    STATUS_NEEDS_HUMAN_REVIEW,
    STATUS_STOPPED_MAX_ROUNDS,
)


ROOT = Path(__file__).resolve().parents[1]
PACKETS = ("Prompts.md", "PromptsWithFullInternet.md")


class ScheduleClient(ScriptedMockClient):
    def __init__(self, *, scenario="solved_round1", key_solver="S3"):
        super().__init__(scenario=scenario)
        self.key_solver = key_solver
        self.events = []

    def _respond(self, role, metadata):
        text = super()._respond(role, metadata)
        if role == "s0":
            replacement = (
                f"key_solver_id: {self.key_solver}"
                if self.key_solver is not None else ""
            )
            text = text.replace("key_solver_id: S3", replacement)
        return text

    def complete(self, prompt, metadata):
        role = metadata.get("s_id") if prompt.role == "subproblem" else prompt.role
        self.events.append((role, "start"))
        response = super().complete(prompt, metadata)
        self.events.append((role, "finish"))
        return response


class SolverScheduleTests(unittest.TestCase):
    def run_packet(self, packet_name, root, client):
        packet = ROOT / "Prompt Packet" / packet_name
        caller = AgentCaller(
            prompts=PacketPrompts.from_file(packet),
            solver_client=client,
            citation_prompts=CitationPromptTemplates.from_file(packet),
        )
        return OpenProblemOrchestrator(
            problem=ProblemInputs(
                problem_id="schedule-test",
                target="Mock target theorem.",
                skeleton="Mock definitions and allowed statements.",
            ),
            caller=caller,
            store=OpenRunStore(root),
            config=OpenRunConfig(max_rounds=1, solver_workers=5),
            controller_config=ControllerConfig(max_branch_depth=0, max_total_branches=0),
        ).run()

    def test_both_packets_require_key_first_and_keep_their_internet_modes(self):
        for name, mode in zip(PACKETS, ("none", "source_supported")):
            with self.subTest(packet=name):
                packet = ROOT / "Prompt Packet" / name
                self.assertTrue(PacketPrompts.from_file(packet).requires_key_solver_first)
                self.assertIn(f"<!-- SOLVER_INTERNET_MODE: {mode} -->", packet.read_text())

    def test_s0_selected_key_finishes_before_siblings_and_s6(self):
        for name in PACKETS:
            for key in ("S1", "S3", "S5"):
                with self.subTest(packet=name, key=key), TemporaryDirectory() as tmp:
                    client = ScheduleClient(key_solver=key)
                    state = self.run_packet(name, Path(tmp), client)
                    self.assertEqual(state.status, STATUS_ACCEPTED_CASCADE_ONLY)
                    solvers = [c["s_id"] for c in client.calls if c["role"] == "subproblem"]
                    self.assertEqual(solvers[0], key)
                    self.assertCountEqual(solvers, [f"S{i}" for i in range(1, 6)])
                    key_finished = client.events.index((key, "finish"))
                    for solver in solvers:
                        if solver != key:
                            self.assertLess(key_finished, client.events.index((solver, "start")))
                        self.assertLess(
                            client.events.index((solver, "finish")),
                            client.events.index(("s6", "start")),
                        )

    def test_unsolved_key_skips_siblings_and_s6_and_records_guidance(self):
        for name in PACKETS:
            with self.subTest(packet=name), TemporaryDirectory() as tmp:
                root = Path(tmp)
                client = ScheduleClient(scenario="hint_then_solved")
                state = self.run_packet(name, root, client)
                self.assertEqual(state.status, STATUS_STOPPED_MAX_ROUNDS)
                self.assertEqual(len(state.guidance), 1)
                self.assertEqual([c["role"] for c in client.calls], ["s0", "subproblem"])
                self.assertEqual(client.calls[-1]["s_id"], "S3")
                gate = json.loads((root / "round_001/parsed/key_solver_gate.json").read_text())
                self.assertEqual(gate["skipped_solvers"], ["S1", "S2", "S4", "S5"])
                self.assertTrue(gate["skipped_s6"])
                self.assertFalse((root / "round_001/S6.md").exists())

    def test_missing_or_invalid_key_stops_before_any_subsolver(self):
        for name in PACKETS:
            for key in (None, "S9"):
                with self.subTest(packet=name, key=key), TemporaryDirectory() as tmp:
                    client = ScheduleClient(key_solver=key)
                    state = self.run_packet(name, Path(tmp), client)
                    self.assertEqual(state.status, STATUS_NEEDS_HUMAN_REVIEW)
                    self.assertEqual(state.guidance, [])
                    self.assertEqual([c["role"] for c in client.calls], ["s0"])

    def test_documented_citation_tree_matches_actual_output(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_packet(PACKETS[0], root, ScheduleClient())
            citation_root = root / "round_001/citation_gate"
            for document in ("Individual Pipeline/citation/README.md", "Outputs/README.md"):
                guide = (ROOT / document).read_text()
                lines = guide.split("```text\n", 1)[1].split("\n```", 1)[0].splitlines()
                start = next(i for i, line in enumerate(lines) if line.endswith("citation_gate/"))
                base_indent = len(lines[start]) - len(lines[start].lstrip(" "))
                parents = []
                checked = 0
                for line in lines[start + 1:]:
                    indent = len(line) - len(line.lstrip(" "))
                    if indent <= base_indent:
                        break
                    depth = (indent - base_indent) // 2
                    parents = parents[:depth - 1]
                    name = line.strip().rstrip("/")
                    path = citation_root.joinpath(*parents, name)
                    with self.subTest(document=document, path=str(path.relative_to(citation_root))):
                        self.assertTrue(path.exists(), f"documented artifact not produced: {path}")
                    checked += 1
                    if line.endswith("/"):
                        parents.append(name)
                self.assertGreaterEqual(checked, 5, "citation tree must include attempts and reports")


if __name__ == "__main__":
    unittest.main()
