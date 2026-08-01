# BMC Cancer 2025 gastric nerve-model audit

This is an isolated PaperRoute evaluation workspace for:

> Development and validation of a novel nerve-related prognostic model for
> gastric cancer based on bulk and single-cell RNA sequencing data.

It is intentionally held at `G0_DIRECTION`. The source PDF and supplement were
reviewed locally but are not committed. `DIR-002` is proposed as the primary
bounded route, `DIR-003` as a conditional higher-burden backup, and `DIR-005`
as training-only reconstruction. None is approved until the owner reviews the
G0 packet.

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

Run:

```bash
paperroute validate workspaces/bmc-cancer-2025-gastric-nerve-model
paperroute status workspaces/bmc-cancer-2025-gastric-nerve-model
paperroute impact workspaces/bmc-cancer-2025-gastric-nerve-model DIR-001
```
