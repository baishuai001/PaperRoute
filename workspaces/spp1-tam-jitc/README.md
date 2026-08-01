# SPP1+TAM JITC pilot

This is a lightweight PaperRoute instance for:

> Targeting SPP1+TAMs associated with liver metastasis reverses
> immunosuppression and synergizes with immunotherapy in colorectal cancer.

The pilot is intentionally at `G0_DIRECTION`. A dated G0 audit now proposes
`DIR-002` as the bounded primary route and `DIR-003` as the higher-burden
backup, but neither direction has been approved. The instance does not contain
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

The recommendation deliberately does not continue the saturated
`SPP1+TAM -> immunosuppression -> therapy` narrative. It asks which published
CRLM myeloid states survive patient-level, cross-cohort and spatial validation,
and where those states fail to transport. `WORK-001`, `DECISION-001` and
`REVIEW-001` remain open until the project owner accepts, changes, or rejects
the proposed primary and backup routes.

Run:

```bash
paperroute validate workspaces/spp1-tam-jitc
paperroute status workspaces/spp1-tam-jitc
paperroute impact workspaces/spp1-tam-jitc DIR-001
```

The G0 scientific audit is evidence-backed but remains a proposal until human
review is completed.
