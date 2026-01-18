---
name: error-message-validator
description: Validates error messages are user-friendly, specific, and actionable
tags: [validation, errors, ux, quality]
---

# Error Message Validator

When writing or reviewing error messages in code, APIs, or UI, ensure messages follow best practices for user experience.

## Core Principles

**Specific:** Tell users exactly what's wrong
- Bad: "Invalid input"
- Good: "Email format invalid. Expected: user@example.com"

**Actionable:** Explain how to fix
- Bad: "Database error"
- Good: "Email already registered. Use different email or reset password."

**Contextual:** Include actual vs expected values
- Bad: "File too large"
- Good: "File too large. Max 5MB. Yours: 8.2MB."

**Plain language:** Avoid technical jargon
- Bad: "Constraint violation on FK_user_events"
- Good: "Cannot delete event. 12 participants registered. Cancel registrations first."

## Auto-Activation

Triggers when:
- Writing error handling code (`raise`, `throw`, `return error`)
- Defining API error responses
- Creating form validation messages
- Reviewing existing error messages
- User mentions "error message", "validation", "user feedback"

## Quality Standards

**Accept if message:**
- Explains exactly what's wrong
- Provides concrete next steps
- Uses plain language (no jargon)
- Includes relevant context (values, limits)

**Reject if message:**
- Too generic ("Error", "Invalid")
- Only technical details (stack traces, codes)
- No recovery path
- Blames user harshly

## Sub-Files (Load When Needed)

**Read `patterns.md` when:**
- Scanning code for error message quality
- Need specific red flags and good patterns
- Checking context-specific messages (auth, validation, permissions)

**Read `api_format.md` when:**
- Writing API error responses
- Need JSON error response format
- Implementing form validation display

## Scripts

- `scan_errors.py` - Scans codebase for generic error messages
  ```bash
  python .claude/skills/error-message-validator/scan_errors.py app/
  ```
