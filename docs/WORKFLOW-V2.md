# Agentic Coding Workflow V2

> For experienced vibe coders building large software projects.
> Structure serves momentum, not bureaucracy.

---

## Start Here (New Projects)

**First time? Follow this path:**

1. **Read this document** - Understand the modes and authority hierarchy
2. **Set up folders** - Copy the `/docs/` structure from Document Structure below
3. **Create SCHEMA_INDEX** - Even if empty, your data model will grow
4. **Create FEATURE_INDEX** - Your master feature list
5. **Start with Quick mode** - Code first, learn the workflow as you go

**Key files to bookmark:**
- This file (WORKFLOW-V2.md) - The source of truth
- [FEATURE_INDEX](./features/FEATURE_INDEX.md) - Where features live
- [FEATURE_MAP](./features/FEATURE_MAP.md) - Cross-feature visibility
- [SCHEMA_INDEX](./data/SCHEMA_INDEX.md) - Your data model

**Templates (copy when needed):**
- [Feature Canon template](./features/_TEMPLATE-feature.md)
- [Phase template](./phases/_TEMPLATE-phase.md)
- [Entity template](./data/entities/_TEMPLATE-entity.md)
- [ADR template](./dev/decisions/_TEMPLATE-adr.md)
- [System doc template](./dev/system/_TEMPLATE-system.md)
- [Notes template](./dev/notes/_TEMPLATE-notes.md)

---

## Scaling Gates

**Before starting, pick your mode:**

| Mode | Scope | Workflow |
|------|-------|----------|
| **Quick** | < 1 day work | Code first, backfill Canon if it sticks |
| **Standard** | 1-5 days | Canon -> Build -> Review |
| **Full** | > 5 days | Canon -> Phase -> Deliverables -> Build -> Review |

*Quick mode produces working code. Standard mode produces documented features. Full mode produces coordinated releases.*

---

## Fast-Paths for Experienced Vibers

**Skip what you already know:**

| If you... | Skip to... | Just add... |
|-----------|------------|-------------|
| Know exactly which feature to build | Execution | Commit note referencing Canon |
| Know there's no system impact | Execution | Nothing |
| Feature fits existing phase | Execution | Link in phase doc after |
| Building isolated utility | Execution | Brief Canon after if it sticks |

**The rule:** Skip planning stages when the answers are obvious. Backfill docs when code survives.

---

## Authority Hierarchy

```
System Docs & ADRs  -> Constraints (what must hold)
Data Model          -> Structure (what entities exist)
Feature Canon       -> Truth (what the app does)
Phase Docs          -> Intent (what we're building next)
```

---

## Document Structure

```
/docs/
  |-- data/                    <- First-class citizen
  |   |-- SCHEMA_INDEX.md
  |   |-- entities/
  |   |   |-- user.md
  |   |   |-- event.md
  |   |   |-- wine.md
  |   |   +-- ...
  |   +-- relationships.md
  |
  |-- features/
  |   |-- FEATURE_INDEX.md
  |   |-- FEATURE_MAP.md       <- Cross-feature visibility
  |   |-- F001-feature-name.md
  |   +-- F002-feature-name.md
  |
  |-- dev/
  |   |-- system/              <- Rarely updated, load-bearing
  |   |   |-- architecture.md
  |   |   |-- auth-model.md
  |   |   +-- deployment.md
  |   |
  |   |-- decisions/           <- Append-only, immutable
  |   |   |-- ADR-001-topic.md
  |   |   +-- ADR-002-topic.md
  |   |
  |   +-- notes/               <- Allowed to rot, non-authoritative
  |       |-- frontend-notes.md
  |       +-- testing-notes.md
  |
  +-- phases/
      |-- PHASE_INDEX.md
      |-- P-01-phase-name.md
      +-- P-02-phase-name.md
```

### Data Model as First-Class Citizen

Feature Canons **link to** entities, they don't describe them.

**In Canon:**
```markdown
## Data Model
- Primary: [User](/docs/data/entities/user.md)
- Related: [Event](/docs/data/entities/event.md) (via attendance)
```

**In `/docs/data/entities/user.md`:**
```markdown
# User Entity

## Fields
- id: uuid
- email: string (unique)
- created_at: timestamp

## Used By
- F001-authentication
- F003-user-profile
- F007-event-registration

## Relationships
- has_many: events (as organizer)
- has_many: attendances
```

---

## Feature Map (System-Level Visibility)

**`/docs/features/FEATURE_MAP.md`** answers:
- Which features share state?
- What are the critical dependency paths?
- Where do changes ripple?

```markdown
# Feature Map

## Shared State Clusters

### User Identity Cluster
Features: F001-auth, F003-profile, F012-permissions
Shared: User entity, session state
Change impact: High - touches auth flow

### Event Core Cluster
Features: F005-events, F007-registration, F009-calendar
Shared: Event entity, date handling
Change impact: Medium - isolated to event domain

## Critical Paths
- User creation -> Profile -> Permissions (must complete in order)
- Event creation -> Registration (no event = no registration)

## Independent Features (safe to parallelize)
- F010-export (read-only)
- F011-themes (UI only)
- F015-analytics (separate data store)
```

---

## Workflow Stages

### Stage 1: Intent & Impact

**Input:** Idea or problem
**Output:** Feature Canon with technical anchors
**Skip if:** You already know the feature shape AND system impact

1. Define why, success criteria, out-of-scope
2. Check Feature Map: does this touch shared state?
3. Check System Docs: any constraints?
4. Create/update Feature Canon (F-XXX)
5. Flag if ADR needed

*Combines original Stages 1-2. One pass, not two.*

---

### Stage 2: Phase Planning

**Input:** Feature Canon(s)
**Output:** Phase with deliverables
**Skip if:** Feature fits existing phase OR Quick mode

1. Group features by intent (not tech)
2. Define 3-9 deliverables per phase
3. Each deliverable: observable change + Canon link + verification
4. Document dependencies

*Only needed for Full mode or new major work.*

---

### Stage 3: Execution

**Input:** Canon section or deliverable
**Output:** Working code
**Agents:** Developer, UI/UX, API Designer

1. Read relevant Canon sections
2. Read technical anchors
3. Build thin solution
4. Commit with Canon reference

```
git commit -m "F007: event registration basic flow

Implements attendee list and capacity check.
Canon: docs/features/F007-event-registration.md"
```

---

### Stage 4: Review & Sync

**Input:** Implemented code
**Output:** Verified code + updated docs
**Agents:** Quality Reviewer, Feature Steward, System Archivist

**Quality Check:**
- Code matches Canon intent?
- Canon claims are testable?
- Contradictions found?

**Doc Sync (if changes warrant):**
- Feature Steward updates Canon
- System Archivist adds ADR if decision made
- Update Feature Map if relationships changed

*Combines original Stages 5-6. Review and sync happen together.*

---

## Done Levels

**Replace binary "done" with progressive maturity:**

| Level | Name | Criteria | When to stop here |
|-------|------|----------|-------------------|
| **L1** | MVP | Code works, basic Canon exists | Quick mode, experiments |
| **L2** | Stable | Quality reviewed, Canon accurate | Standard mode, most features |
| **L3** | Production | System docs updated, ADR if needed, Feature Map current | Full mode, core features |

**Phase completion requires:**
- All deliverables at L2+
- Critical-path features at L3
- Feature Map accurate

---

## Agent Roles by Usage Frequency

### Core Loop (constant use)
| Agent | Purpose | Reads | Writes |
|-------|---------|-------|--------|
| **Developer** | Build features | Canon (behavior), Anchors | Code |
| **Quality Reviewer** | Verify correctness | Canon, Code | Flags only |

### Planning Loop (per-phase)
| Agent | Purpose | Reads | Writes |
|-------|---------|-------|--------|
| **Architect** | Structure phases | Canon, System docs | Phase docs |
| **System Agent** | Assess impact | Canon, System docs | Technical anchors |

### Sync Loop (after changes)
| Agent | Purpose | Reads | Writes |
|-------|---------|-------|--------|
| **Feature Steward** | Keep Canon accurate | Canon, Code | Canon |
| **System Archivist** | Record decisions | System docs, Code | ADRs, System docs |

### Occasional
| Agent | Purpose | When |
|-------|---------|------|
| **Debugger** | Investigate failures | Something broke |

---

## Parallelization Guidance

**Features can be built in parallel when:**
- No shared entity writes (check Feature Map)
- No conflicting system changes
- Different technical anchors
- Independent UI areas

**Safe parallel patterns:**
```
OK:  F010-export + F011-themes      (no overlap)
OK:  F005-events + F020-settings    (different domains)
BAD: F007-registration + F008-waitlist (both write Event)
BAD: F001-auth + F012-permissions   (shared User state)
```

**Coordination points:**
- Shared entity changes -> sequential or explicit sync
- System doc changes -> one at a time
- Same UI component -> one at a time

---

## Recovery Protocols

### "Docs are stale"

**Symptoms:** Canon doesn't match code, confusion about current behavior

**Recovery:**
1. Code is truth when docs are stale
2. Run the feature, document what actually happens
3. Update Canon to match reality
4. Add note: `[Reconciled YYYY-MM-DD]`
5. Don't blame, just fix forward

---

### "I don't know where this belongs"

**Symptoms:** New code doesn't fit existing Canons, unclear ownership

**Recovery:**
1. Check Feature Map for related clusters
2. If touches existing entity -> probably extends existing Canon
3. If new entity needed -> new Canon + entity doc
4. If truly cross-cutting -> might need ADR
5. When in doubt: create minimal Canon, refine later

**Quick test:** "Which Canon would break if this code broke?"

---

### "I broke something"

**Symptoms:** Feature regression, unexpected behavior change

**Recovery:**
1. **Debugger agent:** Identify what changed and why
2. Check: was Canon violated or was Canon wrong?
3. If Canon violated -> fix code
4. If Canon wrong -> fix Canon (might need ADR)
5. Update Feature Map if dependency was hidden
6. Add test to prevent recurrence

---

## Change Propagation

### When Entity changes:
1. Update entity doc in `/docs/data/entities/`
2. Check "Used By" list
3. Review each dependent Canon
4. Update Feature Map if relationships changed

### When Feature Canon changes:
1. Feature Steward updates Canon
2. Check Feature Map for downstream impact
3. Review affected phases

### When System Doc changes:
1. Review all Canons that anchor to it
2. Explicit review, no auto-updates
3. ADR if the change is significant

---

## Quick Reference

### Mode Selection
```
< 1 day   -> Quick   -> Code, backfill if it sticks
1-5 days  -> Standard -> Canon -> Build -> Review
> 5 days  -> Full    -> Canon -> Phase -> Build -> Review
```

### Fast-Path Checklist
- [ ] Do I know the feature shape? (skip Intent if yes)
- [ ] Is system impact obvious/none? (skip Impact analysis if yes)
- [ ] Does this fit a phase? (skip Phase planning if yes)
- [ ] -> Go build

### Done Level Selection
- L1: Prototype, experiment, quick fix
- L2: Real feature, ships to users
- L3: Core feature, others depend on it

### Document Update Frequency
| Document | Update When | By Whom |
|----------|-------------|---------|
| Entity docs | Schema changes | System Archivist |
| Feature Canon | Behavior changes | Feature Steward |
| Feature Map | Relationships change | Feature Steward |
| System Docs | Structural changes | System Archivist |
| ADRs | Never (append-only) | System Archivist |
| Phase Docs | Scope changes | Architect |
| Notes | Whenever useful | Anyone |

---

## Philosophy

1. **Code that works beats docs that describe**
2. **Backfill beats upfront bureaucracy**
3. **Skip what's obvious, document what's not**
4. **Feature Map prevents "I didn't know that would break"**
5. **Done levels match effort to importance**
6. **Recovery protocols assume drift happens**

The workflow exists to prevent expensive mistakes, not to create paperwork. When the answer is obvious, skip the process. When you're unsure, the process helps you think.
