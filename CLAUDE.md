# PIERCIINA / PINK MALL — start here

Read this file before doing anything else in this repository.

## Every fresh session starts the same way

1. `git fetch origin`
2. `git checkout claude/pink-mall-development && git pull origin claude/pink-mall-development`
3. Read this file.
4. Read `.claude/skills/pink-mall-product-onboarding/SKILL.md` — the authoritative
   product-onboarding behavior contract.
5. Read `docs/pink-mall/PROJECT_STATE.md` — the real current state.

## GitHub is the project state. Model memory is not.

The execution container is ephemeral and has destroyed uncommitted work
repeatedly. Only what is committed exists.

Two rules follow, and neither has an exception:

- **Never reconstruct a newer build from memory.** If the state recorded in
  `PROJECT_STATE.md` cannot be found on disk, stop and say so. Do not rebuild
  it, do not approximate it, do not assume a summary is equivalent to the file.
- **Verify by hash, not by filename.** `PROJECT_STATE.md` records the canonical
  SHA-256. Check it before treating a file as the canonical build.

## Two builds, and they verify different things

| File | What it is | Verified by |
|---|---|---|
| `PINKMALL.html` + `assets/` | the canonical website | fresh clone, full regression |
| `PINKMALL_REVIEW_STANDALONE.html` | generated review artifact, images inlined | copied alone into an empty directory |

**Production verification is not portable review verification.** The canonical
HTML references product media at `assets/pink-mall/products/<PM-ID>/`, so a
reviewer who downloads that one file gets dangling paths and no photography.
Both builds must pass before a publication counts as reviewed.

Regenerate the artifact with `python tools/build_standalone_review.py`. It is
never the canonical website, and it is never a reason to change the production
media architecture.

## The canonical website is `PINKMALL.html`

One file. There is no second "latest" HTML in this repository, by design —
having two is what caused the Phase 2A / calibration-build ambiguity that this
structure resolved.

Historical builds are recoverable through git history, not through parallel
files in the working tree.

## Product media: acquisition and presentation are separate

Acquisition delivers the strongest official image at its **native aspect
ratio**. The storefront decides how to fit it, via `media.fit` — `contain` by
default for real supplier photography, with optional `media.surface` (the
backdrop colour, auto-detected during acquisition) and a bounded `media.scale`.

Never prepare a per-SKU canvas to satisfy card or PDP CSS. Onboarding a normal
studio product photograph must not require manual aspect-ratio work.

## Branches

| Branch | Role |
|---|---|
| `claude/pink-mall-development` | working source of truth — commit validated checkpoints here |
| `main` | release only; never modified without an explicit release instruction |
| `claude/pink-mall-hero-carousel-jvhdb8` | historical, superseded; preserved, not merged |

## Checkpoint rule

- experiment or failed task → do not commit canonical state
- `BLOCKED` task → do not replace canonical `PINKMALL.html`
- validated `PASS` checkpoint → commit and push to development
- product approval package → may be persisted without publishing
- published product → commit product and assets only after explicit `APPROVE`
- `main` → never modified without explicit release approval
- pull request / merge / release → only when explicitly requested

See `docs/pink-mall/CHECKPOINT_POLICY.md` for the full policy.

## Standing product constraints

These come from the user and hold across every task:

- Vanilla HTML/CSS/JS in one self-contained file. No frameworks, no build step,
  no external libraries.
- EUR only.
- Do not build a cart, checkout, account, login, payment flow, backend, CMS,
  admin, or inventory API.
- Never invent a phone number, customer, Instagram handle, testimonial, review,
  or purchase count. No stock photography as product media.
- The Viber destination in `CONFIG.viberUrl` is fixed and must not be changed.
  It is a business URL and takes no `?text=` prefill.
- Never publish a product without explicit user approval.

## Repository layout

```text
PINKMALL.html                          canonical website
CLAUDE.md                              this file
README.md
.claude/skills/pink-mall-product-onboarding/
assets/                                live site assets
docs/pink-mall/
    PROJECT_STATE.md                   current real state
    CHECKPOINT_POLICY.md
    checkpoints/                       historical reports and previews
    approval-media/PM-025/             approved but unpublished media
```

`.pink-mall-staging/` is ephemeral scratch and is gitignored. Approved media
that is not yet published lives under `docs/pink-mall/approval-media/`; it moves
to `assets/pink-mall/products/<PM-ID>/` only at publication.
