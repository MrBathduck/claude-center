# Claude Code Configuration

## Commands

| Command | Use When |
|---------|----------|
| `/plan-phase <feature>` | Transform feature idea into structured phase doc |
| `/plan-execution <task>` | Execute a planned phase (3+ files) |
| `/quick-fix <bug>` | Small bugs, 1-3 files max |
| `/debug <error>` | Unclear errors, need investigation |
| `/review-pr [branch]` | Before merging code |
| `/migrate <description>` | Database schema changes |
| `/test-feature <feature>` | Verify feature works end-to-end |
| `/commit [message]` | Ready to commit changes |

### Examples

```bash
# Planning (new features)
/plan-phase Add notification system for task assignments
/plan-phase Settings page improvements from Issues doc

# Bug fixes
/quick-fix Save button returns 500 error
/quick-fix Dropdown not showing options

# Debugging
/debug TypeError: 'NoneType' object has no attribute 'id'
/debug Certificate PDF not generating

# Code review
/review-pr
/review-pr feature/calendar-view
/review-pr #123

# Database migrations
/migrate Add priority field to Task
/migrate Remove deprecated column from Event

# Feature testing
/test-feature User registration flow
/test-feature Certificate generation for attended participants

# Commits
/commit
/commit Fix pagination bug in event list

# Feature development
/plan-execution Add export to PDF for reports
/plan-execution Implement notification system
```

## Agents

| Agent | Purpose |
|-------|---------|
| `developer` | Implements code with tests |
| `debugger` | Investigates errors |
| `quality-reviewer` | Reviews code (security, performance) |
| `ui-ux-designer` | Designs interfaces |
| `api-designer` | Designs REST endpoints |
| `migration-planner` | Plans safe DB changes |
| `test-writer` | Writes pytest tests |
| `qa-validator` | Browser/DB testing |
| `technical-writer` | Documentation |
| `architect` | System design, ADRs |

## Context Management

### SESSION_NOTES.md
Persistent memory file for cross-session continuity.

**Updated by:** `/plan-execution`, `/debug`

**Contains:**
- Completed milestones
- Decisions made
- Blockers encountered
- Handoff context for next session

### Compaction
Automatic context compression when:
- Context > ~65% full
- AND milestone just completed

Prevents mid-task context loss while managing long sessions.

## Decision Tree

```
What are you doing?
|
+-- Planning a feature?   --> /plan-phase (creates phase doc)
|
+-- Executing a plan?     --> /plan-execution (implements phase doc)
|
+-- Fixing a bug?
|   +-- Simple (1-3 files) --> /quick-fix
|   +-- Complex/unclear   --> /debug
|
+-- Changing database?    --> /migrate
|
+-- Testing something?    --> /test-feature
|
+-- Ready to commit?      --> /commit
|
+-- Merging code?         --> /review-pr
```
