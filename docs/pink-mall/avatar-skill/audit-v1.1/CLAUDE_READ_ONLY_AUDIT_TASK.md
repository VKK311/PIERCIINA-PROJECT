# PINK MALL AVATAR SKILL v1.1 — READ-ONLY AUDIT TASK FOR CLAUDE CODE

## Mission
Perform a rigorous, read-only audit of the PINK MALL Avatar Skill v1.1 and the full 190-image private avatar reference library. The purpose of this pass is to test whether the system is ready for controlled campaign/banner generation experiments and to identify exactly what must change before any production integration.

This is an AUDIT, not an implementation task.

## Repository and branch
Repository: `VKK311/PIERCIINA-PROJECT`
Audit branch: `claude/avatar-skill-analysis-v1-1`
Base branch: `claude/pink-mall-development`
Expected base commit at branch creation: `e5c962f2f5a70381ecadfa0ea8ad215ab583e105`

The repository is public. The 190 original JPEG reference images are private and MUST NOT be committed, pushed, added to Git LFS, attached to a PR, or copied into any tracked repo path during this audit.

## Files already in the audit branch
Under `docs/pink-mall/avatar-skill/audit-v1.1/` you should find:
- `PINK_MALL_AVATAR_CLAUDE_SKILL_v1_1.zip`
- `PINK_MALL_AVATAR_CLAUDE_SKILL_v1_1.zip.sha256`
- `AVATAR_LIBRARY_TRANSFER_MANIFEST.json`
- `SOURCE_INDEX.md`
- this task file

The skill ZIP contains the full v1.1 skill package. It also contains an older `GITHUB_INTEGRATION_TASK.md`. DO NOT execute that older task. Treat it only as historical input if useful.

## Private image transfer
The user will attach 10 ZIP parts to the Claude Code session:
- `AVATAR_LIBRARY_PART_01_INA_01.zip`
- `AVATAR_LIBRARY_PART_02_INA_02.zip`
- `AVATAR_LIBRARY_PART_03_INA_03.zip`
- `AVATAR_LIBRARY_PART_04_INA_04.zip`
- `AVATAR_LIBRARY_PART_05_SIS_01.zip`
- `AVATAR_LIBRARY_PART_06_SIS_02.zip`
- `AVATAR_LIBRARY_PART_07_SIS_03.zip`
- `AVATAR_LIBRARY_PART_08_SIS_04.zip`
- `AVATAR_LIBRARY_PART_09_DUO_01.zip`
- `AVATAR_LIBRARY_PART_10_DUO_02.zip`

Each part is below 30 MB. SHA-256 values and exact file membership are defined in `AVATAR_LIBRARY_TRANSFER_MANIFEST.json`.

## Non-negotiable safety and scope rules
1. READ-ONLY audit. Do not commit, push, merge, create a PR, modify `main`, modify `claude/pink-mall-development`, or rewrite existing project files.
2. Do not commit or push any private avatar photo, contact sheet, extracted JPEG, temporary preview, or derivative image.
3. Work with the private JPEGs only in a temporary/untracked local directory outside tracked repo paths, for example `/tmp/pink-mall-avatar-audit/`.
4. Do not infer INA/SIS identity from facial appearance. Use the trusted folder labels `INA/`, `SIS/`, and `DUO/` supplied by the owner.
5. Do not silently trust existing metadata. Verify it against the images where visual inspection is technically available.
6. Do not invent missing visual facts. If your environment cannot visually inspect the JPEGs, stop the visual portion and report that limitation explicitly.
7. Do not generate campaign images in this audit unless the owner later asks. This pass tests selection logic and system design, not production creative output.
8. Preserve the separation between observed identity/reference data and creative campaign hypotheses.

## Phase 0 — Preflight
Run and report:
- current branch
- current HEAD
- `git status --short`
- comparison to `claude/pink-mall-development`

Confirm that the audit branch contains no unintended changes outside `docs/pink-mall/avatar-skill/audit-v1.1/`.

## Phase 1 — Skill package integrity
1. Verify the SHA-256 of `PINK_MALL_AVATAR_CLAUDE_SKILL_v1_1.zip` against the provided `.sha256` file.
2. Extract the skill ZIP to a temporary directory, not a tracked repo path.
3. Read all core skill files, including at minimum:
   - `SKILL.md`
   - `AVATAR_LIBRARY_MANIFEST.json`
   - `CANONICAL_PACKS.json`
   - `INA_AVATAR_BIBLE.json`
   - `SIS_AVATAR_BIBLE.json`
   - `DUO_LIBRARY.json`
   - `REFERENCE_SELECTION_RULES.md`
   - `BRAND_DNA.json`
   - `SISTER_STYLE_PROFILES.json`
   - `CAMPAIGN_STYLE_PRESETS.json`
   - `CREATIVE_GUARDRAILS.md`
   - `PROMPT_ASSEMBLY_RULES.md`
   - `WORKFLOW_5_STEP.md`
   - `TEST_SCENARIOS.json`
   - `TEST_EVALUATION_RUBRIC.json`
   - `IMAGE_LIBRARY_INTEGRATION_POLICY.md`
4. Run `python VALIDATE_SKILL.py` from the extracted skill directory.
5. Independently verify the validator's assumptions rather than treating PASS as proof of semantic correctness.

Expected structural baseline from the current package:
- 190 manifest records
- 77 INA
- 76 SIS
- 37 DUO
- 103 canonical/duo references resolving without subject-label crossing
- 6 test scenarios

## Phase 2 — Private image transfer integrity
After all 10 ZIP parts are attached:
1. Verify every ZIP SHA-256 against `AVATAR_LIBRARY_TRANSFER_MANIFEST.json`.
2. Extract all parts into ONE temporary root so the result is exactly:
   - `INA/`
   - `SIS/`
   - `DUO/`
3. Verify exactly 190 JPEG files:
   - INA = 77
   - SIS = 76
   - DUO = 37
4. Verify every extracted file SHA-256 against the transfer manifest.
5. Confirm there are no duplicate byte-identical files unless explicitly documented.

If any integrity check fails, stop and report the discrepancy before semantic analysis.

## Phase 3 — Visual audit of all 190 images
If your Claude Code environment supports visual inspection of local JPEGs, inspect ALL 190 images in manageable batches.

For each image, assess only task-relevant observable properties such as:
- subject group: INA / SIS / DUO, using trusted folder label
- capture family: face / body / pose / expression / detail / motion / duo composition
- view angle / body orientation where unambiguous
- crop: face / upper-body / three-quarter / full-body
- expression category where useful for selection
- accessory/product relevance: eyewear / hat / jewellery / bag / clothing / none
- pose clarity
- identity-reference usefulness
- technical usefulness: focus, occlusion, perspective distortion, lighting consistency, framing
- whether the image is suitable as a canonical master, supporting reference, or archive-only frame

Do NOT make sensitive trait inferences or identity guesses from appearance.

Compare your visual findings to `AVATAR_LIBRARY_MANIFEST.json`, `CANONICAL_PACKS.json`, both Avatar Bibles, and `DUO_LIBRARY.json`.

Flag:
- wrong classifications
- weak masters promoted too highly
- important references missing from canonical packs
- redundant references
- pose IDs that do not match the actual visual function
- identity packs that are too broad or too narrow
- product-specific gaps
- any INA/SIS cross-contamination risk

## Phase 4 — Selection-system stress test
Do a DRY RUN only. Do not generate images.

For each scenario in `TEST_SCENARIOS.json`:
1. apply the 5-step workflow
2. select the smallest high-value reference pack
3. list each chosen file and its exact role
4. explain why no additional image is needed
5. identify likely drift risks
6. state whether the pack is sufficient for a real generation test

Then perform three additional adversarial dry runs:
- one ambiguous single-sister fashion task
- one product-heavy accessories task
- one complex DUO hero task with text-safe negative space

The goal is to determine whether the selector is robust, not whether the prose prompt sounds attractive.

## Phase 5 — Brand and sister-style audit
Review `BRAND_DNA.json`, `SISTER_STYLE_PROFILES.json`, `CAMPAIGN_STYLE_PRESETS.json`, and `CREATIVE_GUARDRAILS.md` as hypotheses for controlled testing.

Check especially:
- whether PINK MALL remains premium + playful rather than generic fashion
- whether creative roles differentiate INA and SIS without altering identity
- whether DUO rules preserve both identities
- whether product accuracy outranks atmosphere
- whether text-safe composition requirements are explicit enough
- whether any style rule could accidentally change facial/body identity
- whether subjective creative hypotheses are clearly separated from observed reference metadata

Do not treat creative profile language as a statement of real personality.

## Phase 6 — GitHub/storage architecture audit
Recommend the safest long-term storage architecture for:
- skill files
- manifest and hashes
- private full-resolution avatar references
- optional generated previews
- future campaign outputs

Important: the current repository is PUBLIC. Do not recommend putting private master references into ordinary Git history merely because size permits it.

Compare at least these options:
- keep private originals outside the public repo + version only manifests/hashes
- dedicated private repository
- private object storage / asset library
- Git LFS only if used in a private repository or if the owner explicitly accepts public visibility

## Required final report
Return one structured audit report with these sections:

### A. Verdict
One of:
- PASS FOR CONTROLLED TESTING
- PASS WITH REQUIRED CHANGES
- FAIL / NOT READY

### B. Integrity results
Hashes, counts, validator result, extraction result.

### C. 190-image library review
Coverage by INA / SIS / DUO, strongest reference families, gaps, weak or misclassified frames.

### D. Canonical pack audit
Exact packs that should remain, change, expand, or shrink.

### E. Selection-system stress test
Results for all 6 built-in scenarios + 3 adversarial scenarios.

### F. Brand/style audit
What is working, what risks generic output or identity drift, recommended changes.

### G. Privacy/storage recommendation
A concrete target architecture that keeps private reference material private.

### H. Exact proposed changes for v1.2
A numbered list with file name + field/section + exact recommended change.
Do not apply the changes yet.

### I. Testing recommendation
Define the smallest next real generation test set that would reveal the highest-value failures quickly.

## Exit condition
Stop after delivering the audit report. Do not integrate, commit, push, merge, open PRs, or modify production files until the owner explicitly approves a follow-up implementation task.
