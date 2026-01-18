# Feature: <FEATURE_NAME>

**Feature ID:** <FXXX>
**Status:** 🟢 Stable | 🟡 Partial | 🔴 Experimental
**Owner:** Feature Steward
**Last Reviewed:** <YYYY-MM-DD>

---

## 1. Intent

<Why this feature exists. One short paragraph.>

---

## 2. Capabilities

- <Observable behavior 1>
- <Observable behavior 2>
- <Observable behavior 3>

---

## 3. Constraints

- <Deliberate non-goal or limitation 1>
- <Deliberate non-goal or limitation 2>

---

## 4. Inputs

- <Input source 1>
- <Input source 2>

---

## 5. Outputs

- <User-visible output 1>
- <User-visible output 2>

---

## 6. Edge Behavior

- <Condition> → <Behavior>
- <Condition> → <Behavior>

---

## 7. Feature Relationships

### Depends on
- <FXXX Feature Name>

### Enhances
- <FXXX Feature Name>

### Conflicts with
- <FXXX Feature Name> | None

### Shared State
- <state.key>
- <state.key>

---

## 8. Technical Anchors

### System Constraints
- <path/to/system-doc.md>

### Relevant Decisions
- <ADR-XXX>

### Volatile Notes
- <path/to/notes-doc.md>

---

## 9. Known Limitations

- <Known issue or limitation>
- <Known issue or limitation>

---

## 10. Definition of Done

- <Measurable completion condition>
- <Measurable completion condition>

---

# Template Rules

**What this document is**
- A behavioral contract
- A change impact surface
- A truth snapshot

**What this document is NOT**
- A spec
- A design doc
- A system explanation
- A future roadmap

**Size check (important)** 
This entire example is:
- ~250–300 lines max
- Readable in 5 minutes
- Diffable in Git
- Cheap to update

# How agents interact with this doc
- Developer agent - Reads sections 2–6
- Architect agent - Reads sections 7–8
- Quality reviewer - Verifies section 2 vs actual behavior
- Feature Steward - Owns edits after changes