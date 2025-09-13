#!/usr/bin/env bash
set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
FEATURE_DIR="$REPO_ROOT/specs/$CURRENT_BRANCH"
IMPL_PLAN="$FEATURE_DIR/plan.md"
FEATURE_SPEC="$FEATURE_DIR/spec.md"

mkdir -p "$FEATURE_DIR"
touch "$IMPL_PLAN"

cat << JSON
{
  "REPO_ROOT": "$REPO_ROOT",
  "BRANCH": "$CURRENT_BRANCH",
  "SPECS_DIR": "$FEATURE_DIR",
  "IMPL_PLAN": "$IMPL_PLAN",
  "FEATURE_SPEC": "$FEATURE_SPEC"
}
JSON
