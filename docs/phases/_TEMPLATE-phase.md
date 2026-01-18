# P-<XX>: <PHASE_NAME>

> <One-line description of what this phase accomplishes>

---

## Metadata

| Field | Value |
|-------|-------|
| **Status** | planning / active / review / complete / paused |
| **Started** | <YYYY-MM-DD> |
| **Target Completion** | <YYYY-MM-DD> |
| **Actual Completion** | <YYYY-MM-DD or "in progress"> |

---

## Intent

<!-- Why does this phase exist? What user/business outcome does it achieve? -->

<PHASE_PURPOSE>

---

## Features

<!-- Features included in this phase. Link to Canons. -->

| Feature | Status | Critical Path? |
|---------|--------|----------------|
| [F<XXX>-<name>](../features/F<XXX>-<name>.md) | draft | Yes / No |
| [F<XXX>-<name>](../features/F<XXX>-<name>.md) | draft | Yes / No |

---

## Deliverables

<!-- 3-9 observable outcomes. Each links to a Canon and has verification criteria. -->

### 1. <DELIVERABLE_NAME>

- **Canon:** [F<XXX>](../features/F<XXX>-<name>.md) - <section>
- **Observable Change:** <What the user/system can now do>
- **Verification:** <How to confirm it works>
- **Status:** pending / in-progress / complete

### 2. <DELIVERABLE_NAME>

- **Canon:** [F<XXX>](../features/F<XXX>-<name>.md) - <section>
- **Observable Change:** <What the user/system can now do>
- **Verification:** <How to confirm it works>
- **Status:** pending / in-progress / complete

### 3. <DELIVERABLE_NAME>

- **Canon:** [F<XXX>](../features/F<XXX>-<name>.md) - <section>
- **Observable Change:** <What the user/system can now do>
- **Verification:** <How to confirm it works>
- **Status:** pending / in-progress / complete

<!-- Add more deliverables as needed (aim for 3-9 total) -->

---

## Dependencies

<!-- What must be true before this phase can start? -->

- **Requires Phase:** P-<XX> (because <reason>)
- **Requires System:** <System requirement>
- **External:** <External dependency>

---

## Risks

<!-- What could go wrong? How will you mitigate? -->

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| <RISK_1> | Low/Med/High | Low/Med/High | <MITIGATION> |

---

## Progress Log

<!-- Brief updates as phase progresses -->

| Date | Update |
|------|--------|
| <YYYY-MM-DD> | Phase created |

---

## Completion Checklist

- [ ] All deliverables complete
- [ ] All features at L2+
- [ ] Critical-path features at L3
- [ ] Feature Map updated
- [ ] Phase marked complete in PHASE_INDEX.md

---

<!--
USAGE NOTES:
1. Copy this file to P-<XX>-<phase-name>.md
2. Fill in all <PLACEHOLDER> values
3. Add to PHASE_INDEX.md
4. Link features to this phase in their Canon metadata
5. Use Full mode workflow for phases (>5 days work)

WHEN TO USE THIS TEMPLATE:
- Work spans > 5 days (Full mode)
- Multiple features need coordination
- You need deliverable tracking

WHEN TO SKIP THIS TEMPLATE:
- Quick mode (< 1 day) -> Just code
- Standard mode (1-5 days) -> Canon -> Build -> Review (no phase needed)
- Feature fits existing phase -> Add to existing phase instead

PHASE PLANNING (Stage 2 from WORKFLOW-V2):
- Group features by intent, not technology
- Define 3-9 deliverables per phase
- Each deliverable: observable change + Canon link + verification
- Document dependencies

CROSS-REFERENCES:
- Feature links: /docs/features/F<XXX>-<name>.md
- After completion, update: PHASE_INDEX.md, Feature Map

SOURCE OF TRUTH: /docs/WORKFLOW-V2.md
-->
