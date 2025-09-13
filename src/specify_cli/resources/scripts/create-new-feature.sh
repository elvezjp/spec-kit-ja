#!/usr/bin/env bash
set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
DESC="$1"
if [ -z "$DESC" ]; then
  echo "Usage: $0 --json \"feature description\"" >&2
  exit 1
fi

ID=$(date +%y%m%d)-feature
BRANCH="$ID"
FEATURE_DIR="$REPO_ROOT/specs/$BRANCH"
SPEC_FILE="$FEATURE_DIR/spec.md"

mkdir -p "$FEATURE_DIR"
git checkout -b "$BRANCH"
printf "# Feature Specification: %s\n\n" "$DESC" > "$SPEC_FILE"

cat << JSON
{
  "BRANCH_NAME": "$BRANCH",
  "SPEC_FILE": "$SPEC_FILE"
}
JSON
