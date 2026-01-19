# Equipping Agents for the Real World with Agent Skills

**Source:** [Anthropic Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
**Published:** October 2025

## Overview

Agent Skills are organized folders of instructions, scripts, and resources that agents can discover and load dynamically. They enhance Claude's capabilities beyond general-purpose functionality by providing domain-specific expertise and procedural knowledge.

## Core Design Principle: Progressive Disclosure

Information loads hierarchically as needed, similar to how a manual structures content from table of contents through appendices. This prevents context window bloat while ensuring relevant expertise is available when needed.

## Skill Anatomy

### Required Structure
Every skill needs a `SKILL.md` file containing:
- **YAML frontmatter** with `name` and `description` metadata
- **Primary instructions** and guidance
- **References** to optional bundled files

### Three-Level Information Architecture

| Level | Content | When Loaded |
|-------|---------|-------------|
| Level 1 | Metadata (name, description) | At startup |
| Level 2 | Full SKILL.md content | When skill is triggered |
| Level 3+ | Bundled files (reference.md, forms.md) | On demand during execution |

## Skills and Context Windows

Skills integrate with context management by:
- Loading only metadata initially (minimal token cost)
- Expanding full content only when relevant triggers detected
- Loading additional resources only when specifically needed
- Keeping executable scripts outside context until execution

## Code Execution Integration

Skills can bundle pre-written scripts that execute deterministically:
- **Python scripts** for data processing, validation, or API calls
- **Bash scripts** for system operations
- Scripts run without loading entire file contents into context
- Results returned to agent for decision-making

## Example: PDF Skill

A practical implementation demonstrating:
- Form field extraction from PDF documents
- Document manipulation capabilities
- Bundled Python scripts for reliable field detection
- Separate documentation files for form-filling operations

## Developing Skills

### Best Practices
1. **Clear trigger conditions** - Define when the skill should activate
2. **Minimal footprint** - Load only what's needed at each level
3. **Executable validation** - Include scripts that verify correctness
4. **Comprehensive documentation** - Support files for edge cases

### Skill Structure Example
```
my-skill/
├── SKILL.md           # Core instructions (always loaded when triggered)
├── reference.md       # Detailed documentation (loaded on demand)
├── validate.py        # Validation script (executed, not loaded)
└── templates/         # Supporting resources
    └── form.md
```

## Security Considerations

When installing or creating skills:
- **Review script contents** before installation
- **Sandbox execution** where possible
- **Limit permissions** to minimum required
- **Audit external dependencies** in bundled scripts

## Availability

Supported across:
- Claude.ai
- Claude Code
- Claude Agent SDK
- Claude Developer Platform

## Takeaways

1. **Progressive disclosure** prevents context bloat while maintaining capability
2. **Executable scripts** provide deterministic operations without context cost
3. **Metadata triggers** enable smart skill activation
4. **Layered architecture** balances capability with efficiency
5. **Security requires** careful review of bundled scripts
