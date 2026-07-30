from __future__ import annotations

import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from paperroute.core import (
    downstream_impact,
    init_project,
    validate_project,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PROJECT = REPOSITORY_ROOT / "examples" / "spp1-tam-jitc"


def append_tsv(path: Path, values: list[str]) -> None:
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(values)


class PaperRouteCoreTests(unittest.TestCase):
    def test_example_project_validates(self) -> None:
        report = validate_project(EXAMPLE_PROJECT)
        self.assertTrue(report.ok, report.errors)

    def test_direction_impact_reaches_claim_and_module(self) -> None:
        impacted = downstream_impact(EXAMPLE_PROJECT, "DIR-001")
        ids = {item["entity_id"] for item in impacted}
        self.assertIn("CLAIM-001", ids)
        self.assertIn("MODULE-001", ids)

    def test_init_creates_valid_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "draft"
            init_project(target, "PRJ-TEST", "Test project")
            report = validate_project(target)
            self.assertTrue(report.ok, report.errors)

    def test_directional_result_requires_change_request(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(EXAMPLE_PROJECT, target)

            append_tsv(
                target / "registry" / "runs.tsv",
                [
                    "RUN-TEST-001",
                    "completed",
                    "test-commit",
                    "config-hash",
                    "manifest-hash",
                    "RESOURCE-ENV-001",
                    "2026-01-01T00:00:00Z",
                    "2026-01-01T00:01:00Z",
                    "Synthetic test run",
                ],
            )
            append_tsv(
                target / "registry" / "results.tsv",
                [
                    "RESULT-TEST-001",
                    "RUN-TEST-001",
                    "MODULE-001",
                    "CLAIM-001",
                    "provisional",
                    "current",
                    "reroute",
                    "associational",
                    "Synthetic result used only to test feedback validation.",
                    "outputs/test.tsv",
                    "2026-01-01T00:01:00Z",
                ],
            )

            missing_change = validate_project(target)
            self.assertFalse(missing_change.ok)
            self.assertTrue(
                any(
                    "no change request" in error
                    for error in missing_change.errors
                )
            )

            append_tsv(
                target / "registry" / "change_requests.tsv",
                [
                    "CHANGE-TEST-001",
                    "RESULT-TEST-001",
                    "direction",
                    "high",
                    "DIR-001",
                    "Reopen direction audit after the synthetic result.",
                    "proposed",
                    "G0_DIRECTION",
                    "",
                    "2026-01-01T00:02:00Z",
                ],
            )
            linked_change = validate_project(target)
            self.assertTrue(linked_change.ok, linked_change.errors)


if __name__ == "__main__":
    unittest.main()
