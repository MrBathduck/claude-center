# API Error Response Format

## Error Message Structure

### User-facing errors
```
[What's wrong] + [Why it's wrong] + [How to fix]
"Email already registered. Another user has this email. Use different email or reset password."
```

### API error responses (JSON)
```json
{
  "success": false,
  "error": {
    "code": "ERR_EMAIL_EXISTS",
    "message": "Email already registered. Use different email.",
    "field": "email",
    "details": {"email": "user@example.com"}
  }
}
```

## Standard Error Fields

| Field | Required | Description |
|-------|----------|-------------|
| `success` | Yes | Always `false` for errors |
| `error.code` | Yes | Machine-readable code (ERR_*) |
| `error.message` | Yes | Human-readable message |
| `error.field` | No | Field name for validation errors |
| `error.details` | No | Additional context (values, limits) |

## Common Error Codes

```python
# Registration errors in error_codes.py
ERR_EMAIL_EXISTS = "Email already registered"
ERR_EVENT_FULL = "Event at full capacity"
ERR_INVALID_DATE = "Invalid date format"
ERR_PERMISSION_DENIED = "Insufficient permissions"
```

## Form Validation Display

**Best practices:**
- Show inline next to field
- Use red color + icon
- Trigger on blur or submit (not on every keystroke)

**HTML pattern:**
```html
<div class="form-group has-error">
  <label for="email">Email</label>
  <input type="email" id="email" class="form-control is-invalid">
  <div class="invalid-feedback">
    Email already registered. Use different email or reset password.
  </div>
</div>
```

## HTTP Status Code Mapping

| Code | Use For |
|------|---------|
| 400 | Validation errors, malformed requests |
| 401 | Authentication required |
| 403 | Permission denied |
| 404 | Resource not found |
| 409 | Conflict (duplicate, constraint violation) |
| 422 | Unprocessable entity (business logic error) |
| 500 | Server error (log details, show generic message) |

## Server Error Handling

**NEVER expose to user:**
- Stack traces
- Database connection strings
- Internal file paths
- SQL queries

**DO show:**
```json
{
  "success": false,
  "error": {
    "code": "ERR_INTERNAL",
    "message": "Something went wrong. Please try again or contact support."
  }
}
```

**DO log internally:**
```python
logger.error(f"Database error: {str(e)}", exc_info=True)
```
