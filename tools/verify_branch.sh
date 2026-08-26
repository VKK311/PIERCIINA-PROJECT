#!/usr/bin/env bash
# Refuse to commit or push from the wrong place. The managed checkout has
# reverted to the historical branch mid-task more than once; this turns that
# from a silent wrong-branch commit into a loud failure.
set -euo pipefail

WANT="claude/pink-mall-development"
HAVE="$(git branch --show-current)"

[ "$HAVE" = "$WANT" ] || {
    echo "REFUSING: on '$HAVE', expected '$WANT'." >&2
    echo "Discard this worktree and recreate the isolated clone (see CLAUDE.md)." >&2
    exit 1
}
git fetch -q origin "$WANT"
git merge-base --is-ancestor "origin/$WANT" HEAD || {
    echo "REFUSING: HEAD does not descend from origin/$WANT." >&2
    exit 1
}
echo "branch OK: $HAVE @ $(git rev-parse --short HEAD), descends from origin/$WANT"
