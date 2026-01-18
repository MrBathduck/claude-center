# Smart Commit Command

Smart commit with pre-commit checks, changelog updates, and meaningful commit messages.

<commit_message_override>
$ARGUMENTS
</commit_message_override>

## RULE 0: Git Safety (CRITICAL)

**NEVER:**
- Force push (`--force`, `-f`)
- Amend commits without explicit user request
- Skip hooks (`--no-verify`)
- Commit `.env` files or secrets

**ALWAYS:**
- Run tests before committing
- Run linting before committing
- Ask user to confirm commit message
- Follow commit message format from CLAUDE.md

---

## EXECUTION PROTOCOL

### STEP 1: Check Git Status

Run `git status` to understand:
- What files are modified
- What files are staged
- What files are untracked
- Current branch name

If no changes to commit, inform the user and stop.

### STEP 2: Pre-Commit Checks (MANDATORY)

All checks must pass before committing. Run these in parallel when possible:

#### 2.1 Run Tests
```bash
pytest tests/ -v --tb=short
```
- If tests fail: STOP and report which tests failed
- Do not proceed until tests pass

#### 2.2 Run Linting
```bash
ruff check app/ tests/
```
- If linting fails: STOP and report issues
- Suggest fixes if possible

#### 2.3 Build SCSS (if .scss files changed)
Check if any `.scss` files are in the changed files list:
```bash
npm run build:css
```
- If build fails: STOP and report the error

#### 2.4 Security Checks
Scan staged files for:

**Blocked Files:**
- `.env` files (except `.env.example`)
- `credentials.json`, `secrets.json`
- Files containing API keys or tokens

**Debug Code (warn, don't block):**
- `console.log` in JS files (excluding `// eslint-disable` lines)
- `print(` statements in Python (excluding logging, tests)
- `debugger` statements in JS
- `breakpoint()` in Python
- `TODO:` or `FIXME:` comments (info only)

If blocked files found: STOP and warn user.
If debug code found: List it and ask user if they want to proceed.

### STEP 3: Analyze Changes

Read the diff to understand:
- What was added/removed/modified
- Which features/areas are affected
- Breaking changes or migrations

```bash
git diff --cached --stat
git diff --cached
```

If nothing is staged, ask user if they want to stage all changes:
```bash
git add -A
```

### STEP 4: Generate Commit Message

Based on the changes, generate a commit message following this format:

```
<type>: <short description (50 chars max)>

<body - what changed and why (wrap at 72 chars)>

[Generated with Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types:**
- `feat`: New feature or functionality
- `fix`: Bug fix
- `refactor`: Code restructuring without behavior change
- `docs`: Documentation changes only
- `test`: Adding or updating tests
- `style`: Formatting, SCSS, CSS changes (no logic change)
- `chore`: Maintenance tasks, dependencies, config

**Guidelines:**
- Short description: Imperative mood ("Add feature" not "Added feature")
- Body: Explain WHAT changed and WHY, not HOW
- Reference issue numbers if applicable
- Mention breaking changes prominently

**If $ARGUMENTS provided:**
Use the provided message as the short description, but still generate the body.

### STEP 5: Check for Changelog Update

Determine if changes are significant enough for CHANGELOG.md:

**Significant (update changelog):**
- New features (`feat`)
- Bug fixes that affect users (`fix`)
- Breaking changes
- API changes
- Database migrations

**Not significant (skip changelog):**
- Internal refactoring
- Test updates
- Documentation fixes
- Code style changes
- Dependency updates (minor)

If significant, add entry to CHANGELOG.md under "Unreleased" section:
```markdown
## [Unreleased]

### Added
- New feature description

### Changed
- Changed behavior description

### Fixed
- Bug fix description
```

### STEP 6: User Confirmation (MANDATORY)

Present to the user:
1. Summary of changes (files modified)
2. Pre-commit check results (all passed)
3. Proposed commit message
4. Changelog update (if applicable)

Ask: **"Do you want to proceed with this commit? (yes/no/edit)"**

- `yes`: Proceed with commit
- `no`: Abort
- `edit`: Let user modify the message

**NEVER commit without user confirmation.**

### STEP 7: Execute Commit

Once confirmed:

```bash
git commit -m "$(cat <<'EOF'
<type>: <short description>

<body>

[Generated with Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

After commit, show:
- Commit hash
- Branch name
- Reminder: "Run `git push` when ready to push to remote"

---

## ERROR HANDLING

### Tests Fail
```
Pre-commit check failed: Tests

Failed tests:
- test_user_registration: AssertionError at line 45
- test_event_creation: ValidationError

Fix the failing tests before committing.
```

### Linting Fails
```
Pre-commit check failed: Linting

Issues found:
- app/routes/events.py:45: F401 'os' imported but unused
- app/services/user.py:12: E501 line too long (95 > 88 characters)

Run `ruff check --fix app/` to auto-fix some issues.
```

### Sensitive Files Detected
```
BLOCKED: Sensitive files staged

The following files should not be committed:
- .env (contains secrets)
- config/credentials.json (contains API keys)

Run `git reset HEAD <file>` to unstage these files.
```

### Debug Code Found
```
WARNING: Debug code detected

The following files contain debug statements:
- app/routes/events.py:23: console.log("debug")
- app/services/user.py:45: print(user_data)

Do you want to proceed anyway? (yes/no)
```

---

## EXAMPLES

### Example 1: Simple Feature Commit
```
User: /commit

Claude:
Checking git status...
- 3 files modified
- Branch: feature/user-preferences

Running pre-commit checks...
[OK] Tests passed (42 tests)
[OK] Linting passed
[OK] No sensitive files staged
[OK] No debug code found

Changes summary:
- app/models/user.py: Added preferences field
- app/routes/api/users.py: Added preferences endpoint
- tests/test_users.py: Added preference tests

Proposed commit message:
---
feat: Add user preferences storage and API endpoint

Add preferences JSONB field to User model for storing user-specific
settings. New API endpoint GET/PUT /api/users/{id}/preferences
allows reading and updating preferences.

[Generated with Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
---

Changelog update: Added entry under "Added" section

Do you want to proceed with this commit? (yes/no/edit)
```

### Example 2: With Message Override
```
User: /commit Fix pagination bug on events list

Claude:
...pre-commit checks...

Proposed commit message:
---
fix: Fix pagination bug on events list

Corrected off-by-one error in pagination calculation that caused
the last page to be empty when total items were exactly divisible
by page size.

[Generated with Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
---

Do you want to proceed with this commit? (yes/no/edit)
```

### Example 3: SCSS Changes
```
User: /commit

Claude:
Checking git status...
- 2 files modified: _events.scss, _dashboard.scss

Running pre-commit checks...
[OK] Tests passed
[OK] Linting passed
Building SCSS...
[OK] SCSS build successful
[OK] No sensitive files staged

Proposed commit message:
---
style: Update event card and dashboard spacing

Adjust padding and margins for better visual hierarchy on event
cards. Update dashboard grid layout for improved alignment.

[Generated with Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
---

Changelog update: Skipped (style-only changes)

Do you want to proceed with this commit? (yes/no/edit)
```

---

## FORBIDDEN ACTIONS

- Committing without running tests
- Committing with linting errors
- Committing `.env` or secret files
- Committing without user confirmation
- Using `git commit --amend` without explicit request
- Using `git push --force`
- Skipping SCSS build when SCSS files changed

## REQUIRED ACTIONS

- Run all pre-commit checks
- Generate meaningful commit message
- Update CHANGELOG.md for significant changes
- Show user the proposed commit before executing
- Wait for explicit user confirmation
