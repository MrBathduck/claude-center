# Pytest Coverage Guide

## Coverage Commands

### Run with coverage
```bash
pytest --cov=app --cov-report=term-missing
```

### Check specific module
```bash
pytest tests/test_models/ --cov=app.models --cov-report=term
```

### Fail if below threshold
```bash
pytest --cov=app --cov-fail-under=80
```

### Generate HTML report
```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html
```

## Coverage Analysis

**Review coverage report for:**
1. **Untested critical paths:** Auth, payments, permissions
2. **Missing edge cases:** Empty inputs, invalid data, boundary conditions
3. **Error branches:** Exception handling, validation failures
4. **Integration gaps:** Database interactions, API calls

**Common gaps:**
- Error handlers only test happy path, not failures
- Validation tested with valid data, not invalid
- Database operations not tested with constraints
- API endpoints missing auth/permission tests
- Edge cases (empty lists, null values, boundary limits)

## Test Quality Checks

**Good tests:**
- Test both success and failure paths
- Include edge cases (empty, null, max/min values)
- Test error handling
- Verify state changes
- Check permissions/auth
- Independent (don't rely on order)
- Fast (< 1 second each)

**Bad tests:**
- Only test happy path
- Skip error cases
- Test implementation, not behavior
- Fragile (break on minor changes)
- Slow (database setup every test)

## Coverage Recommendations

**For low coverage (<60%):**
- Start with critical paths: auth, payments, data validation
- Write integration tests for complete workflows
- Add unit tests for business logic

**For medium coverage (60-80%):**
- Focus on edge cases and error paths
- Add tests for recently changed code
- Test permission boundaries

**For high coverage (>80%):**
- Review coverage report for quality, not just quantity
- Ensure tests verify behavior, not just execute code
- Check mutation testing for test effectiveness

## Project Configuration

Check project docs for:
- Coverage targets per module
- Test framework and commands
- CI/CD integration
- Coverage reporting tools
- Exclusions (generated code, migrations, etc.)

## Auto-Check Workflow

**When new code added:**
1. Identify affected modules
2. Run coverage for those modules
3. Compare against project standards
4. Flag untested critical paths
5. Suggest specific tests to add

**When tests written:**
1. Run coverage report
2. Check if new tests improve coverage
3. Verify critical paths covered
4. Identify remaining gaps
