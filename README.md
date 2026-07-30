# PaperRoute

PaperRoute is a direction-first, auditable workflow for turning an anchor paper
into an executable study.

It is designed for literature reproduction, independent reconstruction, and
research adaptation where scientific direction, data selection, method choice,
code implementation, and human review must remain traceable.

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

This repository is an alpha scaffold. Version `0.1.0-alpha` focuses on:

1. the direction-audit gate;
2. machine-readable project entities;
3. explicit human review;
4. result-to-change feedback;
5. dependency impact analysis;
6. a small SPP1+TAM pilot instance.

It does not yet orchestrate large sequencing analyses.

## Quick start

Requires Python 3.10 or later and has no runtime dependencies outside the
standard library.

```bash
python -m pip install -e .

paperroute validate examples/spp1-tam-jitc
paperroute status examples/spp1-tam-jitc
paperroute impact examples/spp1-tam-jitc DIR-001
```

Create a new draft project:

```bash
paperroute init ../my-paper-project \
  --project-id PRJ-MY-PAPER \
  --title "My paper adaptation"
```

The generated draft contains a project manifest, registry headers, and folders
for reviews, runs, reports, configuration, code, tests, and outputs.

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

- [Concepts](docs/concepts.md)
- [Workflow and gates](docs/workflow.md)
- [Feedback and review](docs/feedback-loop.md)
- [Roadmap](ROADMAP.md)

## License

A license has not yet been selected. Until one is added, do not assume
permission to redistribute or reuse the code.
