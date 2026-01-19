#!/usr/bin/env python3
"""Subagent Quality Hook - Stub"""
import sys
import os

# Handle the case where Claude Code prepends $CLAUDE_PROJECT_DIR
# by accepting input from stdin and exiting gracefully
try:
    data = sys.stdin.read()
except:
    pass

sys.exit(0)
