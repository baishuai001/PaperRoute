# Changelog

All notable changes to PaperRoute will be documented in this file.

## [Unreleased]

### Added

- A binding G0 scientific decision standard defining scientific validity,
  feasibility, novelty, scientific value, scoped flaws, adaptation, and
  post-approval rerouting.
- Multi-axis direction change maps. Candidates may retain, repair, replace,
  extend, or drop one or more scientific components without treating change
  count as a novelty metric.
- Independent candidate assessments for validity, feasibility, novelty, value,
  implementation burden, learning value, and anchor reuse.
- Project-specific briefs and anchor-flaw registries, plus semantic validation
  that prevents challenged routes from remaining primary recommendations.
- Scientific regression coverage for coherent multi-axis adaptation, missing
  change maps, repair-to-flaw linkage, and challenged recommendation handling.

### Changed

- Removed the mutually exclusive ambition-tier model and singular
  `primary_change_axis` from schema v0.2.0.
- Marked the previous SPP1 and NRRS primary recommendations as challenged and
  reopened both G0 decisions under the corrected model.

### Added in the earlier PR draft

- A second isolated WORK-001 / G0 evaluation workspace for the 2025 BMC
  Cancer gastric nerve-related prognostic model, including anchor fitness,
  construct validity, cohort independence, data/code availability, candidate
  directions, rejected routes, and a workflow-versus-anchor diagnosis.
- G0 hard checks for anchor fitness, construct validity, evidence independence,
  manuscript kernels, and beginner execution burden.
- A documented `workspaces/` boundary so additional test papers cannot mix
  registries, paths, or decisions with the reusable PaperRoute framework.
- A dated, evidence-backed WORK-001 / G0 audit packet for the SPP1+TAM pilot,
  including anchor grammar, data and code evidence, fatal-veto criteria,
  candidate directions, claim ceilings, and explicit stopping conditions.
- Proposed primary, backup, conditional, and training-only directions without
  auto-approving the human G0 decision.

## [0.1.0-alpha.1] - 2026-08-01

### Added

- Binding project discipline centered on producing a scientifically defensible
  manuscript.
- Machine-readable publication goal, scope policy, and manuscript-linked work
  items.
- Pull request checks for manuscript value and stopping conditions.
- Calibrated direction tiers that separate learning value, novelty floor, and
  realistic ambition ceiling from anchor-paper prestige.
- Direction-first project model.
- Machine-readable entity contract.
- Project initialization, validation, status, and impact commands.
- Result-driven change request rule.
- Human review and gate-reopening model.
- Illustrative SPP1+TAM pilot instance.
