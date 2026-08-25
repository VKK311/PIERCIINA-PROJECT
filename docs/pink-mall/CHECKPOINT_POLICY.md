# PINK MALL — Checkpoint Policy

Adopted 2026-08-25, after the fifteenth loss of validated deliverables to
container recycling.

## Why this exists

The remote execution container is ephemeral. Its disk is reclaimed after a
period of inactivity, and everything not committed to git is destroyed with it.

Across this project that happened roughly fifteen times. Each loss cost a full
rebuild of an already-validated artefact. `PINKMALL.html` survived every single
one — for exactly one reason: it was committed. Nothing else was.

The standing "do not commit" instruction was what made the losses permanent.
It is now replaced by this policy.

## The rule

**Every validated artefact is committed to `claude/pink-mall-development`
as soon as it passes its own acceptance gate.**

`claude/pink-mall-hero-carousel-jvhdb8` was the original checkpoint branch and
is now historical: preserved, superseded, not merged.

Committing is persistence, not publication. The branch is a working branch.
Nothing reaches anyone until it is merged, and merging is not authorised.

Explicitly **not** authorised, and not to be done without a fresh, explicit
instruction each time:

- merging into `main`
- opening a pull request
- force-pushing (`--force`, `--force-with-lease`)
- creating a release or tag

## What counts as a checkpoint

An artefact is checkpoint-eligible once it has passed the gate defined by its
own task brief — a source-hash match, a regression suite, an approval preview.
Work in progress is not checkpointed. A failed gate is not checkpointed.

Every checkpoint commit records, in its message, the SHA-256 of each binary or
large artefact it introduces, so any future session can verify recovery.

## Recovery procedure after a recycle

1. `git log --oneline` on the branch — the last checkpoint is the last good state.
2. Verify the restored file against the SHA-256 in its commit message.
3. Resume from there. Do not reconstruct a baseline from memory.

## Hash ledger

| Build | Bytes | SHA-256 |
|---|---|---|
| Phase 2A (`38bfb7f`) | 2 418 264 | `cdfbf57d7b420690b2043c652eaf7e5c2e4e81daf21a3bc4b11478182db5b458` |
| Pre-release, autoplay fixed (baseline) | 2 528 747 | `37b74632a5fa405f2bee3a857f99424a8bb6a1fd4fb0289e6180178395a4a9a7` |
| Real product calibration | 2 537 910 | `dc7050ba22862b4f4f1a07cae0365e6f648dde9d726475223279fd839962a2f0` |

Approved JQ4556 media, restored byte-exact and hash-verified:

| Image | Bytes | SHA-256 |
|---|---|---|
| 01 (PROPOSED MAIN) | 9 164 | `3940078ed620b96e0582ff94089281500d387294f9c5ac6ff4d30f716fbfce5c` |
| 02 | 9 790 | `a4b11cc7d607559815ad46216eab9b432fc7b22c741255645606426b03ad5976` |
| 03 | 10 290 | `7109e8007d878498c7935f33b19464d3e20fded2d70d618719e03cd113dae6a1` |
| 04 | 10 242 | `36c7c06e99cebbe8b58ef675b14417fa8b04edd4c25b75b21a656b029a11e13e` |

## Current checkpoint state

| | |
|---|---|
| Canonical website | `PINKMALL.html` — one file, no competing "latest" |
| Public catalog | PM-001 … PM-024 |
| PM-025 | staged, **not published** |
| JQ4556 in `PINK_MALL_PRODUCTS` | no |
| Next Mall ID | PM-025 |

## Known open items

Carried forward; see `PROJECT_STATE.md` for live status.

1. Staged PM-025 images are 500×500 `w_500` web derivatives — soft at large PDP
   zoom. Higher-resolution exact duplicates preferred before launch. Do not
   AI-upscale.

Resolved since this policy was written: the per-image alt gap (the engine now
renders authored `media.imageAlt` / `media.galleryAlt[]`), and the calibration
fixture (removed from the canonical build).
