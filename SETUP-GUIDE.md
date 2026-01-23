# Claude Code Setup Guide

A beginner-friendly guide to setting up Claude Code in your project.

---

## What is This?

This is a **template folder** containing everything you need to use Claude Code effectively in any project. It includes:

- **Agents** - Specialized AI assistants for different tasks (developer, debugger, architect, etc.)
- **Commands** - Shortcuts like `/commit`, `/debug`, `/plan-phase`
- **Skills** - Auto-activated expertise (migration help, test coverage, error validation)
- **Hooks** - Automatic checks that run when you edit files
- **Workflow** - A structured way to plan and build features

---

## Quick Start (5 minutes)

### Step 1: Copy the `.claude` folder

Copy the entire `.claude` folder to your project root:

```
your-project/
├── .claude/           <-- Copy this folder here
│   ├── agents/
│   ├── commands/
│   ├── hooks/
│   ├── skills/
│   └── settings.json
├── src/
├── package.json
└── ...
```

### Step 2: Copy the `docs` folder

Copy the `docs` folder to your project root:

```
your-project/
├── .claude/
├── docs/              <-- Copy this folder here
│   ├── WORKFLOW-V2.md
│   ├── features/
│   ├── data/
│   ├── dev/
│   ├── phases/
│   └── reviews/
├── src/
└── ...
```

### Step 3: Copy `CLAUDE.md`

Copy `CLAUDE.md` to your project root and customize it for your project:

```
your-project/
├── .claude/
├── docs/
├── CLAUDE.md          <-- Copy and customize this
├── src/
└── ...
```

### Step 4: Done!

Start Claude Code in your project folder. The agents, commands, and skills are now available.

---

## Folder Structure Explained

### `.claude/` - Claude Code Configuration

```
.claude/
├── agents/            # Specialized AI assistants
│   ├── developer.md   # Writes code
│   ├── debugger.md    # Investigates bugs
│   ├── architect.md   # Designs solutions
│   └── ...
│
├── commands/          # Slash commands you can use
│   ├── commit.md      # /commit - Smart git commits
│   ├── debug.md       # /debug - Bug investigation
│   ├── plan-phase.md  # /plan-phase - Feature planning
│   └── ...
│
├── hooks/             # Automatic checks (run on file edits)
│   ├── pre_edit_guard.py
│   ├── post_edit_lint.py
│   └── ...
│
├── skills/            # Auto-activated expertise
│   ├── flask-migration/
│   ├── test-coverage-enforcer/
│   └── ...
│
└── settings.json      # Hook configuration
```

### `docs/` - Project Documentation

```
docs/
├── WORKFLOW-V2.md     # How to use the workflow (READ THIS!)
│
├── features/          # Document your features here
│   ├── FEATURE_INDEX.md
│   ├── FEATURE_MAP.md
│   └── _TEMPLATE-feature.md
│
├── data/              # Document your data models here
│   ├── SCHEMA_INDEX.md
│   ├── entities/
│   └── relationships.md
│
├── dev/               # Development documentation
│   ├── LESSONS-LEARNED.md  # Patterns to follow/avoid
│   ├── decisions/     # Architecture Decision Records (ADRs)
│   ├── system/        # System documentation
│   └── notes/         # Scratch notes
│
├── phases/            # Phase planning for large features
│   ├── PHASE_INDEX.md
│   └── _TEMPLATE-phase.md
│
└── reviews/           # Code review documents
```

---

## How to Use Commands

Commands are shortcuts that start with `/`. Type them in Claude Code:

| Command | What it does | When to use |
|---------|--------------|-------------|
| `/commit` | Creates a smart git commit | When you're ready to commit |
| `/debug <error>` | Investigates a bug | When something breaks |
| `/plan-phase <feature>` | Plans a new feature | Before building something big |
| `/plan-execution` | Executes a planned phase | After planning is approved |
| `/quick-fix <bug>` | Fixes small bugs (1-3 files) | For simple fixes |
| `/review-pr` | Reviews code before merge | Before merging a PR |
| `/migrate <description>` | Plans database changes | For schema changes |
| `/test-feature <feature>` | Tests a feature end-to-end | To verify features work |

### Example Usage

```
You: /debug TypeError: Cannot read property 'id' of undefined

Claude: [Starts systematic investigation...]
```

```
You: /plan-phase Add user authentication with OAuth

Claude: [Creates detailed implementation plan...]
```

---

## How Hooks Work

Hooks are **Python scripts** that Claude Code runs automatically at certain events.

**Important:** The hooks in this template are **starter templates**. You need to customize them for your project.

### Hook Events

| Hook | When it runs | What you can make it do |
|------|--------------|------------------------|
| `pre_edit_guard.py` | Before editing a file | Block edits to sensitive files |
| `post_edit_lint.py` | After editing a file | Run linters, check code quality |
| `check_patterns_hook.py` | After editing a file | Detect anti-patterns, enforce rules |
| `subagent_quality.py` | When an agent finishes | Validate agent output quality |
| `session_notes.py` | When session ends | Save session context for next time |

### Implementing Hooks

Each hook receives JSON input via stdin and should:
1. Read the input
2. Do your checks
3. Exit with code `0` (allow) or non-zero (block)

**Basic hook template:**
```python
#!/usr/bin/env python3
import sys
import json

def main():
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())

    # Get the file being edited (for Edit/Write hooks)
    file_path = input_data.get('tool_input', {}).get('file_path', '')

    # Your logic here
    if should_block(file_path):
        print(f"BLOCKED: Cannot edit {file_path}")
        sys.exit(1)  # Block the action

    sys.exit(0)  # Allow the action

if __name__ == "__main__":
    main()
```

### Hook Configuration

Hooks are configured in `.claude/settings.json`. The paths use **relative paths**:
```json
"command": "python \".claude/hooks/pre_edit_guard.py\""
```

**Do NOT use** `$CLAUDE_PROJECT_DIR` - it doesn't work on all systems.

---

## How Skills Work

Skills provide specialized knowledge. They're defined in `.claude/skills/`.

| Skill | Activates when... | What it helps with |
|-------|-------------------|-------------------|
| `flask-migration` | You mention "migration", "alembic", or edit models | Database schema changes |
| `test-coverage-enforcer` | You mention "coverage", "test", or run tests | Test coverage standards |
| `error-message-validator` | You write error handling code | User-friendly error messages |
| `pattern-enforcer` | You write code | Project patterns and anti-patterns |

### How to Activate Skills

Skills can be activated by:
1. **Mentioning keywords** in your message ("help me with this migration")
2. **Explicitly requesting** ("use the flask-migration skill")
3. **Being referenced by agents** (some agents auto-load specific skills)

---

## Customizing for Your Project

### 1. Edit `CLAUDE.md`

This is the main instruction file for Claude. Customize it with:
- Your project's purpose
- Tech stack (Flask, React, etc.)
- Coding conventions
- Important patterns to follow

### 2. Build & Validation Commands

The developer agent needs to know your project's commands for validation. Add these to your `CLAUDE.md` file:

#### Required Commands

```markdown
## Build Commands

- **lint_command:** `[your lint command]`
  - Examples: `ruff check .`, `eslint src/`, `go vet ./...`, `cargo clippy`

- **test_command:** `[your test command]`
  - Examples: `pytest`, `npm test`, `go test ./...`, `cargo test`
```

#### Optional Commands

```markdown
- **build_command:** `[your build command]` (if applicable)
  - Examples: `npm run build`, `make`, `cargo build`, `go build ./...`

- **typecheck_command:** `[your type check command]` (if applicable)
  - Examples: `mypy .`, `tsc --noEmit`, `pyright`

- **build_css_command:** `[your CSS build command]` (if applicable)
  - Examples: `npm run build:css`, `sass src:dist`
```

#### Example CLAUDE.md Section

```markdown
## Build Commands

- **lint_command:** `ruff check app/ --fix`
- **test_command:** `pytest tests/ -q`
- **build_command:** `npm run build`
- **typecheck_command:** `mypy app/`
```

#### Why This Matters

Without these commands defined:
- The developer agent will ask you every time it needs to validate code
- Validation may be skipped or done incorrectly
- Automated workflows (plan-execution) will be interrupted

Define these once in CLAUDE.md, and all agents will use them consistently.

### 3. Design System Configuration (Optional)

If your project has a frontend/UI, configure the design system so the UI/UX Designer agent can maintain consistency.

#### Step 1: Copy the Template

Copy `design_system.md` from this repository to your project root:

```bash
cp path/to/claude-center/design_system.md ./design_system.md
```

#### Step 2: Fill In Your Values

Edit `design_system.md` and replace the placeholder values with your project's actual:

1. **Colors** - Your brand colors and semantic colors (copy from your CSS variables)
2. **Typography** - Your font families, sizes, and weights
3. **Spacing** - Your spacing scale (if using Tailwind, match your config)
4. **Components** - List your existing reusable components and their locations
5. **Patterns** - Document your loading, error, and empty state patterns

#### Step 3: Keep It Updated

When you add new components or change design tokens:
- Update `design_system.md` to reflect the changes
- The UI/UX Designer agent will automatically use the updated information

#### What This Enables

With a configured design system, the UI/UX Designer agent will:
- Use your exact color tokens (no guessing hex values)
- Follow your spacing scale
- Reuse existing components instead of designing new ones
- Match your established patterns for loading/error/empty states
- Maintain consistency across all UI work

#### Minimal Configuration

If you don't want to fill in everything, at minimum provide:
- **Colors:** Your primary, secondary, and semantic colors
- **Components:** Location of your component library (e.g., `src/components/`)
- **Framework:** What UI framework you use (React, Vue, etc.)

### 4. API Configuration (Optional)

If your project has a REST API, configure these paths so the API Designer agent can maintain consistency.

#### Add to CLAUDE.md

```markdown
## API Configuration

- **api_docs_location:** `docs/api/` or `docs/API-DESIGN.md`
- **error_codes_location:** `src/constants/errors.ts` or `app/utils/error_codes.py`
- **routes_location:** `src/routes/api/` or `app/routes/api/`
- **models_location:** `src/models/` or `app/models/`

### API Response Format
All API responses follow this structure:
```json
{
  "success": true,
  "data": { ... },
  "meta": { "total": 100, "page": 1 }
}
```

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "ERR_VALIDATION",
    "message": "Human readable message",
    "details": { ... }
  }
}
```

### Authentication
- Public endpoints: No decorator
- Authenticated: `@login_required`
- Role-based: `@api_role_required(['admin', 'manager'])`
```

#### Why This Matters

Without API configuration, the API Designer agent will:
- Have to search for patterns (slower, may miss things)
- Ask you questions about response formats
- Not know your error code conventions

With configuration:
- Designs match your existing API patterns exactly
- New endpoints are consistent with existing ones
- Error codes follow your established conventions

#### Minimal Configuration

At minimum, specify:
- **Response format:** What structure your API responses use
- **Error codes location:** Where error codes are defined (if applicable)

### 6. Populate Documentation Templates

As you build features, fill in:
- `docs/features/FEATURE_INDEX.md` - List your features
- `docs/data/SCHEMA_INDEX.md` - Document your data models
- `docs/dev/decisions/` - Record important decisions

### 7. Implement Your Hooks

The hooks in `.claude/hooks/` are starter templates. Customize them for your project:

```python
# Example: Block edits to .env files
if '.env' in file_path:
    print("BLOCKED: Cannot edit .env files")
    sys.exit(1)
```

See the "How Hooks Work" section above for the full template.

### 8. Add Project-Specific Skills (Optional)

Create new skills in `.claude/skills/` for domain-specific knowledge.

---

## Workflow Overview

The workflow helps you build features systematically:

### Mode Selection

| Scope | Mode | Process |
|-------|------|---------|
| Small (< 1 day) | **Quick** | Code first, document if it sticks |
| Medium (1-5 days) | **Standard** | Document → Build → Review |
| Large (> 5 days) | **Full** | Document → Phase Plan → Build → Review |

### Done Levels

| Level | Meaning | When to use |
|-------|---------|-------------|
| **L1** | MVP - Code works | Quick experiments |
| **L2** | Stable - Reviewed and documented | Most features |
| **L3** | Production - Fully documented | Core features |

For full details, read `docs/WORKFLOW-V2.md`.

---

## Troubleshooting

### Hooks Not Running

1. Check that `.claude/settings.json` exists
2. Check hook paths use `.claude/hooks/...` (relative paths)
3. Check Python is installed: `python --version`

### Commands Not Found

1. Check that `.claude/commands/` folder exists
2. Check the command file exists (e.g., `commit.md`)

### Skills Not Activating

1. Check that `.claude/skills/` folder exists (lowercase!)
2. Try explicitly mentioning the skill in your message

### Claude Doesn't Know Project Rules

1. Check that `CLAUDE.md` exists in project root
2. Make sure it contains your project-specific instructions

---

## Requirements

- **Claude Code** installed and configured
- **Python 3.8+** (for hooks)
- **Git** (for commit command)

### Optional

- **ruff** for Python linting: `pip install ruff`
- **pre-commit** for git hooks: `pip install pre-commit`

---

## Getting Help

1. Read `docs/WORKFLOW-V2.md` for the full workflow
2. Read `docs/dev/LESSONS-LEARNED.md` for patterns to follow
3. Check agent files in `.claude/agents/` to understand what each does
4. Check command files in `.claude/commands/` for usage instructions

---

## Quick Reference Card

```
COMMANDS
--------
/commit              Smart git commit
/debug <error>       Investigate bug
/plan-phase <idea>   Plan a feature
/plan-execution      Execute the plan
/quick-fix <bug>     Fix small bug
/review-pr           Review before merge

AGENTS (used automatically)
---------------------------
developer            Writes code
debugger             Investigates bugs
architect            Designs solutions
quality-reviewer     Reviews code
test-writer          Writes tests

KEY FILES
---------
CLAUDE.md            Project instructions (customize this!)
docs/WORKFLOW-V2.md  How to use the workflow
docs/dev/LESSONS-LEARNED.md  Patterns to follow
```

---

**Happy coding!**
