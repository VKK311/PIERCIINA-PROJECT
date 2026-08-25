#!/usr/bin/env bash
# Commit acquired media back to the development branch. Rebase, never force:
# a concurrent human push must never be discarded.
set -euo pipefail

git config user.name  "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

git add -A docs/pink-mall/media-acquisition
if git diff --cached --quiet; then
  echo "no media changes to commit"
  exit 0
fi

git commit -m "[media-bot] Acquire Pink Mall product media [skip ci]"

for i in 1 2 3; do
  if git pull --rebase origin claude/pink-mall-development \
     && git push origin HEAD:claude/pink-mall-development; then
    exit 0
  fi
  sleep $((i * 4))
done

echo "push failed after retries" >&2
exit 1
