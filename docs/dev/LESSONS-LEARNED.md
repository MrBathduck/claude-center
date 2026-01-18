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
| [Services](#services) | Documented |
| [APIs](#apis) | Documented |

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

### L-SV-001: Race Conditions in Shared Resources

**Pattern**: Capacity check and registration creation not atomic. Concurrent requests can overbook.

**Root Cause**: Concurrency not considered during design. No locking strategy.

**Impact**: Events overbooked. Business rule violations. Refunds needed.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Intent | System Agent | Flag shared resources (capacity, inventory, quotas) |
| Planning | Architect | Define locking strategy (optimistic vs pessimistic) |
| Execution | Developer | Use SELECT FOR UPDATE or optimistic locking |
| Testing | Test Writer | Add concurrent access tests |

**Pattern for capacity-limited resources**:
```python
# Use pessimistic locking
with db.session.begin_nested():
    event = db.session.query(Event).filter_by(id=event_id).with_for_update().first()
    if event.registrations_count >= event.capacity:
        raise ValidationError("Event is full")
    # Create registration within same transaction
    registration = Registration(event_id=event_id, ...)
    db.session.add(registration)
```

---

### L-SV-002: N+1 Query Plague (Services)

**Pattern**: Loops loading relationships one at a time. 101 queries for 100 items.

**Root Cause**: No query count testing. Developers unaware of lazy loading behavior.

**Impact**: Dashboard load times >5s. Database overload. Poor UX.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Planning | Architect | Define query budget per operation |
| Execution | Developer | Use joinedload/selectinload for relationships in loops |
| Testing | Test Writer | Add query count assertions |
| Review | Quality Reviewer | Enable SQLALCHEMY_ECHO, verify query counts |

**Checklist for Phase Doc**:
```markdown
## Query Performance Budget
- List endpoint: max 3 queries
- Detail endpoint: max 2 queries
- Bulk operation: max N+2 queries (where N = batch size / 100)
```

*Note: This expands on L-PF-001 with service-specific patterns.*

---

### L-SV-003: Missing Database Transactions

**Pattern**: Multi-step operations (create + audit log) not wrapped in transaction.

**Root Cause**: Transaction management seen as automatic. Atomicity not verified.

**Impact**: Partial failures. Audit logs incomplete. Data inconsistency.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Planning | Architect | Identify multi-step operations, require transaction wrapping |
| Execution | Developer | Use `db.session.begin_nested()` for atomic operations |
| Testing | Test Writer | Add rollback tests (verify all-or-nothing) |

**Pattern**:
```python
def create_with_audit(data, current_user):
    with db.session.begin_nested():
        item = Item(**data)
        db.session.add(item)

        audit = AuditLog(action="create", item_id=item.id, user_id=current_user.id)
        db.session.add(audit)
    # Both committed or both rolled back
    db.session.commit()
    return item
```

---

### L-SV-004: Deprecated ORM Patterns

**Pattern**: 52 instances of `Model.query.get(id)` instead of `db.session.get(Model, id)`.

**Root Cause**: Legacy pattern still in muscle memory. No automated detection.

**Impact**: SQLAlchemy 2.0 incompatibility. Potential session bugs.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Execution | Developer | Use `db.session.get(Model, id)` exclusively |
| Review | Quality Reviewer | Grep for `.query.get(`, flag all instances |
| CI | Automated | Pre-commit hook blocks deprecated patterns |

**Pre-commit check**:
```bash
if grep -r "\.query\.get(" app/; then
    echo "ERROR: Use db.session.get(Model, id) instead of Model.query.get()"
    exit 1
fi
```

---

### L-SV-005: No Logging Infrastructure

**Pattern**: 63 of 79 service files (80%) have zero logging statements.

**Root Cause**: No logging standard. Observability seen as optional.

**Impact**: Production issues undebuggable. Can't trace execution flow.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Planning | Architect | Require logging strategy in Phase Doc |
| Execution | Developer | Log entry, exit, and errors for all service functions |
| Review | Quality Reviewer | Verify logging exists in new service code |

**Minimum logging pattern**:
```python
import logging
logger = logging.getLogger(__name__)

def process_registration(registration_id, current_user):
    logger.info(f"Processing registration {registration_id} for user {current_user.id}")
    try:
        # ... logic ...
        logger.info(f"Registration {registration_id} processed successfully")
        return result
    except ValidationError as e:
        logger.warning(f"Validation failed for registration {registration_id}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing registration {registration_id}: {e}", exc_info=True)
        raise
```

---

### L-SV-006: Inconsistent Error Patterns

**Pattern**: 4 different error handling patterns across services (tuples, exceptions, booleans, dicts).

**Root Cause**: No error contract defined. Each service invented own pattern.

**Impact**: Integration nightmare. Callers must handle 4 different patterns.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Planning | Architect | Define single error pattern (exceptions) in system docs |
| Execution | Developer | Use exceptions only. Define custom exception classes. |
| Review | Quality Reviewer | Flag non-exception error patterns |

**Standard**: Services raise exceptions. Routes catch and convert to responses.
```python
# Service (raises exceptions)
def get_event(event_id, current_user):
    event = db.session.get(Event, event_id)
    if not event:
        raise NotFoundError(f"Event {event_id} not found")
    if event.user_id != current_user.id:
        raise ForbiddenError("Not authorized")
    return event

# Route (catches and converts)
@bp.route('/events/<id>')
def show_event(id):
    try:
        event = event_service.get_event(id, current_user)
        return success_response({"item": event.to_dict()})
    except NotFoundError as e:
        return error_response(ERR_NOT_FOUND, str(e), status=404)
    except ForbiddenError as e:
        return error_response(ERR_FORBIDDEN, str(e), status=403)
```

---

### L-SV-007: Monolithic Service Files

**Pattern**: analytics_service.py grew to 1,928 lines. Impossible to navigate.

**Root Cause**: No file size limit enforced. Services grew organically.

**Impact**: Merge conflicts. Slow IDE. Cognitive overload. Hard to test.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Planning | Architect | Set 800-line limit. Plan splits for large services. |
| Execution | Developer | Split when approaching limit |
| Review | Quality Reviewer | Block files >800 lines |

**Split strategy**:
```
analytics_service.py (1,928 lines)
-> Split by domain
analytics/
    __init__.py (exports all)
    event_analytics.py
    speaker_analytics.py
    registration_analytics.py
    financial_analytics.py
    feedback_analytics.py
    comparison_analytics.py
```

---

## APIs

### L-API-001: Silent Exception Handlers

**Pattern**: 80+ bare `except Exception:` blocks with no logging, just generic error responses.

**Root Cause**: Exception handlers prioritize user response over observability. No logging standard enforced.

**Impact**: Production incidents undebuggable. Silent failures hide bugs. Can't trace errors.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Planning | Architect | Define logging standard in Phase Doc |
| Execution | Developer | All exceptions must log with context before returning |
| Review | Quality Reviewer | Grep for bare except blocks, flag if no logging |

**Required Pattern**:
```python
# WRONG
except Exception:
    return error_response("Something went wrong", status=500)

# RIGHT
except Exception as e:
    logger.error(f"Unexpected error in {function_name}: {e}", exc_info=True)
    return error_response(ERR_INTERNAL, "Something went wrong", status=500)
```

---

### L-API-002: Response Format Chaos

**Pattern**: 3+ different response shapes for similar operations (list, single, mutation).

**Root Cause**: No response schema template defined. Each endpoint invented own format.

**Impact**: Frontend must handle multiple shapes. Brittle integrations. Higher bug rate.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Planning | API Designer | Define standard response templates for list/single/mutation |
| Execution | Developer | Use response template, don't invent new shapes |
| Review | Quality Reviewer | Verify response matches standard template |

**Standard Templates**:
```python
# List response
{"success": True, "data": {"items": [...], "pagination": {...}}}

# Single response
{"success": True, "data": {"item": {...}}}

# Mutation response
{"success": True, "data": {"item": {...}, "message": "Created"}}

# Error response
{"success": False, "error": {"code": "ERR_XXX", "message": "..."}}
```

---

### L-API-003: Duplicate API Helpers

**Pattern**: `get_or_error()` implemented 10+ times identically across 6 files.

**Root Cause**: Each file generated in isolation. No search for existing patterns.

**Impact**: Maintenance nightmare. Inconsistent implementations. Bug fixes missed.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Intent | System Agent | Search for existing helpers before approving new code |
| Execution | Developer | Search codebase before writing ANY helper function |
| Review | Quality Reviewer | Flag duplicate helper implementations |

**Rule**: All API utilities go in `app/routes/api/utils.py` or shared location.

---

### L-API-004: Decorator Inconsistency

**Pattern**: Mixed use of `@role_required` vs `@api_role_required` across API endpoints.

**Root Cause**: Multiple valid patterns coexist. No standard enforced.

**Impact**: Inconsistent auth behavior. Security confusion. Onboarding difficulty.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Planning | Architect | Document single decorator pattern in system docs |
| Execution | Developer | Use only `@api_role_required` for API endpoints |
| Review | Quality Reviewer | Flag any `@role_required` in `/api/` routes |

**Rule**: API routes use `@api_role_required`. Web routes use `@role_required`. Never mix.

---

### L-API-005: Missing Pagination

**Pattern**: List endpoints return unbounded results. No pagination for large datasets.

**Root Cause**: Small dataset testing. Pagination seen as "nice to have."

**Impact**: Large lists timeout. Memory exhaustion. Poor UX with real data.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Intent | System Agent | Flag all list endpoints, require pagination spec |
| Planning | Architect | Pagination required for any endpoint returning >25 items |
| Execution | Developer | Implement pagination with page/per_page params |
| Review | Quality Reviewer | Block list endpoints without pagination |

**Standard Pattern**:
```python
@bp.route('/items')
def list_items():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 25, type=int)
    per_page = min(per_page, 100)  # Cap at 100

    pagination = Item.query.paginate(page=page, per_page=per_page)
    return success_response({
        "items": [item.to_dict() for item in pagination.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages
        }
    })
```

---

### L-API-006: Hardcoded Status Codes

**Pattern**: 100+ instances of `status=400`, `status=404` instead of using utility function.

**Root Cause**: Faster to hardcode. No enforcement of status code utility.

**Impact**: Inconsistent status codes. Refactoring dangerous. Can't change globally.

**Prevention**:

| Stage | Agent | Action |
|-------|-------|--------|
| Execution | Developer | Use `get_status_code(ERROR_CODE)` never hardcode |
| Review | Quality Reviewer | Grep for `status=\d+`, flag hardcoded values |

**Rule**: All status codes come from error_codes.py via utility function.

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
- [ ] Define response format template (L-API-002)
- [ ] Define query budget (L-SV-002)
- [ ] Identify shared resources needing locks (L-SV-001)
- [ ] Plan logging points (L-SV-005)
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
- [ ] No bare exception handlers (L-API-001)
- [ ] Response format matches template (L-API-002)
- [ ] No duplicate helpers (L-API-003)
- [ ] Correct decorator used (L-API-004)
- [ ] Pagination on list endpoints (L-API-005)
- [ ] No hardcoded status codes (L-API-006)
- [ ] Race conditions mitigated (L-SV-001)
- [ ] Transactions for multi-step ops (L-SV-003)
- [ ] No deprecated ORM patterns (L-SV-004)
- [ ] Logging in place (L-SV-005)
- [ ] Exception-based errors only (L-SV-006)
- [ ] File size <800 lines (L-SV-007)
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
| ADR-XXX | API Response Standards | L-API-002 |
| ADR-XXX | API Error Handling | L-API-001 |
| ADR-XXX | Service Error Contract | L-SV-006 |
| ADR-XXX | Service Logging Standard | L-SV-005 |
| ADR-XXX | Concurrency & Locking | L-SV-001 |
| ADR-XXX | Service Module Size Limits | L-SV-007 |

---

## Summary Statistics

| Category | Lessons | Issues Prevented |
|----------|---------|------------------|
| Code Quality | 4 | Duplication, rule violations, template logic, inline JS |
| Performance | 2 | N+1 queries, memory leaks |
| Security & Auth | 1 | Auth bypass |
| Frontend | 2 | Hardcoded colors, error registry |
| Services | 7 | Race conditions, N+1 queries, missing transactions, deprecated ORM, no logging, inconsistent errors, monolithic files |
| APIs | 6 | Silent exceptions, response chaos, duplicate helpers, decorator inconsistency, missing pagination, hardcoded status codes |
| **Total** | **22** | |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-01-19 | Added API lessons (L-API-001 through L-API-006) and Services lessons (L-SV-001 through L-SV-007). Updated ADRs table, Summary Statistics, and Mandatory Workflow Additions. | System |
| 2025-01-17 | Initial lessons from critical issues retrospective | System |
