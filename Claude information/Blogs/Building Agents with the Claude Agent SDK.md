# Building Agents with the Claude Agent SDK

**Source:** [Anthropic Engineering Blog](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
**Published:** September 29, 2025

## Overview

The Claude Agent SDK is a framework for developing autonomous agents based on the philosophy of giving agents a computer to work like humans do. This represents Anthropic's broader vision of agent development beyond just coding applications.

## Core Philosophy

Provide Claude with programmer tools:
- File discovery and navigation
- Code editing and linting
- Script execution
- Iterative debugging capabilities
- Terminal access for diverse digital tasks

## Agent Applications

The SDK supports building various agent types:

| Agent Type | Use Cases |
|------------|-----------|
| Finance Agents | Portfolio analysis, market research |
| Personal Assistants | Scheduling, travel planning |
| Customer Support | Complex request handling |
| Research Agents | Document synthesis, literature review |

## The Agent Loop

The fundamental operation pattern:

```
Gather Context -> Take Action -> Verify Work -> Repeat
```

### 1. Gathering Context

**Agentic Search & File Systems**
- Using bash commands like `grep` and `tail` for intelligent data retrieval
- Precise control over what information enters context

**Semantic Search**
- Faster but less accurate alternative
- Uses vector embeddings for similarity matching
- Good for exploratory searches

### 2. Taking Action

**Tools**
- Primary execution blocks
- Prominently featured in context
- Defined interfaces for specific operations

**Bash/Scripts**
- General-purpose computer access
- Flexible operations beyond defined tools
- System-level capabilities

**Code Generation**
- Precise, reusable outputs
- Complex operations expressed as code
- Can be saved and re-executed

**MCPs (Model Context Protocol)**
- Standardized integrations with external services
- Examples: Slack, GitHub, databases
- Consistent interface for service interaction

### 3. Verification Methods

| Method | Best For |
|--------|----------|
| Rule-based feedback | Code linting, syntax checks |
| Visual feedback | UI tasks (via screenshots) |
| LLM-as-judge | Fuzzy criteria, quality assessment |

## Advanced Patterns

### Subagents
- Enable parallelization of independent tasks
- Provide isolated context windows
- Prevent context pollution between tasks
- Can specialize in different domains

### Compaction
- Automatic summarization when approaching context limits
- Preserves critical information while freeing space
- Enables longer-running agent sessions

## Testing and Iteration

Key evaluation questions:
1. Does the agent understand tasks correctly?
2. Can it identify and fix repeated failures?
3. Should tool capabilities be expanded?
4. Are verification methods catching errors?

## Getting Started

1. Access the SDK at docs.claude.com
2. Existing Claude Code SDK users should review migration guide
3. Start with simple agent loops before adding complexity
4. Test thoroughly with verification at each step

## Takeaways

1. **Computer access** enables human-like problem solving
2. **The agent loop** (context -> action -> verify) is the core pattern
3. **Multiple action types** (tools, bash, code, MCPs) provide flexibility
4. **Verification is essential** - rule-based, visual, and LLM-based
5. **Subagents and compaction** extend agent capabilities
6. **Iterative development** with testing drives improvement
