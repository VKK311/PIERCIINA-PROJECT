# Avatar Image Library Privacy & Storage Policy v1.2

**This is a privacy policy. It was a size policy in v1.1, and that was the wrong frame.**

The 190 source photographs (77 INA, 76 SIS, 37 DUO) are private images of two
identifiable real people. The library includes body-reference and
underwear-series frames. The question is not whether the bytes fit in a
repository. The question is who can see them.

## The controlling fact

**`VKK311/PIERCIINA-PROJECT` is a public repository.**

Anything committed there is world-readable, permanently, including after
deletion — git history retains it and forks and mirrors survive a later purge.

## Prohibited, without exception

- Committing any INA / SIS / DUO source photograph to the public repository.
- Committing any derivative: crop, contact sheet, thumbnail, preview, montage,
  or generated image built from them.
- Attaching them to a pull request, issue, comment, or CI artifact.
- **Git LFS in the public repository.** LFS changes where bytes are stored, not
  who may read them. An LFS object in a public repo is public. This was listed
  as an acceptable option in v1.1 and is now withdrawn.

## Acceptable storage

1. **Owner-controlled private storage** — private object storage or an
   encrypted archive the owner holds. *Recommended.* The public repo keeps only
   manifests and SHA-256 hashes, which is what it does today.
2. **A dedicated private repository** — acceptable when git-native versioning is
   wanted. Git LFS is acceptable *inside that private repository only*.

## What the public repository may contain

- Skill files: JSON, Markdown, Python.
- `AVATAR_LIBRARY_MANIFEST.json` — paths, dimensions, hashes, classifications.
  It contains no pixels.
- Integrity hashes.

Manifest paths are relative (`INA/IMG_3854.JPEG`) and resolve against whatever
private root the operator mounts. That indirection is deliberate: it is what
lets the skill be public while the library stays private.

## Transfer

Move parts directly into the working session and extract to a temporary
untracked directory outside any tracked path. Verify every file SHA-256 against
`AVATAR_LIBRARY_MANIFEST.json` before treating the library as connected.

Delete the temporary directory when the session ends. Never claim the library
is "connected to GitHub" — it is not, and it must not be.

## Generated outputs

Generated campaign images are derivative likenesses of real people. They
inherit these constraints. Decide their storage and disclosure policy in
`CONSENT_AND_PROVENANCE.json` before publishing any of them.

## Consent

Storage safety is not authorisation. See `CONSENT_AND_PROVENANCE.json`.
Every human-authorisation field there is currently unset.
