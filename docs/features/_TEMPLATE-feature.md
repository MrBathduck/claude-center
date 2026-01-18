# F<XXX>: <FEATURE_NAME>

> <One-line description of what this feature does>

---

## Metadata

| Field | Value |
|-------|-------|
| **Status** | draft / in-progress / L1 / L2 / L3 |
| **Phase** | [P-XX](../phases/P-XX-phase-name.md) or "unassigned" |
| **Created** | <YYYY-MM-DD> |
| **Last Updated** | <YYYY-MM-DD> |
| **Owner** | <Name or "unassigned"> |

---

## Why

<!-- What problem does this solve? Why does it matter? -->

<PROBLEM_STATEMENT>

---

## Success Criteria

<!-- How do we know this feature is done? Observable outcomes. -->

- [ ] <CRITERION_1>
- [ ] <CRITERION_2>
- [ ] <CRITERION_3>

---

## Out of Scope

<!-- Explicitly what this feature does NOT do. Prevents scope creep. -->

- <NOT_INCLUDED_1>
- <NOT_INCLUDED_2>

---

## Data Model

<!-- Link to entities, don't describe them here. -->

- **Primary:** [<Entity>](../data/entities/<entity>.md)
- **Related:** [<Entity>](../data/entities/<entity>.md) (via <relationship>)

---

## Behavior

<!-- What the feature does. This is the Canon - the source of truth. -->

### <BEHAVIOR_AREA_1>

<Description of behavior. Be specific enough that violations are detectable.>

### <BEHAVIOR_AREA_2>

<Description of behavior.>

---

## UI/UX

<!-- Optional: Key UI requirements if relevant -->

- <UI_REQUIREMENT_1>
- <UI_REQUIREMENT_2>

---

## Technical Anchors

<!-- Links to system docs, ADRs, or constraints that apply -->

- [Architecture](../dev/system/architecture.md) - <relevant section>
- [ADR-XXX](../dev/decisions/ADR-XXX-topic.md) - <why it applies>

---

## Dependencies

<!-- What must exist before this feature can be built? -->

- **Requires:** F<XXX>-<feature> (because <reason>)
- **Blocks:** F<XXX>-<feature> (must complete first)

---

## Open Questions

<!-- Unresolved decisions. Remove as they're answered. -->

- [ ] <QUESTION_1>
- [ ] <QUESTION_2>

---

## History

<!-- Append-only log of significant changes -->

| Date | Change | By |
|------|--------|-----|
| <YYYY-MM-DD> | Created | <Name> |

---

<!--
USAGE NOTES:
1. Copy this file to F<XXX>-<feature-name>.md
2. Fill in all <PLACEHOLDER> values
3. Delete sections that don't apply (but keep Data Model and Behavior)
4. Add to FEATURE_INDEX.md
5. Check FEATURE_MAP.md for related features

MODE SELECTION (from WORKFLOW-V2.md):
- Quick (< 1 day): Code first, backfill this Canon if it sticks
- Standard (1-5 days): This Canon -> Build -> Review
- Full (> 5 days): This Canon -> Phase -> Build -> Review

WHEN TO SKIP THIS TEMPLATE (Fast-Paths):
- You know exactly which feature to build -> Go to execution, add commit note referencing Canon
- No system impact -> Go to execution
- Feature fits existing phase -> Go to execution, link in phase doc after
- Building isolated utility -> Go to execution, brief Canon after if it sticks

DONE LEVELS:
- L1 (MVP): Code works, this Canon exists with basic info
- L2 (Stable): Quality reviewed, Canon accurate, tests exist
- L3 (Production): System docs updated, Feature Map current, ADR if needed

CROSS-REFERENCES:
- Data Model links to: /docs/data/entities/<entity>.md
- Technical Anchors link to: /docs/dev/system/ and /docs/dev/decisions/
- Phase link in Metadata: /docs/phases/P-XX-<name>.md
- Dependencies reference other Canons: F<XXX>-<feature>.md

SOURCE OF TRUTH: /docs/WORKFLOW-V2.md
-->
