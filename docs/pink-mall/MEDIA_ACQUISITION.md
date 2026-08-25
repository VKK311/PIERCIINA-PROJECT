# PINK MALL — automated product media acquisition

Turns `brand / SKU / price / sizes` into validated local image files, so nobody
has to open a brand page, save images, rename them, or upload them into a
session.

---

## The constraint that shapes everything

The Claude execution container cannot reach brand CDNs. Its egress proxy
answers `403` to `CONNECT`:

```text
assets.adidas.com -> 000  (gateway answered 403 to CONNECT)
www.adidas.de     -> 000  (gateway answered 403 to CONNECT)
www.adidas.com    -> 000  (gateway answered 403 to CONNECT)
api.github.com    -> 200
```

That last line is the whole design. GitHub is always reachable; brand CDNs are
not. So the container never downloads product media. A GitHub-hosted runner —
which has ordinary internet access — does, and commits the bytes back.

## Architecture

```text
four-field input
      │
      ▼
Claude: research identity, write request manifest
      │  git push
      ▼
docs/pink-mall/media-requests/<SKU>.request.json
      │  push triggers the workflow on that path
      ▼
GitHub-hosted runner  ── ordinary internet ──▶  brand site / official CDN
      │
      │  discover → upgrade resolution → acquire → validate
      │  → dedupe → select → previews → contact sheet → manifest
      ▼
docs/pink-mall/media-acquisition/<SKU>/     ← bot commits back
      │  git pull
      ▼
Claude: visual QA, approval package  →  human APPROVE  →  publish
```

**Why this and not something else.**

| Option | Verdict |
|---|---|
| Playwright / headless browser in the container | Same egress proxy, same 403. Adds a browser dependency and solves nothing. |
| Direct Python or Node helper in the container | Same 403. |
| Serverless fetcher (Lambda, Worker, …) | Works, but needs an account, deployment, secrets and a URL to maintain — a second system to keep alive, and a general-purpose fetch endpoint is a liability. |
| **GitHub Actions** | **Chosen.** Zero new infrastructure, zero secrets, no account beyond the one already in use. Runs on the repository that is already the project's memory, so persistence is free. |

The deciding argument is persistence, not just reachability. Results are
**committed**, so they survive container recycling by the same mechanism that
already protects everything else in this project. Artifacts would not: they
expire, and retrieving them needs an extra authenticated call.

## Separation of stages

`discover` and `acquire` are separate functions with separate log stages, on
purpose. **A discovered URL is not media.** Every earlier failure in this
project came from treating "Claude found the official image URL" as "we have
the image". The manifest reflects the distinction: a candidate that was found
but never downloaded appears in `log`, never in `images`.

## Invocation

**Normal path** — Claude writes the request and pushes:

```bash
git add docs/pink-mall/media-requests/<SKU>.request.json
git commit -m "Request media acquisition for <SKU>"
git push origin claude/pink-mall-development
```

The push triggers the workflow. Wait for the bot commit, then:

```bash
git pull origin claude/pink-mall-development
cat docs/pink-mall/media-acquisition/<SKU>/result.json
```

**Re-run one SKU** — `workflow_dispatch` with the `sku` input.

**Locally** (works only for reachable hosts; useful for tests):

```bash
python tools/media_acquisition/acquire.py \
  --request docs/pink-mall/media-requests/<SKU>.request.json \
  --out docs/pink-mall/media-acquisition
```

## Request format

The user never writes this. Claude generates it from the four-field input plus
identity research.

```jsonc
{
  "schemaVersion": 1,
  "brand": "adidas",                    // required
  "manufacturerItemNo": "JQ4556",       // required
  "model": "VL Court Bold Shoes",
  "variant": "Clear Pink / Silver Metallic / Gold Metallic",
  "officialProductPage": "https://…",
  "discoveryPages": ["https://…"],      // extra pages to scrape
  "allowedHosts": ["…"],                // added to the brand allow-list
  "allowedHostSuffixes": ["courir.com"],// permits *.courir.com
  "candidateMedia": [                   // research-derived seeds, NOT media
    { "url": "https://…", "note": "official CDN, lateral view" }
  ],
  "resolution": { "widthLadder": [1880, 1200, 1000, 840, 600] }
}
```

## Result format

`docs/pink-mall/media-acquisition/<SKU>/result.json`

```jsonc
{
  "status": "PASS",                 // PASS | PARTIAL | BLOCKED
  "sku": "JQ4556", "brand": "adidas",
  "counts": { "acquired": 6, "unique_selected": 4, "duplicates_collapsed": 2 },
  "proposedMain": "source/JQ4556-01-original.jpg",
  "contactSheet": "CONTACT_SHEET.webp",
  "images": [{
    "index": 1, "role": "MAIN",
    "file": "source/JQ4556-01-original.jpg",
    "preview": "preview/JQ4556-01.webp",
    "source_url": "…", "requested_url": "…", "anchor_url": "…",
    "source_domain": "assets.adidas.com",
    "discovery_method": "json-ld",     // json-ld | og:image | srcset | html-scan | request-seed
    "acquired_at": "…Z",
    "width": 1880, "height": 1880, "longest_edge": 1880,
    "mime": "image/jpeg", "bytes": 123456,
    "sha256": "…", "dhash": "…",
    "sku_in_url": true,
    "duplicates_collapsed": [ { "url": "…", "sha256": "…" } ],
    "validation": "PASS",
    "warnings": []
  }],
  "log": [ /* every rejected candidate, with the reason */ ]
}
```

Alongside it: `source/` (untouched originals), `preview/` (WebP), and
`CONTACT_SHEET.webp`.

## Source hierarchy

1. official EU brand storefront
2. global official brand site
3. other official regional storefront
4. official brand CDN
5. trusted distributor or major retailer, exact SKU only

No marketplaces, no social, no visual-similarity sourcing. Enforced by the
host allow-list: a host that is not in the brand registry or the request is
refused before a socket opens.

## Exact-match checks

No single signal is trusted alone. The manifest records each so a human can
weigh them:

- SKU present in the asset URL or filename (`sku_in_url`)
- candidate reached from a page that names the exact SKU
- `discovery_method` — JSON-LD and og:image outrank a page scan
- `source_domain` — official CDN outranks a retailer
- perceptual consistency across the retained set

**Variant** is not machine-decidable from a URL. The automation proposes;
the onboarding skill confirms the colorway visually against the contact sheet
before an approval package is produced. Anything unresolved is
`VARIANT MATCH BLOCKED`, and that is a human decision, not an automatic one.

## Resolution policy

Preferred: longest edge ≥ 1000 px. Ideal: ≥ 1600 px. Below 1000 px is kept but
carries a warning.

Larger copies are obtained by rewriting **only** the CDN transform segment of
the same asset URL:

```text
…/images/w_500,f_auto,q_auto/<hash>/<Name>_<SKU>_01_00_standard.jpg
…/images/w_1880,f_auto,q_auto/<hash>/<Name>_<SKU>_01_00_standard.jpg
                ▲ only this changes
```

The asset hash and filename are untouched, so this cannot yield a different
product or colorway. As a second guard, every larger variant is compared by
16×16 dHash against **the originally discovered image** and rejected if it is
not the same photograph.

That anchor choice matters. Anchoring on whichever variant downloaded first
would let a CDN that serves something else at a different width through
unchecked — a local fixture with a planted wrong-view "upgrade" confirmed it,
and the fixed version rejects it at dHash distance 23.

**Never**: AI upscaling, generative fill, recolouring, or any edit to the
product. Only the CDN's own larger copy of the same photograph.

## Validation

Per candidate: HTTP success · size floor and ceiling · HTML-served-as-image
detection · Pillow decode · non-zero dimensions · MIME allow-list · SHA-256 ·
dHash · exact-duplicate collapse · near-duplicate collapse (dHash ≤ 8).

## Failure states

| Status | Meaning | What to do |
|---|---|---|
| `PASS` | ≥ 3 unique exact images downloaded and validated | continue to visual QA |
| `PARTIAL` | identity resolved, < 3 usable images | read `log`; widen `discoveryPages` or add seeds |
| `BLOCKED` | network or source prevented acquisition | read `log`; manual upload is the fallback |
| `VARIANT MATCH BLOCKED` | exact variant cannot be proven | human decision required |

Results are committed even when not `PASS` — `result.json` carries the log that
explains why, which is more useful than a silent failure.

## Recovery after container recycling

Everything is in git. A fresh session runs:

```bash
git fetch origin
git checkout claude/pink-mall-development && git pull
cat docs/pink-mall/media-acquisition/<SKU>/result.json
```

The bytes are right there, with their SHA-256 recorded. Nothing needs to be
re-downloaded, re-uploaded, or recovered from a transcript.

## Adding another brand

One dict in `tools/media_acquisition/brands.py`:

```python
"newbrand": {
    "allowed_hosts": ["www.newbrand.com", "media.newbrand.com"],
    "page_templates": ["https://www.newbrand.com/p/{sku}"],
    "cdn_hosts": ["media.newbrand.com"],
    "width_ladder": [2000, 1600, 1200, 800],
    "sku_in_url": True,
    "view_re": r"_view(\d+)",   # optional, orders candidates
},
```

No other file changes. If the brand's CDN does not use a `w_<n>` transform
segment, resolution upgrading simply does not apply and the discovered size is
used as-is.

## Security

- `http`/`https` only
- host allow-list from the brand registry plus per-request hosts and suffixes
- redirects followed manually so **every hop** is re-checked against the
  allow-list — an open redirect on an official domain cannot become a way to
  fetch arbitrary bytes
- redirect cap 4, request timeout 25 s
- 25 MB response ceiling, checked against `Content-Length` and again while
  reading
- output filenames derived from SKU and index only, never from a remote URL,
  so a hostile path cannot escape the output directory
- no shell interpolation of fetched data — the fetcher is pure Python
- no secrets; the workflow's only permission is `contents: write`
- not a general-purpose fetch service: it runs only on committed request
  manifests in this repository

**Loop safety**: results are written under `docs/pink-mall/media-acquisition/`,
which is deliberately *not* in the workflow's trigger paths. Plus a bot-actor
guard and `[skip ci]`. The bot rebases rather than force-pushes, so a
concurrent human push is never discarded. The workflow never writes to `main`
and never opens a pull request.

## Proven in production

The JQ4556 pilot ran on a GitHub-hosted runner and reached `PASS`:

- 4 exact official images downloaded from `assets.adidas.com`
- every one upgraded `w_500` → `w_1880`, verified against its 500px anchor
- zero user-supplied image files
- two runs produced byte-identical images; only run metadata differs

Observed limitation, worth knowing before adding a brand: adidas product
**pages** answer `403` to the runner — bot protection on datacenter IP ranges —
and a retailer fallback URL `404`ed. The **CDN** served normally. So for adidas,
page scraping contributes nothing and the request manifest's researched seeds
carry the run. A brand whose product pages are reachable will exercise the
JSON-LD, og:image and srcset paths instead; both routes converge on the same
acquire-and-validate stages.

## Search as transport, and the evidence ledger

A brand page returning `403` to the runner is a **transport failure, not an
identity failure**. The search index still holds that page's parsed content and
outbound links, and a regional query often succeeds where a global one returns
nothing — a SKU is language-independent. Converse A08745C resolved in one query
once it was aimed at the Turkish market.

Every route is recorded in `result.json` under `discoveryLedger`, with its
label, URL, result, whether it evidenced the SKU, and how many candidates it
produced:

```text
DIRECT_OFFICIAL_PAGE      DIRECT_OFFICIAL_API      SEARCH_INDEX_OFFICIAL
OFFICIAL_REGIONAL_SEARCH  INDEXED_OUTBOUND_MEDIA   OFFICIAL_CDN_PROBE
TRUSTED_RETAILER_SEARCH   REQUEST_SEED
```

`BLOCKED` may be declared only when the ledger shows every applicable route
exhausted. It also pays for itself in diagnosis: A08745C's first run discovered
305 valid candidates and acquired none, and the ledger showed instantly that a
guessed CDN hostname was dropping all of them.

## Identity evidence, and three false positives

A candidate is admissible when the exact SKU is evidenced by the **asset's
identifying URL portion**, or by the **page it came from** — and then only when
that page *declares* the image as this product's (JSON-LD, `og:image`, gallery
`srcset`), never a blanket sweep.

Both clauses were written against real failures, each of which produced a green
status on the wrong photographs:

1. **Page sweep.** A retailer page names the SKU and also carries editorial
   thumbnails. Five blog images passed as a product set.
2. **Decorative slug.** Thumbor/imgproxy CDNs serve
   `…/product(<real-asset-id>)/<slug>.jpg` where the slug is chosen by the page.
   A white-and-green Gazelle Bold passed as the pink JR5952 because the slug
   said `jr5952`. `asset_identity()` now reads only the identifying portion.
3. **A page that lies about its own product.** The eobuwie page for
   `jr5952-rozowy` declares JSON-LD whose gallery is a different colourway. No
   URL-level rule can detect this.

The third has no automated fix, and that is the honest state of the system:
**automated status is provisional until someone looks at the contact sheet.**
Visual confirmation caught all three.

## What this does not do

It does not publish. Acquired media lives under `docs/pink-mall/` and reaches
`assets/pink-mall/products/<PM-ID>/` only after an explicit human `APPROVE`.
It does not choose the MAIN image on its own authority either: the proposal is
a filename-order heuristic, and visual confirmation remains a human step.
