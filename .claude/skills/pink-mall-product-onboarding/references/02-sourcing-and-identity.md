# Sourcing and Product Identity

## Source hierarchy

Use this order:

1. EU/European official manufacturer storefront
2. global official manufacturer site
3. another official regional manufacturer site
4. trusted distributor or established retailer fallback

For images:
- prefer official manufacturer CDN/media assets tied to the exact product.

Do not use as primary evidence:
- marketplaces;
- eBay;
- Pinterest;
- social posts;
- random SEO shops;
- visual similarity alone.

## Exact-match gate

A product can proceed only if the Manufacturer Item Number is explicitly and reliably tied to the exact product/variant.

Identity states:

### Exact enough to continue
- exact brand/manufacturer;
- exact Manufacturer Item Number;
- exact color/variant.

### BLOCKED
Reliable SKU exists but:
- variant/color conflicts;
- model version conflicts;
- size identity conflict requires user confirmation.

### UNRESOLVED
No reliable exact identity can be established.

For UNRESOLVED, ask only for the minimum extra evidence:
- one product photo;
- supplier screenshot;
- supplier code;
- link if available.

**But only after the refusal gate below permits a refusal at all.** Asking the
user is the last resort, not the first; the routes must be exhausted first and
the audit must say so. Do not keep searching random sources to force a result —
exhaust the *enumerated* routes instead.

## Discovery routes and the evidence ledger

A brand page returning `403` is a **transport failure, not an identity
failure**. Precisely:

- runner gets `403` → `RUNNER_DIRECT_FETCH_FAILED`, nothing more;
- source returns `404` → *this URL* no longer resolves directly, nothing more.

Neither implies `NO PRODUCT EVIDENCE EXISTS`. Index snapshots, regional
mirrors, exact retailer pages and indexed media may all still establish the
product.

Distinguish three states and never collapse them:

- `IDENTITY UNRESOLVED` — no authoritative exact-SKU evidence after expanded
  discovery.
- `DIRECT SOURCE BLOCKED` — one page cannot be fetched. **Not terminal.**
- `MEDIA DISCOVERY BLOCKED` — identity known, but no valid candidate after
  every applicable route.

Record every route attempted, with its query or URL, result, source authority,
exact-SKU evidence, exact-variant evidence and candidate count:

```text
DIRECT_OFFICIAL_PAGE      DIRECT_OFFICIAL_API      OFFICIAL_REGIONAL_SEARCH
SEARCH_INDEX_OFFICIAL     INDEXED_SOURCE_EVIDENCE  INDEXED_OUTBOUND_MEDIA
OFFICIAL_CDN_PROBE        TRUSTED_RETAILER_SEARCH
TRUSTED_RETAILER_INDEXED_EVIDENCE                  IDENTIFIER_EXPANSION
```

`IDENTIFIER_EXPANSION` means searching base SKU → full colour/variant SKU →
MPN → GTIN/EAN — but **only after an exact mapping is evidenced** by a document
that uses both forms. Never generate an expansion and then assume it.

## The refusal gate

`BLOCKED`, `UNRESOLVED`, and *any* request for user-supplied links, photos,
screenshots or confirmation are **forbidden** until a machine-readable refusal
audit shows that every applicable route above was attempted and none produced
sufficient evidence. The audit and the ledger are the proof, and a refusal must
return them.

**If one route contains an exact trusted product document, the identity may not
be called `UNRESOLVED`.** Media may still be missing — that is a *media*
outcome, not an identity one — and the two must be reported separately.

Refusing has a cost. A false refusal sends the user away to fetch something the
pipeline could have found, and it is the failure mode this section exists to
prevent.

## Authority versus transport

The earlier rule — *"search is transport, not evidence"* — was too coarse and
caused false refusals. Replace it with:

> A search engine or index is **not source authority**. But an **indexed
> snapshot of an identifiable source may carry that source's evidence.**

**Authority** belongs to the destination:
official manufacturer → official regional manufacturer → trusted
retailer/distributor.

**Transport** is merely how the bytes arrived:
direct HTTP · brand API · search-index snapshot · cached or archived document.

A direct `403` or `404` is a statement about *this fetch of this URL right
now*. It says nothing about whether the product exists or what the source said.
**A direct failure does not invalidate indexed evidence from the same source.**

Mine indexed results for image links, `src`, `srcset`, CDN domains, Open Graph
media and structured payloads. Search the exact SKU across regions and
languages — a SKU is language-independent, and a regional query often succeeds
where a global one returns nothing.

## Evidence levels

State the level honestly in every approval package.

| Level | Meaning |
|---|---|
| **A — DIRECT** | live official or trusted page, or its API |
| **B — INDEXED EXACT** | indexed/cached document from an identifiable official or trusted domain carrying exact product-specific evidence |
| **C — CORROBORATED INDEXED** | two or more independent trusted indexed sources agreeing on exact SKU + variant |

**A product may proceed on B or C** when direct access is blocked or the
original page has been delisted. That is safer than forcing the user to supply
a link, and far safer than inventing facts.

## Snippet versus document

Do not collapse these two cases:

- a generic two-line **search snippet** → *discovery only*, never evidence;
- an **indexed product document** carrying the exact reference, product fields
  and a gallery → *evidence*.

`INDEXED_SOURCE_EVIDENCE` may establish exact identity when the indexed
document is attributable to an allowed source **and** contains product-specific
evidence: exact SKU or manufacturer item · a full variant code derived from it ·
product title or model · colour/variant · GTIN/EAN/MPN · product-specific size
controls · product-specific image links · JSON-LD / OG / gallery declarations ·
**image filenames containing the exact SKU or variant**.

## Observed hosts are not guessed hosts

When indexed transport exposes product image targets:

1. extract the actual target URLs;
2. record the indexed source page they came from;
3. record the authority tier of that source;
4. put them into `candidateMedia`;
5. add the **observed** CDN hostname to the request allow-list.

If an indexed source literally exposes
`cdn.example.com/…/ppj-pgs30614-327_002.jpg`, then `cdn.example.com` is
**observed evidence**. That is the opposite of guessing a hostname, which is
what wasted an entire A08745C run. Never guess; always observe.

Feed those candidates to the acquisition runner for byte validation,
deduplication, dimensions, hashing, perceptual checks and the contact sheet. A
discovered URL is still not acquired media.

## Identity evidence for a media candidate

A candidate is admissible only when the exact SKU is evidenced by **either**:

- the **asset's identifying URL portion**, or
- the **page it was discovered on**, and then only when that page *declares*
  the image as this product's — JSON-LD, `og:image`, or a gallery `srcset`.

Two failures made these rules necessary, and both produced a green status on
the wrong photographs:

**A page sweep is not a declaration.** A retailer product page names the SKU
and also carries a sidebar of editorial thumbnails. Under page-level evidence
alone, every one inherited the page's identity. Five blog images once passed as
a product set.

**A decorative slug is not an asset identity.** Thumbor/imgproxy-style CDNs put
the real asset id in parentheses and append an SEO slug chosen by the page:

```text
https://img.<cdn>/product(<real-asset-id>)/<slug-naming-any-sku>.jpg
```

A white-and-green Gazelle Bold once passed as evidence for the pink JR5952
because the slug said `jr5952`. Match the SKU only inside the identifying
portion.

**Neither check replaces looking.** Both failures were ultimately caught by
visual confirmation of the contact sheet against the expected variant. Automated
status is provisional until a human or the skill has actually looked.

## Strict variant matching

Never borrow:
- images;
- color;
- material;
- product facts;

from:
- a similar SKU;
- another colorway;
- another season/version;
- a visually similar product.

## Official page removed

If the manufacturer page no longer exists:
- look for official CDN/archived manufacturer presence if reliable;
- then use trusted distributor/retailer fallback.

Fallback may proceed only if exact SKU + exact variant/color are explicit.

Approval preview must say:
`PRIMARY SOURCE: trusted retailer fallback`

Do not present fallback as official manufacturer evidence.

## Regional conflicts

If official regional pages differ:
1. prefer European official data;
2. prefer a page/size source with EU sizing;
3. use global official source next;
4. do not combine contradictory facts without resolving them.

## Child-series classification

Manufacturer age/series classification may be used internally only when necessary for:
- exact identity;
- official size scale;
- QA.

Never expose it publicly.

Do not store it in public tags/copy/alt/name/category.

If provenance metadata retains it internally, ensure it is never rendered or searched publicly.

## Factual extraction

Only extract what PINK MALL needs:
- model name;
- category clues;
- color;
- material;
- official size scale;
- images.

Do not import:
- reviews;
- ratings;
- source availability;
- source price;
- source promotions;
- AI review summaries;
- broad marketing claims.
