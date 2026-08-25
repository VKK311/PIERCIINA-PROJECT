# Installation

This package is the PINK MALL product-onboarding behavior contract.
Install it as a project-level skill.

## Location

Place the package contents at:

```text
.claude/skills/pink-mall-product-onboarding/
    SKILL.md
    INSTALL.md
    examples/
    references/
```

The folder name must be `pink-mall-product-onboarding`, matching the `name`
field in `SKILL.md`. A mismatch stops the skill from being discovered.

## Verify after installing

1. `.claude/skills/pink-mall-product-onboarding/SKILL.md` exists.
2. Its frontmatter `name` reads `pink-mall-product-onboarding`.
3. All nine files under `references/` and the file under `examples/` are present.
4. The skill is listed as available in a new session.

## Persistence

Commit the installed skill to the project's development branch. A session
container is ephemeral; only committed files survive it.

## Scope

Installing the skill does not publish, stage, or modify any product. It only
makes the contract available. Product work still requires its own task and,
before publication, explicit user approval.
