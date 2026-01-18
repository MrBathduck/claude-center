# <SYSTEM_DOC_NAME>

> <One-line description: e.g., "System architecture overview" or "Authentication and authorization model">

---

## Overview

<!-- High-level description. What is this document about? -->

<OVERVIEW>

---

## Core Concepts

<!-- Key ideas that inform the design -->

### <CONCEPT_1>

<Description>

### <CONCEPT_2>

<Description>

---

## Structure

<!-- Diagrams, component descriptions, how things fit together -->

```
<ASCII diagram or description of structure>
```

---

## Constraints

<!-- Hard rules that must not be violated. These are load-bearing. -->

1. **<CONSTRAINT_1>:** <Why this must hold>
2. **<CONSTRAINT_2>:** <Why this must hold>

---

## Patterns

<!-- Standard ways of doing things in this system -->

### <PATTERN_NAME>

**When to use:** <Situation>

**How:**
```
<Code pattern or description>
```

---

## Integration Points

<!-- How this connects to other system docs -->

- **Related to:** [<Other System Doc>](./other-doc.md)
- **Decisions:** [ADR-XXX](../decisions/ADR-XXX-topic.md)

---

## Change Protocol

<!-- How to safely modify this system area -->

1. <STEP_1>
2. <STEP_2>
3. Review all Canons that anchor to this doc

---

## History

| Date | Change | ADR |
|------|--------|-----|
| <YYYY-MM-DD> | Created | - |

---

<!--
USAGE NOTES:
1. Copy to appropriate name: architecture.md, auth-model.md, data-model.md, deployment.md
2. System docs are RARELY updated and LOAD-BEARING
3. Changes here require explicit review of all dependent Canons
4. Consider ADR if making significant changes
5. Update Authority Hierarchy: System Docs & ADRs -> Constraints

IMPORTANT: DO NOT REFERENCE SPECIFIC FEATURES
- System docs define constraints that apply across ALL features
- Feature Canons reference system docs (not the reverse)
- If you need to track which features use this, that belongs in Feature Map

FROM WORKFLOW-V2:
- System docs define constraints (what must hold)
- When System Doc changes: review all Canons that anchor to it
- Changes are explicit, no auto-updates
- ADR if the change is significant

CROSS-REFERENCES:
- Related system docs: /docs/dev/system/
- ADRs: /docs/dev/decisions/ADR-XXX-topic.md
- Feature Canons anchor TO this doc (not referenced FROM this doc)

AGENT RESPONSIBILITY:
- Updated by: System Archivist
- Update frequency: When structural changes occur

SOURCE OF TRUTH: /docs/WORKFLOW-V2.md
-->
