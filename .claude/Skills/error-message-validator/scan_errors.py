#!/usr/bin/env python3
"""Scans code for generic/poor error messages"""
import sys
import re
from pathlib import Path

# Patterns indicating poor error messages
BAD_PATTERNS = [
    (r'"Error"', 'Generic "Error" - be specific about what failed'),
    (r'"Invalid"', 'Generic "Invalid" - specify which field/value'),
    (r'"Failed"', 'Generic "Failed" - explain what failed and why'),
    (r'"Bad request"', 'Generic "Bad request" - explain what\'s wrong'),
    (r'"Something went wrong"', 'Too vague - be specific'),
    (r'"Please try again"', 'No context - explain what to try differently'),
    (r'"Error \d+"', 'HTTP code only - add human-readable message'),
    (r'"\d{3}"', 'Status code only - add context'),
]

# Patterns indicating good error messages (for comparison)
GOOD_PATTERNS = [
    r'already (?:exists|registered)',
    r'must be',
    r'(?:Max|Maximum|Minimum|Min) \d+',
    r'expected.*got',
    r'cannot.*because',
    r'required',
    r'invalid format',
]

def scan_file(filepath):
    """Scan a file for error messages"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return []

    issues = []
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # Skip comments
        if line.strip().startswith('#') or line.strip().startswith('//'):
            continue

        # Check for bad patterns
        for pattern, message in BAD_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append({
                    'file': filepath,
                    'line': i,
                    'content': line.strip(),
                    'issue': message
                })

    return issues

def scan_directory(directory, extensions=None):
    """Scan directory for error messages"""
    if extensions is None:
        extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs'}

    directory = Path(directory)
    issues = []

    for filepath in directory.rglob('*'):
        if filepath.suffix in extensions and filepath.is_file():
            # Skip test files and migrations
            if 'test' in str(filepath) or 'migration' in str(filepath):
                continue
            issues.extend(scan_file(filepath))

    return issues

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else '.'

    print(f"Scanning for generic error messages in: {target}")

    target_path = Path(target)
    if target_path.is_file():
        issues = scan_file(target)
    else:
        issues = scan_directory(target)

    if issues:
        print(f"\n[!] Found {len(issues)} potential issues:\n")
        for issue in issues:
            print(f"  {issue['file']}:{issue['line']}")
            print(f"    {issue['content']}")
            print(f"    → {issue['issue']}\n")
        sys.exit(1)
    else:
        print("[OK] No generic error messages detected")
        sys.exit(0)

if __name__ == "__main__":
    main()
