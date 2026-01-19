# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **Claude Code configuration repository** containing custom commands, agents, skills, and workflow documentation for agentic software development. It's designed to be copied into other projects to provide a structured development workflow.

## Architecture Overview

### Directory Structure

```
.claude/
├── commands/           # Slash commands (/commit, /debug, /migrate, etc.)
├── agents/             # Specialized agents (developer, debugger, architect, etc.)
└── Skills/             # Auto-activated expertise (flask-migration, test-coverage-enforcer, etc.)
    └── <skill-name>/
        ├── SKILL.md    # Core triggers and overview (always loaded)
        ├── *.md        # Detailed content (loaded on demand)
        └── *.py        # Optional executable validation scripts

docs/
├── features/           # Feature Canon (truth about what the app does)
│   ├── FEATURE_INDEX.md
│   └── FEATURE_MAP.md  # Cross-feature visibility
├── data/               # Data model (first-class citizen)
│   ├── SCHEMA_INDEX.md
│   ├── entities/       # Individual entity docs
│   └── relationships.md
├── dev/
│   ├── system/         # Rarely updated, load-bearing docs
│   ├── decisions/      # ADRs (append-only, immutable)
│   └── notes/          # Allowed to rot, non-authoritative
└── phases/             # Phase planning docs
```

### Authority Hierarchy

```
System Docs & ADRs  → Constraints (what must hold)
Data Model          → Structure (what entities exist)
Feature Canon       → Truth (what the app does)
Phase Docs          → Intent (what we're building next)
```

### Key Workflow Concepts

**Mode Selection:**
- **Quick** (< 1 day): Code first, backfill Canon if it sticks
- **Standard** (1-5 days): Canon → Build → Review
- **Full** (> 5 days): Canon → Phase → Deliverables → Build → Review

**Done Levels:**
- **L1 (MVP):** Code works, basic Canon exists
- **L2 (Stable):** Quality reviewed, Canon accurate
- **L3 (Production):** System docs updated, Feature Map current

## Commands

| Command | Purpose |
|---------|---------|
| `/plan-phase <feature>` | Transform feature idea into structured phase doc |
| `/plan-execution <task>` | Execute a planned phase (3+ files) |
| `/quick-fix <bug>` | Small bugs, 1-3 files max |
| `/debug <error>` | Unclear errors, need investigation |
| `/review-pr [branch]` | Before merging code |
| `/migrate <description>` | Database schema changes (Flask-Alembic) |
| `/test-feature <feature>` | Verify feature works end-to-end |
| `/commit [message]` | Ready to commit changes |

## Skills (Auto-Activated)

Skills auto-activate based on context. They use progressive disclosure:

| Skill | Triggers On |
|-------|-------------|
| `error-message-validator` | Writing error handling code, form validation, API error responses |
| `flask-migration` | Editing `app/models/`, mentioning "migration", "alembic", "schema change" |
| `test-coverage-enforcer` | Running tests, writing tests, mentioning "coverage" |

**Running skill scripts manually:**
```bash
python .claude/Skills/flask-migration/check_migration.py migrations/versions/xxxxx.py
python .claude/Skills/error-message-validator/scan_errors.py app/
python .claude/Skills/test-coverage-enforcer/check_coverage.py
```

## Lessons Learned (Key Patterns to Follow)

Reference: `docs/dev/LESSONS-LEARNED.md`

**Critical patterns:**
- **L-CQ-001:** Search for existing implementations before writing ANY utility function
- **L-PF-001:** Use eager loading (`joinedload`/`selectinload`) for relationships in loops
- **L-SA-001:** Authorization checks belong in service layer, not routes
- **L-CQ-003:** No business logic in templates—use model properties
- **L-SV-006:** Services raise exceptions, routes catch and convert to responses

## Modifying This Repository

When adding new commands/agents/skills:
1. **Commands:** Create `<name>.md` in `.claude/commands/`
2. **Agents:** Create `<name>.md` in `.claude/agents/` and add to `.claude/README.md` table
3. **Skills:** Create folder in `.claude/Skills/<name>/` with `SKILL.md`, update `.claude/Skills/README.md`

When modifying workflow:
- Source of truth: `docs/WORKFLOW-V2.md`
- Update lessons in `docs/dev/LESSONS-LEARNED.md` after incidents
