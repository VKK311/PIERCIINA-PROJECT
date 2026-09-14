# Avatar Skill v1.1 — audit input (historical)

This directory holds the **v1.1 package as audited**. It is historical input,
not the canonical skill.

**Canonical source is `docs/pink-mall/avatar-skill/v1.2/`** — loose JSON,
Markdown and Python, reviewable in a Git diff.

## Archive integrity

`PINK_MALL_AVATAR_CLAUDE_SKILL_v1_1.zip` was committed at 7,529 bytes: a
truncated fragment that failed its own `.sha256` and could not be opened
("End-of-central-directory signature not found"). It has been replaced with the
authoritative 47,311-byte package, which verifies exactly:

```
sha256sum -c PINK_MALL_AVATAR_CLAUDE_SKILL_v1_1.zip.sha256
```

`461490e032798eef5e7049277c28bfcdd82430d53291347143dbd29192987874`

The archive holds metadata only — 22 JSON, Markdown and Python files. No
photographs. It is retained for provenance; do not treat it as the source of
truth for v1.2.

## Contents

- `PINK_MALL_AVATAR_CLAUDE_SKILL_v1_1.zip` — verified v1.1 package
- `PINK_MALL_AVATAR_CLAUDE_SKILL_v1_1.zip.sha256` — its hash
- `AVATAR_LIBRARY_TRANSFER_MANIFEST.json` — 10-part private transfer definition
- `SOURCE_INDEX.md`
- `CLAUDE_READ_ONLY_AUDIT_TASK.md` — the audit brief
