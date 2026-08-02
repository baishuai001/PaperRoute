# Paper workspaces

Each immediate subdirectory is one self-contained PaperRoute instance. The
reusable PaperRoute workflow lives at the repository root; paper-specific
facts, directions, decisions, and review state live here.

Current workspaces:

| Workspace | Role | Gate | Purpose |
| --- | --- | --- | --- |
| `spp1-tam-jitc/` | regression pilot | G0 | Re-audit possible adaptations of the SPP1+TAM paper; prior primary recommendation is challenged. |
| `bmc-cancer-2025-gastric-nerve-model/` | regression case | G0 | Re-audit repair and adaptation routes for a prognostic-signature paper; prior primary recommendation is challenged. |

Rules:

1. A paper receives a new directory; never append it to another paper's
   registries or reports.
2. `project_id + entity_id` is the stable identity. `WORK-001` in two
   workspaces refers to two different work items.
3. Cross-paper comparisons belong in root documentation or a purpose-built
   comparison workspace and must cite both project IDs.
4. Source PDFs and supplements are not copied into Git unless redistribution
   is permitted. Record their checksums and local/external provenance instead.
5. Shared code graduates to `src/paperroute/` only when it is genuinely
   reusable and tested; paper-specific code remains inside its workspace.
