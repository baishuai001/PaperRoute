from __future__ import annotations

import csv
import json
from collections import defaultdict, deque
from dataclasses import dataclass, field
from importlib.resources import files
from pathlib import Path
from typing import Any


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_contract() -> dict[str, Any]:
    contract_path = files("paperroute").joinpath(
        "data", "registry-contract.json"
    )
    with contract_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        header = reader.fieldnames or []
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    return header, rows


def _allowed_values(spec: Any, contract: dict[str, Any]) -> set[str]:
    if spec == "@gates":
        return set(contract["gates"])
    return set(spec)


def _split_reference(value: str, multi: bool) -> list[str]:
    if not value:
        return []
    if not multi:
        return [value]
    return [item.strip() for item in value.split(";") if item.strip()]


def load_project(project_dir: Path) -> dict[str, Any]:
    manifest_path = project_dir / "PROJECT.json"
    with manifest_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_registries(
    project_dir: Path, contract: dict[str, Any]
) -> tuple[dict[str, list[dict[str, str]]], ValidationReport]:
    report = ValidationReport()
    registries: dict[str, list[dict[str, str]]] = {}
    registry_dir = project_dir / "registry"

    for name, spec in contract["registries"].items():
        path = registry_dir / spec["file"]
        if not path.exists():
            report.errors.append(f"missing registry: {path}")
            registries[name] = []
            continue

        header, rows = read_tsv(path)
        missing = [
            column
            for column in spec["required_columns"]
            if column not in header
        ]
        if missing:
            report.errors.append(
                f"{spec['file']}: missing columns {', '.join(missing)}"
            )

        for row_number, row in enumerate(rows, start=2):
            for field_name, enum_spec in spec.get("enums", {}).items():
                value = row.get(field_name, "")
                allowed = _allowed_values(enum_spec, contract)
                if value not in allowed:
                    report.errors.append(
                        f"{spec['file']}:{row_number}: invalid "
                        f"{field_name}={value!r}; expected one of "
                        f"{sorted(allowed)}"
                    )
        registries[name] = rows

    return registries, report


def validate_project(project_dir: Path) -> ValidationReport:
    project_dir = Path(project_dir)
    report = ValidationReport()
    contract = load_contract()

    manifest_path = project_dir / "PROJECT.json"
    if not manifest_path.exists():
        report.errors.append(f"missing project manifest: {manifest_path}")
        return report

    try:
        manifest = load_project(project_dir)
    except (OSError, json.JSONDecodeError) as exc:
        report.errors.append(f"invalid PROJECT.json: {exc}")
        return report

    required_manifest = {
        "schema_version",
        "project_id",
        "title",
        "project_status",
        "current_gate",
        "anchor_paper_id",
        "active_direction_id",
        "feedback_policy",
    }
    missing_manifest = sorted(required_manifest - set(manifest))
    if missing_manifest:
        report.errors.append(
            "PROJECT.json: missing keys " + ", ".join(missing_manifest)
        )

    if manifest.get("schema_version") != contract["schema_version"]:
        report.warnings.append(
            "PROJECT.json schema_version does not match installed contract"
        )
    if manifest.get("project_status") not in contract["project_statuses"]:
        report.errors.append(
            f"PROJECT.json: invalid project_status "
            f"{manifest.get('project_status')!r}"
        )
    if manifest.get("current_gate") not in contract["gates"]:
        report.errors.append(
            f"PROJECT.json: invalid current_gate "
            f"{manifest.get('current_gate')!r}"
        )

    registries, registry_report = load_registries(project_dir, contract)
    report.errors.extend(registry_report.errors)
    report.warnings.extend(registry_report.warnings)

    ids_by_registry: dict[str, set[str]] = {}
    global_ids: dict[str, str] = {}

    for name, spec in contract["registries"].items():
        id_field = spec.get("id_field", "")
        ids: set[str] = set()
        if id_field:
            for row_number, row in enumerate(
                registries.get(name, []), start=2
            ):
                entity_id = row.get(id_field, "")
                if not entity_id:
                    report.errors.append(
                        f"{spec['file']}:{row_number}: empty {id_field}"
                    )
                    continue
                if entity_id in ids:
                    report.errors.append(
                        f"{spec['file']}:{row_number}: duplicate "
                        f"{entity_id}"
                    )
                if entity_id in global_ids:
                    report.errors.append(
                        f"{spec['file']}:{row_number}: ID {entity_id} "
                        f"already used in {global_ids[entity_id]}"
                    )
                ids.add(entity_id)
                global_ids[entity_id] = name
        ids_by_registry[name] = ids

    for name, spec in contract["registries"].items():
        for row_number, row in enumerate(registries.get(name, []), start=2):
            for reference in spec.get("references", []):
                field_name = reference["field"]
                values = _split_reference(
                    row.get(field_name, ""),
                    reference.get("multi", False),
                )
                if not values and not reference.get("optional", False):
                    report.errors.append(
                        f"{spec['file']}:{row_number}: empty required "
                        f"reference {field_name}"
                    )
                    continue
                for value in values:
                    target = reference["target"]
                    valid = (
                        value in global_ids
                        if target == "*"
                        else value in ids_by_registry.get(target, set())
                    )
                    if not valid:
                        report.errors.append(
                            f"{spec['file']}:{row_number}: unresolved "
                            f"{field_name}={value}"
                        )

    draft = manifest.get("project_status") == "draft"
    anchor_id = manifest.get("anchor_paper_id", "")
    direction_id = manifest.get("active_direction_id", "")
    if not draft:
        if anchor_id not in ids_by_registry.get("papers", set()):
            report.errors.append(
                f"PROJECT.json: unresolved anchor_paper_id={anchor_id!r}"
            )
        if direction_id not in ids_by_registry.get("directions", set()):
            report.errors.append(
                "PROJECT.json: unresolved "
                f"active_direction_id={direction_id!r}"
            )

    direction_rows = {
        row["direction_id"]: row
        for row in registries.get("directions", [])
        if row.get("direction_id")
    }
    if direction_id in direction_rows and direction_rows[direction_id].get(
        "status"
    ) in {"rejected", "superseded"}:
        report.errors.append(
            "PROJECT.json: active direction is rejected or superseded"
        )

    results_needing_change = {
        row["result_id"]
        for row in registries.get("results", [])
        if row.get("direction_effect") in {"refine", "reroute", "stop"}
    }
    linked_results = {
        row.get("source_result_id", "")
        for row in registries.get("change_requests", [])
    }
    for result_id in sorted(results_needing_change - linked_results):
        report.errors.append(
            f"result {result_id} has a directional effect but no "
            "change request"
        )

    reviews = registries.get("reviews", [])
    completed_approvals = {
        row["review_id"]
        for row in reviews
        if row.get("status") == "completed"
        and row.get("outcome") == "approve"
    }
    for row in registries.get("decisions", []):
        if (
            row.get("status") == "approved"
            and row.get("requires_review") == "true"
            and row.get("approved_review_id") not in completed_approvals
        ):
            report.errors.append(
                f"approved decision {row.get('decision_id')} lacks an "
                "approving completed review"
            )
    for row in registries.get("change_requests", []):
        if (
            row.get("status") in {"approved", "implemented", "closed"}
            and row.get("severity") in {"high", "critical"}
            and row.get("approved_review_id") not in completed_approvals
        ):
            report.errors.append(
                f"high-impact change {row.get('change_id')} lacks an "
                "approving completed review"
            )

    if manifest.get("project_status") == "direction_review" and direction_id:
        matching_reviews = [
            row
            for row in reviews
            if row.get("gate_id") == "G0_DIRECTION"
            and row.get("target_id") == direction_id
            and row.get("status") in {"pending", "completed"}
        ]
        if not matching_reviews:
            report.errors.append(
                "direction_review project lacks a G0 review for the "
                "active direction"
            )

    policy = manifest.get("feedback_policy", {})
    required_effects = set(
        policy.get(
            "effects_requiring_change_request",
            ["refine", "reroute", "stop"],
        )
    )
    if required_effects != {"refine", "reroute", "stop"}:
        report.warnings.append(
            "feedback policy differs from the v0.1 default"
        )

    return report


def init_project(target: Path, project_id: str, title: str) -> Path:
    target = Path(target)
    if target.exists() and any(target.iterdir()):
        raise ValueError(f"target directory is not empty: {target}")

    contract = load_contract()
    target.mkdir(parents=True, exist_ok=True)
    registry_dir = target / "registry"
    registry_dir.mkdir(exist_ok=True)
    for folder in (
        "config",
        "src",
        "tests",
        "runs",
        "outputs",
        "reports",
        "reviews",
    ):
        (target / folder).mkdir(exist_ok=True)

    manifest = {
        "schema_version": contract["schema_version"],
        "project_id": project_id,
        "title": title,
        "project_status": "draft",
        "current_gate": "G0_DIRECTION",
        "anchor_paper_id": "",
        "active_direction_id": "",
        "feedback_policy": {
            "effects_requiring_change_request": [
                "refine",
                "reroute",
                "stop",
            ],
            "invalidate_downstream_on_approved_change": True,
            "require_review_before_high_impact_change": True,
        },
    }
    (target / "PROJECT.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    for spec in contract["registries"].values():
        path = registry_dir / spec["file"]
        path.write_text(
            "\t".join(spec["required_columns"]) + "\n",
            encoding="utf-8",
        )

    return target


def downstream_impact(project_dir: Path, changed_id: str) -> list[dict[str, Any]]:
    contract = load_contract()
    registries, report = load_registries(Path(project_dir), contract)
    if report.errors:
        raise ValueError("; ".join(report.errors))

    adjacency: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for row in registries.get("dependencies", []):
        if row.get("active") == "true":
            adjacency[row["upstream_id"]].append(
                (row["downstream_id"], row["relation"])
            )

    queue: deque[tuple[str, int, str]] = deque()
    for downstream, relation in adjacency.get(changed_id, []):
        queue.append((downstream, 1, relation))

    seen = {changed_id}
    impacted: list[dict[str, Any]] = []
    while queue:
        entity_id, depth, relation = queue.popleft()
        if entity_id in seen:
            continue
        seen.add(entity_id)
        impacted.append(
            {
                "entity_id": entity_id,
                "depth": depth,
                "via_relation": relation,
            }
        )
        for downstream, child_relation in adjacency.get(entity_id, []):
            queue.append((downstream, depth + 1, child_relation))

    return impacted


def status_summary(project_dir: Path) -> dict[str, Any]:
    project_dir = Path(project_dir)
    manifest = load_project(project_dir)
    contract = load_contract()
    registries, registry_report = load_registries(project_dir, contract)
    validation = validate_project(project_dir)

    return {
        "project_id": manifest.get("project_id"),
        "title": manifest.get("title"),
        "project_status": manifest.get("project_status"),
        "current_gate": manifest.get("current_gate"),
        "active_direction_id": manifest.get("active_direction_id"),
        "entity_counts": {
            name: len(rows) for name, rows in registries.items()
        },
        "pending_reviews": [
            row.get("review_id")
            for row in registries.get("reviews", [])
            if row.get("status") == "pending"
        ],
        "pending_decisions": [
            row.get("decision_id")
            for row in registries.get("decisions", [])
            if row.get("status") == "proposed"
        ],
        "open_change_requests": [
            row.get("change_id")
            for row in registries.get("change_requests", [])
            if row.get("status") in {"proposed", "approved", "implemented"}
        ],
        "validation_errors": validation.errors,
        "validation_warnings": (
            registry_report.warnings + validation.warnings
        ),
    }
