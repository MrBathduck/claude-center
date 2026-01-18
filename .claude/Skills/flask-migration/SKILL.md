---
name: flask-migration
description: Automates Flask-Alembic migration workflow with safety checks
tags: [flask, database, migration, alembic]
---

# Flask Migration Workflow

When user modifies SQLAlchemy models, automatically guide through safe migration workflow.

## Standard Flow

1. Generate migration: `flask db migrate -m "Description"`
2. Review generated file in `migrations/versions/`
   - Check auto-detected changes are correct
   - Verify no missing nullable=False on existing tables (requires default)
   - Ensure indexes created for foreign keys
   - Confirm both upgrade() and downgrade() present
3. Apply migration: `flask db upgrade`
4. Verify schema: `psql -U postgres -d guberna_dev -c "\d [table_name]"`

## Safety Checks

**Block if detected:**
- Adding NOT NULL column without default to existing table
- Dropping columns with data (suggest soft delete: `deleted_at`)
- Missing foreign key indexes (performance issue)
- No downgrade() logic (irreversible migration)

**Warn if detected:**
- Modifying applied migration (create new one instead)
- Large data migrations (suggest chunking)

## Auto-Activation

Triggers when:
- User edits files in `app/models/`
- User mentions "migration", "alembic", "schema change"
- User runs `flask db` commands

## Sub-Files (Load When Needed)

**Read `rollback_guide.md` when:**
- Migration failed and needs rollback
- User asks about downgrade procedures
- Need recovery steps after failed migration
- Planning migration with risky changes

## Scripts

- `check_migration.py` - Validates migration file safety
  ```bash
  python .claude/skills/flask-migration/check_migration.py migrations/versions/xxxxx.py
  ```
