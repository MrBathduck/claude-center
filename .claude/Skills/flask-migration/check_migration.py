#!/usr/bin/env python3
"""Validates migration safety"""
import sys
import re

def check_migration(filepath):
    with open(filepath) as f:
        content = f.read()

    issues = []

    # Check for NOT NULL without default
    if re.search(r"sa\.Column.*nullable=False", content) and \
       not re.search(r"server_default=", content):
        issues.append("NOT NULL column without default detected")

    # Check downgrade exists
    if "def downgrade():" not in content or \
       "pass" in content.split("def downgrade():")[1].split("def ")[0]:
        issues.append("Missing downgrade logic")

    return issues

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: check_migration.py <migration_file>")
        sys.exit(1)

    issues = check_migration(sys.argv[1])
    if issues:
        print("MIGRATION ISSUES:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    print("Migration looks safe")
