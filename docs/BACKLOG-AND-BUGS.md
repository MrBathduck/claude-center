# Feature Backlog & Bug Tracking

> Features and bugs are operational data, not documentation.
> They live outside the repo. The repo holds truth, not triage.
>
> **Source of truth for workflow:** [WORKFLOW-V2.md](./WORKFLOW-V2.md)

---

## Two Systems, Two Purposes

| Location | Contains | Purpose |
|----------|----------|---------|
| Google Sheets | Feature backlog, Bug list | Operational triage |
| Repo (`/docs/`) | Feature Canon, Phase Docs | System truth |

This split is intentional. Accept it.

---

## Feature Backlog

### Two Lists, Not One

| List | Max Size | Location | Purpose |
|------|----------|----------|---------|
| **Now** | 3-5 items | Phase Doc (repo) | Active work this phase |
| **Later** | Unlimited | Google Sheet | Ideas parking lot |

**Rule**: "Later" is not a commitment. It's a place to not forget. Review when starting a new phase, pull what matters, delete what doesn't.

**Kill rule**: Feature sits in "Later" for 3+ months without being pulled → delete it. If it was important, it'll come back.

---

### Feature Backlog Sheet Structure

**Sheet name**: `Feature Backlog`

| Column | Type | Values | Purpose |
|--------|------|--------|---------|
| Feature | Text | Short description | What is it |
| Area | Dropdown | CRM, Wine, Tourist, Core, UI, Data, etc. | Filtering |
| Priority | Dropdown | High, Medium, Low | What matters |
| Effort | Dropdown | Small, Medium, Large | Rough sizing |
| Status | Dropdown | Later, Considering, Pulled, Killed | Current state |
| Notes | Text | Context, links, thoughts | Memory aid |

**Example rows**:

| Feature | Area | Priority | Effort | Status | Notes |
|---------|------|----------|--------|--------|-------|
| Bulk contact import | CRM | High | Medium | Later | CSV + dedup logic |
| Wine rating algorithm | Wine | Medium | Large | Considering | Check Vivino approach |
| Dark mode | UI | Low | Medium | Killed | Not worth it for MVP |

**Dropdowns prevent chaos**. Don't use free text for Priority/Effort/Status.

---

### Feature Backlog Workflow

```
1. Have idea → add to sheet (30 sec, Status = Later)
2. Starting new phase → review sheet, pull 3-5 items
3. Pulled items → create Feature Canon if needed, add to Phase Doc
4. Monthly cleanup → delete Killed, review stale items
```

---

## Bug Tracking

### Why Bugs Don't Belong in Markdown

- Can't sort by severity
- Can't filter by status
- Can't see "what's open" at a glance
- You'll never update it

---

### Bug Sheet Structure

**Sheet name**: `Bugs`

| Column | Type | Values | Purpose |
|--------|------|--------|---------|
| ID | Text | B001, B002, etc. | Reference in commits |
| Bug | Text | Short description | What's broken |
| Severity | Dropdown | High, Medium, Low | Triage order |
| Feature | Text | F-XXX or area name | Where it lives |
| Status | Dropdown | Open, In Progress, Fixed, Won't Fix | Current state |
| Found | Date | YYYY-MM-DD | When discovered |
| Notes | Text | Repro steps, commit hash, context | Details |

**Example rows**:

| ID | Bug | Severity | Feature | Status | Found | Notes |
|----|-----|----------|---------|--------|-------|-------|
| B001 | Payment fails on Safari | High | F012-Payments | Open | 2024-01-15 | iOS Safari only |
| B002 | Map doesn't load offline | Medium | F008-Venues | Fixed | 2024-01-10 | Fixed in abc123 |
| B003 | Date picker shows wrong timezone | Low | Core | Open | 2024-01-18 | Edge case |

---

### Bug Workflow

```
1. Find bug → add to sheet (30 sec, Status = Open)
2. Starting coding session → check sheet, pick High severity first
3. Fix bug → Status = Fixed, add commit hash to Notes
4. Weekly cleanup → delete Fixed bugs older than 2 weeks
```

**Commit message format**: `fix: payment Safari issue (B001)`

This links your git history to your bug tracker without tooling.

---

## Maintenance Rules

### Weekly (5 minutes)

- [ ] Delete Fixed bugs older than 2 weeks
- [ ] Check for High severity bugs still Open
- [ ] Quick scan: anything in backlog now critical?

### Monthly (15 minutes)

- [ ] Delete Killed features
- [ ] Review all "Later" items older than 3 months → Kill or Promote
- [ ] Check Feature → Area mapping still makes sense
- [ ] Keep total rows under 50 or it's unusable

### Per Phase Start

- [ ] Review Feature Backlog
- [ ] Pull 3-5 items to Phase Doc
- [ ] Status = Pulled for those items
- [ ] Check: any bugs blocking this phase?

---

## Columns You Don't Need

Don't add these. They create overhead with no value for solo work:

- Assigned to (it's you)
- Sprint (you don't have sprints)
- Story points (meaningless without a team)
- Created by (it's you)
- Due date (you'll ignore it)
- 14 custom fields (you'll never fill them)

---

## Alternative: GitHub Issues

If your code is on GitHub, Issues can replace both sheets:

**Pros**:
- Lives with code
- Commits/PRs auto-link
- Labels = filtering
- Milestones = phases
- Free

**Cons**:
- Heavier UI
- Feels "enterprise"
- Harder to get quick overview

**When to switch**: When you have collaborators, or when sheets get unwieldy (100+ items).

---

## Quick Reference

```
Feature idea     → Sheet (Feature Backlog) → Later
Feature active   → Phase Doc → Now
Feature truth    → Feature Canon (repo)

Bug found        → Sheet (Bugs) → Open
Bug fixed        → Sheet (Bugs) → Fixed → delete after 2 weeks
Bug pattern      → Maybe a Feature Canon update
```

---

## Sheet Setup Checklist

- [ ] Create Google Sheet with two tabs: `Feature Backlog`, `Bugs`
- [ ] Add dropdowns for Priority, Effort, Status, Severity
- [ ] Add conditional formatting: High = red, Fixed = green
- [ ] Bookmark sheet (you'll use it constantly)
- [ ] Add link to sheet in project README or CLAUDE.md
