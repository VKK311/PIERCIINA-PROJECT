#!/usr/bin/env bash
# Commit the regenerated review artifact. Rebase, never force.
set -euo pipefail

git config user.name  "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

git add -A PINKMALL_REVIEW_STANDALONE.html
if git diff --cached --quiet; then
  echo "standalone review build unchanged"
  exit 0
fi

git commit -m "[review-bot] Rebuild standalone review artifact [skip ci]"

for i in 1 2 3; do
  if git pull --rebase origin claude/pink-mall-development \
     && git push origin HEAD:claude/pink-mall-development; then
    exit 0
  fi
  sleep $((i * 4))
done
echo "push failed after retries" >&2
exit 1
