# Plan Phase Command

Transform a feature idea into a structured phase document ready for execution.

<feature_description>  $ARGUMENTS

</feature_description>

---

## RULE 0: Planning Only, No Implementation

You design and document. You NEVER write implementation code. This command produces a phase document that `/plan-execution` will use.

---

## WORKFLOW OVERVIEW

The plan-phase workflow involves multiple agents working together:

```
1. Architect Agent creates initial design (context gathering, structure)
2. System Agent validates and refines (checks for conflicts with existing architecture)
3. User reviews final plan
4. If approved, plan-execution begins
```

Each step is mandatory. Do NOT proceed to the next step if the current step identifies blocking issues.

---

## EXECUTION PROTOCOL

### STEP 0: Mode Detection

Assess the feature scope to determine workflow mode:

| Mode | Scope | Approach |
|------|-------|----------|
| **Quick** | < 1 day, 1-3 files | Skip this command, use `/quick-fix` |
| **Standard** | 1-5 days, 3-10 files | Create phase doc, single phase |
| **Full** | > 5 days, 10+ files | Create phase doc with multiple subphases |

If Quick mode is appropriate, inform the user and suggest `/quick-fix` instead.

### STEP 1: Context Gathering (MANDATORY)

Before planning, gather context using the Explore agent:

```
Use Task tool with:
- subagent_type: "Explore"
- prompt: "Analyze the codebase for implementing: [feature]
  Questions:
  1) What existing files/patterns relate to this feature?
  2) What dependencies exist?
  3) What tests cover related functionality?
  4) What SCSS/JS modules might be affected?
  5) Are there similar features to reference?
  Return: File inventory, pattern summary, existing conventions"
```

### STEP 2: Check Feature Map for Conflicts

Read `/docs/features/FEATURE_MAP.md` (if exists) to identify:
- Shared state clusters this feature might touch
- Critical paths that could be affected
- Related features that need consideration

### STEP 3: System Validation (System Agent)

**This is Phase 2 of the workflow: System Agent validates the design.**

After context gathering and conflict check, invoke **System Agent** to:
- Verify design doesn't conflict with existing architecture
- Check for potential breaking changes
- Identify cross-system interactions
- Refine the phase plan if issues found

The System Agent will edit the phase plan directly if conflicts are detected.

```
Use Task tool with:
- subagent_type: "system-agent"
- prompt: "Perform impact analysis for: [feature]
  Check:
  - System constraints (auth, data model, architecture)
  - Existing ADRs that apply
  - Affected features from FEATURE_MAP
  - Technical Anchors needed
  - Cross-system interactions and dependencies
  - Potential breaking changes to existing features
  Return: Impact report with PROCEED/BLOCK/PROCEED WITH CAUTION"
```

**System Agent Response Handling:**

| Response | Action |
|----------|--------|
| PROCEED | Continue to STEP 4 |
| PROCEED WITH CAUTION | Continue but document risks in phase plan |
| BLOCK | Stop and report blocking issues to user |

If system-agent returns BLOCK, stop and report the blocking issues to the user.

### Handling Conflicts

If System Agent detects conflicts:
1. System Agent adds `## Conflict Detected` section to phase plan
2. Plan returns to Architect for review
3. Architect either accepts resolution or proposes alternative
4. User makes final decision on unresolved conflicts

Do NOT proceed to implementation with unresolved conflicts.

### STEP 4: Design the Phase Document

Create the phase document following the template at `.claude/plans/_TEMPLATE-phase.md`.

**Required sections:**
1. YAML frontmatter (title, status: draft, created, author: architect-agent)
2. Overview (2-3 sentences)
3. Success Criteria (measurable, checkbox format)
4. Dependencies (with ADR/notes references)
5. Subphases with:
   - Implementation Tasks (checkbox format)
   - Primary Files (may expand during implementation)
   - Edge Cases to handle
   - Verification steps
6. Quality Gates section
7. Senior Developer Review section (placeholder)

### STEP 5: Senior Developer Review (MANDATORY - Agent Step)

**This is automatic, not a human review.**

After drafting the phase document, adopt the persona of a senior developer who:
- Hates the project and looks for any excuse to reject
- Has seen every failure mode
- Demands proof, not promises

Review the document adversarially for:
- **Weak spots**: Vague requirements, missing acceptance criteria
- **Missing edge cases**: Error states, empty states, concurrent access
- **Unrealistic scope**: Too much for one phase, hidden complexity
- **Unaddressed failure modes**: What happens when X fails?
- **Testing gaps**: Untestable requirements, missing integration tests
- **Dependency risks**: External services, timing assumptions

**Fix every issue you find.** Then document what you found and fixed in the "Senior Developer Review (Agent)" section:

```markdown
### Senior Developer Review (Agent)
Reviewed: [DATE]

**Issues Found & Fixed:**
- [Issue]: [How addressed]
- [Issue]: [How addressed]
```

### STEP 6: Present to User

Present the completed phase document to the user with:
1. Summary of what's planned
2. Key decisions made
3. System Agent validation results (conflicts detected and resolved)
4. Risks identified
5. Senior Developer Review findings
6. Next steps (Gemini verification, then `/plan-execution`)

**Important:** If there are unresolved conflicts from System Agent validation, clearly highlight them and request user decision before proceeding.

---

## PHASE DOCUMENT STRUCTURE

```markdown
---
title: "Phase X.Y: [Feature Name]"
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: architect-agent
tags:
  - [feature-area]
  - [ui | backend | database | integration]
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
| [What's needed] | [ADR-XXX or /docs/dev/notes/ link] | Pending/Ready |

## Phase Completion Criteria

This phase is DONE when:
- [ ] All subphase tasks completed
- [ ] All manual verifications passed
- [ ] [Any phase-specific criteria]

---

## Subphase 1: [Name]

### Description
[What this subphase accomplishes]

### Implementation Tasks
- [ ] Task 1: [Specific, actionable description]
- [ ] Task 2: [Specific, actionable description]

### Primary Files (may expand)
- `path/to/file1.py` - [What changes]
- `path/to/file2.ts` - [What changes]

### Edge Cases
- [ ] Handle case when [scenario 1]
- [ ] Handle case when [scenario 2]

### Verification
- [ ] Unit tests written and passing
- [ ] Manual testing completed

---

## Quality Gates

### Documentation Quality
- [ ] YAML frontmatter complete and accurate
- [ ] All tasks have checkbox format
- [ ] Success criteria are measurable
- [ ] Dependencies explicitly listed

### External Validation
- [ ] Verified through Gemini LLM (date: ___________)

### System Agent Validation
- [ ] System Agent impact analysis completed (see notes below)
- [ ] No unresolved conflicts (or documented with resolution)

### Agent Review
- [ ] Senior Developer Review completed by agent (see notes below)

### Approval
- [ ] Document status changed to "approved"
- [ ] Ready for `/plan-execution`

---

### System Agent Validation

> Automatically populated during planning by System Agent.

**Validated:** YYYY-MM-DD
**Recommendation:** [PROCEED|BLOCK|PROCEED WITH CAUTION]

**Architecture Check:**
- Conflicts with existing architecture: [None or describe]
- Breaking changes identified: [None or describe]
- Cross-system interactions: [List]

**Resolved Conflicts:**
- [Conflict 1]: [Resolution]
- [Conflict 2]: [Resolution]

**Unresolved Conflicts (if any):**
- [Conflict]: [Awaiting user decision]

---

### Senior Developer Review (Agent)

> Automatically populated during planning.

**Reviewed:** YYYY-MM-DD

**Issues Found & Fixed:**
- [Issue 1]: [How addressed]
- [Issue 2]: [How addressed]

---

## Deferred Tasks

> Tasks that cannot be completed in this phase.

| Task | Reason | Target Phase |
|------|--------|--------------|

---

## Execution Log

| Date | Subphase | Status | Notes |
|------|----------|--------|-------|
```

---

## DELEGATION REFERENCE

| Situation | Delegate To |
|-----------|-------------|
| Codebase exploration | Explore agent |
| Impact analysis | system-agent |
| API design needed | api-designer |
| Database changes needed | migration-planner |
| UI/UX design needed | ui-ux-designer |

---

## QUALITY CHECKLIST (Before Presenting)

Before presenting the phase document to the user, verify:

- [ ] All tasks are specific and actionable (not vague)
- [ ] Success criteria are measurable (not subjective)
- [ ] Edge cases are enumerated
- [ ] Dependencies are explicit with references
- [ ] System Agent validation completed (no unresolved conflicts)
- [ ] Senior Developer Review completed
- [ ] No implementation code in the document
- [ ] Scope is realistic for the mode (Standard/Full)

**Final plan must include:**
- Original architect design
- System Agent validation results
- Any resolved conflicts documented

---

## FORBIDDEN ACTIONS

- Writing implementation code
- Skipping System Agent validation
- Skipping impact analysis
- Skipping Senior Developer Review
- Creating phase docs for Quick mode tasks
- Leaving vague requirements ("make it better")
- Assuming dependencies are ready without checking
- Proceeding to implementation with unresolved conflicts

## REQUIRED ACTIONS

- Gather context before planning
- Check Feature Map for conflicts
- Run System Agent validation (Phase 2 of workflow)
- Apply Senior Developer Review adversarially
- Document all findings and fixes
- Document System Agent validation results
- Resolve or escalate all conflicts before presenting
- Present clear next steps to user
