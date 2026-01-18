# Jest Coverage Guide

This project is Flask-focused. JavaScript testing is minimal.

## Basic Commands

### Run with coverage
```bash
jest --coverage
```

### Check thresholds
```bash
jest --coverage --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80}}'
```

## When to Use

JavaScript testing applies to:
- Frontend utility functions
- Chart rendering logic
- Form validation (client-side)
- API client functions

## Framework Detection

| Framework | Coverage Tool |
|-----------|---------------|
| Jest | Built-in |
| Mocha | nyc/istanbul |
| Vitest | Built-in (c8) |

## Note

For this project, focus on pytest for backend coverage. JavaScript files are primarily UI and use manual testing via browser.
