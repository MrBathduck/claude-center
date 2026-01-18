# Entity Relationships

> How entities connect to each other. Update when relationships change.
>
> **Source of truth:** [WORKFLOW-V2.md](../WORKFLOW-V2.md)
> **See also:** [SCHEMA_INDEX.md](./SCHEMA_INDEX.md) for the master entity list

---

## Relationship Diagram

```
┌─────────────┐
│   Entity A  │
└──────┬──────┘
       │ has_many
       ▼
┌─────────────┐         ┌─────────────┐
│   Entity B  │────────▶│   Entity C  │
└─────────────┘ belongs └─────────────┘
                  to
```

<!-- Replace with actual entity relationships -->

---

## Relationship Types

| Type | Meaning | Example |
|------|---------|---------|
| `has_one` | 1:1 relationship | User has_one Profile |
| `has_many` | 1:N relationship | User has_many Events |
| `belongs_to` | N:1 relationship | Event belongs_to User |
| `has_many_through` | M:N via junction | User has_many Events through Attendance |

---

## Detailed Relationships

### <Entity A> Relationships

| Relationship | Target | Via | Notes |
|--------------|--------|-----|-------|
| has_many | <Entity B> | - | <description> |
| has_one | <Entity C> | - | <description> |

### <Entity B> Relationships

| Relationship | Target | Via | Notes |
|--------------|--------|-----|-------|
| belongs_to | <Entity A> | - | <description> |

---

## Junction Tables

<!-- For many-to-many relationships -->

### <JunctionEntity>

- **Connects:** <Entity A> <-> <Entity B>
- **Purpose:** <Why this junction exists>
- **Additional fields:** <Fields beyond the two FKs>

---

## Cascade Rules

<!-- What happens when entities are deleted? -->

| When deleting... | Cascade to... | Action |
|------------------|---------------|--------|
| User | Events (owned) | Soft delete / Orphan / Cascade |
| Event | Attendances | Cascade delete |

---

## Integrity Constraints

<!-- Business rules enforced at data level -->

1. <CONSTRAINT_1>
2. <CONSTRAINT_2>

---

## Change Log

| Date | Change | Impact |
|------|--------|--------|
| <YYYY-MM-DD> | Initial relationships | - |

---

<!--
USAGE NOTES:
- Update when entity relationships change
- Check Feature Map for features affected by relationship changes
- System Archivist maintains this document

FROM WORKFLOW-V2:
When Entity changes:
1. Update entity doc in /docs/data/entities/
2. Check "Used By" list
3. Review each dependent Canon
4. Update Feature Map if relationships changed
-->
