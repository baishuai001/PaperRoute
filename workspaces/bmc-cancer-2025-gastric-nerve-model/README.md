# BMC Cancer 2025 gastric nerve-model audit

This is an isolated PaperRoute evaluation workspace for:

> Development and validation of a novel nerve-related prognostic model for
> gastric cancer based on bulk and single-cell RNA sequencing data.

It is intentionally held at `G0_DIRECTION`. The source PDF and supplement were
reviewed locally but are not committed. The earlier `DIR-002` primary,
`DIR-003` backup, and `DIR-004` reserve recommendations are now `challenged`
because they were generated under the retired single-axis/ambition-tier model.
`DIR-005` remains training-only. No manuscript direction is approved.

The central G0 finding is that this anchor is useful mainly as a **repair and
construct-validation case**, not as a complete method or code template. The
published score is called nerve-related, but the available evidence also fits
endothelial, fibroblast, epithelial, purity, stage, and MSI composition. The
paper provides no exact code, reuses three screening cohorts as named
validation cohorts, omits a transportable cutoff and several preprocessing
details, and places its in-house single-cell data behind controlled access.

Review files:

- [Anchor fitness and research grammar](reports/g0_anchor_fitness.md)
- [Evidence and reproducibility audit](reports/g0_evidence_snapshot.tsv)
- [Dataset access and independence map](reports/g0_dataset_independence.tsv)
- [Candidate direction matrix](reports/g0_direction_matrix.tsv)
- [WORK-001 / G0 review packet](reports/g0_review_packet.md)
- [Workflow-versus-anchor diagnosis](reports/g0_diagnosis.md)
- [Scoped anchor flaws](registry/anchor_flaws.tsv)
- [Multi-axis candidate change maps](registry/direction_changes.tsv)
- [Independent candidate assessments](registry/direction_assessments.tsv)

The old G0 reports are preserved as regression evidence, not current
recommendations. A new candidate portfolio must compare repair, scientifically
justified single- or multi-axis adaptation, evidence extension, and donor
combinations before the owner selects a route.

Run:

```bash
paperroute validate workspaces/bmc-cancer-2025-gastric-nerve-model
paperroute status workspaces/bmc-cancer-2025-gastric-nerve-model
paperroute impact workspaces/bmc-cancer-2025-gastric-nerve-model DIR-001
```
