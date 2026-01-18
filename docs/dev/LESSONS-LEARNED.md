# Lessons Learned Registry

> Patterns of failure and how to prevent them.
> Add new lessons as issues are discovered. Reference this in Phase Docs.
>
> **Source of truth for workflow:** [WORKFLOW-V2.md](../WORKFLOW-V2.md)

---

## How to Use This Document

1. **Before planning a feature**: Check if any lessons apply
2. **During Phase Doc creation**: Reference relevant lessons in requirements
3. **During review**: Verify lessons were followed
4. **After incidents**: Add new lessons here

---

## Lesson Categories

| Category | Status |
|----------|--------|
| [Code Quality](#code-quality) | Documented |
| [Performance](#performance) | Documented |
| [Security & Auth](#security--auth) | Documented |
| [Frontend Architecture](#frontend-architecture) | Documented |
| [Services](#services) | Pending |
| [APIs](#apis) | Pending |

---

## Code Quality

### L-CQ-001: Code Duplication (Copy-Paste Epidemic)

**Pattern**: Same utility function written 6 times across features (escapeHtml, showToast, debounce, etc.)

**Root Cause**: No pre-implementation search requirement. Developers code in isolation.

**Impact**: 900+ duplicate lines. Maintenance nightmare. Bugs fixed in one place, not others.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Intent | System Agent | Search for existing implementations before approving feature |
| Planning | Architect | Add "Shared utilities to use" section in Phase Doc |
| Execution | Developer | Search codebase before writing ANY utility function |
| Review | Quality Reviewer | Run `jscpd` for duplicate detection |

**Checklist for Phase Doc**:
```markdown
## Pre-Implementation Search (Required)
- [ ] Searched for existing implementations of required utilities
- [ ] Identified shared code to reuse: [list]
- [ ] New utilities will be created in shared location first
```

**ADR Needed**: ADR: Shared Utility Library Architecture

---

### L-CQ-002: CLAUDE.md Rules Ignored

**Pattern**: 200+ violations of documented rules (hardcoded colors, missing error codes, etc.)

**Root Cause**: Rules exist but aren't enforced. No checklist. No automation.

**Impact**: Technical debt accumulates. Inconsistent codebase. Rules become fiction.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Planning | Architect | Extract relevant CLAUDE.md rules into Phase Doc checklist |
| Execution | Developer | Complete CLAUDE.md checklist before requesting review |
| Review | Quality Reviewer | Verify checklist completed |
| CI | Automated | Pre-commit hooks block violations |

**Checklist for Phase Doc**:
```markdown
## CLAUDE.md Compliance (Required)
- [ ] No hardcoded hex colors (use SCSS variables)
- [ ] All errors registered in error_codes.py
- [ ] Ownership validation in service layer
- [ ] [Add feature-specific rules]
```

**ADR Needed**: ADR: CLAUDE.md as Binding Constraints

---

### L-CQ-003: Business Logic in Templates

**Pattern**: Complex calculations in Jinja (capacity percentages, filtered counts, etc.)

**Root Cause**: Faster to write in template. No enforcement of separation.

**Impact**: Untestable logic. Duplicated across templates. Poor performance.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Planning | Architect | Specify "No template logic" in Phase Doc |
| Execution | Developer | Use model properties for computed values |
| Review | Quality Reviewer | Flag `{% set %}` with calculations |

**Rule**: If logic is more than simple conditionals, it goes in Python.

**Pattern**:
```python
# Model property (testable)
@property
def capacity_percentage(self):
    if not self.capacity:
        return 0
    return round(self.active_count / self.capacity * 100, 1)

# Template (display only)
{{ event.capacity_percentage }}%
```

**ADR Needed**: ADR: Template Logic Boundary

---

### L-CQ-004: Inline JavaScript Explosion

**Pattern**: 1,000+ lines of inline `<script>` blocks in templates.

**Root Cause**: No extraction requirement. Easier to write inline.

**Impact**: Can't cache. Can't minify. Can't test. Hard to maintain.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Planning | Architect | Specify "No inline JS >20 lines" in Phase Doc |
| Execution | Developer | Extract to `app/static/js/[feature]/[module].js` |
| Review | Quality Reviewer | Count inline JS lines, flag if >20 |

**Rule**: `<script>` blocks >20 lines must be extracted.

**ADR Needed**: ADR: JavaScript Architecture

---

## Performance

### L-PF-001: N+1 Query Plague

**Pattern**: Loop without eager loading causes 301 queries for 100 items.

**Root Cause**: Small dataset testing. No query logging during development.

**Impact**: 8+ critical performance issues. Pages timeout with real data.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Intent | System Agent | Flag if feature involves list operations |
| Planning | Architect | Specify eager loading requirements |
| Execution | Developer | Enable SQLALCHEMY_ECHO during development |
| Review | Quality Reviewer | Verify eager loading used for relationships |
| Testing | Test Writer | Add query count assertions |

**Checklist for Phase Doc** (if data layer involved):
```markdown
## Performance Requirements
- [ ] List endpoints use eager loading (joinedload/selectinload)
- [ ] Tested with 100+ items using seed-stress
- [ ] Query count verified with SQLALCHEMY_ECHO
```

**Pattern**:
```python
# WRONG
events = Event.query.all()
for event in events:
    print(event.registrations)  # N+1 query!

# RIGHT
events = Event.query.options(joinedload(Event.registrations)).all()
for event in events:
    print(event.registrations)  # Already loaded
```

**ADR Needed**: ADR: Query Performance Standards

---

### L-PF-002: Memory Leaks (HTMX Lifecycle)

**Pattern**: Charts and Sortable instances created but never destroyed on HTMX swap.

**Root Cause**: Developers treat HTMX like traditional page reload. Pattern not documented.

**Impact**: 5+ modules with memory leaks. Browser slows down over time.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Intent | System Agent | Flag if feature uses charts/Sortable/event listeners |
| Planning | Architect | Specify HTMX cleanup requirement |
| Execution | Developer | Add htmx:beforeSwap cleanup handler |
| Review | Quality Reviewer | Verify cleanup exists for dynamic elements |

**Required Pattern**:
```javascript
// Create instance
const chart = new ApexCharts(el, options);
chart.render();
window.chartInstance = chart;

// REQUIRED: Cleanup on HTMX swap
document.addEventListener('htmx:beforeSwap', function() {
    if (window.chartInstance) {
        window.chartInstance.destroy();
        window.chartInstance = null;
    }
});
```

**ADR Needed**: ADR: HTMX Dynamic Resource Management

---

## Security & Auth

### L-SA-001: Authorization in Wrong Layer

**Pattern**: Auth checks in routes only. Services have no ownership validation.

**Root Cause**: Faster to add decorator to route. Service-layer pattern not enforced.

**Impact**: CLI commands, background jobs, and future APIs bypass auth.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Intent | System Agent | Check auth-model.md for requirements |
| Planning | Architect | Specify service-layer auth in Phase Doc |
| Execution | Developer | Add `current_user` parameter to service functions |
| Review | Quality Reviewer | Verify ownership check in service, not route |
| Testing | Test Writer | Add ownership validation tests |

**Rule**: Routes delegate to services. Services validate ownership.

**Pattern**:
```python
# Service (validates ownership)
def get_event(event_id: int, current_user: User) -> Event:
    event = db.session.get(Event, event_id)
    if event.user_id != current_user.id:
        raise ForbiddenError()
    return event

# Route (delegates to service)
@bp.route('/events/<id>')
def show_event(id):
    event = event_service.get_event(id, current_user)  # Auth happens here
    return render_template('event/show.html', event=event)
```

**ADR Needed**: ADR: Authorization Layering

---

## Frontend Architecture

### L-FA-001: Hardcoded Colors

**Pattern**: 100+ instances of raw hex codes instead of SCSS variables.

**Root Cause**: No automated enforcement. Faster to hardcode.

**Impact**: Inconsistent theming. Can't change colors globally.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Execution | Developer | Use SCSS variables only |
| Review | Quality Reviewer | Grep for hex codes in SCSS |
| CI | Automated | Pre-commit hook blocks hex codes |

**Pre-commit check**:
```bash
if grep -r '#[0-9a-fA-F]\{6\}' --include='*.scss' app/; then
    echo "ERROR: Hardcoded hex colors. Use SCSS variables."
    exit 1
fi
```

---

### L-FA-002: Missing Error Registry

**Pattern**: Plain string errors returned instead of registered error codes.

**Root Cause**: error_codes.py exists but not enforced.

**Impact**: Inconsistent error messages. Can't localize. Can't track.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Execution | Developer | Add new errors to error_codes.py |
| Review | Quality Reviewer | Verify all error strings are registered |

---

## Services

> Add lessons for service-layer issues here.

### L-SV-001: [Title]

**Pattern**: [What went wrong]

**Root Cause**: [Why it happened]

**Impact**: [What it caused]

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|

**ADR Needed**: [If applicable]

---

## APIs

> Add lessons for API-related issues here.

### L-API-001: [Title]

**Pattern**: [What went wrong]

**Root Cause**: [Why it happened]

**Impact**: [What it caused]

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|

**ADR Needed**: [If applicable]

---

## Mandatory Workflow Additions

Based on lessons learned, these are now **required** in the workflow:

### Phase 0: Pre-Implementation (System Agent + Architect)

```markdown
Before ANY coding:
- [ ] Search for existing implementations (L-CQ-001)
- [ ] Extract CLAUDE.md rules into Phase Doc (L-CQ-002)
- [ ] Identify shared utilities to reuse (L-CQ-001)
- [ ] Check auth-model.md if auth involved (L-SA-001)
- [ ] Flag if list operations need eager loading (L-PF-001)
- [ ] Flag if dynamic UI needs HTMX cleanup (L-PF-002)
```

### Phase 3: Pre-Merge Verification (Developer + Quality Reviewer)

```markdown
Before merge:
- [ ] No hardcoded hex colors (L-FA-001)
- [ ] No inline JS >20 lines (L-CQ-004)
- [ ] No N+1 queries (L-PF-001)
- [ ] Auth in service layer (L-SA-001)
- [ ] No business logic in templates (L-CQ-003)
- [ ] HTMX cleanup for dynamic elements (L-PF-002)
- [ ] All errors in error_codes.py (L-FA-002)
- [ ] CLAUDE.md compliance verified (L-CQ-002)
```

---

## ADRs To Create

| ID | Title | Lesson Reference |
|----|-------|------------------|
| ADR-XXX | Shared Utility Library Architecture | L-CQ-001 |
| ADR-XXX | CLAUDE.md as Binding Constraints | L-CQ-002 |
| ADR-XXX | Template Logic Boundary | L-CQ-003 |
| ADR-XXX | JavaScript Architecture | L-CQ-004 |
| ADR-XXX | Query Performance Standards | L-PF-001 |
| ADR-XXX | HTMX Dynamic Resource Management | L-PF-002 |
| ADR-XXX | Authorization Layering | L-SA-001 |

---

## Summary Statistics

| Category | Lessons | Issues Prevented |
|----------|---------|------------------|
| Code Quality | 4 | Duplication, rule violations, template logic, inline JS |
| Performance | 2 | N+1 queries, memory leaks |
| Security & Auth | 1 | Auth bypass |
| Frontend | 2 | Hardcoded colors, error registry |
| Services | 0 | Pending |
| APIs | 0 | Pending |
| **Total** | **9** | |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-01-17 | Initial lessons from critical issues retrospective | System |
