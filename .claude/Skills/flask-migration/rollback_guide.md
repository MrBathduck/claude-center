# Migration Rollback Guide

## Standard Downgrade

Rollback last migration:
```bash
flask db downgrade -1
```

Rollback to specific revision:
```bash
flask db downgrade <revision_id>
```

Rollback all migrations:
```bash
flask db downgrade base
```

## Recovery Steps After Failed Migration

### 1. Check Current State
```bash
flask db current
flask db history
```

### 2. If Partial Migration Applied

Check what was applied:
```sql
-- PostgreSQL
SELECT * FROM alembic_version;
\d [table_name]  -- Check table structure
```

Manual cleanup if needed:
```sql
-- Remove partial changes
DROP TABLE IF EXISTS [new_table];
ALTER TABLE [table] DROP COLUMN IF EXISTS [new_column];

-- Reset alembic version
UPDATE alembic_version SET version_num = '<previous_revision>';
```

### 3. Fix and Retry

1. Delete failed migration file
2. Fix model issues
3. Generate new migration: `flask db migrate -m "Description"`
4. Review and apply: `flask db upgrade`

## Common Rollback Scenarios

### Added Column That Shouldn't Exist
```bash
flask db downgrade -1
# Delete migration file
# Fix model
# Regenerate migration
```

### Data Migration Failed Mid-Way
```python
# In migration file, add chunking:
def upgrade():
    conn = op.get_bind()
    # Process in batches
    batch_size = 1000
    offset = 0
    while True:
        result = conn.execute(
            text(f"SELECT id FROM table LIMIT {batch_size} OFFSET {offset}")
        )
        rows = result.fetchall()
        if not rows:
            break
        # Process batch
        offset += batch_size
```

### Wrong Column Type
```bash
flask db downgrade -1
# Edit model with correct type
flask db migrate -m "Fix column type"
flask db upgrade
```

## Prevention Checklist

Before applying migrations:

1. **Backup database** (production)
   ```bash
   pg_dump -U postgres guberna_prod > backup_$(date +%Y%m%d).sql
   ```

2. **Test on dev first**
   ```bash
   flask db upgrade  # On dev database
   # Verify functionality
   ```

3. **Review migration file**
   - Check upgrade() logic
   - Verify downgrade() works
   - Run check_migration.py

4. **Plan rollback**
   - Know the previous revision ID
   - Have downgrade tested
   - Document data that might be lost

## Emergency Recovery

If database is in bad state:

1. **Restore from backup**
   ```bash
   psql -U postgres guberna_dev < backup.sql
   ```

2. **Stamp to known good revision**
   ```bash
   flask db stamp <known_good_revision>
   ```

3. **Regenerate migrations from models**
   ```bash
   # Delete all migration files after known good
   flask db migrate -m "Regenerated migrations"
   flask db upgrade
   ```

## Never Do in Production

- Modify already-applied migrations
- Run `flask db-reset`
- Drop tables with data without backup
- Apply untested migrations directly
