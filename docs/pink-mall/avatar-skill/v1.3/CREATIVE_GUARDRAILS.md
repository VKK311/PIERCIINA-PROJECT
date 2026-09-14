# PINK MALL Creative Guardrails v1.3

These rules apply after identity/reference selection and before any final visual-generation handoff.

## Priority order

1. Identity fidelity
2. Product accuracy
3. Wardrobe authority
4. Pierciina heritage
5. Campaign readability / intended crop
6. PINK MALL brand character
7. Creative flourish

If two requirements conflict, preserve the higher item in this list.

## Identity

- Never merge INA and SIS facial characteristics, body geometry, tattoos, piercings, or other stable identity markers.
- Do not invent permanent markers that are not supported by approved references.
- Do not treat temporary styling, makeup, clothing, lighting, or pose distortion as anatomy.
- Prefer canonical identity anchors over lower-tier or stylized references.
- If the requested angle is not adequately supported, lower confidence or request/capture a better reference rather than claiming a strong lock.

## Product

- Preserve real product shape, color, branding, hardware, proportions and distinctive details when a product reference is supplied.
- Do not allow hands, hair, props or effects to hide a product's key identifying features unless the brief explicitly asks for a non-product-led editorial frame.
- Product-led campaigns must remain commercially legible.

## Brand

- Maintain PINK MALL as premium, playful, feminine, polished and slightly strange.
- Controlled surrealism is encouraged when it serves the concept.
- Prefer one memorable strange idea over many unrelated gimmicks.
- Avoid generic stock-fashion energy.
- Avoid cheap party styling, childish cartoon pink, muddy lighting and cluttered compositions.

## Sister distinction

- INA and SIS should feel related but not interchangeable.
- The style profiles are creative defaults, not personality facts; adjust them after testing without changing biometric/identity records.
- In DUO work, keep separate identity anchors for both sisters before adding a shared composition reference.

## Identity collision

- Two subjects must read as two different people. `identityCollisionDetected`
  and `subjectRoleSwapDetected` are hard gates.
- DUO references stage a composition. They never decide whose face is whose.
- On collision, escalate to sequential identity lock. Never edit canonical
  identity pools to resolve a single failed generation.

## Wardrobe

- `referencePhotoWardrobe = IGNORE_FOR_STYLING`. Calibration clothing is not
  fashion direction and is never a fallback.
- Styling comes from the current catalogue, an approved campaign wardrobe
  reference, or an owner-approved trend brief — in that order.
- No authority means `wardrobeConfidence: LOW` and `wardrobeSourceValid: false`,
  stated plainly, not worked around.

## Pierciina heritage

- PINK MALL is an evolution of Pierciina, never a replacement.
- Carry the lineage: deep magenta, cream, warm gold, retro display type,
  marquee and signage language, stars and sparkles, boutique poster energy,
  playful handmade imperfection.
- Hold roughly 70% premium ecommerce usability / 30% strange sister-chaos Y2K.
- Never produce a generic futuristic pink mall, a generic luxury shopping
  centre, Barbie-like pink, or an anonymous chrome-heavy AI-fashion look.
- `brandHeritageMatch` is scored and gated.

## Evidence honesty

- Report `identityConfidence`, `compositionConfidence` and `productConfidence`
  separately. A single blended confidence hides the case this library actually
  has: strong identity evidence, absent composition evidence.
- Lower composition confidence when the request needs an aspect ratio,
  text-safe geometry or environment the library does not contain. All 190 frames
  are portrait, single-location, centre-framed.
- Never rank identity evidence by `frameLaplacianVar`.
- `SIS.IDENTITY_DETAILS` is `notCaptured`. Do not substitute INA's frames.

## Product authority

- `productGeometrySource` (catalogue image) and `productWearReference` (avatar
  frame) are separate fields and must never be merged.
- A full-body eyewear or headwear frame is a wear reference only. It carries no
  readable logo, hardware or lens geometry.

## Consent

- `CONSENT_AND_PROVENANCE.json` currently has every human-authorisation field
  set to `OWNER_CONFIRMATION_REQUIRED`.
- Controlled internal testing is permitted. Commercial publication of a
  generated likeness is not, until the owner completes those fields.
- Source photographs and their derivatives must never reach the public
  repository. See `IMAGE_LIBRARY_INTEGRATION_POLICY.md`.

## Commercial usability

- Reserve negative space when text is expected.
- Protect crop safety for the requested format.
- Do not place essential face/product information only in the outer 10–15% of a frame intended for responsive banners.
- A beautiful image that cannot function in its intended placement is a failed
  campaign asset. This is enforced, not advisory: `compositionUsable` is a hard
  gate in `TEST_EVALUATION_RUBRIC.json` and a `false` fails the test regardless
  of weighted score.
- Check the chosen preset's `compositionSafety` block — `textSafeRegion`,
  `subjectZone`, `edgeMargin` — before declaring an asset usable.
- A visually beautiful image still FAILS if either sister collapses into the
  other, if calibration clothing was copied, or if Pierciina heritage was lost.

## Scope

This skill selects references and assembles art-direction context. It does not silently approve production publication, replace product source-of-truth data, or redefine the sisters' canonical identities.
