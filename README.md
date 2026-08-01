# PaperRoute

PaperRoute is a direction-first, auditable workflow for turning an anchor paper
into an executable study.

Its primary output is a scientifically defensible manuscript produced by a
beginner-led project. The workflow is a means to that end, not an object of
unbounded optimization. See the binding
[Project Discipline](PROJECT_DISCIPLINE.md).

It is designed for literature reproduction, independent reconstruction, and
research adaptation where scientific direction, data selection, method choice,
code implementation, and human review must remain traceable.

PaperRoute treats anchor-paper prestige, learning value, and target-manuscript
ambition as separate judgments. Its default beginner route is bounded,
publishable adaptation: enough innovation to avoid relabelling, but no automatic
escalation to top-tier mechanistic claims without the required evidence.

PaperRoute is not a paper manager, a data warehouse, or a collection of
analysis notebooks. Its core is a versioned set of entities and dependencies:

```text
anchor paper
  -> direction candidates
  -> approved direction
  -> claims and evidence requirements
  -> resources and analysis modules
  -> runs and results
  -> result-driven change requests
  -> impact analysis and renewed review
```

## Why result feedback is first-class

An analysis result may support the current direction, require refinement,
contradict a claim, or make the project infeasible. PaperRoute therefore does
not treat the approved direction as permanently fixed.

Results carry a `direction_effect`:

- `none`: no directional implication;
- `continue`: continue the approved plan;
- `refine`: revise parameters, datasets, methods, or a bounded claim;
- `reroute`: reconsider the active research direction;
- `stop`: stop or block the current route.

Every `refine`, `reroute`, or `stop` result must be linked to a change request.
Before a change is accepted, PaperRoute reports which downstream entities would
become stale and which review gate must reopen.

## Current status

This repository is an alpha scaffold. Version `0.1.0-alpha.1` focuses on:

1. the direction-audit gate;
2. machine-readable project entities;
3. explicit human review;
4. result-to-change feedback;
5. dependency impact analysis;
6. isolated paper workspaces for pilot and evaluation cases.

It does not yet orchestrate large sequencing analyses.

## Quick start

Requires Python 3.10 or later and has no runtime dependencies outside the
standard library.

```bash
python -m pip install -e .

paperroute validate workspaces/spp1-tam-jitc
paperroute status workspaces/spp1-tam-jitc
paperroute impact workspaces/spp1-tam-jitc DIR-001
```

Create a new draft project:

```bash
paperroute init ../my-paper-project \
  --project-id PRJ-MY-PAPER \
  --title "My paper adaptation"
```

The generated draft contains a project manifest, registry headers, and folders
for reviews, runs, reports, configuration, code, tests, and outputs.

## Repository layers

PaperRoute and the papers audited with it may share one repository, but they
are different entities:

- the repository root, `src/paperroute/`, `docs/`, and `tests/` contain the
  reusable workflow;
- every directory under `workspaces/` is an isolated paper instance with its
  own `PROJECT.json`, registries, reports, decisions, and review state;
- identifiers such as `WORK-001` and `DIR-001` are scoped to one workspace and
  must never be joined across workspaces without the project ID;
- source PDFs, large data, credentials, and controlled human data remain
  outside Git and are referenced through provenance records only.

See [Workspace boundaries](workspaces/README.md) before adding another paper.

## Repository boundaries

Commit:

- code, schemas, configuration, registries, decisions, reviews, tests;
- data manifests and checksums;
- small source tables, reports, and run manifests.

Do not commit:

- credentials or tokens;
- controlled or patient-identifiable data;
- large FASTQ, H5AD, RDS, image, or cache files;
- copyrighted source PDFs unless redistribution is permitted.

Large data remain in external storage and are connected to a project through
manifests, checksums, access state, and provenance.

## Documentation

- [Project Discipline](PROJECT_DISCIPLINE.md)
- [Concepts](docs/concepts.md)
- [Workflow and gates](docs/workflow.md)
- [Feedback and review](docs/feedback-loop.md)
- [Roadmap](ROADMAP.md)

## License

A license has not yet been selected. Until one is added, do not assume
permission to redistribute or reuse the code.
