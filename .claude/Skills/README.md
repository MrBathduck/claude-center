# Claude Code Skills

Skills are auto-activated expertise with optional executable scripts. Claude detects when to use them based on context.

## Structure

Skills use progressive disclosure pattern:
- `SKILL.md` - Core triggers, overview, when to load sub-files
- Sub-files (*.md) - Detailed content loaded only when needed
- Scripts (*.py) - Optional executable validation

```
.claude/skills/skill-name/
├── SKILL.md              # Required: core instructions
├── sub-topic.md          # Optional: detailed content
└── helper_script.py      # Optional: executable validation
```

---

## Installed Skills

### error-message-validator

**Purpose:** Validates error messages are user-friendly, specific, and actionable

**Auto-activates when:**
- Writing error handling code (`raise`, `throw`, `return error`)
- Creating form validation messages
- Defining API error responses
- Mentioning "error message", "validation"

**Files:**
| File | Content | Load When |
|------|---------|-----------|
| `SKILL.md` | Core principles, quality standards | Always |
| `patterns.md` | Red flags, good patterns, context-specific checks | Scanning code quality |
| `api_format.md` | JSON error format, form validation display | Writing API errors |
| `scan_errors.py` | Scans codebase for generic error messages | Manual scan |

**Quality standards:**
- Specific: "Email format invalid. Expected: user@example.com"
- Generic: "Invalid input"

---

### flask-migration

**Purpose:** Automates Flask-Alembic migration workflow with safety checks

**Auto-activates when:**
- Editing files in `app/models/`
- Mentioning "migration", "alembic", "schema change"
- Running `flask db` commands

**Files:**
| File | Content | Load When |
|------|---------|-----------|
| `SKILL.md` | Standard flow, safety checks | Always |
| `rollback_guide.md` | Downgrade procedures, recovery steps | Migration failed |
| `check_migration.py` | Validates migration file safety | Before applying |

**What it does:**
- Guides through migration workflow (generate -> review -> apply -> verify)
- Checks for NOT NULL without defaults
- Ensures downgrade() logic exists
- Validates foreign key indexes

---

### test-coverage-enforcer

**Purpose:** Enforces test coverage standards and identifies untested critical paths

**Auto-activates when:**
- Running test commands (`pytest`, `jest`)
- Writing new tests
- Adding new features
- Mentioning "coverage", "test", "untested"

**Files:**
| File | Content | Load When |
|------|---------|-----------|
| `SKILL.md` | Coverage standards, quality gates | Always |
| `pytest_guide.md` | Python/pytest commands, analysis | Running Python tests |
| `jest_guide.md` | JavaScript/Jest config | Testing JS code |
| `critical_paths.md` | What MUST be tested, priorities | Reviewing coverage gaps |
| `check_coverage.py` | Runs coverage and validates thresholds | Manual check |

**Coverage targets:**
- Models 90%+, Routes 80%+, Utils 100%

---

## Usage

**Manual activation:** Not needed - skills auto-activate when context matches

**Testing activation:** Mention skill triggers in conversation
- "Let me check the migration" -> flask-migration activates
- "This error message says 'Invalid'" -> error-message-validator activates
- "Run the tests" -> test-coverage-enforcer activates

**Running scripts manually:**
```bash
# Check migration safety
python .claude/skills/flask-migration/check_migration.py migrations/versions/xxxxx.py

# Scan for generic errors
python .claude/skills/error-message-validator/scan_errors.py app/

# Check test coverage
python .claude/skills/test-coverage-enforcer/check_coverage.py
```

---

## Adding New Skills

**Structure:**
```
.claude/skills/skill-name/
├── SKILL.md              # Required: triggers + overview
├── detailed_topic.md     # Optional: load when needed
└── helper_script.py      # Optional: executable
```

**SKILL.md template:**
```markdown
---
name: skill-name
description: Brief description
tags: [relevant, tags]
---

# Skill Name

What the skill does.

## Auto-Activation
Triggers when:
- [Context or keywords]

## Core Content
[Essential info always loaded]

## Sub-Files (Load When Needed)
**Read `topic.md` when:**
- [Specific scenarios]

## Scripts
- `script.py` - Description
```

**Progressive disclosure principle:**
- Keep SKILL.md lean (triggers + summary only)
- Extract detailed content to sub-files
- Reference sub-files with "when to load" guidance
- Claude loads sub-files only when context requires them

---

## Project-Specific Skills

These skills are configured for the GUBERNA project but work generically:
- Coverage targets: Check project docs for customization
- Error message standards: Adapt to project style guide
- Migration patterns: Works with any Flask-Alembic project

For other projects, review SKILL.md files and adjust thresholds/patterns as needed.
