# PINK MALL · AVATAR LAB
### The Interactive Pose Masterclass

An interactive learning environment built from `PINK_MALL_AVATAR_MASTERCLASS.docx`
(v1.0, August 2026). It is not a converted document: the methodology is the data
layer, and the page is an instrument built on top of it.

| | |
|---|---|
| Deliverable | `PINK_MALL_AVATAR_MASTERCLASS.html` — one portable file, opens offline |
| Data export | `data/AVATAR_MASTERCLASS_DATA.json` — the same pose layer, for automation |
| Source diagrams | `assets/source-diagrams/` — the 30 PNGs from the DOCX, kept for provenance |
| Dependencies | none. Vanilla HTML + CSS + JS, no build step, no network calls |
| Size | ~230 KB |

---

## 1 · The one idea

**Every figure on the page is computed, never drawn.** A single parametric SVG
croquis engine reads a pose's `rig` and renders it. That is what makes the rest
possible: if a diagram were a picture, a control could not change it.

The same renderer draws the library thumbnails, the pose detail, the camera
lab, the good/wrong comparison, the duo camera view, the motion frame strip and
the dark figure on the shoot card. One engine, ~40 call sites.

```
pose.rig ──► FIG.build() ──► joints ──► FIG.svg() ──► SVG string
                  ▲
      variation engine / camera height / lens / motion frame
```

## 2 · Architecture

Three `<script>` blocks, in order:

1. **DATA** — `SOLO_POSES`, `DUO_POSES`, `MOTION`, plus the supporting content
   arrays (`QUALITY_BAR`, `MECH_STEPS`, `FACE_SET`, `BODY_SET`, `PRODUCTS`,
   `QC_CRITERIA`, `RUN_OF_SHOW`, `RETOUCH_OK/NO`, `PIPELINE`, `BIBLE_FIELDS`,
   `TECH_MODES`). No markup.
2. **FIGURE ENGINE** — `FIG.build(rig, opts)` computes joints;
   `FIG.svg(rig, opts)` returns an SVG string.
3. **APP** — one IIFE. Renders sections, wires controls, owns persistence.

### Figure engine options

| Option | Effect |
|---|---|
| `fit` | `'card'` / `'tight'` / omit — viewBox crop, so thumbnails fill their tile |
| `thin` | thinner strokes for small sizes |
| `dark` | light-on-dark palette (used by the shoot card) |
| `ghost` | muted, for the rear figure in a duo |
| `annotate` | measurement gutter with leader lines + weight bars |
| `zones` | seven clickable body hotspots |
| `crop` | `full` / `34` / `waist` / `portrait` framing overlay with crop marks |
| `camera` | `0..3` camera-height marker (HIGH / EYE / MID / LOW HERO) |
| `lines` | shoulder + hip measurement lines (default on) |
| `plumb`, `grid` | centre-of-mass plumb line, background grid |
| `uid` | required when several figures share a page — namespaces SVG `<defs>` ids |

### Pose model

```js
{
  id:'P07', name:'Hand-on-Hip Negative Space',
  mode:'PRODUCT',                  // REFERENCE | PRODUCT | HERO
  difficulty:'foundation',         // foundation | intermediate | hero
  lang:['asymmetrical','strong'],  // body-language filter
  bestFor, purpose, body, camera, watch, shotCode,   // ← source text
  crop:['full','34','waist'], product:['bag','clothing'], lens:'70–100 mm eq.',
  steps:[[label, instruction] × 7],// FEET→HEAD, drives Build mode + Director mode
  errors:[…], correction:'…', variants:[…], tags:[…],
  rig:R({…}),                      // the correct pose
  wrong:R({…}), wrongLabel:'…'     // the common error, for the comparison
}
```

**Provenance rule.** `bestFor · body · camera · watch · shotCode` are the
document's own text. `steps · errors · correction · variants · tags · rig ·
wrong` are derived: the numbers come from the pose's own source text, and where
the source is silent the fallback is the document's §06 baseline (knees
unlocked · ribs stacked · shoulders down · soft wrists · neutral chin). Nothing
contradicts the source. The same rule is stated in a comment above the data.

### `rig` parameters

`stance`, `footOut`, `front` (step, cm), `weight` (% on the support leg),
`kneeSoft:[L,R]`, `hipShift` (cm), `hipRot`, `torsoRot`, `yaw` (whole-body°),
`shoulderTilt`, `armL`/`armR` `{out, elbow, hand, back}`, `headTurn`,
`headTilt`, `chin`, `seat:'chair'|'stool'`, `lift`, `slump`, plus flags
`hat`, `glasses`, `glare`, `hair`, `camLow`, `wide`, `walk`.

`hand` accepts: `relax` `hip` `grip` `face` `facepress` `temple` `lens` `bag`
`bagpress` `lapel` `cross` `fist`.

## 3 · Adding a new pose

1. Append one object to `SOLO_POSES` with the fields above.
2. Give it a `rig` and a `wrong` + `wrongLabel`.
3. Nothing else. The library card, filters, search, detail sheet, Build mode,
   Director mode, shoot queue, checklist, shot-code dropdown and JSON export all
   read from the array.

To make it findable in Bulgarian, add Bulgarian words to `tags` — search covers
`id, name, bestFor, body, watch, purpose, tags, product`.

## 4 · Sister A / Sister B Avatar Bible

Deliberately empty. `BIBLE_FIELDS` lists nine fields; §02 renders an input per
field per sister and stores them under `pinkmall_avatarlab_v1:bible` as
`{A:{field:value}, B:{…}}`. The ending section counts filled fields and reports
foundation status.

**No physical attribute of either sister is invented anywhere in this file.**
Placeholders read `NOT CALIBRATED YET`. Populate them after the Foundation
Shoot from real frames; nothing needs rebuilding.

## 5 · Replacing placeholders with real photography later

The croquis is a *teaching* figure and should stay. Real photography belongs
beside it:

- add `reference:{a:'…url', b:'…url'}` to a pose object;
- in `renderSheet()` the `.dt__stage` block is the single place to add an
  `<img>` next to `#sheetfig`;
- the hero's two `NOT CALIBRATED` figures are built in `#herofigs` — swap that
  array for real master frames when they exist.

Keep the generated figure as the annotation layer: it carries the measurements.

## 6 · localStorage

Namespace `pinkmall_avatarlab_v1`. All keys are exposed at
`window.PINK_MALL_AVATAR_LAB.storageKeys`.

| Key | Holds |
|---|---|
| `:done` | mastered poses / completed shots |
| `:fav` | favourites |
| `:notes` | per-pose personal notes |
| `:shoot` | shoot queue index + per-shot checkboxes |
| `:ros` | run-of-show block completion |
| `:chk` | master shot checklist, per sister |
| `:qc` | saved QC records (max 20) |
| `:bible` | Avatar Bible for A and B |
| `:hist` | generated shot-code log (max 25) |
| `:mode` | last active mode |
| `:take` | take counter |

Every read and write is wrapped in `try/catch`, so private mode degrades to a
working page without persistence. **RESET** in the rail clears all of it behind
a confirm.

## 7 · Automation surface

`window.PINK_MALL_AVATAR_LAB` exposes `solo`, `duo`, `motion`, `faceMasters`,
`bodyMasters`, `products`, `qcCriteria`, `runOfShow`, `pipeline`, `bibleFields`,
`storageKeys` and `session()`. **EXPORT POSE LIBRARY JSON** in §15 copies it.

`data/AVATAR_MASTERCLASS_DATA.json` is a build of exactly that object and is the
file to point a future pipeline at.

Shot codes follow the source:
`SIS_A_P02_45L_NEUTRAL_FULL_MASTER_001.webp` — `RAW` switches the extension to
`CR3`, matching the document's own examples.

## 8 · Accessibility and print

Semantic sections and headings; every control is a real `<button>`, `<select>`
or `<input>`; `aria-pressed` on toggles, `aria-current` on the active section,
`aria-modal` dialogs, visible focus rings, 44 px minimum tap targets.
`prefers-reduced-motion` disables animation and smooth scrolling — no lesson
depends on motion. Body-map hotspots respond to Enter/Space as well as click.

Keyboard: `←` `→` move between poses in the detail sheet; `←` `→` `Space`
advance Director Mode; `Esc` closes any overlay.

Print CSS drops navigation, animation and dark fills. Four buttons in §16 scope
the page first: SOLO POSES, DUO POSES, MASTER CHECKLIST, CAMERA/LIGHT MAP.
The solo and duo field sheets are print-only blocks generated from the same data.

## 9 · What is NOT in here

- No physical description of either sister.
- No body-idealization language. §14 states the rule and the retouch panel
  encodes it: temporary technical cleanup is allowed, anatomy is not.
- No stock photography. Every illustration is generated.
- No framework, no CDN, no fonts fetched, no analytics.
