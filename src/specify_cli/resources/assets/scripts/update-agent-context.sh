#!/usr/bin/env bash
# Minimal stub to mirror repository script; real repo script is more capable.
set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
FEATURE_DIR="$REPO_ROOT/specs/$CURRENT_BRANCH"
PLAN="$FEATURE_DIR/plan.md"

TARGET="$REPO_ROOT/CLAUDE.md"
AGENT_NAME="Claude Code"

if [ ! -f "$PLAN" ]; then
  echo "ERROR: No plan.md at $PLAN" >&2
  exit 1
fi

if [ ! -f "$TARGET" ]; then
  cp "$REPO_ROOT/templates/agent-file-template.md" "$TARGET"
fi

echo "Updated $AGENT_NAME context at $TARGET"
