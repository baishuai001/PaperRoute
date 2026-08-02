# Concepts

## Three levels

### Workflow template

The reusable process, entity contract, validation rules, and review gates.

### Workflow instance

One paper-specific project with an anchor paper, direction candidates, claims,
resources, decisions, modules, reviews, and results.

### Workflow run

One immutable execution snapshot identified by code, configuration, data
manifest, environment, timestamps, and output artifacts.

## Source of truth

PaperRoute separates machine-readable state from generated prose:

1. `PROJECT_DISCIPLINE.md` defines the binding purpose and scope rules.
2. `PROJECT.json` stores project identity, publication goal, and current gate.
3. `registry/*.tsv` stores entities, references, and statuses.
4. work items connect activity to manuscript output and a stop condition.
5. decisions and reviews store human judgment.
6. code reads approved configuration and registries.
7. runs record what actually executed.
8. Markdown reports are views generated from those sources.

A decision that exists only in chat is not a project decision. A threshold that
exists only inside a script is not an approved parameter. A figure without a
source table and run record is not a complete result.

## Core entities

- `Paper`: anchor or supporting literature.
- `Direction`: a versioned manuscript kernel: plain-language question,
  biological unit, decisive evidence, falsifier, anchor-role profile, target
  contribution, and claim ceiling.
- `DirectionChange`: one retain, repair, replace, extend, or drop action on a
  named scientific axis, with rationale, contribution role, evidence, donor
  plan, risk, and linked anchor flaw.
- `DirectionAssessment`: independent judgments of scientific validity,
  feasibility, novelty, scientific value, implementation burden, learning
  value, and anchor reuse. These judgments are not collapsed into one score.
- `AnchorFlaw`: a scoped correctness, reproducibility, evidence, feasibility,
  reporting, or limitation finding with an explicit required response.
- `Claim`: a testable scientific statement and its claim ceiling.
- `Resource`: dataset, method, code, document, or environment.
- `WorkItem`: manuscript-linked work with a minimum deliverable and stop rule.
- `Module`: an analysis specification linked to one claim.
- `Decision`: a proposed or accepted scientific or technical judgment.
- `Review`: human approval, rejection, requested change, or reopening.
- `Run`: a concrete execution.
- `Result`: an output with evidential level and directional implication.
- `ChangeRequest`: a proposed adjustment triggered by a result or new evidence.
- `Dependency`: an edge used for traceability and downstream impact analysis.

## Lifecycle and validity

Lifecycle describes where an entity is in the workflow. Validity describes
whether it can still support downstream work.

For example, a module may remain `implemented` but become `stale` when its
upstream direction, dataset, method, or claim changes. It must be rerun before
its outputs can return to `current`.
