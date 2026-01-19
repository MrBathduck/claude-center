# Claude Code Configuration Rework Plan

> Comprehensive analysis and recommendations for creating a reusable Claude Code setup for large-scale projects.

**Created:** 2026-01-19
**Updated:** 2026-01-19 (Clarified Senior Developer Review as agent step, simplified Gemini checkpoint)
**Source of Truth:** `docs/WORKFLOW-V2.md`

---

## Executive Summary

The current setup has solid foundations (commands, agents, skills) but underutilizes Claude Code's capabilities. Key gaps: **no hooks** (the most impactful missing feature), **skills not invoked automatically**, **agents lack proper frontmatter**, and **no plugins packaging** for reusability. This plan addresses these gaps while aligning with WORKFLOW-V2's philosophy: "Structure serves momentum, not bureaucracy."

---

## Section 1: Current State Analysis

### 1.1 What Exists Today

#### Commands (8 total) - `.claude/commands/`
| Command | Purpose | Quality |
|---------|---------|---------|
| `/commit` | Smart commit with pre-checks | Excellent - comprehensive |
| `/debug` | Evidence-based debugging | Excellent - structured protocol |
| `/plan-phase` | Feature planning | Good - needs WORKFLOW-V2 alignment |
| `/plan-execution` | Execute planned phases | Good - comprehensive delegation |
| `/quick-fix` | Small bug fixes | Assumed present |
| `/migrate` | Database migrations | Assumed present |
| `/test-feature` | Feature testing | Assumed present |
| `/review-pr` | PR code review | Assumed present |

**Assessment:** Commands are well-documented but verbose. Progressive disclosure pattern not applied - full content loads immediately.

#### Agents (14 total) - `.claude/agents/`
| Agent | Purpose | Issues |
|-------|---------|--------|
| `architect` | Design solutions, ADRs | Missing `tools` restriction |
| `developer` | Implement with tests | Missing `tools` list |
| `debugger` | Investigate errors | Missing `tools` list |
| `quality-reviewer` | Code review | Missing `tools` restriction |
| `ui-ux-designer` | Interface design | Not reviewed |
| `api-designer` | REST endpoint design | Not reviewed |
| `migration-planner` | DB schema changes | Not reviewed |
| `test-writer` | Write pytest tests | Not reviewed |
| `qa-validator` | Browser/DB testing | Not reviewed |
| `technical-writer` | Documentation | Not reviewed |
| `system-agent` | Impact assessment | Not reviewed |
| `system-archivist` | Record decisions | Not reviewed |
| `feature-steward` | Canon accuracy | Not reviewed |
| `adr-writer` | ADR creation | Not reviewed |

**Assessment:** Agents have good system prompts but lack proper frontmatter fields (`tools`, `permissionMode`, `skills`). No tool restrictions mean agents can do anything, reducing safety and focus.

#### Skills (3 total) - `.claude/Skills/`
| Skill | Purpose | Issues |
|-------|---------|--------|
| `error-message-validator` | Validate error messages | Has scripts, good structure |
| `flask-migration` | Flask-Alembic workflow | Has scripts, rollback guide |
| `test-coverage-enforcer` | Coverage standards | Has scripts, framework guides |

**Assessment:** Skills follow progressive disclosure pattern correctly but:
- Missing YAML frontmatter (`name`, `description` required)
- Skills directory is `.claude/Skills/` (uppercase) - should be `.claude/skills/` (lowercase)
- Python scripts exist but aren't referenced properly for execution

#### Plugins - `.claude/settings.json`
Four official plugins enabled:
- `github@claude-plugins-official`
- `code-review@claude-plugins-official`
- `feature-dev@claude-plugins-official`
- `frontend-design@claude-plugins-official`

**Assessment:** Good use of official plugins, but these overlap with custom commands/agents. Need to define boundaries.

### 1.2 What's Missing

| Component | Status | Impact |
|-----------|--------|--------|
| **Hooks** | None | High - no automation, no guardrails |
| **Output Styles** | None | Medium - no mode switching |
| **Plugin Packaging** | Not done | High - cannot share/reuse across projects |
| **SESSION_NOTES.md** | Referenced but not implemented | Medium - no cross-session memory |

**Note on MCP Servers:** GitHub MCP is already enabled via the official plugin. This is a BASIC setup intended to work with any project type, so additional MCPs (database, Sentry, Slack, etc.) are intentionally not included. Projects can add domain-specific MCPs as needed.

### 1.3 Issues to Solve Through Automation

The lessons learned document reveals recurring failures across 6 categories. **The goal is to PREVENT these issues through proper automation** - hooks, agents, commands, and skills that enforce patterns automatically rather than relying on human memory.

| Issue | Frequency | Solution Approach |
|-------|-----------|-------------------|
| CLAUDE.md rules ignored | High | **Hook**: PostToolUse compliance check |
| Code duplication | High | **Hook**: PreToolUse search before write |
| N+1 queries | High | **Hook**: PostToolUse query pattern lint |
| Hardcoded colors/status | High | **Hook**: PostToolUse grep for violations |
| Missing logging | High | **Agent**: Developer agent with logging skill |
| Silent exception handlers | High | **Hook**: PostToolUse exception check |

**Critical Insight:** Every documented lesson should be SOLVED through automation. When an issue recurs, the response should be: "Let's create a hook/skill/agent to prevent this" - NOT "let's add it to the lessons document."

---

## Section 2: Claude Code Capabilities Analysis

### 2.1 Capabilities Summary (from Documentation)

| Capability | Description | Current Use |
|------------|-------------|-------------|
| **Hooks** | Shell commands at lifecycle events | Not used |
| **Skills** | Auto-invoked expertise with scripts | Partially used (3 skills, no auto-invocation) |
| **Subagents** | Isolated context with tool restrictions | Used but not optimized |
| **CLI Mode** | Non-interactive CLI for scripts and CI/CD | Not used |
| **Plugins** | Packaged, shareable extensions | Official only |
| **Output Styles** | Mode switching (coding/learning) | Not used |

### 2.2 CLI Mode (formerly "Headless/Programmatic Mode")

**What it is:** Running Claude Code non-interactively from the command line using the `-p` flag. This enables:
- CI/CD integration (automated PR reviews, test generation)
- Script automation (batch processing, scheduled tasks)
- Piping data to Claude (e.g., `gh pr diff | claude -p "Review for security"`)

**Example usage:**
```bash
# Run a task non-interactively
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"

# Get structured JSON output
claude -p "Summarize this project" --output-format json

# Automated commit workflow
claude -p "Review staged changes and create commit" \
  --allowedTools "Bash(git diff:*),Bash(git log:*),Bash(git commit:*)"
```

**Relevance to this setup:** CLI mode is useful for GitHub Actions workflows (automated PR reviews, issue labeling) but is NOT required for the basic interactive workflow this setup targets. The official GitHub plugin already handles most CI/CD use cases. Consider CLI mode only if you need custom automation beyond what the plugin provides.

### 2.3 Detailed Capability Analysis

#### Hooks (HIGH PRIORITY - NOT USED)

**Hook Events Available:**
- `PreToolUse` - Before tool calls (can block)
- `PermissionRequest` - Permission dialogs (can allow/deny)
- `PostToolUse` - After tool calls complete
- `UserPromptSubmit` - Before processing user input
- `Notification` - Notification events
- `Stop` - When Claude finishes responding
- `SubagentStop` - When subagents complete
- `PreCompact` - Before context compaction
- `SessionStart` - Session begins
- `SessionEnd` - Session ends

**High-Value Hook Implementations:**

1. **PostToolUse - Auto-format on Edit/Write**
   - Run prettier/ruff after file modifications
   - Catches style violations immediately

2. **PreToolUse - Block sensitive files**
   - Prevent edits to `.env`, production configs
   - Enforce guardrails automatically

3. **PostToolUse - Compliance check**
   - After Edit/Write, grep for pattern violations
   - Return feedback to Claude for immediate correction

4. **Stop - Update SESSION_NOTES.md**
   - Auto-document session state on completion
   - Enable cross-session continuity

5. **SubagentStop - Quality gate enforcement**
   - Run quality checks after subagent completes
   - Block progression if checks fail

#### Skills - Progressive Disclosure Pattern

**Current Problem:** Skills exist but Claude doesn't auto-invoke them because:
1. Missing required YAML frontmatter
2. Description field absent (Claude uses this for triggering)
3. Directory casing issue

**From Documentation - Required Structure:**
```yaml
---
name: skill-name
description: Brief description (max 1024 chars). Claude uses this to decide when to apply.
allowed-tools: Read, Grep, Glob  # Optional: restrict tools
context: fork  # Optional: run in isolated context
---

# Skill content here
```

**Key Features Not Used:**
- `allowed-tools`: Can restrict skill to read-only
- `context: fork`: Run skill in isolated subagent
- `hooks`: Skill-scoped hooks (cleanup on completion)
- `user-invocable: false`: Hide from menu but allow auto-invocation

#### Subagents - Tool Restrictions

**Current Problem:** Agents have no `tools` field, meaning they inherit all tools.

**From Documentation - Available Fields:**
```yaml
---
name: code-reviewer
description: When to use this agent
tools: Read, Grep, Glob, Bash  # Explicit allowlist
disallowedTools: Write, Edit  # Explicit denylist
model: sonnet  # or opus, haiku, inherit
permissionMode: default | acceptEdits | dontAsk | bypassPermissions | plan
skills: pr-review, security-check  # Skills to inject
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
---
```

**Missing Opportunities:**
- `architect` should have `disallowedTools: Write, Edit, Bash` (analysis only)
- `quality-reviewer` should have `tools: Read, Grep, Glob` (read-only)
- All agents should specify `skills` they need

### 2.4 Capability-to-Issue Mapping

Every documented lesson should map to an automation solution:

| Issue | Solution | Capability |
|-------|----------|------------|
| L-CQ-001: Code duplication | Pre-search before writing | Hooks (PreToolUse) |
| L-CQ-002: CLAUDE.md ignored | Post-write compliance check | Hooks (PostToolUse) |
| L-CQ-003: Logic in templates | Block template edits with logic | Hooks (PreToolUse) |
| L-CQ-004: Inline JS explosion | Count lines on template edit | Hooks (PostToolUse) |
| L-PF-001: N+1 queries | Query lint on service edit | Hooks (PostToolUse) |
| L-PF-002: Memory leaks | Require cleanup pattern | Hooks (PostToolUse) |
| L-SA-001: Auth in wrong layer | Block route auth patterns | Hooks (PostToolUse) |
| L-FA-001: Hardcoded colors | Grep SCSS after edit | Hooks (PostToolUse) |
| L-SV-005: No logging | Check logger import | Hooks (PostToolUse) |
| L-API-001: Silent exceptions | Check exception handlers | Hooks (PostToolUse) |

---

## Section 3: Popular Community Hooks

Based on community resources ([awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code), [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery), [Anthropic best practices](https://www.anthropic.com/engineering/claude-code-best-practices)):

### 3.1 Security & Blocking Patterns

| Hook | Event | Purpose |
|------|-------|---------|
| **Dangerous Command Blocker** | PreToolUse | Blocks `rm -rf`, `sudo rm`, `chmod 777`, writes to system dirs |
| **Sensitive File Guard** | PreToolUse | Prevents edits to `.env`, `credentials.json`, `.git/*` |
| **Branch Protection** | PreToolUse | Blocks edits when on `main` or `master` branch |

**Example PreToolUse security hook:**
```python
# Exit code 2 blocks the tool with message to stderr
import sys, json
input_data = json.loads(sys.stdin.read())
if "rm -rf" in input_data.get("command", ""):
    print("Blocked: dangerous rm -rf command", file=sys.stderr)
    sys.exit(2)
```

### 3.2 Quality & Formatting Patterns

| Hook | Event | Purpose |
|------|-------|---------|
| **Auto-formatter** | PostToolUse | Runs ruff/prettier after file edits |
| **TypeScript Quality** | PostToolUse | Compilation, linting, formatting with SHA256 caching for <5ms validation |
| **TDD Guard** | PreToolUse | Enforces test-driven development - blocks code changes without tests |
| **Test Runner** | PostToolUse | Auto-runs tests when test files change |

### 3.3 Context & Workflow Patterns

| Hook | Event | Purpose |
|------|-------|---------|
| **Context Injector** | UserPromptSubmit | Appends project status/requirements to every prompt |
| **Session Logger** | SessionStart | Loads git status, recent issues automatically |
| **Transcript Backup** | PreCompact | Saves conversation before context compression |
| **Completion Validator** | Stop | Ensures task meets criteria before allowing Claude to stop |

### 3.4 Notification & Collaboration Patterns

| Hook | Event | Purpose |
|------|-------|---------|
| **TTS Announcer** | Notification | Text-to-speech when Claude needs input |
| **Britfix** | PostToolUse | Auto-converts to British English (intelligently avoids code identifiers) |
| **HCOM Multi-Agent** | Custom | Enables @-mention targeting between agents |

### 3.5 Recommended Hooks for This Setup

Based on documented issues and community patterns:

1. **`pre_edit_guard.py`** (PreToolUse) - Block sensitive files, dangerous patterns
2. **`post_edit_lint.py`** (PostToolUse) - Run formatters, check violations
3. **`check_patterns.py`** (PostToolUse) - Enforce project-specific patterns
4. **`session_notes.py`** (Stop) - Update SESSION_NOTES.md
5. **`context_loader.py`** (SessionStart) - Load git status, recent work

---

## Section 4: Proposed Architecture

### 4.1 Layered Architecture

```
                    ┌─────────────────────────────────────┐
                    │          WORKFLOW-V2.md             │
                    │    (Modes: Quick/Standard/Full)     │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────▼───────────────────┐
                    │             HOOKS                    │
                    │   (Automated Enforcement Layer)      │
                    │  PreToolUse │ PostToolUse │ Stop    │
                    └─────────────────┬───────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
┌───────▼───────┐           ┌────────▼────────┐          ┌─────────▼─────────┐
│   COMMANDS    │           │     AGENTS      │          │      SKILLS       │
│ (User Entry)  │           │ (Specialists)   │          │ (Auto-Expertise)  │
├───────────────┤           ├─────────────────┤          ├───────────────────┤
│ /plan-phase   │──────────►│ architect       │          │ error-validator   │
│ /plan-exec    │──────────►│ developer       │◄────────►│ flask-migration   │
│ /debug        │──────────►│ debugger        │          │ test-coverage     │
│ /commit       │           │ quality-reviewer│          │ pattern-enforcer  │
│ /quick-fix    │──────────►│ developer       │          │ (NEW)             │
└───────────────┘           └─────────────────┘          └───────────────────┘
```

### 4.2 WORKFLOW-V2 Stage Mapping

| Workflow Stage | Commands | Agents | Skills | Hooks |
|----------------|----------|--------|--------|-------|
| **Stage 1: Intent & Impact** | `/plan-phase` | architect, system-agent | - | PreToolUse: search existing |
| **Stage 2: Phase Planning** | `/plan-phase` | architect | - | - |
| **Stage 3: Execution** | `/plan-execution`, `/quick-fix` | developer, ui-ux-designer, api-designer | flask-migration, error-validator | PostToolUse: lint/format |
| **Stage 4: Review & Sync** | `/review-pr`, `/commit` | quality-reviewer, feature-steward, system-archivist | test-coverage | Stop: update SESSION_NOTES |

### 4.3 Trigger Matrix

| Trigger | Type | What Fires |
|---------|------|------------|
| User types `/plan-phase` | Manual | Command → architect agent |
| User types `/debug` | Manual | Command → debugger agent |
| Claude edits `.py` file | Automatic | PostToolUse → ruff + test-coverage skill |
| Claude edits `.scss` file | Automatic | PostToolUse → check hardcoded colors |
| Claude edits `services/*.py` | Automatic | PostToolUse → pattern-enforcer skill |
| Mentions "migration" | Automatic | flask-migration skill activates |
| Mentions "error message" | Automatic | error-validator skill activates |
| Session ends | Automatic | Stop hook → write SESSION_NOTES.md |

### 4.4 Proposed Directory Structure

```
.claude/
├── settings.json           # Plugin enables, permissions
├── settings.local.json     # Local overrides (gitignored)
│
├── commands/               # Slash commands (user-invoked)
│   ├── commit.md
│   ├── debug.md
│   ├── plan-phase.md
│   ├── plan-execution.md
│   ├── quick-fix.md
│   ├── migrate.md
│   ├── test-feature.md
│   └── review-pr.md
│
├── agents/                 # Subagents (Claude-delegated)
│   ├── architect.md        # Design only, no write tools
│   ├── developer.md        # Full tools, skills injected
│   ├── debugger.md         # Investigation tools
│   ├── quality-reviewer.md # Read-only tools
│   ├── ui-ux-designer.md   # Design + frontend tools
│   ├── api-designer.md     # Design only
│   ├── migration-planner.md # DB-focused tools
│   ├── test-writer.md      # Test tools + coverage skill
│   ├── feature-steward.md  # Canon accuracy (Sync Loop)
│   ├── system-archivist.md # ADRs and system docs (Sync Loop)
│   └── system-agent.md     # Impact assessment (Planning Loop)
│
├── skills/                 # Auto-invoked expertise (lowercase!)
│   ├── error-message-validator/
│   │   ├── SKILL.md        # With proper frontmatter
│   │   ├── patterns.md
│   │   └── scan_errors.py
│   ├── flask-migration/
│   │   ├── SKILL.md
│   │   ├── rollback_guide.md
│   │   └── check_migration.py
│   ├── test-coverage-enforcer/
│   │   ├── SKILL.md
│   │   ├── pytest_guide.md
│   │   └── check_coverage.py
│   └── pattern-enforcer/   # NEW: Enforces project patterns
│       ├── SKILL.md
│       ├── checklist.md
│       └── check_patterns.py
│
├── hooks/                  # NEW: Automation scripts
│   ├── post_edit_lint.py   # Run linters after edits
│   ├── pre_edit_guard.py   # Block sensitive files
│   ├── check_patterns.py   # Pattern enforcement
│   └── session_notes.py    # Update SESSION_NOTES on stop
│
├── output-styles/          # NEW: Mode switching
│   └── planning-mode.md    # Read-only planning style
│
└── SESSION_NOTES.md        # Cross-session memory (gitignored)
```

### 4.5 Hooks Configuration

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/pre_edit_guard.py\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/post_edit_lint.py\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/session_notes.py\""
          }
        ]
      }
    ]
  }
}
```

---

## Section 5: Implementation Roadmap

### Phase 1: Foundation (Day 1-2)
**Goal:** Fix existing issues, enable basic automation

| Task | Priority | Dependency |
|------|----------|------------|
| 1.1 Rename `.claude/Skills/` to `.claude/skills/` | Critical | None |
| 1.2 Add YAML frontmatter to all skills | Critical | 1.1 |
| 1.3 Add `tools` field to all agents | High | None |
| 1.4 Create `.claude/hooks/` directory | High | None |
| 1.5 Implement `pre_edit_guard.py` hook | High | 1.4 |
| 1.6 Implement `post_edit_lint.py` hook | High | 1.4 |
| 1.7 Create `SESSION_NOTES.md` template | Medium | None |

### Phase 2: Skills Enhancement (Day 3-4)
**Goal:** Make skills auto-invoke correctly

| Task | Priority | Dependency |
|------|----------|------------|
| 2.1 Rewrite `error-message-validator/SKILL.md` with proper triggers | High | 1.2 |
| 2.2 Rewrite `flask-migration/SKILL.md` with proper triggers | High | 1.2 |
| 2.3 Rewrite `test-coverage-enforcer/SKILL.md` with proper triggers | High | 1.2 |
| 2.4 Create `pattern-enforcer` skill | High | 1.2 |
| 2.5 Add skill references to relevant agents | Medium | 1.3, 2.1-2.4 |

### Phase 3: Agent Optimization (Day 5-6)
**Goal:** Proper tool restrictions and skill injection

| Task | Priority | Dependency |
|------|----------|------------|
| 3.1 Optimize `architect.md` - analysis only | High | 1.3 |
| 3.2 Optimize `developer.md` - skills injected | High | 2.5 |
| 3.3 Optimize `quality-reviewer.md` - read-only | High | 1.3 |
| 3.4 Optimize `debugger.md` - investigation focus | Medium | 1.3 |
| 3.5 Add subagent hooks for quality gates | Medium | Phase 2 |

### Phase 4: Advanced Hooks (Day 7-8)
**Goal:** Full pattern enforcement automation

| Task | Priority | Dependency |
|------|----------|------------|
| 4.1 Create `check_patterns.py` for violation detection | High | Phase 1 |
| 4.2 Implement N+1 query detection hook | Medium | 4.1 |
| 4.3 Implement hardcoded color detection hook | Medium | 4.1 |
| 4.4 Implement logging check hook | Medium | 4.1 |
| 4.5 Implement `session_notes.py` Stop hook | Medium | 1.7 |

### Phase 5: Plugin Packaging (Day 9-10)
**Goal:** Create reusable plugin for other projects

| Task | Priority | Dependency |
|------|----------|------------|
| 5.1 Create plugin manifest (`.claude-plugin/plugin.json`) | High | Phase 1-4 |
| 5.2 Reorganize for plugin structure | High | 5.1 |
| 5.3 Create README with installation instructions | Medium | 5.2 |
| 5.4 Test plugin loading with `--plugin-dir` | High | 5.2 |
| 5.5 (Optional) Publish to marketplace | Low | 5.4 |

### Dependency Graph

```
Phase 1 (Foundation)
    │
    ├──► Phase 2 (Skills)
    │        │
    │        └──► Phase 3 (Agents)
    │                 │
    └──► Phase 4 (Hooks) ◄─┘
              │
              └──► Phase 5 (Plugin)
```

---

## Section 6: Agent Recommendations

### 6.1 WORKFLOW-V2 Agent Roles

Understanding WHY each agent exists in the workflow is critical. From WORKFLOW-V2:

**Core Loop (constant use):**
| Agent | Purpose | Reads | Writes |
|-------|---------|-------|--------|
| **Developer** | Build features | Canon (behavior), Anchors | Code |
| **Quality Reviewer** | Verify correctness | Canon, Code | Flags only |

**Planning Loop (per-phase):**
| Agent | Purpose | Reads | Writes |
|-------|---------|-------|--------|
| **Architect** | Structure phases | Canon, System docs | Phase docs |
| **System Agent** | Assess impact | Canon, System docs | Technical anchors |

**Sync Loop (after changes):**
| Agent | Purpose | Reads | Writes |
|-------|---------|-------|--------|
| **Feature Steward** | Keep Canon accurate | Canon, Code | Canon |
| **System Archivist** | Record decisions | System docs, Code | ADRs, System docs |

**Occasional:**
| Agent | Purpose | When |
|-------|---------|------|
| **Debugger** | Investigate failures | Something broke |

### 6.2 Keep and Optimize

All agents serve specific purposes in the workflow. They need optimization, not removal:

| Agent | Role | Modifications |
|-------|------|---------------|
| `architect.md` | Planning Loop | Add `disallowedTools: Write, Edit, Bash`, add `permissionMode: plan` |
| `developer.md` | Core Loop | Add `tools: *`, add `skills: error-message-validator, test-coverage-enforcer` |
| `debugger.md` | Occasional | Add `tools: Read, Grep, Glob, Bash`, remove Write/Edit |
| `quality-reviewer.md` | Core Loop | Add `tools: Read, Grep, Glob`, add `permissionMode: plan` |
| `ui-ux-designer.md` | Execution | Add `tools: Read, Write, Edit, Bash`, add frontend skills |
| `api-designer.md` | Execution | Add `disallowedTools: Write, Edit, Bash` |
| `migration-planner.md` | Execution | Add `skills: flask-migration` |
| `test-writer.md` | Execution | Add `skills: test-coverage-enforcer` |
| `system-agent.md` | Planning Loop | Add `tools: Read, Grep, Glob` for impact assessment |
| `feature-steward.md` | Sync Loop | Critical for Canon accuracy after implementation |
| `system-archivist.md` | Sync Loop | Critical for ADR creation and system doc updates |

### 6.3 Consolidation Opportunities

Some agents may have overlapping responsibilities:

| Agent | Consider Merging With | Reason |
|-------|----------------------|--------|
| `qa-validator` | `quality-reviewer` | Similar validation focus |
| `technical-writer` | Main Claude | Low-frequency documentation tasks |
| `adr-writer` | `system-archivist` | ADR writing is part of archivist role |

**Important:** Do NOT remove `system-agent`, `system-archivist`, or `feature-steward`. These serve distinct purposes in the Planning and Sync loops defined by WORKFLOW-V2.

### 6.4 Command Recommendations

#### Keep As-Is
- `/commit` - Excellent, comprehensive
- `/debug` - Excellent, evidence-based protocol

#### Modify

| Command | Modifications |
|---------|---------------|
| `/plan-phase` | Add WORKFLOW-V2 mode detection, reference Feature Map |
| `/plan-execution` | Remove redundant agent descriptions (they're in agent files), add skill references |
| `/quick-fix` | Ensure it delegates to developer, not implements directly |
| `/review-pr` | Add pattern enforcement checklist integration |

#### `/plan-execution` Additional Requirements

**Deferred/Incomplete Task Handling:**
When a task cannot be completed during execution:
1. MUST explain WHY the task was deferred or not completed
2. MUST add the deferred task to the appropriate phase document with:
   - Clear description of what remains
   - Reason for deferral
   - Any dependencies or blockers
3. Never leave tasks "hanging" without a documented home

**Manual Testing Instructions:**
When a subphase requires manual testing:
1. Explain HOW to test the feature (specific steps)
2. Explain WHERE in the UI/system to perform the test
3. ASSUME the server is ALREADY running - do NOT explain how to start the server
4. Focus on actionable test steps, for example:
   - "Navigate to `/settings` in your browser"
   - "Click the 'Save' button"
   - "Verify the success toast appears"
   - "Check that the data persists after page refresh"

#### Consider Adding

| Command | Purpose |
|---------|---------|
| `/explore` | Explicit codebase exploration (vs implicit Explore agent) |
| `/session-status` | Show SESSION_NOTES.md state and todo progress |

---

## Section 7: Skills Recommendations

### 7.1 Fix Existing Skills

All three skills need:
1. Rename parent directory to lowercase
2. Add proper YAML frontmatter
3. Add explicit trigger descriptions

**Example Fix for `error-message-validator/SKILL.md`:**
```yaml
---
name: error-message-validator
description: Validates error messages are user-friendly, specific, and actionable. Auto-activates when writing error handling code, form validation, or API error responses. Mention "error message" or "validation" to trigger.
allowed-tools: Read, Grep, Glob
---
```

### 7.2 Add New Skill: Pattern Enforcer

This skill embodies the philosophy that lessons learned should be SOLVED through automation:

| Skill | Purpose | Triggers |
|-------|---------|----------|
| `pattern-enforcer` | Enforce project patterns automatically | Any code edit |

**What it checks:**
- Hardcoded hex colors in SCSS (should use variables)
- Deprecated patterns (`.query.get()` etc.)
- Bare `except Exception:` without logging
- Missing logger imports in services
- Business logic in templates
- Silent exception handlers

**Philosophy:** When a pattern violation is discovered during development, the response should be to update this skill to catch it automatically in the future.

---

## Section 8: Hooks Recommendations

### 8.1 Implement These Hooks

| Hook | Event | Purpose | Priority |
|------|-------|---------|----------|
| `pre_edit_guard.py` | PreToolUse (Edit\|Write) | Block `.env`, secrets, config | Critical |
| `post_edit_lint.py` | PostToolUse (Edit\|Write) | Run ruff/prettier | High |
| `check_patterns.py` | PostToolUse (Edit\|Write) | Check pattern violations | High |
| `session_notes.py` | Stop | Update SESSION_NOTES.md | Medium |
| `subagent_quality.py` | SubagentStop | Run quality checks | Medium |

### 8.2 Hook Implementation Specs

**`pre_edit_guard.py`:**
- Input: `tool_input.file_path`
- Block: `.env`, `credentials.json`, `secrets.json`, `.git/*`
- Exit code 2 to block with message

**`post_edit_lint.py`:**
- Input: `tool_input.file_path`
- Run: `ruff check` for `.py`, `npx prettier` for `.ts/.js/.scss`
- Return feedback to Claude if issues found

**`check_patterns.py`:**
- Input: `tool_input.file_path`
- Check for patterns that should be prevented:
  - Hardcoded hex colors in SCSS
  - `.query.get(` deprecated pattern
  - Bare `except Exception:` without logging
  - Missing logger import in services
  - Business logic in templates

---

## Section 9: Plugin Structure Recommendation

For reusability across projects, package as a plugin:

```
claude-agentic-workflow/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── commit.md
│   ├── debug.md
│   ├── plan-phase.md
│   ├── plan-execution.md
│   ├── quick-fix.md
│   └── review-pr.md
├── agents/
│   ├── architect.md
│   ├── developer.md
│   ├── debugger.md
│   ├── quality-reviewer.md
│   ├── feature-steward.md
│   └── system-archivist.md
├── skills/
│   ├── error-message-validator/
│   ├── test-coverage-enforcer/
│   └── pattern-enforcer/
├── hooks/
│   └── hooks.json
└── README.md
```

**`plugin.json`:**
```json
{
  "name": "agentic-workflow",
  "description": "Structured workflow for large-scale agentic development with automated quality enforcement",
  "version": "1.0.0",
  "author": {
    "name": "Your Team"
  }
}
```

---

## Section 10: Migration Checklist

### Pre-Migration
- [x] Backup current `.claude/` directory
- [x] Document current working state
- [x] Identify any custom modifications to preserve

### Phase 1 Checklist
- [ ] Create `.claude/hooks/` directory
- [ ] Rename `.claude/Skills/` to `.claude/skills/`
- [ ] Update all skills with YAML frontmatter
- [ ] Add `tools` field to all agents
- [ ] Implement `pre_edit_guard.py`
- [ ] Implement `post_edit_lint.py`
- [ ] Create `SESSION_NOTES.md` template
- [ ] Test hooks with `claude --debug`
- [ ] Create phase document template with YAML frontmatter and checklists (see Appendix E)

### Phase 2 Checklist
- [ ] Rewrite `error-message-validator/SKILL.md`
- [ ] Rewrite `flask-migration/SKILL.md`
- [ ] Rewrite `test-coverage-enforcer/SKILL.md`
- [ ] Create `pattern-enforcer` skill
- [ ] Test skill auto-invocation
- [ ] Update `/plan-phase` command with senior developer review step
- [ ] Update `/plan-execution` command with deferred task handling and manual testing requirements

### Phase 3 Checklist
- [ ] Update `architect.md` with tool restrictions
- [ ] Update `developer.md` with skills
- [ ] Update `quality-reviewer.md` as read-only
- [ ] Update Sync Loop agents (feature-steward, system-archivist)
- [ ] Update Planning Loop agents (system-agent)
- [ ] Test agent delegation

### Phase 4 Checklist
- [ ] Implement `check_patterns.py`
- [ ] Implement `session_notes.py`
- [ ] Add SubagentStop hooks
- [ ] Full integration test

### Phase 5 Checklist
- [ ] Create plugin manifest
- [ ] Reorganize for plugin structure
- [ ] Test with `--plugin-dir`
- [ ] Write installation documentation

---

## Section 11: Phase Document Improvements

Phase documents are the bridge between planning and execution. They must be structured for clarity, trackability, and quality assurance.

### 11.1 YAML Frontmatter Requirement

All phase documents MUST include YAML frontmatter, consistent with skills and agents:

```yaml
---
title: "Phase X.Y: [Feature Name]"
status: draft | in-review | approved | in-progress | completed
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: [agent or user who created]
reviewers: []
estimated-effort: [hours or days]
dependencies:
  - "Phase X.Z must be completed"
  - "API endpoint /foo must exist"
tags:
  - feature-area
  - complexity-level
---
```

### 11.2 Checklist Structure Requirements

Phase documents MUST use checkbox-based checklists for completion tracking:

**Subphase Checklist Format:**
```markdown
## Subphase 1: [Name]

### Implementation Tasks
- [ ] Task 1 description
- [ ] Task 2 description
- [ ] Task 3 description

### Verification
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] Code review approved
```

**Benefits:**
- Clear visual progress indicator
- Easy to track what remains
- Enables partial completion tracking
- Works with GitHub's task list rendering

### 11.3 Gemini LLM Verification Checkpoint

Every phase document MUST include a Gemini verification checkbox. This is a simple external validation step performed outside of Claude.

**Required Checkbox:**
```markdown
- [ ] Verified through Gemini LLM (date: ___________)
```

The Gemini verification is done externally by copying the phase document to Gemini and having it review for clarity, completeness, and logical consistency. The phase document only needs to track that this step was completed.

### 11.4 Senior Developer Review Protocol

**This is an AGENT step, not a human review.** The Senior Developer Review is built into the `/plan-phase` workflow and is performed automatically by Claude before presenting the document to the user.

**How It Works:**
1. The `/plan-phase` command creates the phase document draft
2. **Automatically**, the same agent then reviews the document adversarially, adopting the persona of "a senior developer who hates the project"
3. The agent identifies issues (weak spots, missing edge cases, unrealistic estimates, hidden complexity, unaddressed failure modes, gaps in testing)
4. The agent fixes the issues it found
5. The final document presented to the user includes a summary of what was found and fixed

**This is NOT a manual step.** The user receives a completed, reviewed document. The "Senior Developer Review Notes" section in the phase document simply records what the agent found and addressed during its adversarial pass.

**Phase Document Section (Agent Output):**
```markdown
### Senior Developer Review (Agent)
Reviewed: YYYY-MM-DD

**Issues Found & Fixed:**
- [Issue 1]: [How it was addressed]
- [Issue 2]: [How it was addressed]
```

### 11.5 Complete Phase Document Quality Gates

Every phase document must pass these gates before execution begins:

```markdown
## Quality Gates

### Documentation Quality
- [ ] YAML frontmatter complete and accurate
- [ ] All tasks have checkbox format
- [ ] Success criteria are measurable
- [ ] Dependencies explicitly listed
- [ ] Rollback strategy defined

### External Validation
- [ ] Verified through Gemini LLM (date: ___________)

### Agent Review
- [ ] Senior Developer Review completed by agent (see notes below)

### Approval
- [ ] Document status changed to "approved"
- [ ] Ready for `/plan-execution`
```

**Note:** The "Senior Developer Review" checkbox confirms the agent completed its adversarial review pass. The details of what was found and fixed appear in the "Senior Developer Review (Agent)" section of the document.

---

## Appendix A: Agent Frontmatter Templates

### Analysis-Only Agent (architect, api-designer)
```yaml
---
name: architect
description: Analyzes requirements and designs solutions. Does NOT implement code.
tools: Read, Grep, Glob
disallowedTools: Write, Edit, Bash
model: inherit
permissionMode: plan
---
```

### Implementation Agent (developer)
```yaml
---
name: developer
description: Implements specifications with tests. Writes production code.
tools: Read, Write, Edit, Bash, Grep, Glob
model: inherit
skills: error-message-validator, test-coverage-enforcer
---
```

### Review Agent (quality-reviewer)
```yaml
---
name: quality-reviewer
description: Reviews code for real issues. Read-only analysis.
tools: Read, Grep, Glob
disallowedTools: Write, Edit, Bash
model: inherit
permissionMode: plan
---
```

### Sync Loop Agent (feature-steward)
```yaml
---
name: feature-steward
description: Keeps Feature Canon accurate after implementation. Updates Canon to match actual code behavior.
tools: Read, Write, Edit, Grep, Glob
disallowedTools: Bash
model: inherit
---
```

### Sync Loop Agent (system-archivist)
```yaml
---
name: system-archivist
description: Records architectural decisions in ADRs. Updates system docs when structure changes.
tools: Read, Write, Edit, Grep, Glob
disallowedTools: Bash
model: inherit
---
```

---

## Appendix B: Skill Frontmatter Template

```yaml
---
name: skill-name-lowercase
description: |
  Brief description of what this skill does.
  Auto-activates when: [specific triggers].
  Keywords: [comma, separated, triggers]
allowed-tools: Read, Grep, Glob, Bash
---

# Skill Name

[Overview paragraph]

## Auto-Activation Triggers
- When user mentions: [keywords]
- When editing files in: [paths]
- When creating: [artifact types]

## Core Instructions
[Essential content - keep under 500 lines]

## Reference Files (Load When Needed)
- `details.md` - Load when [scenario]
- `examples.md` - Load when [scenario]

## Bundled Scripts
- `validate.py` - Run to [purpose]. Usage: `python validate.py <input>`
```

---

## Appendix C: WORKFLOW-V2 Alignment Matrix

| WORKFLOW-V2 Concept | Implementation |
|---------------------|----------------|
| Quick mode (< 1 day) | `/quick-fix` command, minimal hooks |
| Standard mode (1-5 days) | `/plan-phase` + `/plan-execution` |
| Full mode (> 5 days) | Full command suite + all agents |
| Feature Canon | Skills reference Canon structure |
| Done Levels (L1-L3) | Quality gates in SubagentStop hooks |
| Recovery Protocols | `/debug` command, escalation in agents |
| Core Loop Agents | developer, quality-reviewer |
| Planning Loop Agents | architect, system-agent |
| Sync Loop Agents | feature-steward, system-archivist |
| Context Management | SESSION_NOTES.md + Stop hooks |

---

## Appendix D: Community Resources

For further hook patterns and examples:
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - Curated list of skills, hooks, and commands
- [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) - Deep dive into hook patterns
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Official recommendations
- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide) - Official documentation
- [eesel.ai Hooks Guide](https://www.eesel.ai/blog/hooks-in-claude-code) - Complete automation guide

---

## Appendix E: Phase Document Template

Complete template for phase documents with all required elements.

```markdown
---
title: "Phase X.Y: [Feature Name]"
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: architect-agent
tags:
  - feature-area
  - ui | backend | database | integration
---

# Phase X.Y: [Feature Name]

## Overview

[2-3 sentence description of what this phase accomplishes and why it matters.]

## Success Criteria

- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Dependencies

| Dependency | Reference | Status |
|------------|-----------|--------|
| [What's needed] | [ADR-XXX or `/docs/dev/notes/` link] | Pending/Ready |
| Authentication approach | See ADR-001 | Ready |
| Database schema design | `/docs/dev/notes/schema-design.md` | Pending |

## Phase Completion Criteria

This phase is DONE when:
- [ ] All subphase tasks completed
- [ ] All manual verifications passed
- [ ] [Any other specific criteria for this phase]

---

## Subphase 1: [Name]

### Description
[What this subphase accomplishes]

### Implementation Tasks
- [ ] Task 1: [Specific, actionable description]
- [ ] Task 2: [Specific, actionable description]
- [ ] Task 3: [Specific, actionable description]

### Primary Files (may expand)
- `path/to/file1.py` - [What changes]
- `path/to/file2.ts` - [What changes]

### Edge Cases
- [ ] Handle case when [scenario 1]
- [ ] Handle case when [scenario 2]

### Verification
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Manual testing completed (agent will explain steps in terminal)

---

## Subphase 2: [Name]

[Repeat structure from Subphase 1]

---

## Files Actually Modified

> Populated after execution

| File | Change Type | Subphase |
|------|-------------|----------|
| | | |

---

## Quality Gates

### Documentation Quality
- [ ] YAML frontmatter complete and accurate
- [ ] All tasks have checkbox format
- [ ] Success criteria are measurable
- [ ] Dependencies explicitly listed with ADR/notes references

### External Validation
- [ ] Verified through Gemini LLM (date: ___________)

### Agent Review
- [ ] Senior Developer Review completed by agent (see notes below)

### Approval
- [ ] Document status changed to "approved"
- [ ] Ready for `/plan-execution`

---

## Senior Developer Review (Agent)

> This section is automatically populated by the `/plan-phase` agent during its adversarial review pass.

**Reviewed:** YYYY-MM-DD

**Issues Found & Fixed:**
- [Issue 1]: [How it was addressed in the document]
- [Issue 2]: [How it was addressed in the document]
- [Issue 3]: [How it was addressed in the document]

---

## Deferred Tasks

> Tasks that could not be completed during execution are tracked here.

| Task | Reason Deferred | Target Phase | Dependencies |
|------|-----------------|--------------|--------------|
| [Task description] | [Why it was deferred] | Phase X.Z | [Any blockers] |

---

## Execution Log

| Date | Subphase | Status | Notes |
|------|----------|--------|-------|
| YYYY-MM-DD | Subphase 1 | Completed | [Any relevant notes] |
| YYYY-MM-DD | Subphase 2 | In Progress | [Any relevant notes] |
```

---

## Conclusion

This rework plan transforms the current Claude Code setup from a collection of useful but disconnected components into an integrated system that:

1. **Automates pattern enforcement** via hooks (prevents issues rather than documenting them)
2. **Enables smart skill invocation** through proper frontmatter
3. **Restricts agents appropriately** based on their WORKFLOW-V2 roles
4. **Preserves all workflow-critical agents** (Core Loop, Planning Loop, Sync Loop)
5. **Maintains session continuity** via SESSION_NOTES.md
6. **Packages for reuse** as a shareable plugin

The key philosophy shift: **Every recurring issue should be solved through automation** (hooks, skills, agents, commands) rather than being documented for manual review.

**Estimated Effort:** 10 working days for full implementation
**Recommended Start:** Phase 1 (Foundation) - highest impact, lowest risk
