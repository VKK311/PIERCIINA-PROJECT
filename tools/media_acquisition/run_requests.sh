#!/usr/bin/env bash
# Run every request manifest (or just $ONLY_SKU). Never aborts the whole run
# on one SKU: a PARTIAL or BLOCKED result is still worth committing, because
# result.json carries the log that explains why.
set -uo pipefail
shopt -s nullglob

rc=0
any=0
for req in docs/pink-mall/media-requests/*.request.json; do
  sku="$(basename "$req" .request.json)"
  if [ -n "${ONLY_SKU:-}" ] && [ "$ONLY_SKU" != "$sku" ]; then
    echo "skip $sku"
    continue
  fi
  any=1
  echo "::group::acquire $sku"
  python tools/media_acquisition/acquire.py \
    --request "$req" \
    --out docs/pink-mall/media-acquisition || rc=$?
  echo "::endgroup::"
done

[ "$any" = "0" ] && echo "no matching request manifests"
echo "rc=$rc" >> "${GITHUB_OUTPUT:-/dev/null}"
exit 0
