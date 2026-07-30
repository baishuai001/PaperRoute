# Workflow and gates

PaperRoute uses a two-pass audit. The first pass gathers enough evidence to
choose a direction without downloading every large dataset. The second pass
performs deep data, method, code, and implementation audit after the direction
is approved.

## G0 - Direction

- Extract the anchor paper's research grammar.
- Define invariants and candidate substitution or extension axes.
- Audit nearby literature, novelty, feasibility, fatal confounding, and claim
  ceiling.
- Select a primary and backup direction through human review.

## G1 - Evidence

- Inventory papers, datasets, files, methods, and code.
- Resolve identifiers, access conditions, patient overlap, and missing inputs.
- Classify evidence as exact, approximate, blocked, or invalid.

## G2 - Design

- Convert claims into analysis specifications.
- Define biological units, estimands, covariates, input contracts, outputs,
  controls, and validation.
- Separate discovery from validation.

## G3 - Implementation

- Build dataset adapters and common analysis modules.
- Pin configuration and environment.
- Add unit, smoke, integration, and scientific-invariant tests.

## G4 - Verification

- Execute approved modules.
- Verify data, computational, statistical, and scientific correctness.
- Register provisional and verified results.

## G5 - Claim audit

- Compare results with claims and claim ceilings.
- Record support, contradiction, uncertainty, and unresolved evidence.
- Trigger refinement, rerouting, or stopping where needed.

## G6 - Release

- Freeze an immutable run manifest.
- Generate source tables, figures, review packets, and a reproducibility report.
- Tag a reviewed release.

## Reopening

Approval is versioned, not permanent. New results or external evidence may
reopen an earlier gate. Reopening creates a new direction, claim, decision, or
method version; it does not silently overwrite the previously reviewed state.
