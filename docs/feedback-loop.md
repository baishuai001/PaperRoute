# Result feedback and human review

PaperRoute assumes that results can change the plan.

```text
run
 -> result
 -> directional effect
 -> change request
 -> dependency impact
 -> human review
 -> new version or rejection
 -> stale downstream entities
 -> rerun
```

## Directional effects

- `none`: the result has no implication for project direction.
- `continue`: the result is compatible with the current route.
- `refine`: data, code, methods, parameters, evidence, or a bounded claim may
  change while the approved manuscript kernel remains the same.
- `reroute`: the central question, target effect, primary outcome, decisive
  evidence, or contribution type changes so that the approved evidence chain
  no longer answers the new manuscript kernel.
- `stop`: continuing the current route is not justified.

The validator requires a change request for every `refine`, `reroute`, or
`stop` result.

Alternative transformations compared before G0 approval are candidates, not
reroutes. Replacing one or multiple axes during candidate generation is allowed
when the change map and independent assessments are complete. The reroute rule
applies only after a direction has been approved or activated.

## Change requests

A change request records:

- the triggering result, if any;
- the manuscript-linked work item;
- change type and severity;
- affected entities;
- proposed action;
- expected manuscript implication;
- gate to reopen;
- review and implementation status.

High-impact changes to direction, claims, datasets, methods, or scope should not
be applied without a completed approving review.

## Impact analysis

Dependencies are directed from upstream to downstream. The command

```bash
paperroute impact PROJECT_DIR ENTITY_ID
```

lists all downstream entities that may become stale if `ENTITY_ID` changes.
Version `0.1` reports impact but does not automatically mutate project files.
This is deliberate: invalidation should be reviewed before it is applied.

## Adjustment without hindsight bias

Result-driven adaptation is permitted, but it must remain distinguishable from
the original plan:

1. preserve the original direction and analysis version;
2. record the observed result before changing the plan;
3. create a change request with rationale;
4. assess all affected claims and modules;
5. obtain review for high-impact changes;
6. create a new version;
7. label post-result analyses as exploratory unless independently validated.

This prevents a negative result from being silently converted into a different
positive hypothesis.

Feedback is not permission for unlimited optimization. A change request without
a manuscript-linked work item, an expected output, and a stopping condition is
out of scope.
