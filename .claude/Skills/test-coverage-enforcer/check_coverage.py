#!/usr/bin/env python3
"""Runs pytest coverage and validates against thresholds"""
import sys
import subprocess
import re
from pathlib import Path

# Default thresholds (override via command args or project config)
DEFAULT_THRESHOLDS = {
    'models': 90,
    'routes': 80,
    'utils': 100,
    'overall': 80
}

def run_coverage(module=None):
    """Run pytest with coverage"""
    cmd = ['pytest', '--cov=app', '--cov-report=term-missing']
    if module:
        cmd.extend(['--cov', f'app.{module}', f'tests/test_{module}/'])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout + result.stderr
    except FileNotFoundError:
        return "Error: pytest not found. Install with: pip install pytest pytest-cov"

def parse_coverage(output):
    """Extract coverage percentage from pytest output"""
    # Look for lines like: app/models/__init__.py    85%
    coverage = {}
    for line in output.split('\n'):
        match = re.search(r'app/(\w+)/.*?(\d+)%', line)
        if match:
            module, percent = match.groups()
            coverage[module] = int(percent)

    # Extract total coverage
    total_match = re.search(r'TOTAL.*?(\d+)%', output)
    if total_match:
        coverage['overall'] = int(total_match.group(1))

    return coverage

def check_thresholds(coverage, thresholds):
    """Check if coverage meets thresholds"""
    failures = []
    for module, threshold in thresholds.items():
        actual = coverage.get(module, 0)
        if actual < threshold:
            failures.append(f"{module}: {actual}% < {threshold}% (target)")
    return failures

def main():
    module = sys.argv[1] if len(sys.argv) > 1 else None

    print(f"Running coverage check{f' for {module}' if module else ''}...")
    output = run_coverage(module)
    print(output)

    coverage = parse_coverage(output)
    failures = check_thresholds(coverage, DEFAULT_THRESHOLDS)

    if failures:
        print("\n[!] Coverage below thresholds:")
        for failure in failures:
            print(f"  - {failure}")
        sys.exit(1)
    else:
        print("\n[OK] Coverage meets all thresholds")
        sys.exit(0)

if __name__ == "__main__":
    main()
