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
SPP1_PROJECT = REPOSITORY_ROOT / "workspaces" / "spp1-tam-jitc"
BMC_PROJECT = (
    REPOSITORY_ROOT
    / "workspaces"
    / "bmc-cancer-2025-gastric-nerve-model"
)


def append_tsv(path: Path, values: list[str]) -> None:
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(values)


def read_tsv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def write_tsv_rows(
    path: Path, fieldnames: list[str], rows: list[dict[str, str]]
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


class PaperRouteCoreTests(unittest.TestCase):
    def test_example_project_validates(self) -> None:
        report = validate_project(SPP1_PROJECT)
        self.assertTrue(report.ok, report.errors)

    def test_bmc_audit_workspace_validates(self) -> None:
        report = validate_project(BMC_PROJECT)
        self.assertTrue(report.ok, report.errors)

    def test_direction_impact_reaches_candidates_but_not_retired_module(
        self,
    ) -> None:
        impacted = downstream_impact(SPP1_PROJECT, "DIR-001")
        ids = {item["entity_id"] for item in impacted}
        self.assertIn("CLAIM-001", ids)
        self.assertIn("DIR-002", ids)
        self.assertNotIn("MODULE-001", ids)

    def test_init_creates_valid_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "draft"
            init_project(target, "PRJ-TEST", "Test project")
            report = validate_project(target)
            self.assertTrue(report.ok, report.errors)
            self.assertTrue(
                (target / "registry" / "work_items.tsv").exists()
            )
            self.assertTrue(
                (target / "registry" / "direction_changes.tsv").exists()
            )
            manifest = json.loads(
                (target / "PROJECT.json").read_text(encoding="utf-8")
            )
            self.assertTrue(
                manifest["project_brief"]["decision_policy"][
                    "allow_multi_axis_change"
                ]
            )

    def test_publication_goal_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(SPP1_PROJECT, target)
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

    def test_project_brief_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(SPP1_PROJECT, target)
            manifest_path = target / "PROJECT.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            del manifest["project_brief"]
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n",
                encoding="utf-8",
            )
            report = validate_project(target)
            self.assertFalse(report.ok)
            self.assertTrue(
                any("project_brief" in error for error in report.errors)
            )

    def test_candidate_cannot_change_a_project_disallowed_axis(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(BMC_PROJECT, target)
            manifest_path = target / "PROJECT.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["project_brief"]["allowed_change_axes"].remove(
                "biological_object"
            )
            manifest_path.write_text(
                json.dumps(manifest, indent=2) + "\n",
                encoding="utf-8",
            )
            report = validate_project(target)
            self.assertFalse(report.ok)
            self.assertTrue(
                any(
                    "project-disallowed axis='biological_object'" in error
                    for error in report.errors
                )
            )

    def test_work_item_requires_a_stop_condition(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(SPP1_PROJECT, target)
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

    def test_non_umbrella_direction_requires_every_core_axis(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(SPP1_PROJECT, target)
            registry_path = target / "registry" / "direction_changes.tsv"
            fieldnames, rows = read_tsv_rows(registry_path)
            rows = [
                row
                for row in rows
                if not (
                    row["direction_id"] == "DIR-002"
                    and row["axis"] == "primary_outcome"
                )
            ]
            write_tsv_rows(registry_path, fieldnames, rows)

            report = validate_project(target)
            self.assertFalse(report.ok)
            self.assertTrue(
                any(
                    "DIR-002 lacks core change-map axes" in error
                    and "primary_outcome" in error
                    for error in report.errors
                )
            )

    def test_repair_action_requires_a_linked_flaw(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(BMC_PROJECT, target)
            registry_path = target / "registry" / "direction_changes.tsv"
            fieldnames, rows = read_tsv_rows(registry_path)
            target_row = next(
                row
                for row in rows
                if row["change_id"] == "CHANGE-D002-02"
            )
            target_row["linked_flaw_ids"] = ""
            write_tsv_rows(registry_path, fieldnames, rows)

            report = validate_project(target)
            self.assertFalse(report.ok)
            self.assertTrue(
                any(
                    "CHANGE-D002-02 uses action=repair" in error
                    for error in report.errors
                )
            )

    def test_candidate_must_respond_to_every_fatal_anchor_flaw(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(BMC_PROJECT, target)
            registry_path = target / "registry" / "direction_changes.tsv"
            fieldnames, rows = read_tsv_rows(registry_path)
            target_row = next(
                row
                for row in rows
                if row["change_id"] == "CHANGE-D003-04"
            )
            target_row["linked_flaw_ids"] = "FLAW-006"
            write_tsv_rows(registry_path, fieldnames, rows)

            report = validate_project(target)
            self.assertFalse(report.ok)
            self.assertTrue(
                any(
                    "DIR-003 does not explicitly respond" in error
                    and "FLAW-005" in error
                    for error in report.errors
                )
            )

    def test_multi_axis_adaptation_is_allowed(self) -> None:
        fieldnames, rows = read_tsv_rows(
            BMC_PROJECT / "registry" / "direction_changes.tsv"
        )
        self.assertIn("action", fieldnames)
        changed_axes = {
            row["axis"]
            for row in rows
            if row["direction_id"] == "DIR-003"
            and row["action"] in {"replace", "extend", "drop"}
        }
        self.assertGreaterEqual(len(changed_axes), 3)
        report = validate_project(BMC_PROJECT)
        self.assertTrue(report.ok, report.errors)

    def test_challenged_direction_cannot_remain_primary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(BMC_PROJECT, target)
            registry_path = (
                target / "registry" / "direction_assessments.tsv"
            )
            fieldnames, rows = read_tsv_rows(registry_path)
            target_row = next(
                row
                for row in rows
                if row["direction_id"] == "DIR-002"
            )
            target_row["recommendation"] = "primary"
            write_tsv_rows(registry_path, fieldnames, rows)

            report = validate_project(target)
            self.assertFalse(report.ok)
            self.assertTrue(
                any(
                    "challenged direction DIR-002 cannot remain" in error
                    for error in report.errors
                )
            )

    def test_approved_manuscript_direction_must_pass_assessment(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(BMC_PROJECT, target)
            directions_path = target / "registry" / "directions.tsv"
            fieldnames, rows = read_tsv_rows(directions_path)
            target_row = next(
                row for row in rows if row["direction_id"] == "DIR-004"
            )
            target_row["status"] = "approved"
            write_tsv_rows(directions_path, fieldnames, rows)

            report = validate_project(target)
            self.assertFalse(report.ok)
            self.assertTrue(
                any(
                    "approved manuscript direction DIR-004 does not pass"
                    in error
                    for error in report.errors
                )
            )

    def test_directional_result_requires_change_request(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "project"
            shutil.copytree(SPP1_PROJECT, target)

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
