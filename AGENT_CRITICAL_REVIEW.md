# Agent Critical Review: A Senior Developer's Perspective

> **Review Date:** 2026-01-19
> **Reviewer Stance:** Senior developer who is skeptical of this setup
> **Purpose:** Identify gaps, missing guardrails, and failure modes in the agent system

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Agent-by-Agent Analysis](#agent-by-agent-analysis)
3. [Systemic Issues Across All Agents](#systemic-issues-across-all-agents)
4. [Real-World Issues That Would Be Missed](#real-world-issues-that-would-be-missed)
5. [Gap Analysis: Agents vs Reality](#gap-analysis-agents-vs-reality)
6. [Recommendations](#recommendations)
7. [Priority Action Items](#priority-action-items)

---

## Executive Summary

### The Core Problem

These agent definitions suffer from fundamental design problems:
- **Inconsistent constraint enforcement**
- **Unclear handoff protocols**
- **Vague failure recovery**
- **Scope boundaries that exist on paper but have no enforcement mechanism**

The "penalty" system (e.g., "-$1000") is pure theater with no actual enforcement.

### By The Numbers

| Metric | Finding |
|--------|---------|
| Total agents reviewed | 14 |
| Agents with scope creep risk | 8 (57%) |
| Agents with undefined handoffs | 11 (79%) |
| Agents with hardcoded paths | 6 (43%) |
| Overlapping responsibilities | 4 major conflicts |
| Real issues these agents would catch | ~20% |

### The Brutal Truth

**From 450+ real issues found in project reviews, the current agents would catch maybe 20%.** The agents are designed for reviewing new code shown to them, but are completely blind to existing codebase problems.

---

## Agent-by-Agent Analysis

### 1. architect.md

**Purpose:** Design complete solutions before implementation

#### Scope Creep Risk: HIGH

- Lines 31-37 list responsibilities that overlap heavily with `system-agent.md` (security considerations, technical debt, performance bottlenecks). Who owns what?
- "Design complete solutions" is dangerously broad. What stops this from becoming a 50-page document?
**comments Developper :** 
- THe system agent is a follow-up of the architect agent. The system agent needs to verify what the architect agent has designed and needs to verify how this influences the rest of the software. It needs to verify how it will interact with other parts, how there is interaction between the system created & system that exists, and how, possibly, the new system may break the old system. From his founding, the system needs to make the necessary changes to the phase plan so that it is better. 
*Question: Do we need to allow the system agent to write or not?* 
- Each phase file can only be maximum 2000 lines or a maximum of 22K tokens. 

#### Missing Guardrails

- No maximum output length defined despite calling for "concise" responses
- No limit on analysis depth. "Read relevant code with Grep/Glob (targeted, not exhaustive)" - but what defines "exhaustive"?
- Circuit breakers require "user confirmation" but what if the user rubber-stamps everything?
**comments Developper :** 
- Each phase file can only be maximum 2000 lines or a maximum of 22K tokens
- *question:* How can we define what depth of analysis is correct for this agent? 
- The architect agent needs to use the 'askuserquestiontool'

#### Collaboration Gaps

- How does architect hand off to developer? No explicit protocol
- Says "NEVER write implementation code" but then provides implementation step templates with `[file_path:line_number]` - what is the developer supposed to do with this?
**comments Developper :** 
- Architect makes a plan, and the plan is verified by the the human developper. Once approved, it automaticly goes to the developper agent as written in the plan-execution command. 

#### Output Vagueness

- "Enumerate EVERY test required" - but `test-writer.md` exists. Who decides which tests? Duplication guaranteed.
**comments Developper :** 
- Architect can not write tests. Architect only makes a plan and gives the goals, the criteria, and the what's included and what not

#### Failure Modes

- What happens when existing architecture patterns conflict? No conflict resolution protocol.
- No escalation path when circuit breakers are tripped.
**comments Developper :** 
- The system agent needs to verify the plan of the architect agent so that it is not conflicting with system agent. 

**Additional comments Developper :** 
- Do we need to update the command "plan-phase" to let the architect agent & the system agent work together?

---

### 2. developer.md

**Purpose:** Implement specifications from architect

#### Scope Creep Risk: MEDIUM

- "NEVER make design decisions" conflicts with "Ask for clarification when specifications are incomplete". The line between "clarification" and "design decision" is blurry.
**comments Developper :** 
- The developper agent needs to use the askuserquestiontool in case it is confronted with a decision. 

#### Missing Guardrails

- Hard-coded commands `npm run build:css`, `ruff check app/` - what if the project uses different tooling? The agent will fail silently or error out.
- No timeout or retry limits for validation cycles
**comments Developper :** 
- Let's mark this also as a question that the user needs to be asked with the setup guide.md

#### Collaboration Gaps

- References "specifications" repeatedly but never defines what format those should come in from architect
- No protocol for "specs are incomplete, I asked, but answer was still unclear"
**comments Developper :** 
- Specifications are coming from the phase plan, but the developper agent can also be called in when there is not a phase plan. For example if the debugger agent has found a bug/issue
- Use the askuserquestiontool

#### Output Vagueness

- "Implementation Complete" output format is good, but no error categorization. A lint failure and a test failure are treated identically.
**comments Developper :** 
- *question: How should we handle this situation?*

#### Failure Modes

- "The orchestrator will NOT re-read files to verify your work" - so if developer lies or misreports, no one catches it
- No retry protocol when linting fails repeatedly
**comments Developper :** 
- Normally, in the plan-execution command, the last agent to be used is the quality reviewer agent who will verify the work
- *question: How should we handle this situation?*

---

### 3. quality-reviewer.md

**Purpose:** Review code for real issues

#### Scope Creep Risk: LOW (actually well-constrained)

#### Missing Guardrails

- "NEVER review without being asked by architect" - but nothing enforces this. Any user can invoke the reviewer directly.
- No maximum number of issues to flag. Could dump 50 findings and overwhelm.
**comments Developper :** 
- This is okay. The user may invoke this. 
- That is okay. If we have 50 issues, it means we have a lot of issues to fix. 

#### Collaboration Gaps

- Issues found go... where? No handoff protocol to developer or architect.
- What if reviewer and architect disagree? No conflict resolution.
**comments Developper :** 
- The issues go into terminal for the user to read & solve. if the plan execution was called in, the developper will solve issues immediatly. 
- that is okay. 

#### Output Vagueness

- "State your verdict clearly" but no defined verdict options (PASS/FAIL/CONDITIONAL?)
- No severity classification in output format
**comments Developper :** 
- Give it a letter grading
- It already does so 

#### Failure Modes

- Reviewer can only read, not run code. How does it verify concurrency bugs without execution?
- "Verify against production scenarios" - how? It cannot access production.
**comments Developper :** 
- The developper will solve the issues. 
---

### 4. debugger.md

**Purpose:** Investigate and diagnose bugs

#### Scope Creep Risk: HIGH

- Has Bash access but "NEVER implement fixes". Nothing stops it from running `git commit` or deploying.
- "Create test files" but `test-writer.md` exists. Who owns test files?
**comments Developper :** 
*question: How can we solve this? The debugger agent hands off the work to the developper agent*

#### Missing Guardrails

- Uses `disallowedTools: Write, Edit` but then describes writing debug statements and test files. **Contradiction.** Either the frontmatter is wrong or the instructions are wrong.
- "$2000 penalty" / "$1000 penalty" - pure fiction with no enforcement mechanism
**comments Developper :** 
*question: How can we solve this? The debugger agent hands off the work to the developper agent*
- Remove all the penalty amounts everywhere

#### Collaboration Gaps

- Output is "FIX STRATEGY" but developer needs actual specs. Who translates?
- "zen analyze", "zen consensus", "zen thinkdeep" - undefined tools. What are these?

#### Output Vagueness

- "High-level approach, NO implementation" - so after all that debugging, someone else has to figure out the actual fix?
**comments Developper :** 
- Yes, the developper agent

#### Failure Modes

- "ALL debug statements MUST be removed" - but if debugger crashes mid-session, who cleans up?
- No timeout on investigation. Could run forever.

---

### 5. ui-ux-designer.md

**Purpose:** Design user interfaces and experiences

#### Scope Creep Risk: HIGH

- Has Write, Edit, Bash tools but "MUST NOT write full React/Vue/Python files". What stops it?
- "You MAY provide CSS snippets, HTML structures" - slippery slope to "just one more component"
**comments Developper :** 
- Does this need to be fixed? what is your opinion on this?

#### Missing Guardrails

- No file size limits on "illustrative code"
- "MUST check CLAUDE.md and scan the project" - but what if project has no design system? Says "ask the user" but no fallback behavior defined.
**comments Developper :** 
- How should we setup the design system? Can this be done through, for example, 'claude.scss.md' ?

#### Collaboration Gaps

- Produces "Design Specifications" but `developer.md` never references receiving them
- "Request confirmation" for new components - from whom? Architect? User?
**comments Developper :** 
- the UI/ux designer often is used in the plan-execution command

#### Output Vagueness

- ASCII art wireframes - is this actually useful to developers?
- "Animation timing" specs but no way to validate they actually work
**comments Developper :** 
- Yes, useful! 
- What is animation timing? 

#### Failure Modes

- What if existing design system is inconsistent? No handling.
- No protocol for "user rejected my design"
**comments Developper :** 
- It needs to follow the already existing design elements that have been created. 
- Ask the user again for other designs

**Additional comments Developper :**
- Currently, the UI/UX designer does not take in consideration the variables that exist in the sytem already or modals & frameworks that already exists. It needs to verify & use the correct UI/UX system that is already implemented (if it exists).
- My current assesment of this agent is that it is not thinking outside the box on how it can improve user interface & especially user experience. I believe that the UI/UX agent needs also to ask the developper (human) questions on what is best? The askuserquestiontool is ideal for this. 
*Question: How can we improve further the design skills of this agent* 

---

### 6. api-designer.md

**Purpose:** Design REST API endpoints

#### Scope Creep Risk: LOW (well-constrained with `disallowedTools`)

#### Missing Guardrails

- Hard-codes Flask-specific file paths: `Docs/Development Docs/03-api-design.md`, `app/utils/error_codes.py`. If project structure differs, agent will fail or hallucinate.
- Error codes MUST exist in `error_codes.py` - but what if file does not exist?
**comments Developper :** 
- With our new system of docs, can we redirect them their, without hardcoding the location? 
- Is this a standard file that exists in most software programs? or can we just mention error code file?

#### Collaboration Gaps

- "The developer implements based on your specifications" - but `developer.md` never references API specs
- No review cycle - designs go straight to implementation?
**comments Developper :** 
- Tell me how to improve? 

#### Output Vagueness

- Specification template is detailed (good)
- But "NEW ERROR CODE REQUIRED" goes... where? Who creates it?
**comments Developper :** 
- Tell me how to improve? 

#### Failure Modes

- If existing API patterns are inconsistent, no conflict resolution
- No versioning consideration for breaking changes
**comments Developper :** 
- We need to make sure that patterns are consistent. It will help us in later phases

---

### 7. migration-planner.md

**Purpose:** Plan database migrations safely

#### Scope Creep Risk: LOW (well-constrained)

#### Missing Guardrails

- Hard-codes PostgreSQL patterns but also mentions "SQLite compatibility". Which is it?
- No limit on analysis depth for complex migrations
**comments Developper :** 
- How can we improve on this?

#### Collaboration Gaps

- Who executes the migration after planning? No handoff defined.
- "Verify downgrade works" - but planner cannot run migrations. Who verifies?
**comments Developper :** 
- can the developper execute & verify this?

#### Output Vagueness

- "Pre-Migration Checklist" includes "Backup database" - but this is operations work, not planning
**comments Developper :** 
- Tell me how to improve?

#### Failure Modes

- What if existing migration history is corrupt or inconsistent?
- No rollback monitoring after migration is run by someone else
**comments Developper :** 
- Tell me how to improve?
---

### 8. test-writer.md

**Purpose:** Write comprehensive tests

#### Scope Creep Risk: MEDIUM

- "NEVER write implementation code" but creating test fixtures often requires understanding implementation deeply
- Factory patterns are very specific to one project - will fail on others

#### Missing Guardrails

- Coverage targets are hard-coded: "Models: 90%+". What if CLAUDE.md specifies different targets?
- No maximum test file size

#### Collaboration Gaps

- `architect.md` says "enumerate EVERY test required". `test-writer.md` receives... what? No input format defined.
- Who reviews tests? `quality-reviewer.md` does not mention test review.

#### Output Vagueness

- Output format is good but no error case (what if tests cannot be written?)

#### Failure Modes

- If factories are missing or broken, agent has no fallback
- No retry protocol for flaky test failures

---

### 9. feature-steward.md

**Purpose:** Keep Feature Canon in sync with code

#### Scope Creep Risk: MEDIUM

- "Canon follows code" but agent cannot run code (no Bash). How does it verify?
- "Run or review the feature" - cannot run without Bash.

#### Missing Guardrails

- Done Level transitions (L1->L2->L3) have no enforcement mechanism
- What stops Canon from being updated for aspirational behavior? Only honor system.

#### Collaboration Gaps

- "Flag for System Archivist" but no notification mechanism
- How does this coordinate with developer completing work?

#### Output Vagueness

- Output format is clear but "Flags" section is free-form

#### Failure Modes

- If code and Canon disagree, agent is told to "investigate which is correct" but has no execution capability
- What if FEATURE_INDEX.md is corrupted or missing?

---

### 10. system-archivist.md

**Purpose:** Update system docs for structural changes

#### Scope Creep Risk: LOW (well-constrained)

#### Missing Guardrails

- "ADRs are append-only. Never edit existing ADRs." - but tool has Edit capability. Nothing enforces this.
- No maximum number of updates per session

#### Collaboration Gaps

- "Notify Feature Steward" - how? No mechanism defined.
- Both `system-archivist` and `adr-writer` deal with ADRs. Who owns what?

#### Output Vagueness

- "No Action Taken" output option is good for clarity

#### Failure Modes

- If system docs are already stale or conflicting, no recovery protocol
- ADR numbering conflicts if multiple sessions run concurrently

---

### 11. system-agent.md

**Purpose:** Impact analysis before coding

#### Scope Creep Risk: MEDIUM

- Analysis scope is broad: auth, data, architecture, deployment, features
- "Block if unresolved conflicts exist" but agent has no blocking mechanism

#### Missing Guardrails

- "Flag for System Archivist" repeated but never defines the flagging mechanism
- Impact analysis checklist has no minimum completion requirement

#### Collaboration Gaps

- Writes Technical Anchors in Feature Canon but Feature Steward also writes Canon. Conflict.
- "Block execution" - blocks whom? How?

#### Output Vagueness

- Recommendation format has PROCEED/BLOCK/PROCEED WITH CAUTION but no criteria for each

#### Failure Modes

- If FEATURE_MAP.md does not exist, agent fails silently
- "Assume isolated features are truly isolated" warning exists but no verification method

---

### 12. adr-writer.md

**Purpose:** Create Architecture Decision Records

#### Scope Creep Risk: MEDIUM

- Very detailed ADR structure (good) but overlaps with `system-archivist.md`
- "Create backlink tasks" - task management tool? Not in tools list.

#### Missing Guardrails

- 5 relationship types are strictly defined (good constraint)
- But "Fallback rule" allows deviation - weakens constraint

#### Collaboration Gaps

- `system-archivist.md` also creates ADRs. Who is primary?
- No review cycle for ADR quality

#### Output Vagueness

- Template is extremely detailed - possibly over-specified

#### Failure Modes

- If ADR index does not exist, discovery workflow fails
- Concurrent ADR creation could cause numbering conflicts

---

### 13. technical-writer.md

**Purpose:** Create documentation after feature completion

#### Scope Creep Risk: LOW

#### Missing Guardrails

- Token limits (150/100) are arbitrary and cannot be enforced by the system
- "Count tokens before finalizing" - agent cannot actually count tokens

#### Collaboration Gaps

- "Document completed features after implementation" - but when is implementation "complete"? Who signals this?
- Creates ADRs but `adr-writer.md` is dedicated ADR agent. Duplication.

#### Output Vagueness

- Token counting heuristic is approximate and unreliable

#### Failure Modes

- What if implementation is not actually working despite being "complete"?
- No verification that examples actually work

---

### 14. qa-validator.md

**Purpose:** Validate features work end-to-end

#### Scope Creep Risk: MEDIUM

- Has all tools including Write, Edit but described as validator, not implementer
- "Execute the test now" - can write test files, potentially permanent changes

#### Missing Guardrails

- Database query patterns assume Flask/SQLAlchemy - will fail on other stacks
- Hard-coded patterns for `app/models` paths

#### Collaboration Gaps

- Who fixes failing tests? No handoff to developer.
- PASS/FAIL goes... where? No escalation.

#### Output Vagueness

- Output format is very detailed (good)
- But "Issues Found" section is free-form

#### Failure Modes

- If database access fails, all patterns break
- No retry limits for flaky tests
- Browser tools not in tools list but referenced throughout

---

## Systemic Issues Across All Agents

### Issue 1: The Penalty System is Theater

Lines like "-$1000 penalty" and "-$2000 penalty" appear in multiple agents. There is **no mechanism to enforce these**. They are psychological prompts at best.

**Agents affected:** debugger.md, developer.md, others

**Example:**
```markdown
- Creating new factories when appropriate ones exist: -$1000 penalty
```

**Reality:** Nothing stops the agent from doing this. No hook checks for it. No validation occurs.

---

### Issue 2: No Actual Enforcement of Tool Restrictions

`disallowedTools` in frontmatter is a good idea, but many agents describe behaviors that would require those tools.

**Example:** `debugger.md` disallows Write/Edit but describes creating test files.

**Contradiction Matrix:**

| Agent | Disallowed | But Instructions Say |
|-------|------------|---------------------|
| debugger.md | Write, Edit | "Create test files" |
| ui-ux-designer.md | (none) | "MUST NOT write full React/Vue/Python files" |
| quality-reviewer.md | Write, Edit, Bash | "Verify against production scenarios" |

---

### Issue 3: Hardcoded Project Assumptions

Multiple agents assume Flask/SQLAlchemy project structure:

| Agent | Hardcoded Assumption |
|-------|---------------------|
| developer.md | `npm run build:css`, `ruff check app/`, `pytest tests/` |
| test-writer.md | `tests/factories.py`, `tests/conftest.py`, `app/utils/error_codes.py` |
| api-designer.md | `Docs/Development Docs/03-api-design.md`, `app/utils/error_codes.py` |
| migration-planner.md | All patterns are Flask/SQLAlchemy/PostgreSQL specific |
| qa-validator.md | `app/models` paths, Flask-SQLAlchemy queries |

**Impact:** These agents will fail silently or produce wrong output on projects with different structures.

---

### Issue 4: Undefined Handoff Mechanisms

"Flag for X" appears constantly but no flagging mechanism exists:

| Agent | Says | Mechanism Defined? |
|-------|------|-------------------|
| system-agent.md | "Flag for System Archivist" | NO |
| system-archivist.md | "Notify Feature Steward" | NO |
| feature-steward.md | "flag for System Archivist" | NO |
| architect.md | "Hand off to developer" | NO |
| quality-reviewer.md | "Issues found" → ??? | NO |

**Impact:** Flags go nowhere. No agent checks the flag queue. Inter-agent communication is aspirational, not actual.

---

### Issue 5: No Failure Recovery Protocols

No agent has instructions for:
- What to do if required file (CLAUDE.md) is missing
- What to do if pattern can't be determined
- What to do if stuck in loop
- Maximum iterations before escalating

**Impact:** Agents can loop forever, produce garbage, or silently fail.

---

### Issue 6: Overlapping Responsibilities

Multiple agents claim ownership of the same artifacts:

#### ADR Ownership Conflict
| Agent | ADR Involvement |
|-------|-----------------|
| architect.md | "When asked, use this format..." |
| adr-writer.md | Entire purpose is ADR writing |
| system-archivist.md | Creates ADRs for structural changes |
| technical-writer.md | Has ADR format section |

**Who actually owns ADRs?** Nobody knows.

#### Test Ownership Conflict
| Agent | Test Involvement |
|-------|-----------------|
| architect.md | "Enumerate EVERY test required" |
| test-writer.md | Entire purpose is writing tests |
| debugger.md | "Create test files" |
| qa-validator.md | Can write test files |

**Who actually owns tests?** Nobody knows.

#### Feature Canon Ownership Conflict
| Agent | Canon Involvement |
|-------|-------------------|
| feature-steward.md | Primary Canon maintainer |
| system-agent.md | Writes Technical Anchors in Canon |

**What if they write conflicting information?** Nobody knows.

---

### Issue 7: "Check CLAUDE.md" is Not a Guardrail

Every agent says "check CLAUDE.md" but:
- CLAUDE.md might not have the information they need
- No fallback behavior is defined
- No error handling if CLAUDE.md is missing or incomplete

**Example failure:** Agent needs CSS build command, CLAUDE.md doesn't specify one, agent either guesses wrong or crashes.

---

## Real-World Issues That Would Be Missed

Based on analysis of 450+ issues found in actual project reviews, here's what the agents would miss:

### Code Quality Issues Found in Real Projects

| Issue | Lines Affected | Would Agents Catch? |
|-------|---------------|---------------------|
| 6 duplicate `escapeHtml()` implementations | 60+ | **NO** |
| 6 duplicate `showToast()` implementations | 60+ | **NO** |
| 6 duplicate `getCsrfToken()` implementations | 30+ | **NO** |
| 4 duplicate `debounce()` implementations | 40+ | **NO** |
| Registration table rows duplication | 324+ | **NO** |
| Document options duplication | 650+ | **NO** |
| 3 different JavaScript patterns (IIFE, ES6, Global) | Codebase-wide | **NO** |
| Monolithic files (1,454+ lines) | Multiple files | **NO** |
| Inconsistent service return patterns | 4 patterns | **MAYBE** |

**Total duplicated code: 900+ lines that agents would not detect.**

---

### Architecture Issues Found in Real Projects

| Issue | Would Agents Catch? | Why Not? |
|-------|---------------------|----------|
| Business logic in templates (capacity calculations in Jinja2) | **PARTIAL** | `pattern-enforcer` skill might catch |
| Authorization in routes instead of services | **NO** | No agent checks placement |
| Services return 4 different patterns (tuple, exception, boolean, dict) | **NO** | No interface contract enforcement |
| No shared JS utility library | **NO** | No frontend architecture ownership |
| Dual route handler architecture | **NO** | No duplication detection |

---

### Security Issues Found in Real Projects

| Issue | Severity | Would Agents Catch? | Why Not? |
|-------|----------|---------------------|----------|
| Missing note ownership validation | CRITICAL | **NO** | No resource ownership check protocol |
| No validation for negative page numbers | HIGH | **NO** | No input boundary validation checklist |
| Incomplete `escapeHtml()` missing quote escaping | HIGH | **NO** | No sanitization completeness check |
| CSV injection risk | MEDIUM | **NO** | Not in any "MUST FLAG" list |
| Missing CSRF on exports | MEDIUM | **NO** | CSRF not mentioned anywhere |
| Certificate endpoint missing auth | CRITICAL | **PARTIAL** | Generic "missing auth" mention only |

---

### Performance Issues Found in Real Projects

| Issue | Impact | Would Agents Catch? | Why Not? |
|-------|--------|---------------------|----------|
| N+1 queries in 15+ places | 100 items = 301 queries | **NO** | No N+1 detection protocol |
| Missing pagination on multiple endpoints | Memory exhaustion | **PARTIAL** | `api-designer` requires it for new, not existing |
| Chart memory leaks | Browser crashes | **NO** | No frontend memory leak detection |
| In-memory pagination | Performance | **NO** | No pattern detection |
| Missing database indexes | Slow queries | **NO** | Not checked |

---

### Testing Issues Found in Real Projects

| Issue | Would Agents Catch? | Why Not? |
|-------|---------------------|----------|
| No frontend JavaScript tests | **NO** | `test-writer.md` is 100% Python |
| No N+1 query count tests | **NO** | No performance test patterns |
| 80% of services missing logging | **PARTIAL** | `pattern-enforcer` might catch |
| No visual regression tests | **NO** | Not mentioned anywhere |
| No filter operator tests | **NO** | Specific patterns not enumerated |

---

## Gap Analysis: Agents vs Reality

### Coverage Matrix

| Issue Category | Responsible Agent | Detection Rate | Gap |
|----------------|-------------------|----------------|-----|
| Code Duplication | quality-reviewer | ~5% | No search protocol |
| N+1 Queries | quality-reviewer | ~0% | No pattern recognition |
| Security (Auth) | quality-reviewer | ~30% | Generic, not specific |
| Security (Validation) | api-designer, quality-reviewer | ~20% | No boundary checks |
| Frontend Quality | ui-ux-designer | ~10% | Design focus, not code quality |
| Frontend Testing | test-writer | ~0% | Python-only |
| Architecture Violations | architect, pattern-enforcer | ~40% | Review-only, no search |
| Documentation Gaps | technical-writer | ~30% | No validation |

### Root Cause Analysis

**Why do agents miss so much?**

1. **Agents review what's shown, not what exists**
   - No agent actively searches the codebase for problems
   - They wait for code to be presented for review

2. **No duplication detection**
   - Before writing ANY utility function, agents should search for existing implementations
   - This doesn't happen

3. **No cross-file pattern analysis**
   - 3 different JavaScript patterns coexist
   - No agent detects this inconsistency

4. **Security is checklist theater**
   - "Check for missing authentication" is too vague
   - Need specific patterns: "Every .get(id) needs ownership check"

5. **Performance is an afterthought**
   - N+1 queries are the #1 performance killer
   - No agent knows how to detect them

---

## Recommendations

### New Skills Needed

#### 1. duplication-detector (NEW SKILL)

**Purpose:** Actively search for duplicate code patterns

**Triggers:**
- Before any PR review
- Weekly codebase scan
- When adding new utility functions

**Checks:**
- Functions with similar names across files
- Identical code blocks > 10 lines
- Copy-paste detection heuristics
- Utility function candidates (used in 3+ files)

**Would catch:** 900+ lines of duplicated code

---

#### 2. n-plus-one-detector (NEW SKILL)

**Purpose:** Detect N+1 query patterns in ORM code

**Triggers:**
- When editing model relationship code
- When editing code with loops over querysets
- During PR review

**Checks:**
- Loops that access relationship attributes
- Missing `joinedload`/`selectinload` calls
- Query count in tests (if available)

**Would catch:** 15+ N+1 query patterns

---

#### 3. security-ownership-validator (NEW SKILL)

**Purpose:** Verify resource ownership checks exist

**Triggers:**
- When editing routes that access user-owned resources
- When adding new CRUD endpoints
- During security review

**Checks:**
- All `.get()` calls verify ownership
- No direct ID access without ownership check
- CSRF protection on state-changing operations
- Input sanitization completeness

**Would catch:** Authorization bypass bugs, CSRF gaps

---

### New Agent Needed

#### frontend-reviewer (NEW AGENT)

**Purpose:** JavaScript/frontend code quality and testing

**Responsibilities:**
- JavaScript pattern consistency enforcement
- Frontend test coverage tracking
- Memory leak detection in component lifecycle
- Shared utility library enforcement

**Would catch:**
- 6 duplicate `escapeHtml()` implementations
- 3 different JS patterns (IIFE, ES6 Class, Global Namespace)
- Chart memory leaks
- Missing frontend tests

---

### Agent Modifications Needed

#### quality-reviewer.md - Add Search Protocol

**Add before review begins:**
```markdown
## Pre-Review Search Protocol

BEFORE reviewing code, actively search for systemic issues:

### Step 1: Duplicate Detection
- Search for function definitions matching new/changed code
- Pattern: Function with same name in multiple files
- Action: Flag if same function implemented > 1 place

### Step 2: N+1 Query Detection
- Search in code being reviewed for loops over relationships
- Verify each has `joinedload()` or `selectinload()` in query
- Pattern: `for item in parent.children:` without eager loading
- Action: Flag as PERFORMANCE KILLER

### Step 3: Ownership Validation
- For every route that accesses a resource by ID
- Verify ownership check exists
- Pattern: `Model.query.get(id)` without `.filter(owner_id=current_user.id)`
- Action: Flag as SECURITY VULNERABILITY
```

---

#### developer.md - Remove Hardcoded Commands

**Replace hardcoded commands with:**
```markdown
## Build Environment
Check CLAUDE.md for:
- CSS build command (e.g., `npm run build:css`)
- Linting command (e.g., `ruff check app/`)
- Test command (e.g., `pytest tests/`)

If CLAUDE.md missing these, ask user before proceeding.
```

**Add duplication prevention:**
```markdown
## Duplication Prevention
BEFORE writing any utility function:
1. Search codebase for existing implementations
2. Search for similar functionality
3. If found: Reuse existing, do not create duplicate
4. If not found: Add to shared utilities (check CLAUDE.md for location)
```

---

#### All Agents - Add Failure Recovery

**Add to every agent:**
```markdown
## Failure Recovery Protocol

1. If CLAUDE.md missing: STOP and ask user for project context
2. If pattern unclear after 3 attempts: STOP and request clarification
3. If same error repeats 3 times: STOP and report blocker
4. Maximum iterations per task: 10 (configurable)
5. Stuck detection: If no progress in 5 iterations, summarize and escalate
```

---

#### All Agents - Add Handoff Protocol

**Add to every agent:**
```markdown
## Handoff Protocol

When flagging for another agent:
1. Create flag file: `.claude/flags/YYYY-MM-DD-<agent>-<topic>.md`
2. Flag file contains: trigger condition, source agent, target agent, context
3. Target agent MUST check `.claude/flags/` before completing ANY task
4. Target agent resolves flag OR escalates to user
```

---

### Ownership Clarification Needed

#### ADR Ownership
```
CLEAR OWNERSHIP:
- architect.md: RECOMMENDS ADR topics, DRAFTS inline ADR proposals
- adr-writer.md: WRITES formal ADR documents (called by architect)
- system-archivist.md: UPDATES ADR index, adds backlinks
- technical-writer.md: DOES NOT write ADRs (remove section)
```

#### Test Ownership
```
CLEAR OWNERSHIP:
- architect.md: Enumerates TEST SCENARIOS (what must be verified)
- test-writer.md: Converts scenarios to TEST IMPLEMENTATIONS (how to verify)
- test-writer.md MUST implement all architect scenarios + MAY add edge cases
```

---

## Priority Action Items

### P0 - Critical (Fix Immediately)

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | Add duplication detection to `quality-reviewer.md` | Catches 900+ lines duplicated code | Low |
| 2 | Add N+1 query detection to `quality-reviewer.md` | Catches 15+ performance issues | Low |
| 3 | Add ownership validation to security checklist | Catches authorization bypass | Low |

### P1 - High (Fix This Sprint)

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 4 | Create `frontend-reviewer` agent | Catches JS duplication, tests gap | Medium |
| 5 | Fix hardcoded paths in all agents | Works on any project | Medium |
| 6 | Define handoff mechanism | Inter-agent communication works | Medium |

### P2 - Medium (Fix This Month)

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 7 | Clarify ADR ownership | No confusion about who writes | Low |
| 8 | Add failure recovery protocols | Stuck agents recover | Medium |
| 9 | Add frontend testing to `test-writer.md` | Frontend tests written | Medium |

### P3 - Low (Backlog)

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 10 | Create `n-plus-one-detector` skill | Automated scanning | High |
| 11 | Create `security-ownership-validator` skill | Automated security | High |
| 12 | Add file size/complexity thresholds | Prevent monoliths | Low |

---

## Conclusion

The current agent system has solid foundations but significant blind spots. The agents are designed for **reviewing new code** but are completely blind to **existing codebase problems**.

**The key insight:** Real projects accumulate technical debt over time. Agents need **search-and-discover protocols**, not just **review-what-I-see protocols**.

The recommended changes would increase issue detection from ~20% to potentially ~70% with relatively low effort for the P0 and P1 items.

---

*Document generated from critical review analysis on 2026-01-19*
