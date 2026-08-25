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

Do not keep searching random sources to force a result.

## Discovery routes and the evidence ledger

A brand page returning `403` is a **transport failure, not an identity
failure**. Distinguish three states and never collapse them:

- `IDENTITY UNRESOLVED` — no authoritative exact-SKU evidence after expanded
  discovery.
- `DIRECT SOURCE BLOCKED` — one page cannot be fetched. **Not terminal.**
- `MEDIA DISCOVERY BLOCKED` — identity known, but no valid candidate after
  every applicable route.

Record every route attempted, with its query or URL, result, source authority,
exact-SKU evidence, exact-variant evidence and candidate count:

```text
DIRECT_OFFICIAL_PAGE      DIRECT_OFFICIAL_API      SEARCH_INDEX_OFFICIAL
OFFICIAL_REGIONAL_SEARCH  INDEXED_OUTBOUND_MEDIA   OFFICIAL_CDN_PROBE
TRUSTED_RETAILER_SEARCH
```

`BLOCKED` or `UNRESOLVED` may be declared **only after all applicable routes
are exhausted**, and the ledger is the proof.

Search is a **transport**, not just a question. An index holds the parsed
content and outbound links of pages that refuse a direct fetch. Mine indexed
results for image links, `src`, `srcset`, CDN domains, Open Graph media and
structured payloads. Search the exact SKU across regions and languages — a SKU
is language-independent, and a regional query often succeeds where a global one
returns nothing.

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
