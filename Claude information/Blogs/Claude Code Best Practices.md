# Claude Code: Best Practices for Agentic Coding

**Source:** [Anthropic Engineering Blog](https://www.anthropic.com/engineering/claude-code-best-practices)
**Published:** 2025

## Overview

Claude Code is a command-line tool enabling AI-assisted development workflows. It is intentionally low-level and unopinionated, providing close to raw model access without forcing specific methodologies.

## Customizing Your Setup

### CLAUDE.md Files

Create `CLAUDE.md` files to document:
- Bash commands and their purposes
- Code style guidelines
- Testing instructions
- Repository conventions

**Placement Options:**
- Project root (project-specific)
- Parent directories (shared across projects)
- Home folder (`~/.claude/CLAUDE.md`) for global settings

**Example Structure:**
```markdown
# Bash commands
- npm run build: Build the project
- npm run typecheck: Run typechecker

# Code style
- Use ES modules syntax, not CommonJS
- Destructure imports when possible

# Testing
- Run tests with: npm test
- Coverage report: npm run coverage
```

### Tool Permissions

Manage permissions through:
- Allowlists in configuration
- The `/permissions` command
- CLI flags for one-time adjustments

### GitHub Integration

Install GitHub's `gh` CLI for enhanced integration with:
- Issue management
- Pull request workflows
- Repository operations

## Expanding Tool Capabilities

### Bash Environment
Leverage existing tools and custom scripts in your development environment.

### MCP (Model Context Protocol) Servers

Configure in:
- Project-level `.mcp.json`
- Global settings
- Checked-in configuration files

### Custom Slash Commands

Create reusable commands in `.claude/commands/` directories:
- Use `$ARGUMENTS` keyword for parameter passing
- Commands like `/project:fix-github-issue` can combine multiple operations

## Common Workflows

### 1. Explore, Plan, Code, Commit

**Pattern:** Research first, create detailed plans, then implement
- Start with codebase exploration
- Document understanding before changing code
- Plan changes explicitly before implementation

### 2. Test-Driven Development

**Pattern:** Write tests before code implementation
- Define expected behavior via tests
- Let tests guide implementation
- Verify continuously

### 3. Visual Iteration

**Pattern:** Use screenshots and design mocks as reference
- Provide visual targets
- Iterate based on visual comparison
- Useful for UI development

### 4. Safe YOLO Mode

**Pattern:** Run uninterrupted in isolated containers
- Use `--dangerously-skip-permissions` flag
- Only in sandboxed environments
- Useful for automated pipelines

### 5. Codebase Q&A

**Pattern:** Query codebases like pair programming
- Ask questions about code structure
- Understand unfamiliar codebases
- Get explanations of complex logic

### 6. Git and GitHub Integration

**Pattern:** Leverage CLI tools for version control
- Commit workflows
- Issue management
- Pull request creation and review

## Optimization Strategies

| Strategy | Benefit |
|----------|---------|
| Specific instructions upfront | Reduces back-and-forth |
| Include images/screenshots | Visual context improves accuracy |
| Tab-completion for files | Ensures correct file references |
| Include documentation URLs | Provides authoritative context |
| Use `/clear` between tasks | Fresh context prevents confusion |
| Create checklists | Tracks multi-step workflows |

## Extended Thinking Modes

Allocate increasing computational budgets:

| Mode | Use Case |
|------|----------|
| "think" | Standard reasoning |
| "think hard" | Complex problems |
| "think harder" | Very complex analysis |
| "ultrathink" | Maximum reasoning depth |

## Headless Mode & Automation

### Non-Interactive Usage

Use `-p` flag for CI/CD contexts:
- Automated issue triage
- Code review automation
- Pipeline integration

### Output Formats

`--output-format stream-json` for programmatic consumption of results.

## Multi-Claude Workflows

### Parallel Instances

Run separate instances for:
- Code writing vs. verification
- Independent feature development
- Large-scale migrations

### Git Worktrees

Enable independent simultaneous tasks:
- Each worktree has its own working directory
- Allows parallel work on different branches
- Prevents interference between tasks

### Fan-Out Patterns

For large-scale operations:
- Distribute work across multiple agents
- Aggregate results
- Useful for codebase-wide changes

## Configuration Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project instructions |
| `.claude/settings.json` | Permission settings |
| `.mcp.json` | MCP server configuration |
| `.claude/commands/*.md` | Custom slash commands |

## Takeaways

1. **CLAUDE.md is essential** - Document project conventions
2. **Permissions are configurable** - Balance safety and convenience
3. **Workflows vary** - Choose pattern matching your task
4. **Tools extend capability** - MCP and custom commands add power
5. **Thinking modes scale** - Match reasoning depth to problem complexity
6. **Automation enables scale** - Headless mode for CI/CD integration
7. **Parallelization multiplies** - Multiple instances for large tasks
