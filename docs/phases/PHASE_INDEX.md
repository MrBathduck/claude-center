# Phase Index

> Master list of all phases. Phases group features by intent, not technology.
>
> **Source of truth:** [WORKFLOW-V2.md](../WORKFLOW-V2.md)

---

## When to Use Phases

Phases are for **Full mode** work (> 5 days). From [WORKFLOW-V2.md](../WORKFLOW-V2.md):

| Mode | Scope | Workflow |
|------|-------|----------|
| **Quick** | < 1 day | Code first, backfill Canon if it sticks |
| **Standard** | 1-5 days | Canon -> Build -> Review |
| **Full** | > 5 days | Canon -> Phase -> Deliverables -> Build -> Review |

**Skip phases** for Quick and Standard mode work. Create a phase when:
- Work spans > 5 days
- Multiple features need coordination
- You need deliverable tracking

---

## How to Use This Index

1. **New phase?** Copy [_TEMPLATE-phase.md](./_TEMPLATE-phase.md) to `P-<XX>-<phase-name>.md`
2. **Add entry here** with status `planning`
3. **Define 3-9 deliverables** in the phase doc
4. **Link features** from [FEATURE_INDEX.md](../features/FEATURE_INDEX.md) to this phase

---

## Status Legend

| Status | Meaning |
|--------|---------|
| `planning` | Defining scope and deliverables |
| `active` | Currently being built |
| `review` | All deliverables complete, final verification |
| `complete` | Shipped, all features at L2+ |
| `paused` | On hold |

---

## Phases

| ID | Name | Status | Features | Progress |
|----|------|--------|----------|----------|
| P-01 | [Example Phase](./P-01-example-phase.md) | planning | F001, F002 | 0/3 |
<!-- Add new phases above this line -->

---

## Current Focus

**Active Phase:** P-XX - <Phase Name>

**Next Up:** P-XX - <Phase Name>

---

## Phase Completion Requirements

From [WORKFLOW-V2.md](../WORKFLOW-V2.md):
- All deliverables at L2+
- Critical-path features at L3
- [Feature Map](../features/FEATURE_MAP.md) accurate

---

## Related Documents

- **[WORKFLOW-V2.md](../WORKFLOW-V2.md)** - Full workflow documentation, Stage 2 Phase Planning
- **[FEATURE_INDEX.md](../features/FEATURE_INDEX.md)** - Master feature list
- **[FEATURE_MAP.md](../features/FEATURE_MAP.md)** - Cross-feature dependencies

---

## Notes

- Phases use P-XX format (P-01, P-02, etc.)
- Each phase should have 3-9 deliverables
- Features can belong to only one phase
- Phase planning is Stage 2 in the WORKFLOW-V2 workflow
