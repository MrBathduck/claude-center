# Effective Context Engineering for AI Agents

**Source:** [Anthropic Engineering Blog](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
**Published:** 2025

## Overview

Context engineering is the natural progression of prompt engineering, focusing on curating optimal tokens during LLM inference rather than just writing effective prompts. The core challenge is optimizing token utility against inherent LLM constraints.

## Key Concept: The Attention Budget

Models experience "context rot" - as token count increases, recall accuracy decreases. This stems from the transformer architecture's n-squared pairwise token relationships, creating diminishing returns on longer contexts.

**Guiding Principle:** Find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome.

## Context Engineering vs. Prompt Engineering

| Aspect | Prompt Engineering | Context Engineering |
|--------|-------------------|---------------------|
| Focus | Writing effective prompts | Curating tokens across agent loops |
| Scope | Single interaction | Multi-turn sessions |
| Approach | Discrete | Iterative |
| Challenge | Clarity | Token efficiency |

## Anatomy of Effective Context

### System Prompts

**The Altitude Problem:**
- Too specific (hardcoded logic) = brittle
- Too vague = inconsistent behavior
- Goal: Find the right level of abstraction

**Organization Strategies:**
- Use XML tags or Markdown headers for structure
- Sections like `<background_information>` and `<instructions>`
- Clear separation of concerns

### Tool Design

| Principle | Rationale |
|-----------|-----------|
| Minimize overlap | Avoids ambiguous decision points |
| Ensure clarity | Agent knows when to use each tool |
| Token efficiency | Bloated toolsets waste context |
| Single responsibility | One tool, one purpose |

### Examples

- Include relevant examples in context
- Match example complexity to actual tasks
- Avoid examples that don't generalize

## Context Retrieval Strategies

### Pre-computed Retrieval
- Embeddings generated beforehand
- Fast lookup at runtime
- May miss nuanced relevance

### Just-In-Time Loading (Agentic Search)
- Dynamic loading during runtime
- Uses commands like `grep`, `head`, `tail`
- More accurate but requires more reasoning

**Claude Code Example:**
Maintains lightweight file path references and uses Bash commands for selective data loading without full object materialization.

## Long-Horizon Task Techniques

### 1. Compaction

Summarize conversation history while preserving:
- Architectural decisions
- Unresolved bugs
- Key context

Then reinitiate with compressed summary plus recent context.

### 2. Structured Note-Taking

Agents maintain persistent files (e.g., `NOTES.md`) outside the context window:
- Self-managed memory
- Survives context resets
- Enables multi-hour task coherence

### 3. Sub-Agent Architecture

Specialized agents handle focused tasks:
- Clean context windows for each sub-task
- Return 1,000-2,000 token summaries (not exhaustive outputs)
- Prevents context pollution

## Practical Techniques

### File System Navigation
```bash
# Selective loading instead of full file reads
head -n 50 file.py    # First 50 lines
tail -n 20 file.py    # Last 20 lines
grep -n "pattern" .   # Search with line numbers
```

### Context Organization
```xml
<system_context>
  <background_information>
    Project details and constraints
  </background_information>

  <instructions>
    Specific behavioral guidance
  </instructions>

  <tools>
    Available capabilities
  </tools>
</system_context>
```

## Common Anti-Patterns

1. **Loading everything** - Full files when snippets suffice
2. **Redundant context** - Same information in multiple forms
3. **Stale information** - Outdated context consuming tokens
4. **Excessive tools** - Too many options create confusion
5. **Verbose outputs** - Requesting more detail than needed

## Takeaways

1. **Context is finite** - Treat tokens as a precious budget
2. **Quality over quantity** - High-signal tokens beat more tokens
3. **Just-in-time loading** - Fetch what you need when you need it
4. **Structured notes** - External memory extends agent capabilities
5. **Sub-agents compartmentalize** - Clean context windows for focused tasks
6. **Compaction preserves** - Summarize to extend session length
