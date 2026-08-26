#!/usr/bin/env bash
# Run the request manifests this run is actually for.
#
# ONLY_SKUS is a comma-separated allow-list chosen by the workflow's Select
# step: the SKUs whose manifests changed in this push, or one SKU from a manual
# dispatch. Empty ONLY_SKUS with SELECT_MODE=regression-all means every
# manifest, on purpose. Empty ONLY_SKUS with SELECT_MODE=none means a code-only
# change, and the correct behaviour there is to run nothing — onboarding one
# product must not silently re-acquire the entire historical catalogue.
#
# Never aborts the whole run on one SKU: a PARTIAL or BLOCKED result is still
# worth committing, because result.json carries the log that explains why.
set -uo pipefail
shopt -s nullglob

MODE="${SELECT_MODE:-regression-all}"
LIST="${ONLY_SKUS:-${ONLY_SKU:-}}"

if [ -z "$LIST" ] && [ "$MODE" = "none" ]; then
  echo "code-only change: no request manifest changed, so no SKU is re-acquired."
  echo "For a deliberate regression sweep, dispatch this workflow with run_all=true."
  echo "rc=0" >> "${GITHUB_OUTPUT:-/dev/null}"
  exit 0
fi

wanted() {
  [ -z "$LIST" ] && return 0          # regression-all
  case ",${LIST}," in (*",$1,"*) return 0 ;; esac
  return 1
}

echo "selection mode: ${MODE}; skus: ${LIST:-<all>}"

rc=0
any=0
for req in docs/pink-mall/media-requests/*.request.json; do
  sku="$(basename "$req" .request.json)"
  if ! wanted "$sku"; then
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
