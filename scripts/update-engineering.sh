#!/usr/bin/env bash
# Pull the latest engineering plugin from anthropics/knowledge-work-plugins,
# re-apply the Plane customization, and replace plugins/engineering with the result.
# Review `git diff` afterwards, then commit and push: claude.ai picks it up on the next sync.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UPSTREAM_URL="https://github.com/anthropics/knowledge-work-plugins.git"
UPSTREAM_PATH="engineering"
REF="${1:-main}"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --quiet --depth 1 --branch "$REF" --filter=blob:none --sparse "$UPSTREAM_URL" "$TMP/upstream"
git -C "$TMP/upstream" sparse-checkout set "$UPSTREAM_PATH"
SHA="$(git -C "$TMP/upstream" rev-parse HEAD)"
SRC="$TMP/upstream/$UPSTREAM_PATH"
VERSION="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("version",""))' "$SRC/.claude-plugin/plugin.json")"

python3 "$ROOT/scripts/customize_engineering.py" "$SRC" >/dev/null

rm -rf "$ROOT/plugins/engineering"
cp -R "$SRC" "$ROOT/plugins/engineering"

python3 - "$ROOT/upstream.json" "$SHA" "$VERSION" <<'EOF'
import json, sys
path, sha, version = sys.argv[1:]
data = json.load(open(path))
data["engineering"].update({"commit": sha, "version": version})
json.dump(data, open(path, "w"), indent=2)
open(path, "a").write("\n")
EOF

echo "engineering: upstream $VERSION @ ${SHA:0:12}"
git -C "$ROOT" diff --stat -- plugins/engineering upstream.json || true
