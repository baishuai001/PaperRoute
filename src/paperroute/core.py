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
            for field_name in spec.get("nonempty_fields", []):
                if not row.get(field_name, ""):
                    report.errors.append(
                        f"{spec['file']}:{row_number}: empty required "
                        f"value {field_name}"
                    )
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
        "publication_goal",
        "project_brief",
        "scope_policy",
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

    publication_goal = manifest.get("publication_goal", {})
    required_goal_keys = {
        "primary_output",
        "audience",
        "approach",
        "quality_axes",
        "success_definition",
    }
    missing_goal_keys = sorted(
        required_goal_keys - set(publication_goal)
        if isinstance(publication_goal, dict)
        else required_goal_keys
    )
    if missing_goal_keys:
        report.errors.append(
            "PROJECT.json publication_goal: missing keys "
            + ", ".join(missing_goal_keys)
        )
    if isinstance(publication_goal, dict):
        for key in required_goal_keys - {"quality_axes"}:
            value = publication_goal.get(key)
            if not isinstance(value, str) or not value.strip():
                report.errors.append(
                    f"PROJECT.json publication_goal: {key} must be "
                    "a non-empty string"
                )
    required_quality_axes = {
        "feasibility",
        "scientific_validity",
        "novelty",
        "scientific_value",
        "logical_rigor",
        "implementation_burden",
        "learning_value",
        "anchor_reuse",
    }
    quality_axes = (
        set(publication_goal.get("quality_axes", []))
        if isinstance(publication_goal, dict)
        else set()
    )
    missing_quality_axes = sorted(required_quality_axes - quality_axes)
    if missing_quality_axes:
        report.errors.append(
            "PROJECT.json publication_goal: missing quality axes "
            + ", ".join(missing_quality_axes)
        )

    project_brief = manifest.get("project_brief", {})
    required_brief_keys = {
        "manuscript_goal",
        "anchor_use_intent",
        "allowed_change_axes",
        "preferred_contribution_types",
        "resource_constraints",
        "decision_policy",
    }
    missing_brief_keys = sorted(
        required_brief_keys - set(project_brief)
        if isinstance(project_brief, dict)
        else required_brief_keys
    )
    if missing_brief_keys:
        report.errors.append(
            "PROJECT.json project_brief: missing keys "
            + ", ".join(missing_brief_keys)
        )
    if isinstance(project_brief, dict):
        for key in {
            "manuscript_goal",
            "anchor_use_intent",
            "resource_constraints",
        }:
            value = project_brief.get(key)
            if not isinstance(value, str) or not value.strip():
                report.errors.append(
                    f"PROJECT.json project_brief: {key} must be "
                    "a non-empty string"
                )
        allowed_change_axes = project_brief.get("allowed_change_axes", [])
        if not isinstance(allowed_change_axes, list) or not allowed_change_axes:
            report.errors.append(
                "PROJECT.json project_brief: allowed_change_axes must be "
                "a non-empty list"
            )
        else:
            invalid_axes = sorted(
                set(allowed_change_axes) - set(contract["g0_change_axes"])
            )
            if invalid_axes:
                report.errors.append(
                    "PROJECT.json project_brief: invalid allowed_change_axes "
                    + ", ".join(invalid_axes)
                )
        contribution_types = project_brief.get(
            "preferred_contribution_types", []
        )
        if not isinstance(contribution_types, list) or not contribution_types:
            report.errors.append(
                "PROJECT.json project_brief: "
                "preferred_contribution_types must be a non-empty list"
            )

        decision_policy = project_brief.get("decision_policy", {})
        required_decision_rules = {
            "allow_multi_axis_change",
            "require_explicit_change_map",
            "require_independent_quality_assessments",
            "require_candidate_portfolio",
            "require_human_selection",
            "treat_repair_as_non_novel_by_default",
        }
        missing_decision_rules = sorted(
            required_decision_rules - set(decision_policy)
            if isinstance(decision_policy, dict)
            else required_decision_rules
        )
        if missing_decision_rules:
            report.errors.append(
                "PROJECT.json project_brief decision_policy: missing keys "
                + ", ".join(missing_decision_rules)
            )
        elif any(
            decision_policy.get(rule) is not True
            for rule in required_decision_rules
        ):
            report.errors.append(
                "PROJECT.json project_brief decision_policy: all binding "
                "rules must be true"
            )

    scope_policy = manifest.get("scope_policy", {})
    required_scope_keys = {
        "allowed_work_reasons",
        "optimization_stop_rule",
        "require_work_item_for_modules",
        "require_manuscript_implication_for_results",
    }
    missing_scope_keys = sorted(
        required_scope_keys - set(scope_policy)
        if isinstance(scope_policy, dict)
        else required_scope_keys
    )
    if missing_scope_keys:
        report.errors.append(
            "PROJECT.json scope_policy: missing keys "
            + ", ".join(missing_scope_keys)
        )
    if isinstance(scope_policy, dict):
        stop_rule = scope_policy.get("optimization_stop_rule")
        if not isinstance(stop_rule, str) or not stop_rule.strip():
            report.errors.append(
                "PROJECT.json scope_policy: optimization_stop_rule must "
                "be a non-empty string"
            )
        for key in {
            "require_work_item_for_modules",
            "require_manuscript_implication_for_results",
        }:
            if scope_policy.get(key) is not True:
                report.errors.append(
                    f"PROJECT.json scope_policy: {key} must be true"
                )
    default_work_reasons = set(
        contract["registries"]["work_items"]["enums"]["reason"]
    )
    configured_work_reasons = (
        set(scope_policy.get("allowed_work_reasons", []))
        if isinstance(scope_policy, dict)
        else set()
    )
    if configured_work_reasons != default_work_reasons:
        report.errors.append(
            "PROJECT.json scope_policy allowed_work_reasons must match "
            "the binding project discipline"
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

    allowed_anchor_roles = set(contract["anchor_roles"])
    configured_change_axes = set(
        project_brief.get("allowed_change_axes", [])
        if isinstance(project_brief, dict)
        else []
    )
    changes_by_direction: dict[str, list[dict[str, str]]] = defaultdict(list)
    for change in registries.get("direction_changes", []):
        changes_by_direction[change.get("direction_id", "")].append(change)
        if (
            change.get("action") in {"replace", "extend", "drop"}
            and change.get("axis") not in configured_change_axes
        ):
            report.errors.append(
                f"direction change {change.get('change_id')} changes "
                f"project-disallowed axis={change.get('axis')!r}"
            )
        if change.get("action") == "repair" and not change.get(
            "linked_flaw_ids"
        ):
            report.errors.append(
                f"direction change {change.get('change_id')} uses action=repair "
                "without a linked anchor flaw"
            )
        if (
            change.get("action") == "repair"
            and change.get("contribution_role") == "novelty"
        ):
            report.warnings.append(
                f"direction change {change.get('change_id')} treats repair "
                "as novelty; human review must verify a generalizable new "
                "contribution rather than correction alone"
            )

    assessments_by_direction: dict[str, list[dict[str, str]]] = defaultdict(
        list
    )
    for assessment in registries.get("direction_assessments", []):
        assessments_by_direction[assessment.get("direction_id", "")].append(
            assessment
        )

    fatal_flaw_ids = {
        flaw.get("flaw_id", "")
        for flaw in registries.get("anchor_flaws", [])
        if flaw.get("severity") == "fatal_if_unrepaired"
        and flaw.get("status") != "resolved"
    }

    for row in registries.get("directions", []):
        direction_name = row.get("direction_id", "(unknown)")
        anchor_roles = set(
            _split_reference(row.get("anchor_roles_used", ""), True)
        )
        invalid_roles = sorted(anchor_roles - allowed_anchor_roles)
        if invalid_roles:
            report.errors.append(
                f"direction {direction_name} has invalid anchor roles: "
                + ", ".join(invalid_roles)
            )

        if row.get("direction_kind") == "umbrella":
            continue

        changes = changes_by_direction.get(direction_name, [])
        axis_counts: dict[str, int] = defaultdict(int)
        for change in changes:
            axis_counts[change.get("axis", "")] += 1
        missing_axes = sorted(
            set(contract["g0_core_axes"]) - set(axis_counts)
        )
        duplicate_axes = sorted(
            axis for axis, count in axis_counts.items() if count > 1
        )
        if missing_axes:
            report.errors.append(
                f"direction {direction_name} lacks core change-map axes: "
                + ", ".join(missing_axes)
            )
        if duplicate_axes:
            report.errors.append(
                f"direction {direction_name} repeats change-map axes: "
                + ", ".join(duplicate_axes)
            )
        linked_flaws = {
            flaw_id
            for change in changes
            for flaw_id in _split_reference(
                change.get("linked_flaw_ids", ""), True
            )
        }
        unaddressed_fatal_flaws = sorted(fatal_flaw_ids - linked_flaws)
        if unaddressed_fatal_flaws:
            report.errors.append(
                f"direction {direction_name} does not explicitly respond to "
                "fatal anchor flaws: " + ", ".join(unaddressed_fatal_flaws)
            )

        assessments = assessments_by_direction.get(direction_name, [])
        if len(assessments) != 1:
            report.errors.append(
                f"direction {direction_name} requires exactly one independent "
                f"assessment row; found {len(assessments)}"
            )
            continue
        assessment = assessments[0]
        recommendation = assessment.get("recommendation")
        assessment_status = assessment.get("status")

        if (
            row.get("direction_kind") == "training_only"
            and recommendation != "training_only"
        ):
            report.errors.append(
                f"training-only direction {direction_name} must use "
                "recommendation=training_only"
            )
        if row.get("status") == "challenged" and recommendation in {
            "primary",
            "backup",
        }:
            report.errors.append(
                f"challenged direction {direction_name} cannot remain a "
                f"{recommendation} recommendation"
            )
        if row.get("status") in {"approved", "active"}:
            if assessment_status != "approved":
                report.errors.append(
                    f"approved direction {direction_name} lacks an approved "
                    "independent assessment"
                )
            if row.get("direction_kind") == "manuscript_candidate":
                failed_dimensions = [
                    field_name
                    for field_name in {
                        "scientific_validity",
                        "feasibility",
                        "novelty",
                        "scientific_value",
                    }
                    if assessment.get(field_name) != "pass"
                ]
                if failed_dimensions:
                    report.errors.append(
                        f"approved manuscript direction {direction_name} does "
                        "not pass: " + ", ".join(sorted(failed_dimensions))
                    )

    if (
        manifest.get("project_status") == "direction_review"
        and isinstance(project_brief, dict)
        and project_brief.get("decision_policy", {}).get(
            "require_candidate_portfolio"
        )
    ):
        manuscript_candidates = [
            row
            for row in registries.get("directions", [])
            if row.get("direction_kind") == "manuscript_candidate"
            and row.get("status") not in {"superseded", "rejected"}
        ]
        if len(manuscript_candidates) < 2:
            report.errors.append(
                "direction-review project requires at least two live "
                "manuscript candidates so trade-offs remain reviewable"
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
            "feedback policy differs from the v0.2 default"
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
        "publication_goal": {
            "primary_output": "A scientifically defensible manuscript",
            "audience": "Beginner-led project with AI assistance",
            "approach": (
                "Audited imitation and justified adaptation, not copying"
            ),
            "quality_axes": [
                "feasibility",
                "scientific_validity",
                "novelty",
                "scientific_value",
                "logical_rigor",
                "implementation_burden",
                "learning_value",
                "anchor_reuse",
            ],
            "success_definition": (
                "An evidence-linked manuscript draft with reproducible "
                "source tables, figures, methods, and explicit limitations"
            ),
        },
        "project_brief": {
            "manuscript_goal": (
                "Define the intended manuscript contribution before ranking "
                "candidate adaptations."
            ),
            "anchor_use_intent": (
                "Record whether the anchor supplies the question, design, "
                "data, method, code, evidence chain, narrative, or a negative "
                "example."
            ),
            "allowed_change_axes": list(contract["g0_change_axes"]),
            "preferred_contribution_types": [
                "biological",
                "clinical",
                "methodological",
                "resource",
                "validation",
            ],
            "resource_constraints": (
                "Replace this draft text with confirmed data, code, compute, "
                "time, skill, access, and experimental constraints."
            ),
            "decision_policy": {
                "allow_multi_axis_change": True,
                "require_explicit_change_map": True,
                "require_independent_quality_assessments": True,
                "require_candidate_portfolio": True,
                "require_human_selection": True,
                "treat_repair_as_non_novel_by_default": True,
            },
        },
        "scope_policy": {
            "allowed_work_reasons": [
                "manuscript_claim",
                "evidence_gap",
                "correctness_risk",
                "reproducibility_requirement",
                "review_requirement",
            ],
            "optimization_stop_rule": (
                "Stop when the minimum implementation needed for manuscript "
                "validity, reproducibility, and reviewability is complete"
            ),
            "require_work_item_for_modules": True,
            "require_manuscript_implication_for_results": True,
        },
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
        "primary_output": manifest.get("publication_goal", {}).get(
            "primary_output"
        ),
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
        "open_work_items": [
            row.get("work_id")
            for row in registries.get("work_items", [])
            if row.get("status")
            in {"proposed", "approved", "in_progress", "blocked"}
        ],
        "validation_errors": validation.errors,
        "validation_warnings": (
            registry_report.warnings + validation.warnings
        ),
    }
