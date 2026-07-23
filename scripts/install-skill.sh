#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-agents}"
SCOPE="${2:-global}"
python3 -m companion_vault.cli skill-install --target "$TARGET" --scope "$SCOPE"
