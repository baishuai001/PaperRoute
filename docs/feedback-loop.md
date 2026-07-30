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
- `refine`: a bounded change may be needed.
- `reroute`: the active direction should be reconsidered.
- `stop`: continuing the current route is not justified.

The validator requires a change request for every `refine`, `reroute`, or
`stop` result.

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
