# PINK MALL Avatar Skill v1.1 — Audit Source Index

Purpose: integrity/provenance index for the isolated Claude Code audit branch.

## GitHub context
- Repository: `VKK311/PIERCIINA-PROJECT`
- Repository visibility at preparation time: **PUBLIC**
- Audit branch: `claude/avatar-skill-analysis-v1-1`
- Base branch: `claude/pink-mall-development`
- Base commit at branch creation: `e5c962f2f5a70381ecadfa0ea8ad215ab583e105`

## Privacy rule
The original avatar JPEGs are NOT committed to GitHub because the repository is public.
They are transferred privately to Claude Code in 10 ZIP parts below 30 MB each and must remain untracked/local during the audit.

## Original source archive
- File: `Avatarskill.rar`
- Bytes: `200471798`
- SHA-256: `9b90375bddbd39b957faa71d03b1f2881e04e6956743fb0c7a16a9b862ef96cd`
- Expected extracted library: 190 JPEGs
  - INA: 77
  - SIS: 76
  - DUO: 37

## Skill package
- Package: `PINK_MALL_AVATAR_CLAUDE_SKILL_v1_1.zip`
- The package was locally validated before publication to the audit branch with `python VALIDATE_SKILL.py`.
- Local validator result at preparation time: PASS.

## Private transfer
See `AVATAR_LIBRARY_TRANSFER_MANIFEST.json` for:
- every transfer ZIP SHA-256
- expected counts and extraction instructions

Per-image SHA-256 values are in `AVATAR_LIBRARY_MANIFEST.json` inside the skill ZIP.

## Audit policy
This branch is for review only. No avatar photos, contact sheets, temporary extractions, or generated derivatives should be committed to this public repository.
