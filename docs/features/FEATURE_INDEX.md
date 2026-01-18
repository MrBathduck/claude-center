# Feature Index

> Master list of all features. Update when features are created or status changes.
>
> **Source of truth:** [WORKFLOW-V2.md](../WORKFLOW-V2.md)

---

## How to Use This Index

1. **New feature?** Copy [_TEMPLATE-feature.md](./_TEMPLATE-feature.md) to `F<XXX>-<feature-name>.md`
2. **Add entry here** with status `draft`
3. **Check [FEATURE_MAP.md](./FEATURE_MAP.md)** for shared state and dependencies
4. **Pick your mode** (from WORKFLOW-V2):
   - **Quick** (< 1 day): Code first, backfill Canon if it sticks
   - **Standard** (1-5 days): Canon -> Build -> Review
   - **Full** (> 5 days): Canon -> Phase -> Build -> Review

---

## Status Legend

| Status | Meaning | When to use |
|--------|---------|-------------|
| `draft` | Canon exists, not yet built | Planning stage |
| `in-progress` | Currently being implemented | Active development |
| `L1` | MVP - Code works, basic Canon exists | Quick mode, experiments |
| `L2` | Stable - Quality reviewed, Canon accurate | Standard mode, most features |
| `L3` | Production - System docs updated, Feature Map current | Full mode, core features |
| `deprecated` | No longer maintained | Feature retired |

**Note:** `draft` and `in-progress` are pre-completion states. L1/L2/L3 are Done Levels indicating feature maturity.

---

## Features

| ID | Name | Status | Phase | Last Updated |
|----|------|--------|-------|--------------|
| F001 | [Example Feature](./F001-example-feature.md) | draft | P-01 | YYYY-MM-DD |
<!-- Add new features above this line -->

---

## Quick Stats

- **Total Features:** 0
- **In Progress:** 0
- **At L2+:** 0
- **At L3:** 0

---

## Related Documents

- **[FEATURE_MAP.md](./FEATURE_MAP.md)** - Cross-feature relationships, shared state clusters, critical paths
- **[WORKFLOW-V2.md](../WORKFLOW-V2.md)** - Full workflow documentation, mode selection, Done Levels
- **[PHASE_INDEX.md](../phases/PHASE_INDEX.md)** - Phase planning (for Full mode)

---

## Notes

- Features use F-XXX format (F001, F002, etc.)
- Link to phase in Phase column when assigned
- Update status as features progress through Done Levels
- When in doubt about mode, start with Standard
