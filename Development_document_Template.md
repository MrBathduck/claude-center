# <DOCUMENT TITLE>

**Document Type:** System | Decision | Notes  
**Authority Level:** High | Medium | Low  
**Owner:** System Archivist  
**Last Reviewed:** <YYYY-MM-DD>

---

## Decision Summary

**ADR ID:** ADR-XXX  
**Decision Date:** <YYYY-MM-DD>  
**Status:** Accepted | Superseded | Deprecated

---

## 1. Purpose

<Why this document exists.
What kind of knowledge it preserves.
What problem it prevents.>

---

## 2. Scope

### In Scope
- <What this document explicitly covers>
- <Boundaries of responsibility>

### Out of Scope
- <What this document will NOT describe>
- <What belongs in Feature Canon or code>

---

## 3. Context (Optional)

<Relevant background needed to understand this document.
Keep factual and concise.>

---

## 4. Core Content

<This section varies by document type>

### For SYSTEM documents
- System boundaries
- Conceptual architecture
- Invariants and constraints
- Contracts between components

### For DECISION documents (ADR)
- Decision statement
- Alternatives considered
- Chosen option
- Consequences (positive and negative)

### For NOTES documents
- Observations
- Heuristics
- Temporary conclusions
- Open questions

---

## 5. Constraints & Invariants

- <Rule that must always hold>
- <Assumption the system relies on>

---

## 6. Change Policy

This document MUST be updated when:
- <Structural or irreversible change condition>

This document MUST NOT be updated when:
- <UI behavior changes>
- <Feature logic evolves without system impact>

---

## 7. Links & References

### Related Feature Canons
- <FXXX Feature Name> (if applicable)

### Related Decisions
- <ADR-XXX>

### Related System Docs
- <path/to/system-doc.md>

---

## 8. Risks & Failure Modes (Optional)

- <What breaks if this document is ignored?>
- <Known danger zones>

---

## 9. Document Status

- 🟢 Stable
- 🟡 Requires Review
- 🔴 Potentially Outdated

---

## 10. Why This Document Works (and What to Resist)

### Why this works
- <What kind of clarity this document provides>
- <What cost it avoids>

### What to resist
- <Common misuse or over-extension>
- <Content that does not belong here>

---

## 11. Size & Readability Check

- Target length: <X–Y lines>
- One concept per section
- Diagrams preferred over prose
- Bullet points over paragraphs

---

## 12. Agent Interaction Rules

### System Archivist
- Owns creation and updates
- Ensures consistency with system reality

### Feature Steward
- May reference this document
- Must not modify core content

### Developer / UI / API Agents
- Read-only access
- Must not update this document

### Quality Reviewer
- Flags contradictions or missing updates
- Does not edit directly
