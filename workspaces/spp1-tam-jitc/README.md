# SPP1+TAM JITC pilot

This is a lightweight PaperRoute instance for:

> Targeting SPP1+TAMs associated with liver metastasis reverses
> immunosuppression and synergizes with immunotherapy in colorectal cancer.

The pilot is intentionally at `G0_DIRECTION`. The earlier recommendation of
`DIR-002` as primary and `DIR-003` as backup is now `challenged`: it relied on
the retired single-axis/ambition-tier model and has not been approved. The
instance does not contain
the source PDF, raw sequencing data, controlled data, or paper-specific
unpublished inputs.

Its purpose is to demonstrate:

- an anchor paper;
- a proposed direction;
- a proposed claim;
- candidate data, method, and code resources;
- a high-risk direction decision;
- a pending human review;
- manuscript-linked work items with explicit stopping conditions;
- dependencies used for impact analysis.

## G0 review packet

- [Anchor grammar and boundaries](reports/g0_anchor_grammar.md)
- [Evidence snapshot](reports/g0_evidence_snapshot.tsv)
- [Direction matrix](reports/g0_direction_matrix.tsv)
- [Human review packet](reports/g0_review_packet.md)
- [Current v0.2 candidate portfolio](reports/g0_candidate_portfolio.md)
- [Scoped anchor flaws](registry/anchor_flaws.tsv)
- [Multi-axis candidate change maps](registry/direction_changes.tsv)
- [Independent candidate assessments](registry/direction_assessments.tsv)

The old direction matrix and review packet are preserved as regression evidence,
not current recommendations. The current portfolio proposes `DIR-006` as primary,
`DIR-007` as backup, `DIR-008` as reserve, and rejects `DIR-009`; all remain
proposals until owner review. `WORK-001`, `DECISION-002`, and `REVIEW-001` remain
open. No G1 data acquisition or manuscript implementation is authorized.

Run:

```bash
paperroute validate workspaces/spp1-tam-jitc
paperroute status workspaces/spp1-tam-jitc
paperroute impact workspaces/spp1-tam-jitc DIR-001
```

The G0 scientific audit is evidence-backed but remains a proposal until human
review is completed.
