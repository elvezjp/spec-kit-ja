#!/usr/bin/env bash
set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
FEATURE_DIR="$REPO_ROOT/specs/$CURRENT_BRANCH"

cat << JSON
{
  "REPO_ROOT": "$REPO_ROOT",
  "BRANCH": "$CURRENT_BRANCH",
  "FEATURE_DIR": "$FEATURE_DIR",
  "PLAN": "$FEATURE_DIR/plan.md",
  "TASKS": "$FEATURE_DIR/tasks.md"
}
JSON
