# Agentic Coding Workflow

## Authority Hierarchy

```
System Docs & ADRs  → Constraints (what must hold)
Feature Canon       → Truth (what the app does)
Phase Docs          → Intent & Sequencing (what we're building next)
Deliverables        → Execution Targets (what agents work on)
```

---

## Document Structure

```
/docs/
  ├── features/
  │   ├── FEATURE_INDEX.md
  │   ├── F001-feature-name.md
  │   └── F002-feature-name.md
  │
  ├── dev/
  │   ├── system/           ← Rarely updated, load-bearing
  │   │   ├── architecture.md
  │   │   ├── auth-model.md
  │   │   ├── data-model.md
  │   │   └── deployment.md
  │   │
  │   ├── decisions/        ← Append-only, immutable
  │   │   ├── ADR-001-topic.md
  │   │   └── ADR-002-topic.md
  │   │
  │   └── notes/            ← Allowed to rot, non-authoritative
  │       ├── frontend-notes.md
  │       └── testing-notes.md
  │
  └── phases/
      ├── PHASE_INDEX.md
      ├── P-01-phase-name.md
      └── P-02-phase-name.md
```

---

## Workflow Stages

### Stage 1: Intent Definition

**Input:** Idea or problem statement
**Output:** Feature Canon draft
**Agent:** Product Agent / Human

1. Define why this feature exists
2. Define what success looks like
3. Define what is explicitly out of scope
4. Create Feature Canon (F-XXX)

---

### Stage 2: System Impact Analysis

**Input:** Feature Canon
**Output:** Technical Anchors, potential ADRs
**Agent:** System Agent

1. Read Feature Canon
2. Check: "What might break?"
3. Identify system constraints
4. Flag if ADR is needed
5. Update Feature Canon with Technical Anchors

---

### Stage 3: Phase Planning

**Input:** Feature Canon(s), System constraints
**Output:** Phase Document with Deliverables
**Agent:** Architect Agent

1. Group features by intent (not by tech)
2. Define 3-9 deliverables per phase
3. Each deliverable must:
   - Produce observable change
   - Tie to ≥1 Feature Canon
   - Have clear verification step
4. Document dependencies & preconditions

---

### Stage 4: Execution

**Input:** Phase Deliverable
**Output:** Working code
**Agents:** Developer, UI/UX, API Designer

For each deliverable:
1. Read relevant Feature Canon sections (2-6)
2. Read Technical Anchors (system docs, ADRs)
3. Implement thin solution
4. Commit code

---

### Stage 5: Quality Review

**Input:** Implemented deliverable
**Output:** Verified or rejected deliverable
**Agent:** Quality Reviewer

1. Verify code behavior matches Feature Canon
2. Verify Feature Canon claims are testable
3. Flag contradictions or missing updates
4. Pass → proceed | Fail → return to Stage 4

---

### Stage 6: Documentation Sync

**Input:** Verified deliverable
**Output:** Updated documentation
**Agents:** Feature Steward, System Archivist

**Feature Steward:**
- Updates Feature Canon if behavior changed
- Updates Feature Relationships if coupling changed
- Updates status if maturity changed

**System Archivist:**
- Adds ADR if decision was made
- Updates system doc only if structural change occurred
- Ignores UI tweaks & logic changes

---

### Stage 7: Phase Completion

**Input:** All deliverables verified & documented
**Output:** Completed phase
**Agent:** Architect Agent

1. Verify all deliverables complete
2. Verify Feature Canons still accurate
3. Verify required ADRs accepted
4. Mark phase Completed or Deprecated
5. Review: does next phase need adjustment?

---

## Agent Responsibilities Summary

| Agent | Reads | Writes | Never Touches |
|-------|-------|--------|---------------|
| Product Agent | - | Feature Canon (draft) | Dev docs |
| System Agent | Feature Canon, System docs | Technical Anchors | Feature behavior |
| Architect Agent | Feature Canon, System docs | Phase docs | Code |
| Developer/UI/API | Feature Canon (2-6), Anchors | Code | Any docs |
| Quality Reviewer | Feature Canon, Code | Flags only | Any docs |
| Feature Steward | Feature Canon, Code | Feature Canon | Dev docs |
| System Archivist | System docs, Code | System docs, ADRs | Feature Canon |
| Debugger | Code, Logs | Bug reports | Docs |

---

## Change Propagation

### When Feature Canon changes:
1. Feature Steward updates Canon
2. Impact review: which phases reference this feature?
3. For each impacted phase:
   - Deliverable still valid? → keep
   - Deliverable partially invalid? → revise
   - Deliverable invalid? → remove or move

### When Phase changes:
- Feature Canon stays authoritative
- Dev Docs stay untouched
- Only phase deliverables and goals change

### When System Doc changes:
- Review all Feature Canons that anchor to it
- No automatic updates, explicit review only

---

## Definition of Done

A deliverable is DONE when:
- [ ] Code works
- [ ] Feature Canon updated (if behavior changed)
- [ ] System impact noted (if any)
- [ ] Quality review passed

A phase is DONE when:
- [ ] All deliverables verified
- [ ] Feature Canons still accurate
- [ ] Required ADRs accepted
- [ ] Phase marked Completed

---

## Quick Reference: Document Update Frequency

| Document Type | Update Frequency | Trigger |
|---------------|------------------|---------|
| Feature Canon | After meaningful behavior change | Feature Steward |
| System Docs | Rarely, after structural change | System Archivist |
| ADRs | Append-only, never edit | System Archivist |
| Notes | When useful, allowed to lag | Anyone |
| Phase Docs | During planning, after scope change | Architect Agent |
