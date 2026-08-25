# PINK MALL — project state

Updated: structure cleanup + pre-publish hardening.
Status: **STRUCTURE CLEAN / HARDENING PASS.**

This file records the real state. Trust it over any summary, and verify the
canonical build by hash before treating it as canonical.

## Canonical

| | |
|---|---|
| CANONICAL BRANCH | `claude/pink-mall-development` |
| CANONICAL WEBSITE | `PINKMALL.html` |
| CANONICAL WEBSITE SHA-256 | `fa639d3c87f80cfff062114b2b2602fed282754f642e2a07eb7e5a7b38aa12c9` |
| CANONICAL WEBSITE BYTES | 2537658 |

## Engine

| | |
|---|---|
| REAL PRODUCT ENGINE | PASS |
| PER-IMAGE ALT | PASS — canonical `media.imageAlt` / `media.galleryAlt[]` |
| CALIBRATION FIXTURE | REMOVED |

## Catalog

| | |
|---|---|
| PUBLIC CATALOG | PM-001 … PM-024 |
| NEXT ID | PM-025 |
| JQ4556 | staged, awaiting final human approval — NOT PUBLISHED |

## Media acquisition automation

| | |
|---|---|
| AUTOMATION | committed — `tools/media_acquisition/`, `.github/workflows/media-acquisition.yml` |
| SELF-TEST | PASS — `python tools/media_acquisition/selftest.py`, 12/12 guards |
| JQ4556 PILOT | **BLOCKED** — no workflow run is created for this repository |

The pilot has **not** passed. `GET /actions/runs` reports `total_count: 0`
after a push that matches the workflow's trigger paths, and a
`workflow_dispatch` returns 404. GitHub Actions appears to be disabled for
this repository; the Actions admin API is blocked by the session's egress
proxy, so it cannot be checked or enabled from here.

**To unblock:** repository owner enables Actions at
`https://github.com/VKK311/PIERCIINA-PROJECT/settings/actions`
("Allow all actions and reusable workflows"), then pushes any change under
`docs/pink-mall/media-requests/` — or re-runs the request commit — to trigger
acquisition. Until then, media for a new product still has to be supplied by
hand.

## Known non-blocking issue

Staged PM-025 product media is 500×500 web-derivative resolution. Acceptable
for approval and card preview; higher-resolution exact official duplicates are
preferred before launch and full PDP display. Do not AI-upscale.

## Next step

Explicit PM-025 approval, then a publication task.
