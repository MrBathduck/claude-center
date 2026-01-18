# ADR-<XXX>: <DECISION_TITLE>

> <One-line summary of the decision>

---

## Metadata

| Field | Value |
|-------|-------|
| **Status** | proposed / accepted / deprecated / superseded |
| **Date** | <YYYY-MM-DD> |
| **Deciders** | <Names or roles> |
| **Supersedes** | ADR-XXX (if applicable) |
| **Superseded by** | ADR-XXX (if applicable) |

---

## Context

<!-- What is the situation? What forces are at play? -->

<CONTEXT_DESCRIPTION>

---

## Decision

<!-- What did we decide? Be specific. -->

We will <DECISION>.

---

## Rationale

<!-- Why this decision over alternatives? -->

<RATIONALE>

---

## Alternatives Considered

### <ALTERNATIVE_1>

- **Pros:** <benefits>
- **Cons:** <drawbacks>
- **Why rejected:** <reason>

### <ALTERNATIVE_2>

- **Pros:** <benefits>
- **Cons:** <drawbacks>
- **Why rejected:** <reason>

---

## Consequences

### Positive

- <POSITIVE_CONSEQUENCE_1>
- <POSITIVE_CONSEQUENCE_2>

### Negative

- <NEGATIVE_CONSEQUENCE_1>
- <NEGATIVE_CONSEQUENCE_2>

### Risks

- <RISK_1>

---

## Affected Areas

<!-- What does this decision impact? -->

- **Features:** F<XXX>, F<XXX>
- **System Docs:** [<doc>](../system/<doc>.md)
- **Entities:** [<entity>](../../data/entities/<entity>.md)

---

## Implementation Notes

<!-- Optional: Guidance for implementing this decision -->

<NOTES>

---

<!--
USAGE NOTES:
1. Copy to ADR-<XXX>-<topic>.md
2. ADRs are APPEND-ONLY and IMMUTABLE
3. To change a decision, create a new ADR that supersedes this one
4. Update "Superseded by" field in old ADR
5. Written by System Archivist

FROM WORKFLOW-V2:
- ADRs are append-only, immutable
- Record significant decisions
- Part of Authority Hierarchy: System Docs & ADRs -> Constraints
- Update frequency: Never (create new to supersede)

WHEN TO CREATE AN ADR:
- Significant architectural decision
- Technology choice with long-term impact
- Pattern that will be used across features
- Reversal of a previous decision
- Decision that was debated and needs rationale preserved

CROSS-REFERENCES (in Affected Areas section):
- Features: Link to F<XXX>-<name>.md that this decision affects
- System Docs: Link to /docs/dev/system/ docs impacted
- Entities: Link to /docs/data/entities/ if data model affected

Feature Canons should reference this ADR in their "Technical Anchors" section.

AGENT RESPONSIBILITY:
- Written by: System Archivist
- When: After significant decisions are made

SOURCE OF TRUTH: /docs/WORKFLOW-V2.md
-->
