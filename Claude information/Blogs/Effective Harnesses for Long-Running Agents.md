# Effective Harnesses for Long-Running Agents

**Source:** [Anthropic Engineering Blog](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
**Published:** November 26, 2025

## Overview

This article addresses a fundamental challenge in AI agent development: maintaining continuity across multiple context windows. When agents work on complex, multi-session projects, they lose memory between sessions - similar to engineers working in shifts where each new engineer arrives with no memory of what happened previously.

## Key Problem

Long-running agents face discrete work sessions with no automatic memory carryover. This creates challenges for:
- Multi-day development projects
- Complex tasks requiring iterative progress
- Quality assurance across sessions

## Two-Part Architecture Solution

### 1. Initializer Agent
Sets up the initial environment with structured files that persist across sessions.

### 2. Coding Agent
Handles incremental progress with clear documentation, focusing on one feature at a time.

## Core Components

### Feature Lists
- A JSON file containing comprehensive end-to-end feature descriptions
- All features initially marked as failing
- Critical rule: Never remove or edit tests to avoid missing or buggy functionality

Example structure:
```json
{
  "category": "functional",
  "description": "New chat button creates conversation",
  "steps": ["Navigate", "Click button", "Verify creation"],
  "passes": false
}
```

### Incremental Progress
- Single-feature focus per session
- Git commits after each completed feature
- Progress summaries for next session handoff

### Testing Strategy
- Browser automation tools (e.g., Puppeteer MCP) for end-to-end verification
- End-to-end tests preferred over unit tests alone for agent workflows

## Startup Sequence

Each new session follows this sequence:
1. Run `pwd` to confirm working directory
2. Read progress files and git logs
3. Select highest-priority incomplete feature
4. Start development server via init script
5. Run basic functionality tests before proceeding

## Key Files to Maintain

| File | Purpose |
|------|---------|
| `init.sh` | Environment setup script |
| `claude-progress.txt` | Session documentation and handoff notes |
| `feature_list.json` | Structured requirements tracking |

## Best Practices

- **Immutable Test Specs:** Never modify test descriptions to make them pass
- **Atomic Commits:** Commit after each feature completion
- **Progress Documentation:** Always update progress files before session ends
- **Environment Verification:** Always verify working directory and state at session start

## Future Directions

The research suggests exploring:
- **Multi-agent architectures** with specialized agents (testing, QA, cleanup)
- **Cross-domain applications** beyond web development (scientific research, financial modeling)
- **Hierarchical task decomposition** for more complex projects

## Takeaways

1. Structure enables continuity - well-organized files bridge context windows
2. Testing drives progress - feature lists with pass/fail status guide work
3. Documentation is essential - progress files ensure smooth handoffs
4. Verification prevents regression - always test before and after changes
