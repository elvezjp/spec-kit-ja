#!/usr/bin/env bash
set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
FEATURE_DIR="$REPO_ROOT/specs/$CURRENT_BRANCH"

AVAILABLE_DOCS=()
[ -f "$FEATURE_DIR/plan.md" ] && AVAILABLE_DOCS+=("plan.md")
[ -f "$FEATURE_DIR/research.md" ] && AVAILABLE_DOCS+=("research.md")
[ -f "$FEATURE_DIR/data-model.md" ] && AVAILABLE_DOCS+=("data-model.md")
[ -d "$FEATURE_DIR/contracts" ] && AVAILABLE_DOCS+=("contracts/")
[ -f "$FEATURE_DIR/quickstart.md" ] && AVAILABLE_DOCS+=("quickstart.md")

cat << JSON
{
  "FEATURE_DIR": "$FEATURE_DIR",
  "AVAILABLE_DOCS": [$(printf '"%s",' "${AVAILABLE_DOCS[@]}" | sed 's/,$//')]
}
JSON
