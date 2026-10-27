#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
PACKAGE_DIR="$DIST_DIR/package"

rm -rf "$DIST_DIR"
mkdir -p "$PACKAGE_DIR"

pip install -r "$ROOT_DIR/requirements.txt" -t "$PACKAGE_DIR"
cp "$ROOT_DIR/src/banking_chatbot/fulfillment.py" "$PACKAGE_DIR/fulfillment.py"

(
  cd "$PACKAGE_DIR"
  zip -r ../lambda.zip .
)
