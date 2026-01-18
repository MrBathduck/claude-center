# Error Message Patterns

## Red Flags (Suggest Improvements)

**Generic messages:**
- "Error", "Invalid", "Failed", "Bad request"

**HTTP codes only:**
- "Error 400", "500 Internal Server Error"

**Technical jargon:**
- "Constraint violation", "Null pointer", "Stack overflow"

**No recovery path:**
- Errors without suggesting next steps

**Passive voice:**
- "The request was invalid" -> "Email format invalid"

## Good Patterns (Approve)

**Specific field:**
- "Password must be at least 8 characters"

**Comparison:**
- "Start date must be before end date"

**Current state:**
- "Event at full capacity (50/50)"

**Clear action:**
- "Join waiting list?" or "Try again with valid email"

**Numbered limits:**
- "Max 5MB", "Between 1-100"

## Language Guidelines

**DO:**
- Use active voice ("Email format invalid")
- Be concise (1-2 sentences max)
- Use "you" or "your" ("Your file is too large")
- Suggest alternatives ("Use PNG or JPG instead")
- Include actual values when helpful ("Max 100 characters. Yours: 142")

**DON'T:**
- Use passive voice ("The email was found to be invalid")
- Use jargon ("FK constraint violated", "Serialization failed")
- Blame user ("You entered wrong data")
- Be vague ("Something went wrong", "Please try again later")
- Expose internal details ("Database connection timeout on pg_connection_123")

## Context-Specific Checks

### Authentication errors
- Bad: "Invalid credentials"
- Good: "Email or password incorrect. Forgot password?"

### Validation errors
- Bad: "Field required"
- Good: "Email required"

### Permission errors
- Bad: "Access denied"
- Good: "Admin access required. Contact your administrator."

### Capacity/limit errors
- Bad: "Limit reached"
- Good: "Event at full capacity (50/50). Join waiting list?"

### File upload errors
- Bad: "Upload failed"
- Good: "Only PDF files allowed. Your file: document.docx"
