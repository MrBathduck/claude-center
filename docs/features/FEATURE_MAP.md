# Feature Map

> Cross-feature visibility. Answers: Which features share state? What are critical paths? Where do changes ripple?
>
> **Source of truth:** [WORKFLOW-V2.md](../WORKFLOW-V2.md)
> **See also:** [FEATURE_INDEX.md](./FEATURE_INDEX.md) for the master feature list

---

## Shared State Clusters

<!-- Group features that share entities or state. High-change-impact clusters need careful coordination. -->

### <CLUSTER_NAME> Cluster
- **Features:** F001-xxx, F002-xxx, F003-xxx
- **Shared:** <Entity names>, <state types>
- **Change Impact:** High | Medium | Low
- **Notes:** <Why these are grouped, coordination requirements>

<!-- Add more clusters as patterns emerge -->

---

## Critical Paths

<!-- Sequences that must complete in order. Breaking these causes cascading failures. -->

- `<Feature A>` -> `<Feature B>` -> `<Feature C>` (must complete in order because <reason>)

<!-- Example:
- User creation -> Profile -> Permissions (auth flow dependency)
- Event creation -> Registration (no event = no registration)
-->

---

## Independent Features

<!-- Safe to build in parallel. No shared writes, no conflicting changes. -->

| Feature | Why Independent |
|---------|-----------------|
| F0XX-xxx | Read-only / UI-only / Separate data store |

---

## Parallelization Rules

**Features can be built in parallel when:**
- No shared entity writes
- No conflicting system changes
- Different technical anchors
- Independent UI areas

**Require sequential work:**
- Same entity writes -> coordinate or serialize
- System doc changes -> one at a time
- Same UI component -> one at a time

---

## Change Impact Matrix

<!-- Optional: For complex projects, map which features affect which -->

| If you change... | Check these features... |
|------------------|------------------------|
| User entity | F001, F003, F012 |
| Event entity | F005, F007, F009 |

---

## Last Updated

<YYYY-MM-DD> - <Brief note on what changed>
