# Critical Paths - What MUST Be Tested

## Priority Levels

### CRITICAL (Must test - no exceptions)

**Authentication/Authorization:**
- Login/logout flows
- Password hashing and verification
- Session management
- Token validation (if applicable)
- Role-based access control checks

**Financial/Payments:**
- Price calculations
- Discount application
- Invoice totals (if applicable)
- Refund logic

**Data Validation:**
- Input sanitization
- XSS prevention
- SQL injection prevention
- File upload validation
- Email format validation

**Database Operations:**
- Transaction rollbacks on error
- Cascade delete behavior
- Foreign key constraints
- Unique constraint handling

**API Security:**
- CSRF token validation
- Rate limiting (if applicable)
- Permission checks on all endpoints
- Input validation on POST/PUT/DELETE

### HIGH (Should test)

**Business Logic:**
- Registration workflows
- Event capacity management
- Status transitions
- Scheduling logic
- Email sending triggers

**Form Validation:**
- Required field checks
- Format validation
- Cross-field validation
- Error message generation

**State Transitions:**
- Event status changes
- Registration status changes
- User role changes
- Soft delete operations

### MEDIUM (Nice to test)

**UI Components:**
- Form rendering
- Error display
- Success messages
- Navigation states

**Helpers/Utilities:**
- Date formatting
- String manipulation
- Number formatting
- Translation helpers

### LOW (Optional)

**Simple Operations:**
- Getters/setters
- Property access
- Configuration loading
- Constants/enums

## Testing Checklist

For each critical path, verify:

- [ ] Happy path works
- [ ] Invalid input handled
- [ ] Edge cases covered (empty, null, max values)
- [ ] Error messages are user-friendly
- [ ] Permissions are checked
- [ ] Database state is correct after operation
- [ ] Audit trail created (if applicable)

## Common Gaps to Check

1. **Auth endpoints without permission tests**
   - Admin-only routes accessible by regular users?
   - API endpoints missing @role_required?

2. **Validation only tested with valid data**
   - What happens with empty string?
   - What happens with very long input?
   - What happens with special characters?

3. **Database operations without constraint tests**
   - Duplicate key handling?
   - Foreign key violation handling?
   - Null value handling?

4. **Error paths not tested**
   - What if external service fails?
   - What if database connection drops?
   - What if file system is full?

## Per-Module Requirements

| Module | Minimum Coverage | Critical Focus |
|--------|------------------|----------------|
| `app/models/` | 90% | Validation, relationships |
| `app/services/` | 90% | Business logic, error handling |
| `app/routes/api/` | 80% | Auth, permissions, validation |
| `app/routes/` | 80% | Auth, form handling |
| `app/utils/` | 100% | Edge cases |
