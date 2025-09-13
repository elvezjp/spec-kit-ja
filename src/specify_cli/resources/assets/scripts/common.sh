#!/usr/bin/env bash
set -e

root() {
  git rev-parse --show-toplevel
}

abs() {
  python3 - "$1" << 'PY'
import sys, pathlib
print(pathlib.Path(sys.argv[1]).resolve())
PY
}
