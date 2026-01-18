# <ENTITY_NAME> Entity

> <One-line description of what this entity represents>

---

## Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | uuid | PK | Unique identifier |
| <field_name> | <type> | <constraints> | <description> |
| <field_name> | <type> | <constraints> | <description> |
| created_at | timestamp | not null | Record creation time |
| updated_at | timestamp | not null | Last modification time |

---

## Relationships

| Type | Target | Foreign Key | Notes |
|------|--------|-------------|-------|
| has_many | <Entity> | - | <description> |
| belongs_to | <Entity> | <entity>_id | <description> |
| has_one | <Entity> | - | <description> |
| has_many_through | <Entity> | via <Junction> | <description> |

---

## Used By

<!-- Features that depend on this entity. Update when Canons reference this entity. -->

- [F<XXX>-<feature>](../../features/F<XXX>-<feature>.md)
- [F<XXX>-<feature>](../../features/F<XXX>-<feature>.md)

---

## Indexes

| Name | Fields | Type | Purpose |
|------|--------|------|---------|
| <index_name> | <field(s)> | unique / btree / etc. | <why needed> |

---

## Validation Rules

<!-- Business rules enforced on this entity -->

1. <RULE_1>
2. <RULE_2>

---

## State Transitions

<!-- If entity has status/state field -->

```
<state_1> --> <state_2> --> <state_3>
                 |
                 v
            <state_4>
```

| From | To | Trigger | Side Effects |
|------|-----|---------|--------------|
| <state_1> | <state_2> | <action> | <effects> |

---

## Example

```json
{
  "id": "uuid-here",
  "<field>": "<value>",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

---

## History

| Date | Change | Migration |
|------|--------|-----------|
| <YYYY-MM-DD> | Created | - |

---

<!--
USAGE NOTES:
1. Copy to <entity>.md (lowercase, singular: user.md, event.md)
2. Add to SCHEMA_INDEX.md
3. Update relationships.md
4. Link from Feature Canons in their Data Model section

IMPORTANT: KEEP "USED BY" SECTION UPDATED
- When a Feature Canon references this entity, add it to the "Used By" list
- This enables impact analysis when the entity changes
- Feature Canons link TO this entity (Data Model section)
- This entity links BACK to Canons (Used By section)

FROM WORKFLOW-V2:
- Entity docs are first-class citizens
- Feature Canons LINK to entities, they don't describe them
- When entity changes:
  1. Update this doc
  2. Check "Used By" list
  3. Review each dependent Canon
  4. Update Feature Map if relationships changed
- Updated by: System Archivist when schema changes

CROSS-REFERENCES:
- Used By: Links to /docs/features/F<XXX>-<feature>.md
- Relationships: Links to other entities in /docs/data/entities/
- After changes: Update SCHEMA_INDEX.md, relationships.md, and Feature Map

EXAMPLE FROM WORKFLOW-V2:
In Canon Data Model section:
- Primary: [User](/docs/data/entities/user.md)
- Related: [Event](/docs/data/entities/event.md) (via attendance)

SOURCE OF TRUTH: /docs/WORKFLOW-V2.md
-->
