# Workflow and gates

PaperRoute uses a two-pass audit. The first pass gathers enough evidence to
choose a direction without downloading every large dataset. The second pass
performs deep data, method, code, and implementation audit after the direction
is approved.

At every gate, proposed work must pass the manuscript-relevance test:

1. Which manuscript claim, section, figure, evidence gap, or review does it
   serve?
2. What is the minimum sufficient output?
3. What is the stopping condition?
4. Would not doing it materially weaken scientific validity or reproducibility?

## G0 - Direction

- Extract the anchor paper's research grammar.
- Separate anchor-paper prestige, learning value, and target-manuscript
  ambition; one does not automatically determine the others.
- Define invariants and candidate substitution or extension axes.
- Audit nearby literature, novelty, feasibility, fatal confounding, and claim
  ceiling.
- Give every candidate a learning objective, target contribution, novelty
  floor, ambition ceiling, and one of four ambition tiers.
- Apply fatal-veto criteria before comparative ranking so that novelty cannot
  compensate for unavailable core data, invalid design, or unsupported claims.
- Present at least one realistic bounded route before recommending a
  high-burden mechanistic route.
- Select a primary and backup direction through human review.

### G0 ambition tiers

- `training_reproduction`: reproduction or independent reconstruction for
  learning; normally preparatory rather than a new manuscript by itself.
- `bounded_adaptation`: one primary change axis plus necessary validation; the
  default candidate for a beginner-led manuscript.
- `evidence_extension`: additional cohorts, scales, endpoints, or robustness
  evidence with a higher integration burden.
- `mechanistic_extension`: new intervention, experimental, or causal evidence;
  eligible only after the required resources are confirmed.

The tiers describe evidence burden and project risk. They are not journal
promises and do not map mechanically to impact factors.

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
Reopening must also explain whether the change strengthens the manuscript,
changes its contribution, lowers its claim ceiling, or makes the route
unpublishable.
