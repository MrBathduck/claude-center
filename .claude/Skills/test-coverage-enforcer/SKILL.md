---
name: test-coverage-enforcer
description: Enforces test coverage standards and identifies untested code paths
tags: [testing, coverage, quality, pytest]
---

# Test Coverage Enforcer

When writing tests or reviewing code, ensure adequate test coverage and identify critical untested paths.

## Coverage Standards

**Check project documentation first** for specific targets. Common standards:
- **Models/Core Logic:** 90%+ (business-critical)
- **Routes/API Endpoints:** 80%+ (user-facing)
- **Utilities/Helpers:** 100% (reused everywhere)
- **Overall Project:** 80%+ minimum

## Critical Coverage Gaps

**CRITICAL (Must test):**
- Authentication/authorization logic
- Payment/financial calculations
- Data validation and sanitization
- Database transactions and rollbacks
- API endpoints (especially POST/PUT/DELETE)
- Error handling paths
- Permission checks

**HIGH (Should test):**
- Business logic functions
- Form validation
- State transitions (status changes)
- Search/filter functionality

## Auto-Activation

Triggers when:
- Running test commands (`pytest`, `jest`, `go test`)
- Writing new tests
- Adding new features/functions
- User mentions "coverage", "test", "untested"
- Before completing implementation tasks

## Quality Gates

**Before marking task complete:**
1. Run coverage report
2. Check coverage meets project standards
3. Identify critical untested code
4. Add tests for gaps or document why not tested

**Warnings to issue:**
- Coverage below project threshold
- New code added without tests
- Critical paths (auth, payments) untested
- Only happy path tested, no error cases

## Sub-Files (Load When Needed)

**Read `pytest_guide.md` when:**
- Running Python tests
- Need pytest-specific commands
- Writing pytest fixtures or parametrized tests

**Read `jest_guide.md` when:**
- Testing JavaScript code
- Need Jest-specific configuration

**Read `critical_paths.md` when:**
- Identifying what MUST be tested
- Reviewing coverage gaps
- Prioritizing test writing

## Scripts

- `check_coverage.py` - Runs pytest coverage and validates thresholds
  ```bash
  python .claude/skills/test-coverage-enforcer/check_coverage.py
  python .claude/skills/test-coverage-enforcer/check_coverage.py models
  ```
