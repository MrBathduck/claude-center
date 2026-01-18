# Schema Index

> Master index of all entities in the data model. Data model is a first-class citizen.
>
> **Source of truth:** [WORKFLOW-V2.md](../WORKFLOW-V2.md)

---

## How to Use This Index

1. **New entity?** Copy [_TEMPLATE-entity.md](./entities/_TEMPLATE-entity.md) to `entities/<entity>.md`
2. **Add entry here** in the Entities table
3. **Update [relationships.md](./relationships.md)** with new relationships
4. **Link from Feature Canons** in their Data Model section

**Remember:** Feature Canons LINK to entities, they don't describe them. Keep entity definitions here.

---

## Entities

| Entity | Description | Used By | Last Updated |
|--------|-------------|---------|--------------|
| [User](./entities/user.md) | <Description> | F001, F003 | YYYY-MM-DD |
<!-- Add new entities above this line -->

---

## Quick Reference

### Core Entities
<!-- Primary business objects -->
- **User** - <brief description>

### Supporting Entities
<!-- Secondary objects, junction tables, etc. -->

### System Entities
<!-- Audit logs, configs, etc. -->

---

## Entity Relationships

See [relationships.md](./relationships.md) for full relationship diagram.

**Quick overview:**
```
<Entity A> --has_many--> <Entity B>
<Entity B> --belongs_to--> <Entity A>
```

---

## Naming Conventions

- Entity files: lowercase, singular (user.md, event.md)
- Entity names in docs: PascalCase (User, Event)
- Database tables: lowercase, plural (users, events)
- Foreign keys: <entity>_id (user_id, event_id)

---

## Adding New Entities

1. Create entity doc from template: `entities/_TEMPLATE-entity.md`
2. Add to this index
3. Update [relationships.md](./relationships.md)
4. Link from relevant Feature Canons

---

## Related Documents

- **[relationships.md](./relationships.md)** - Full relationship diagram and cascade rules
- **[WORKFLOW-V2.md](../WORKFLOW-V2.md)** - Data model as first-class citizen, change propagation rules
- **[FEATURE_MAP.md](../features/FEATURE_MAP.md)** - Which features share entities

---

## Notes

- Entities are first-class citizens in this workflow
- Feature Canons LINK to entities, they don't describe them
- When entity changes, check "Used By" list and review dependent Canons
- System Archivist updates entity docs when schema changes

---

## Change Propagation (from WORKFLOW-V2)

When Entity changes:
1. Update entity doc in `/docs/data/entities/`
2. Check "Used By" list
3. Review each dependent Canon
4. Update Feature Map if relationships changed
