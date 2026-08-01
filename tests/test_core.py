from __future__ import annotations

import csv
import json
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
            self.assertTrue(
                (target / "registry" / "work_items.tsv").exists()
            )

    def test_publication_goal_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(EXAMPLE_PROJECT, target)
            manifest_path = target / "PROJECT.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            del manifest["publication_goal"]
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n",
                encoding="utf-8",
            )
            report = validate_project(target)
            self.assertFalse(report.ok)
            self.assertTrue(
                any("publication_goal" in error for error in report.errors)
            )

    def test_work_item_requires_a_stop_condition(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(EXAMPLE_PROJECT, target)
            registry_path = target / "registry" / "work_items.tsv"
            with registry_path.open(
                encoding="utf-8", newline=""
            ) as handle:
                reader = csv.DictReader(handle, delimiter="\t")
                fieldnames = reader.fieldnames
                rows = list(reader)
            self.assertIsNotNone(fieldnames)
            rows[0]["stop_condition"] = ""
            with registry_path.open(
                "w", encoding="utf-8", newline=""
            ) as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=fieldnames,
                    delimiter="\t",
                    lineterminator="\n",
                )
                writer.writeheader()
                writer.writerows(rows)

            report = validate_project(target)
            self.assertFalse(report.ok)
            self.assertTrue(
                any(
                    "empty required value stop_condition" in error
                    for error in report.errors
                )
            )

    def test_direction_requires_a_valid_ambition_tier(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(EXAMPLE_PROJECT, target)
            registry_path = target / "registry" / "directions.tsv"
            with registry_path.open(
                encoding="utf-8", newline=""
            ) as handle:
                reader = csv.DictReader(handle, delimiter="\t")
                fieldnames = reader.fieldnames
                rows = list(reader)
            self.assertIsNotNone(fieldnames)
            rows[0]["ambition_tier"] = "automatic_top_tier"
            with registry_path.open(
                "w", encoding="utf-8", newline=""
            ) as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=fieldnames,
                    delimiter="\t",
                    lineterminator="\n",
                )
                writer.writeheader()
                writer.writerows(rows)

            report = validate_project(target)
            self.assertFalse(report.ok)
            self.assertTrue(
                any(
                    "invalid ambition_tier" in error
                    for error in report.errors
                )
            )

    def test_approved_direction_requires_a_decided_ambition_tier(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(EXAMPLE_PROJECT, target)
            registry_path = target / "registry" / "directions.tsv"
            with registry_path.open(
                encoding="utf-8", newline=""
            ) as handle:
                reader = csv.DictReader(handle, delimiter="\t")
                fieldnames = reader.fieldnames
                rows = list(reader)
            self.assertIsNotNone(fieldnames)
            rows[0]["status"] = "approved"
            rows[0]["primary_change_axis"] = "immune_state"
            with registry_path.open(
                "w", encoding="utf-8", newline=""
            ) as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=fieldnames,
                    delimiter="\t",
                    lineterminator="\n",
                )
                writer.writeheader()
                writer.writerows(rows)

            report = validate_project(target)
            self.assertFalse(report.ok)
            self.assertTrue(
                any(
                    "approved direction DIR-001 has undecided "
                    "ambition_tier" in error
                    for error in report.errors
                )
            )

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
                    "The synthetic result would require revising the "
                    "manuscript direction.",
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
                    "WORK-001",
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
