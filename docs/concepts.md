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

1. `PROJECT.json` stores project identity and current gate.
2. `registry/*.tsv` stores entities, references, and statuses.
3. decisions and reviews store human judgment.
4. code reads approved configuration and registries.
5. runs record what actually executed.
6. Markdown reports are views generated from those sources.

A decision that exists only in chat is not a project decision. A threshold that
exists only inside a script is not an approved parameter. A figure without a
source table and run record is not a complete result.

## Core entities

- `Paper`: anchor or supporting literature.
- `Direction`: a versioned retain/replace/extend research route.
- `Claim`: a testable scientific statement and its claim ceiling.
- `Resource`: dataset, method, code, document, or environment.
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
