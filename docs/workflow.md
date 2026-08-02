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

G0 follows the binding [decision standard](g0-decision-standard.md):

1. **Project brief** — state the manuscript goal, intended anchor roles,
   permitted change axes, contribution preferences, resource constraints, and
   human decision policy.
2. **Anchor decomposition** — extract disease context, biological object,
   central relation, primary outcome, evidence architecture, data, methods,
   code, and claim level.
3. **Flaw triage** — distinguish claim-, module-, resource-, and route-level
   flaws from ordinary limitations and opportunities. A flaw does not
   automatically become the new manuscript question.
4. **Candidate portfolio** — generate scientifically coherent combinations of
   retain, repair, replace, extend, and drop actions. Multi-axis change is
   permitted; change count is not a novelty metric.
5. **Change maps** — give every non-umbrella candidate exactly one explicit
   decision for each core axis, plus rationale, contribution role, evidence,
   donor plan, linked flaw, and risk.
6. **Independent assessment** — audit scientific validity, feasibility,
   novelty, scientific value, implementation burden, learning value, and anchor
   reuse separately. Do not collapse them into an ambition tier or total score.
7. **Manuscript kernel** — state the plain-language question, biological unit,
   decisive evidence, falsifier, target contribution, and claim ceiling.
8. **Human selection** — present non-dominated trade-offs. AI recommendations
   remain proposed until the project owner approves one direction and records
   the rationale.

### Required G0 outputs

G0 is not complete until the review packet contains:

1. a project-specific brief rather than the generic goal of “a defensible
   manuscript”;
2. an anchor-role verdict separating question, design, data, method, code,
   evidence-chain, narrative, and negative-example reuse;
3. a flaw register with scope, severity, required response, and candidate
   implication;
4. a dataset access, overlap, independence, and minimum-field map;
5. a candidate portfolio with explicit rejected or challenged routes;
6. one core-axis change map and one independent assessment per candidate;
7. a manuscript kernel and minimum sufficient evidence for every live
   manuscript candidate;
8. a training-only route when useful, kept separate from manuscript candidates;
9. a diagnosis of whether weak recommendations arose from the workflow, the
   anchor paper, the available evidence, or their interaction.

G0 has no single ambition-tier enum. Evidence level, implementation burden,
learning value, anchor reuse, and scientific contribution are orthogonal and
may coexist in different combinations.

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
