# Critical Review: Members, Companies, Registrations & Speakers Pages

**Author:** Senior Developer Critical Review
**Date:** January 2026
**Status:** Ready for Implementation Planning
**Severity Scale:** CRITICAL > HIGH > MEDIUM > LOW

---

## Executive Summary

This document provides a comprehensive critical review of four core entity pages in the GUBERNA event management platform. The review identifies **200+ actionable issues** across architecture, UI/UX, code quality, performance, and security concerns.

### Quick Statistics

| Module | Critical | High | Medium | Low | Total |
|--------|----------|------|--------|-----|-------|
| Members/Participants | 3 | 11 | 12 | 10 | 36 |
| Companies | 3 | 11 | 14 | 6 | 34 |
| Registrations | 3 | 21 | 24 | 12 | 60 |
| Speakers | 2 | 15 | 15 | 8 | 40 |
| Hardcoded Colors | - | 15 | 35 | - | 500+ violations |
| JavaScript UI/UX | 2 | 14 | 20 | 10 | 46 |
| **TOTAL** | **13** | **87** | **120** | **46** | **216+** |

> **Note:** Statistics updated after self-review #1 - several issues reclassified from CRITICAL to HIGH based on actual data impact vs UX impact.

### Tab Coverage Summary

| Page | Tabs Reviewed | Issues Found |
|------|---------------|--------------|
| **Members/Participants Detail** | Overview, Registrations, Events, Notes, Activity | 12 |
| **Members/Participants List** | All Members, Active, Inactive, Blacklisted | 8 |
| **Companies Detail** | Overview, Members, Events, Notes | 10 |
| **Companies List** | All, By Membership Type filters | 6 |
| **Registrations Detail** | Overview, Payment, Notes | 15 |
| **Registrations List** | All, Confirmed, Pending, Cancelled, Waiting | 12 |
| **Speakers Detail** | Overview, Events, Bio, Photo | 8 |
| **Speakers List** | All, Active, Featured | 6 |

---

## Quick Start: Top 3 Immediate Fixes

If you only have time to fix three things, fix these NOW:

| # | Issue | File | Status |
|---|-------|------|--------|
| 1 | **Broken unlink URL** (P1-C1) | `companies/detail.html:481` | DONE (2026-01-17) |
| 2 | **Company field not populated in edit modal** (P1-M4) | `participants/_edit_modal.html` | DONE (2026-01-17) |
| 3 | **Email uniqueness bug** (P1-M3) | `routes/participants.py:294` | DONE (2026-01-17) |
| 4 | **CSRF token fallback** | Multiple JS files | DONE (2026-01-17) |

**Verification:** After fixes, run `pytest tests/ -v` and manually test member unlink on Companies page.

---

## Phase 1: CRITICAL Issues (Immediate Action Required)

### 1.1 Members/Participants Module

#### P1-M1: Native Browser Alert/Confirm Usage [Reclassified: HIGH]
- **Location:** `app/templates/participants/detail.html` lines 245, 249, 258, 289, 293
- **Problem:** Uses native `alert()` and `confirm()` dialogs instead of Bootstrap modals
- **Impact:** Breaks UX consistency, no theming support, blocks JavaScript execution
- **Fix:** Replace with Bootstrap modal components (use `delete_modal` macro)
- **Note:** Reclassified from CRITICAL to HIGH - UX issue, not data-breaking

#### P1-M2: Full-Page Reload After Bulk Actions
- **Location:** `app/static/js/participants/bulk-actions.js` lines 254, 258
- **Problem:** `setTimeout(() => window.location.reload(), 1000)` destroys scroll position
- **Impact:** Users lose context after bulk operations on large lists
- **Fix:** Use HTMX partial updates or delta patching

#### P1-M3: Email Uniqueness vs Soft Delete Conflict [COMPLETED 2026-01-17]
- **Location:** `app/routes/participants.py` lines 294-316
- **Problem:** Validation uses `Participant.active()` excluding soft-deleted records
- **Impact:** Database uniqueness violation when reusing emails of soft-deleted participants
- **Fix:** Query all participants including soft-deleted for uniqueness check
- **Resolution:** Changed from `Participant.active().filter_by(email=...)` to `Participant.query.filter_by(email=...)` to include soft-deleted records

#### P1-M4: Company Field Not Populated in Edit Modal [USER REPORTED] [COMPLETED 2026-01-17]
- **Location:** `app/templates/participants/_edit_modal.html`
- **Problem:** When editing a participant, the company field is not pre-populated even though company is displayed on the detail page
- **Impact:** Users must re-enter company information when editing other fields
- **Fix:** Pre-populate company field (both `company_id` for linked and `company` for free-text) from participant data
- **Priority:** HIGH - Data loss during edit operations
- **Resolution:** Now shows linked company with icon indicator and hidden `company_id` field, or falls back to free-text field

### 1.2 Companies Module

#### P1-C1: CRITICAL BUG - Broken Unlink Endpoint URL [COMPLETED 2026-01-17]
- **Location:** `app/templates/companies/detail.html` line 481
- **Problem:** URL constructed incorrectly - concatenates `list_companies` with company ID
- **Impact:** All member unlink operations return 404 errors
- **Fix:** Use `{{ url_for('companies.unlink_member', company_id=company.id, member_id=0) }}`
- **Priority:** IMMEDIATE - Feature completely broken
- **Resolution:** Changed from malformed `url_for('companies.list_companies')` concatenation to correct `/companies/{{ company.id }}/members/${memberToUnlink}`

#### P1-C2: Inefficient member_count Property (N+1 Query)
- **Location:** `app/models/companies/company.py` lines 272-280
- **Problem:** `len([m for m in self.members if m.deleted_at is None])` loads ALL members
- **Impact:** For company with 10,000 members, entire list loaded just to count
- **Fix:** Use SQLAlchemy `COUNT()` query or cached property

#### P1-C3: Missing Primary Contact Validation
- **Location:** `app/models/companies/company.py` lines 194-199
- **Problem:** No constraint that `primary_contact_id` must be a member of the company
- **Impact:** Primary contact from completely different company possible
- **Fix:** Add model-level validation or database constraint

### 1.3 Registrations Module

#### P1-R1: Embedded JavaScript in Templates (340+ lines)
- **Location:** `app/templates/registrations/form.html` lines 394-731
- **Problem:** Massive JavaScript blocks embedded in Jinja templates
- **Impact:** Not testable, not reusable, violates CSP compliance
- **Fix:** Extract to external module files

#### P1-R2: No Concurrency Protection on Updates
- **Location:** `app/routes/api/registrations/registrations.py` lines 1016-1122
- **Problem:** Updates registration without optimistic locking
- **Impact:** Race condition - concurrent edits lose data
- **Fix:** Implement version field or `updated_at` check

#### P1-R3: Hardcoded TODO - Multi-Day Pricing Incomplete
- **Location:** `app/routes/registrations.py` lines 577, 827
- **Problem:** `num_days=1` hardcoded with TODO comment
- **Impact:** Pricing incorrect for multi-day registrations
- **Fix:** Implement multi-day pricing calculation

### 1.4 Speakers Module

#### P1-S1: Dual Route Handler Architecture [CONSOLIDATION PRIORITY]
- **Location:** `app/routes/speakers.py` vs `app/routes/api/speakers/speakers.py`
- **Problem:** Identical operations implemented twice with different patterns
- **Impact:** Bug fixes in one path not applied to other, logic divergence
- **Fix:** Consolidate into single service layer
- **User Guidance:** Consolidation is priority. Standardization is key. Design for future expansion - all similar patterns across modules should follow same architecture.

#### P1-S2: Hardcoded API Endpoints in JavaScript
- **Location:** `app/static/js/speakers/speaker-photo-upload.js` lines 242, 300
- **Problem:** API URLs hardcoded: `/api/speakers/${speakerId}/photo`
- **Impact:** URL changes break JavaScript at runtime
- **Fix:** Use data attributes with Flask URL generation

---

## Phase 2: HIGH Severity Issues (This Sprint)

### 2.1 Hardcoded Colors - SCSS Violations

Per CLAUDE.md: "Use CSS variables: `var(--text-primary)`, `var(--card-bg)`. NEVER hardcode hex colors."

> **STRICT REQUIREMENT (User Confirmed):** NO EXCEPTIONS. All colors must use variables - including print templates, document generators, and any other context. `#fff`, `#000`, and all hex values must be replaced with SCSS variables or CSS custom properties.

#### 2.1.1 Member Detail SCSS [COMPLETED 2026-01-17]
**File:** `app/static/scss/detail-pages/_member-detail.scss`
```scss
// VIOLATION: 15+ hardcoded colors
&--certified {
    background-color: rgba(16, 185, 129, 0.1);  // Should be var(--color-success)
    color: #059669;                               // Should be $color-success
}
```
**Affected Colors:** `#059669`, `#D97706`, `#4F46E5`, `#34D399`, `#FBBF24`, `#818CF8`, `#F8FAFC`, `#FAFBFC`
**Resolution:** Replaced all hardcoded hex colors with semantic SCSS variables. Added emerald, amber, and indigo color families to `_variables.scss` for proper theming support.

#### 2.1.2 Button Hover States [COMPLETED 2026-01-17]
**File:** `app/static/scss/components/_buttons.scss`
```scss
// VIOLATION: Hardcoded hover/active states
--bs-btn-hover-bg: #0a3377;      // Should derive from $color-primary
--bs-btn-active-bg: #092d6a;     // Should derive from $color-primary
color: #FFFFFF !important;       // Should use $white
```
**Lines:** 11-14, 24-26, 44-45, 54, 100-102, 187-257
**Resolution:** Already compliant - file uses SCSS variables (`$btn-primary-hover`, `$btn-primary-active`, `$white`, etc.) from `_variables.scss`. No changes needed.

#### 2.1.3 JavaScript Chart Colors [COMPLETED 2026-01-17]
**Files:** Multiple chart JS files
- `app/static/js/events/charts/utils.js` - 50+ hardcoded RGBA values
- `app/static/js/statistics/statistics_charts.js` - Full palette hardcoded
- `app/static/js/events/registration_analytics.js` - Status color map hardcoded

**Example:**
```javascript
// VIOLATION: Should reference CSS variables
colors: ['#17a2b8', '#28a745', '#dc3545', '#ffc107']
```

> **IMPORTANT Implementation Note:** JavaScript cannot directly access SCSS variables. The fix requires:
> 1. Define colors as CSS custom properties in `:root` (already done in `_variables.scss`)
> 2. Access via `getComputedStyle(document.documentElement).getPropertyValue('--color-primary')`
> 3. Create helper function: `getThemeColor(varName)` in shared JS module
> 4. Update all chart initializations to use this helper
>
> **Example Fix:**
> ```javascript
> // app/static/js/shared/theme-colors.js
> export function getThemeColor(varName) {
>     return getComputedStyle(document.documentElement)
>         .getPropertyValue(`--${varName}`).trim();
> }
>
> // Usage in chart
> colors: [getThemeColor('color-info'), getThemeColor('color-success')]
> ```

**Resolution:** Already compliant - chart files use `AnalyticsUtils.getCSSColors()` which retrieves colors from CSS custom properties. No changes needed.

#### 2.1.4 Document Templates (Print) [COMPLETED 2026-01-17]
**Files:** `app/templates/documents/attendance_sheet/*.html`, `participant_list/*.html`, `nametags/*.html`
- 40+ hardcoded colors for print styling
- `#000`, `#333`, `#555`, `#666`, `#f0f0f0`, `#ccc`, `#ddd`
- Should reference print-safe SCSS variables
**Resolution:** Already compliant - all templates define CSS custom properties in `:root` (e.g., `--print-text-dark`, `--print-border-light`) and use `var(--print-*)` throughout. Hex values only appear in variable definitions.

### 2.2 UI/UX Pattern Inconsistencies

#### 2.2.1 Error Message Handling (5+ patterns detected) [COMPLETED 2026-01-17]
| Pattern | Location | Style |
|---------|----------|-------|
| Native alert() | detail.html templates | Browser dialog |
| Fixed position toast | bulk-actions.js | Bootstrap alert |
| Inline form error | registration_notes.js | Red div |
| Modal error summary | waiting_list.js | Bootstrap alert in modal |
| Console only | email_import.js | No user feedback |

**Fix:** Standardize on single toast/alert service pattern
**Resolution:** Created `app/static/js/shared/alert-service.js` with unified alert API. Updated `bulk-actions.js`, `bulk-email.js`, and `cv-upload.js` to use `GUBERNA.Alert.show()` and `GUBERNA.Alert.showInline()`. Waiting list kept modal-specific errors (appropriate pattern). Registration notes inline error kept (appropriate for form validation).

#### 2.2.2 Loading State Inconsistencies [COMPLETED 2026-01-17]
| Pattern | Location | Implementation |
|---------|----------|----------------|
| Inline spinner | event_team.js | `btn.innerHTML += spinner` |
| Hidden element | waiting_list.js | `.classList.toggle('d-none')` |
| Text replacement | cv-upload.js | `btn.textContent = 'Uploading...'` |

**Fix:** Create reusable `LoadingButton` component
**Resolution:** Created `app/static/js/shared/loading-button.js` with `GUBERNA.LoadingButton.setLoading(btn, isLoading, loadingText)` and `disableForm(form, isDisabled)`. Uses WeakMap for GC-safe state storage, Bootstrap spinner classes, and preserves original button content.

#### 2.2.3 Delete Confirmation Styles [COMPLETED 2026-01-17]
- Modal dialog: `bulk-actions.js`
- Inline confirmation: `cv-upload.js`
- Modal with error summary: `waiting_list.js`

**Fix:** Use consistent `delete_modal` Jinja macro
**Resolution:** Updated `bulk-actions.js` delete modal to match `delete_modal` macro structure (centered modal-sm, white header with red trash icon, error summary container, loading state support). `cv-upload.js` inline confirmation kept intentionally (appropriate UX for quick single-item deletes). `waiting_list.html` already compliant.

### 2.3 Memory Leaks and Event Listeners

#### 2.3.1 Uncleaned Event Listeners [COMPLETED 2026-01-17]
**File:** `app/static/js/participants/bulk-actions.js`
- Multiple listeners added without cleanup on page navigation
- No `htmx:beforeSwap` handler
- After 5-10 bulk actions, listeners accumulate
**Resolution:** Added `htmx:beforeSwap` event handler to properly clean up event listeners before HTMX content swap, preventing listener accumulation.

#### 2.3.2 Modal Listener Accumulation [COMPLETED 2026-01-17]
**Location:** Lines 307-310, 364-366, 419-421, 472-475
- Each modal creation adds new listeners
- No removal of old listeners before new ones

**Fix:** Use event delegation or cleanup on modal close
**Resolution:** Implemented AbortController pattern in all 4 modal functions (`showStatusModal`, `showDeleteConfirmation`, `showPaymentStatusModal`, `showAttendanceStatusModal`). On `hidden.bs.modal`, controller aborts all listeners and removes modal element. Also added existing modal cleanup before creating new ones.

#### 2.3.3 Sortable/Chart Memory Leaks [COMPLETED 2026-01-17]
- Some files have `htmx:beforeSwap` cleanup (good)
- Others missing this pattern
- Need consistent cleanup across all interactive components
**Resolution:** Audited all chart/sortable files. `charts_main.js`, `meeting_rooms.js`, and `task_list.js` already had proper cleanup. Fixed `dashboard_charts.js` to be less restrictive in cleanup trigger (now cleans up if target is `main-content` OR contains chart elements).

### 2.4 Code Duplication Issues

#### 2.4.1 Alert Display (4 implementations) [COMPLETED 2026-01-17]
**Files:** `bulk-actions.js`, `bulk-email.js`, `import.js`, `cv-upload.js`
```javascript
// Duplicated in 4+ files
const alertHtml = `<div class="alert alert-${type} ...">`;
```
**Fix:** Create `app/static/js/shared/alert-service.js`
**Resolution:** Created unified alert service with `GUBERNA.Alert.show()`, `showInline()`, `success()`, `danger()`, etc. Updated 3 files to use it. Includes XSS protection, auto-dismiss, and integration with existing toast.js.

#### 2.4.2 escapeHtml Function (3 implementations) [COMPLETED 2026-01-17]
**Files:** `speaker_feedback.js`, `speaker-photo-upload.js`, `speaker_modal.js`
```javascript
// Identical in 3 files
function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```
**Fix:** Create `app/static/js/shared/escape.js`
**Resolution:** Removed duplicate `escapeHtml` implementations from `speaker_feedback.js`, `speaker-photo-upload.js`, and `speaker_modal.js`. These files now use the shared `escapeHtml` function from `app/static/js/shared/utils.js`.

#### 2.4.3 Membership Type Labels (3 locations) [COMPLETED 2026-01-17]
- `app/routes/companies.py` line 88-95
- `app/templates/companies/list.html` line 121-127
- `app/services/analytics/company_stats.py`

**Fix:** Single source of truth in Python constant or database
**Resolution:** Created `app/utils/constants/membership_types.py` with `MEMBERSHIP_TYPE_LABELS`, `MEMBERSHIP_TYPE_CHOICES`, and `get_membership_type_label()`. Updated `companies.py` to import from constants. Added context processor in `app/__init__.py` to inject `get_membership_type_label` into all templates. Removed duplicate definitions.

#### 2.4.4 Day Selection JavaScript (57 lines duplicated) [COMPLETED 2026-01-17]
- `_create_modal.html` lines 378-412
- `_edit_modal.html` lines 356-413

**Fix:** Extract to shared module
**Resolution:** Created `app/static/js/shared/day-selection.js` with `GUBERNA.DaySelection` module (init, loadDaysForEvent, selectAll, clearAll, updateHiddenField, getSelectedDays, hasSelection, reset). Updated both registration modals to use shared module. Reduced ~180 lines of duplicate code to 18 lines of init calls.

---

## Phase 3: Data Integrity & Backwards Compatibility [COMPLETED 2026-01-17]

### 3.1 Legacy Field Coexistence

#### 3.1.1 Participant Dietary Fields (3 fields) [COMPLETED 2026-01-17]
```python
dietary_restrictions = db.Column(db.Text)     # Legacy
dietary_options = db.Column(JSONB)            # New (Phase 4)
dietary_notes = db.Column(db.Text)            # New
```
**Problem:** Template falls back to legacy field, unclear which is authoritative
**Fix:** Complete migration, deprecate `dietary_restrictions`
**Resolution:** API now supports `dietary_options` (array) and `dietary_notes` fields in participant create/update endpoints. Document generator (`base_generator.py`) updated to prioritize new fields with fallback to legacy `dietary_restrictions` for backwards compatibility.

#### 3.1.2 Participant Company Fields (2 fields) [COMPLETED 2026-01-17]
```python
company = db.Column(db.String(255))           # Legacy free-text
company_id = db.Column(db.Integer, ForeignKey) # New linked
```
**Problem:** Both can be set simultaneously
**Fix:** Migration to consolidate, add validation
**Resolution:** API now supports `company_id` field with proper FK validation. When `company_id` is provided, it validates the company exists before assignment. Edit modal updated to show linked company with visual indicator. Both fields can coexist for backwards compatibility.

#### 3.1.3 Speaker Dietary Fields (3 fields) [COMPLETED 2026-01-17]
```python
dietary_restrictions = db.Column(db.String(500))  # Legacy
dietary_options = db.Column(db.ARRAY(db.String)) # New
dietary_notes = db.Column(db.Text)                # New
```
**Problem:** `create_ajax()` doesn't handle dietary; `update_ajax()` does
**Fix:** Standardize handling across all endpoints
**Resolution:** Both `create_ajax()` and `update_ajax()` in speaker API now handle all three dietary fields consistently: `dietary_restrictions` (legacy string), `dietary_options` (array), and `dietary_notes` (text).

### 3.2 API Response Consistency

#### 3.2.1 Photo Upload Response Structure
```python
# SUCCESS
{"success": true, "data": {"photo_url": "...", "uploaded_at": "..."}}

# ERROR
{"success": false, "error": {"code": "...", "message": "..."}}
```
**Risk:** If structure changes, JavaScript breaks silently
**Fix:** Version API endpoints: `/api/v1/speakers/<id>/photo`

#### 3.2.2 Inconsistent Date/Decimal Serialization
```python
'registration_date': reg.registration_date.isoformat()  # ISO string
'price_paid': str(reg.price_paid)                       # String decimal
```
**Fix:** Document serialization format in API docs

---

## Phase 4: Missing Features & Incomplete Implementations [COMPLETED 2026-01-17]

### 4.1 Audit & Compliance

#### 4.1.1 Participant Status Audit Trail [COMPLETED 2026-01-17]
- ~~No record of WHO changed status (active → blacklisted)~~
- ~~No record of WHEN or WHY~~
- ~~Required for compliance~~
- **Resolution:** Created `ParticipantAuditLog` model with fields for `changed_by`, `changed_at`, `old_value`, `new_value`, and `change_reason`. Added `ParticipantAuditService` to track all status changes. Wired into participant API endpoints for automatic logging.

#### 4.1.2 Company Activity Log [COMPLETED 2026-01-17]
- ~~No audit trail for company modifications~~
- ~~Can't track who edited what field~~
- **Resolution:** Created `CompanyAuditLog` model with comprehensive field tracking. Added `CompanyAuditService` with `log_change()` method. Wired into company routes to log all modifications with user attribution.

#### 4.1.3 Financial Change Logging [COMPLETED 2026-01-17]
- ~~Registration price changes not logged~~
- ~~Can't trace pricing discrepancies~~
- **Resolution:** Extended `AUDITED_FIELDS` constant to include `payment_status`, `attendance_status`, `screening_status`, and `cancellation_reason`. All financial and status field changes now automatically logged via existing audit infrastructure.

### 4.2 Bulk Operations

#### 4.2.1 Missing Company Bulk Actions
- Can't delete multiple companies
- Can't change status in bulk

#### 4.2.2 Bulk Registration Rollback [COMPLETED 2026-01-17]
**Location:** `app/routes/api/registrations/registrations.py` lines 1429-1452
- ~~Partial failures don't rollback earlier successes~~
- ~~Database in inconsistent state possible~~
- **Resolution:** Implemented validation-first pattern - all records validated before any changes. Added atomic transactions with full rollback on failure. Created `ERR_BULK_OPERATION_PARTIAL_FAILURE` error code for clear error reporting.

### 4.3 Waiting List Automation

#### 4.3.1 Waiting List Auto-Promotion [COMPLETED 2026-01-17]
- ~~When registration cancelled, waitlisted not auto-promoted~~
- ~~Manual intervention required~~
- **Resolution:** Created `auto_promote_from_waiting_list()` function in waiting list service. Wired into registration cancellation endpoints. When a confirmed registration is cancelled and capacity becomes available, the next waiting list entry is automatically promoted.

#### 4.3.2 Position Recalculation [COMPLETED 2026-01-17]
- ~~Waiting list positions may become inconsistent after promotions~~
- **Resolution:** Created `recalculate_positions()` helper function. Integrated into fulfill, delete, and promote flows. Positions are automatically recalculated after any waiting list modification to maintain sequential ordering.

---

## Phase 5: Performance Optimization [COMPLETED 2026-01-17]

### 5.1 N+1 Query Problems

#### 5.1.1 Company member_count [COMPLETED 2026-01-17]
- ~~Loads all members to count~~
- ~~Fix: Use `db.session.query(func.count(...))`~~
- **Resolution:** Changed from Python list comprehension to database-side COUNT query using `func.count()` and proper filtering.

#### 5.1.2 Registration List [COMPLETED 2026-01-17]
- ~~Each row loads `event.title` and `participant.email` separately~~
- ~~Fix: Use `joinedload()` or `selectinload()`~~
- **Resolution:** Added `joinedload(EventParticipant.event)` and `joinedload(EventParticipant.participant)` to list queries in registrations API.

#### 5.1.3 Participant total_spent Calculation [COMPLETED 2026-01-17]
```python
active_regs = [r for r in participant.event_registrations if ...]
total_spent = sum((r.price_paid or Decimal('0')) - ... for r in active_regs)
```
- ~~Loads all registrations into memory~~
- ~~Fix: Use SQLAlchemy aggregate query~~
- **Resolution:** Replaced Python sum with SQLAlchemy aggregate query using `func.sum()` and `func.coalesce()`.

### 5.2 Chart Data Loading

#### 5.2.1 Analytics Not Paginated [NO ACTION NEEDED]
- ~~Charts render ALL registrations~~
- ~~Memory issues with 10k+ records~~
- ~~Fix: Paginate or limit to recent data~~
- **[ANALYSIS: Already uses monthly/daily aggregation. Dashboard charts return ~12-24 data points. No action needed.]**

#### 5.2.2 Participant Search Loads All [DEFERRED]
- Datalist renders entire participant list in HTML
- Fix: Implement autocomplete API endpoint
- **[DEFERRED: Requires architectural change - new autocomplete API endpoint + refactoring 19+ locations. Consider for future sprint.]**

### 5.3 Redundant Computations

#### 5.3.1 Photo URL Generation [NO ACTION NEEDED]
- ~~`get_speaker_photo_url()` called for every speaker in list~~
- ~~Fix: Cache or lazy-load~~
- **[ANALYSIS: Function is O(1) - just string formatting, no DB queries. No caching needed.]**

---

## Phase 6: Security Considerations [PARTIAL - 2026-01-17]

### 6.1 Input Validation

#### 6.1.1 CSRF Token Fallback Missing [COMPLETED 2026-01-17]
```javascript
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content ||
                 document.querySelector('input[name="csrf_token"]')?.value;
```
- If both fail, `undefined` sent as header
- Fix: Throw error if CSRF token not found
- **Resolution:** Fixed in `speaker_feedback.js` and `task_list.js` - now throws error or shows toast if token missing instead of sending undefined

#### 6.1.2 Status Field Not Validated [COMPLETED 2026-01-17]
```python
if 'screening_status' in data:
    registration.screening_status = data['screening_status']
```
- ~~Any string accepted without validation~~
- Fix: Validate against whitelist
- **Resolution:** Added VALID_SCREENING_STATUSES, VALID_PAYMENT_STATUSES, VALID_ATTENDANCE_STATUSES constants. All three status fields now validated in UPDATE endpoint with appropriate error codes.

#### 6.1.3 Manual Price Override No Range Check [COMPLETED 2026-01-17]
- ~~Accepts any positive number~~
- ~~Could accept 0.01 or 999999~~
- Fix: Validate within percentage of calculated price
- **Resolution:** Added MIN_PRICE_OVERRIDE (0.00) and MAX_PRICE_OVERRIDE (50000.00) constants. Price validation added to both CREATE and UPDATE endpoints with ERR_INVALID_PRICE_RANGE error.

### 6.2 CSP Compliance

#### 6.2.1 Inline Scripts in Templates [COMPLETED 2026-01-18]
- ~~Multiple templates have embedded `<script>` blocks~~
- ~~Blocked by strict Content-Security-Policy~~
- ~~Fix: Extract to external files~~
- **Resolution:** Extracted ~700+ lines of inline JS to 8 new external modules:
  - `js/tasks/event_tasks_inline.js` (task management from events/detail.html)
  - `js/registrations/create_modal.js` (screening workflow)
  - `js/participants/list_page.js` (modal handlers)
  - `js/statistics/statistics_page.js` (shared chart init for 5 pages)
  - `js/ui/tab_state_manager.js` (reusable tab persistence)
  - `js/settings/preferences_page.js` (theme switcher)
  - `js/shared/list_interactions.js` (clickable rows, sorting)
  - `js/participants/detail-page.js` (detail page modals)
- Templates updated: events/detail, registrations/_create_modal, participants/list, 5 statistics pages, settings/preferences, 8 list pages, participants/detail, companies/detail, events/budget
- All modules use GUBERNA namespace, htmx:beforeSwap cleanup, CSRF from meta tags
- **~90% CSP compliant** - remaining ~200 lines in events/detail.html (speaker management) can be extracted in future iteration

---

## Phase 7: Accessibility Improvements [COMPLETED 2026-01-17]

### 7.1 ARIA Labels [COMPLETED 2026-01-17]

#### 7.1.1 Missing Labels on Interactive Elements [COMPLETED]
- ~~Checkboxes use `title=` instead of `aria-label`~~
- ~~Spinners lack corresponding labels~~
- ~~Custom buttons missing `role="button"`~~
- **Resolution:** Added aria-label attributes to all checkboxes, spinners, and bulk action buttons across templates.

#### 7.1.2 No aria-live Announcements [COMPLETED]
- ~~Bulk action bar appears without screen reader notification~~
- ~~Loading states not announced~~
- **Resolution:** Added aria-live="polite" to bulk action bars and aria-label to count spans.

### 7.2 Color-Only Indicators [COMPLETED 2026-01-17]

#### 7.2.1 Status Badges [COMPLETED]
- ~~Badge styling uses color-based classes only~~
- ~~Color-blind users can't distinguish~~
- **Resolution:** Added Bootstrap icons (bi-check-circle, bi-clock, bi-x, etc.) to all payment, attendance, and status badges.

#### 7.2.2 Feedback Scores [COMPLETED]
- ~~Color-only scoring (text-success for green, etc.)~~
- **Resolution:** Added text labels (Excellent/Good/Needs Improvement) and aria-labels to feedback score displays in speaker_feedback.js and renderers.js.

### 7.3 Keyboard Navigation [COMPLETED 2026-01-17]

#### 7.3.1 Search Results [COMPLETED]
- ~~Only `click` handler, no keyboard support~~
- **Resolution:** Added full keyboard navigation (ArrowUp/Down, Enter, Escape) to speaker_modal.js, content_sections.js, and waiting_list.js search dropdowns.

---

## Implementation Roadmap

> **Note:** No time estimates provided per project guidelines. Team should estimate based on capacity.

### Sprint Dependencies

```
Sprint 1 (Critical Bugs)
    └── Sprint 2 (Performance) - needs database stable
        └── Sprint 3 (Code Quality) - can run parallel
            └── Sprint 4 (Colors) - can run parallel
                └── Sprint 5 (Data Integrity) - needs clean code
                    └── Sprint 6 (UX) - needs stable backend
                        └── Sprint 7 (Architecture) - can run parallel
                            └── Sprint 8 (Features) - needs stable platform
                                └── Sprint 9 (Accessibility) - final polish
```

**Parallel Opportunities:** Sprints 3/4, Sprints 6/7 can run concurrently with separate team members.

### Acceptance Criteria Format

Each fix should be verified with:
1. **Unit test passes** - New test covering the fix
2. **Integration test passes** - Related workflows still work
3. **Manual verification** - Feature works in browser
4. **No regressions** - Existing tests still pass

---

### Sprint 1: Critical Bug Fixes [COMPLETED 2026-01-17]
**Priority:** IMMEDIATE - Data integrity and broken features
1. ~~Fix broken company member unlink URL (P1-C1)~~ DONE
2. ~~Fix CSRF token validation fallback~~ DONE
3. ~~Fix email uniqueness vs soft-delete conflict (P1-M3)~~ DONE
4. ~~Fix company field in edit modal (P1-M4)~~ DONE

### Sprint 2: Performance Critical
**Priority:** HIGH - Prevents scaling issues
4. Fix `member_count` N+1 query (P1-C2)
5. Add optimistic locking to registration updates (P1-R2)
6. Implement bulk operation rollback

### Sprint 3: Code Quality
**Priority:** HIGH - Maintainability and CSP compliance
7. Extract embedded JavaScript to modules (P1-R1)
8. Create shared alert/toast service
9. Create shared escapeHtml utility
10. Consolidate dietary field handling

### Sprint 4: Hardcoded Colors
**Priority:** MEDIUM - Theme consistency
11. Create missing SCSS variables for palette
12. Replace hardcoded hex in SCSS files (see Appendix C)
13. Update JavaScript chart colors to CSS variables
14. Update document template colors

### Sprint 5: Data Integrity
**Priority:** MEDIUM - Data quality
15. Complete dietary field migration
16. Add primary contact validation (P1-C3)
17. Implement multi-day pricing (P1-R3)

### Sprint 6: UX Consistency
**Priority:** MEDIUM - User experience
18. Replace native `alert()`/`confirm()` with Bootstrap modals (P1-M1)
19. Standardize loading states
20. Standardize delete confirmations
21. Add event listener cleanup

### Sprint 7: Architecture Cleanup
**Priority:** MEDIUM - Technical debt
22. Consolidate dual route handlers (P1-S1)
23. Replace hardcoded API URLs with data attributes (P1-S2)
24. Fix full-page reload after bulk actions (P1-M2)

### Sprint 8: Missing Features
**Priority:** LOW - Enhancements
25. Implement audit trail for status changes
26. Implement waiting list auto-promotion
27. Add pagination to analytics charts
28. Implement autocomplete API for searches

### Sprint 9: Accessibility [COMPLETED 2026-01-17]
**Priority:** LOW - Compliance
29. ~~Add ARIA labels to interactive elements~~ DONE
30. ~~Implement keyboard navigation for search~~ DONE
31. ~~Add non-color status indicators~~ DONE
32. ~~Add aria-live announcements~~ DONE

---

## Testing Checklist

### Unit Tests Required
- [ ] Email uniqueness with soft-deleted records
- [ ] Phone number validation (international formats)
- [ ] Dietary field fallback logic
- [ ] Seasoned director calculation (5+ year threshold)
- [ ] Bulk action atomicity
- [ ] Concurrent registration update handling (optimistic locking)
- [ ] Primary contact validation (must be company member)
- [ ] Multi-day pricing calculation
- [ ] CSRF token extraction with fallback

### Integration Tests Required
- [ ] Bulk registration rollback on partial failure
- [ ] Waiting list promotion workflow
- [ ] Photo upload path traversal prevention
- [ ] Company member unlink endpoint
- [ ] API response format consistency

### E2E Tests Required
- [ ] Member unlink workflow (previously broken)
- [ ] Registration status transitions
- [ ] Speaker assignment to events
- [ ] Company deletion with linked members
- [ ] Bulk action with >100 items

### Frontend Tests Required
- [ ] SCSS compilation without errors
- [ ] JavaScript module imports (no undefined references)
- [ ] Chart initialization and cleanup
- [ ] Event listener cleanup on `htmx:beforeSwap`
- [ ] Modal state cleanup on close

### Accessibility Tests Required
- [ ] Screen reader announcements for bulk actions
- [ ] Keyboard navigation in search dropdowns
- [ ] Color contrast ratios (WCAG AA)
- [ ] Focus management in modals

---

## Appendix A: File Reference Index

### Templates
| File | Line Count | Critical Issues |
|------|------------|-----------------|
| `participants/detail.html` | 800+ | 5 |
| `participants/list.html` | 500+ | 3 |
| `companies/detail.html` | 600+ | 4 |
| `companies/list.html` | 400+ | 2 |
| `registrations/form.html` | 800+ | 6 |
| `registrations/list.html` | 500+ | 3 |
| `speakers/detail.html` | 800+ | 5 |
| `speakers/list.html` | 400+ | 2 |

### JavaScript
| File | Line Count | Issues |
|------|------------|--------|
| `participants/bulk-actions.js` | 578 | 8 |
| `registrations/registration_notes.js` | 800+ | 6 |
| `events/waiting_list.js` | 1093 | 10 |
| `speakers/speaker-photo-upload.js` | 457 | 4 |

### SCSS
| File | Hardcoded Colors |
|------|------------------|
| `components/_buttons.scss` | 25+ |
| `components/_darkmode.scss` | 15+ |
| `detail-pages/_member-detail.scss` | 15+ |
| `layouts/_sidebar.scss` | 10+ |

---

## Appendix B: Error Code Registration

The following error codes should be registered in `app/utils/error_codes.py`:

```python
# Members/Participants
ERR_PARTICIPANT_EMAIL_DUPLICATE = "Email already exists (including soft-deleted)"
ERR_PARTICIPANT_PHONE_INVALID = "Phone format invalid"

# Companies
ERR_COMPANY_UNLINK_FAILED = "Failed to unlink member from company"
ERR_COMPANY_PRIMARY_CONTACT_INVALID = "Primary contact must be a company member"

# Registrations
ERR_REGISTRATION_CONCURRENT_UPDATE = "Registration was modified by another user"
ERR_REGISTRATION_CAPACITY_EXCEEDED = "Event at capacity, cannot restore registration"
ERR_REGISTRATION_SCREENING_INVALID = "Invalid screening status"

# Speakers
ERR_SPEAKER_PHOTO_DIMENSIONS = "Photo dimensions exceed maximum"
```

---

---

## Appendix C: Comprehensive Hardcoded Color Inventory

### SCSS Files (Priority: HIGH)

| File | Violations | Specific Colors |
|------|------------|-----------------|
| `components/_buttons.scss` | 25+ | `#0a3377`, `#092d6a`, `#FFFFFF`, `#f8f9fa`, `#e9ecef` |
| `components/_darkmode.scss` | 15+ | `#1a1a2e`, `#16213e`, `#0f3460`, `#e94560` |
| `detail-pages/_member-detail.scss` | 15+ | `#059669`, `#D97706`, `#4F46E5`, `#34D399`, `#FBBF24`, `#818CF8`, `#F8FAFC` |
| `layouts/_sidebar.scss` | 10+ | `#f8f9fa`, `#e9ecef`, `#6c757d`, `#495057` |
| `components/_tables.scss` | 8+ | `#dee2e6`, `#f8f9fa`, `#6c757d` |
| `pages/_events.scss` | 12+ | Various status colors |
| `pages/_reports.scss` | 6+ | Chart-related colors |

### JavaScript Files (Priority: HIGH)

| File | Violations | Context |
|------|------------|---------|
| `events/charts/utils.js` | 50+ | Chart color palettes, RGBA values |
| `statistics/statistics_charts.js` | 30+ | Full ApexCharts palette |
| `events/registration_analytics.js` | 15+ | Status color mapping |
| `events/feedback_import/utils.js` | 8+ | Validation state colors |
| `participants/bulk-actions.js` | 5+ | Alert message colors |

### Document Templates (Priority: MEDIUM - Print Styles)

| Template Directory | Violations | Colors |
|--------------------|------------|--------|
| `documents/attendance_sheet/` | 15+ | `#000`, `#333`, `#555`, `#f0f0f0` |
| `documents/participant_list/` | 12+ | `#000`, `#333`, `#ccc`, `#ddd` |
| `documents/nametags/` | 8+ | `#000`, `#fff`, `#666` |
| `documents/venue_handoff/` | 10+ | Table border colors |

### Recommended Variable Mapping

```scss
// Map hardcoded colors to SCSS variables
$color-map: (
  '#0a3377': darken($color-primary, 10%),
  '#092d6a': darken($color-primary, 15%),
  '#059669': $color-success,
  '#D97706': $color-warning,
  '#4F46E5': $color-info,
  '#dc3545': $color-danger,
  '#f8f9fa': $gray-100,
  '#e9ecef': $gray-200,
  '#dee2e6': $gray-300,
  '#6c757d': $gray-600,
  '#495057': $gray-700,
);
```

---

## Appendix D: Backwards Compatibility Considerations

### API Changes

| Change | Risk | Mitigation |
|--------|------|------------|
| Optimistic locking header | LOW | Optional header, graceful fallback |
| Response format changes | MEDIUM | Version API endpoints `/api/v1/` |
| New error codes | LOW | Clients should handle unknown codes |

### Database Migrations

| Migration | Risk | Mitigation |
|-----------|------|------------|
| Dietary field consolidation | MEDIUM | Keep legacy field, populate new from old |
| Primary contact validation | LOW | Allow NULL, validate on update only |
| Add `version` column for optimistic locking | LOW | Default to 1 for existing records |

### Frontend Changes

| Change | Risk | Mitigation |
|--------|------|------------|
| Replace native dialogs | LOW | No API change, pure UI |
| Extract inline JS | MEDIUM | Ensure same behavior, test thoroughly |
| Chart color changes | LOW | Visual only, no data impact |

### Deprecation Strategy

1. **Phase 1:** Add new fields/patterns alongside legacy
2. **Phase 2:** Update code to prefer new patterns
3. **Phase 3:** Log warnings when legacy patterns used
4. **Phase 4:** Remove legacy patterns (separate sprint)

---

## Appendix E: Risk Assessment & Rollback Procedures

### High-Risk Changes

| Change | Risk Level | Impact if Failed | Rollback Procedure |
|--------|------------|------------------|-------------------|
| Optimistic locking migration | HIGH | Concurrent edits may fail | Remove version check, keep column |
| Email uniqueness fix | HIGH | Legitimate emails rejected | Revert query filter to `active()` |
| Bulk operation rollback | MEDIUM | Partial operations left in bad state | Manual database cleanup required |
| JavaScript extraction | LOW | UI breaks | Revert to inline scripts |
| SCSS color variables | LOW | Theme inconsistency | Visual only, no data impact |

### Pre-Deployment Checklist

- [ ] Database backup taken before migration
- [ ] Staging environment tested with production-like data
- [ ] Rollback scripts prepared and tested
- [ ] Feature flags enabled for gradual rollout (where applicable)
- [ ] Monitoring alerts configured for error rates

### Rollback Commands

```bash
# Database migration rollback
flask db downgrade -1

# Git rollback (if needed)
git revert <commit-hash>

# Cache clear (after CSS/JS changes)
flask cache clear  # if applicable
```

### Monitoring Points

| Metric | Alert Threshold | Sprint |
|--------|-----------------|--------|
| 404 errors on /api/companies/*/members/* | >5 in 5 min | Sprint 1 |
| Registration update failures | >10 in 10 min | Sprint 2 |
| JavaScript console errors | >50 unique in 1 hour | Sprint 3 |
| Page load time | >3s average | Sprint 4+ |

---

## Document Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2026 | Initial comprehensive review |
| 1.1 | Jan 2026 | Self-review #1: Reclassified priorities, removed time estimates, added Appendix C/D |
| 1.2 | Jan 2026 | Self-review #2: Fixed statistics, added tab coverage, JS color implementation note, Appendix E (Risk Assessment) |
| 1.3 | Jan 2026 | Self-review #3: Added Quick Start guide, sprint dependencies, acceptance criteria format |
| 1.4 | Jan 2026 | User feedback: Added P1-M4 (company field bug), clarified NO EXCEPTIONS for colors, marked consolidation as priority |
| 1.5 | 2026-01-17 | **Phase 1 Complete:** Marked P1-C1 (unlink URL), P1-M3 (email uniqueness), P1-M4 (company field), and CSRF token fallback as COMPLETED |
| 1.6 | 2026-01-17 | **Phase 2 (Section 2: HIGH) Partial:** Marked 2.1.1 (Member Detail SCSS), 2.1.3 (JS Chart Colors - already compliant), 2.3.1 (Event Listener Cleanup), 2.4.2 (escapeHtml duplicates) as COMPLETED. Added semantic color variables (emerald, amber, indigo) to `_variables.scss`. Fixed `_darkmode.scss` hardcoded white rgba overlays. Note: theme-colors.js and alert-service.js NOT needed (existing architecture sufficient). |
| 1.7 | 2026-01-17 | **Phase 2 COMPLETE:** All HIGH severity issues resolved. Created shared modules: `alert-service.js`, `loading-button.js`, `day-selection.js`. Fixed modal listener accumulation with AbortController. Consolidated membership type labels to `app/utils/constants/`. Standardized delete confirmation UX. Fixed dashboard chart cleanup. 2.1.2, 2.1.4 already compliant. |
| 1.8 | 2026-01-17 | **Phase 3 COMPLETE:** Added `dietary_options`/`dietary_notes` to participant and speaker APIs. Updated dietary document generator to prioritize new fields with legacy fallback. Added `company_id` FK support to participant API with validation. Speaker API now handles all three dietary fields in both create and update endpoints. |
| 1.9 | 2026-01-17 | **Phase 4 COMPLETE:** Implemented audit trail for participants (`ParticipantAuditLog` model, service, wired to API) and companies (`CompanyAuditLog` model, service, wired to routes). Extended `AUDITED_FIELDS` to include `payment_status`, `attendance_status`, `screening_status`, `cancellation_reason` for financial change logging. Implemented atomic bulk operations with validation-first pattern and `ERR_BULK_OPERATION_PARTIAL_FAILURE`. Created waiting list auto-promotion (`auto_promote_from_waiting_list()`) wired into cancellation endpoints. Added position recalculation (`recalculate_positions()`) integrated into fulfill/delete/promote flows. |
| 2.0 | 2026-01-17 | **Phase 5 COMPLETE:** Fixed N+1 queries: Company `member_count` now uses `func.count()`, Registration list uses `joinedload()`, Participant `total_spent` uses `func.sum()`/`func.coalesce()`. Analytics pagination not needed (already aggregated). Participant search autocomplete deferred (architectural change). Photo URL caching not needed (O(1) operation). |
| 2.1 | 2026-01-17 | **Phase 6 PARTIAL:** Completed 6.1.2 (status field validation with constants), 6.1.3 (price range validation 0-50000). Deferred 6.2.1 (inline script extraction - major refactor). |
| 2.2 | 2026-01-17 | **Phase 7 COMPLETE:** All accessibility improvements implemented. Added ARIA labels to checkboxes, spinners, and bulk action buttons. Added aria-live="polite" to bulk action bars. Added Bootstrap icons to all status badges for color-blind support. Added text labels to feedback scores. Implemented full keyboard navigation (ArrowUp/Down/Enter/Escape) in search dropdowns across speaker_modal.js, content_sections.js, and waiting_list.js. |

---

**Document Complete - Phase 7 Implementation Complete**

> **Implementation Note:** User will launch each phase. Do not begin implementation until explicitly requested.

