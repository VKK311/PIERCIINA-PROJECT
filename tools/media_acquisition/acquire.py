#!/usr/bin/env python3
"""PINK MALL — exact product media acquisition.

Turns a request manifest into validated local image files plus a provenance
manifest. Designed to run on a GitHub-hosted runner, because the Claude
execution container cannot reach brand CDNs (CONNECT 403 at the egress proxy)
while it can always reach GitHub.

Pipeline, deliberately separated so that "we found a URL" is never mistaken
for "we have the bytes":

    discover -> upgrade resolution -> acquire -> validate -> dedupe
             -> select -> derive previews -> contact sheet -> manifest

Usage:
    python acquire.py --request docs/pink-mall/media-requests/JQ4556.request.json
                      --out     docs/pink-mall/media-acquisition
"""

import argparse
import datetime
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brands import brand_rule  # noqa: E402

# ── Guards ────────────────────────────────────────────────────────────────
TIMEOUT = 25
MAX_REDIRECTS = 4
MAX_BYTES = 25 * 1024 * 1024
MIN_BYTES = 1024
MAX_PAGE_BYTES = 6 * 1024 * 1024
MAX_CANDIDATES = 160
MAX_LINK_HOPS = 6
OK_MIME = {"image/jpeg", "image/png", "image/webp", "image/avif"}
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Selection thresholds
IDEAL_EDGE = 1600
PREFERRED_EDGE = 1000
MIN_EDGE = 400
DUPLICATE_DISTANCE = 8      # dHash bits; <= is the same shot
MAX_KEEP = 5
MIN_KEEP = 3


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── Network ───────────────────────────────────────────────────────────────
class Refused(Exception):
    pass


def _check_url(url, allowed):
    """allowed is (exact_hosts, host_suffixes). Suffixes let a request permit a
    retailer's media subdomains without having to guess their names, while
    still never opening the door to an arbitrary host."""
    exact, suffixes = allowed
    p = urllib.parse.urlsplit(url)
    if p.scheme not in ("http", "https"):
        raise Refused("scheme %r not allowed" % p.scheme)
    host = (p.hostname or "").lower()
    if not host:
        raise Refused("no host")
    if host in exact:
        return host
    for suf in suffixes:
        if host == suf or host.endswith("." + suf):
            return host
    raise Refused("host %s not in allow-list" % host)


class _NoAutoRedirect(urllib.request.HTTPRedirectHandler):
    """Follow redirects manually so every hop is re-checked against the
    allow-list. An open redirect off an official domain must not become a
    way to fetch arbitrary bytes."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_opener = urllib.request.build_opener(_NoAutoRedirect)


def http_get(url, allowed, max_bytes=MAX_BYTES, accept="*/*", timeout=None):
    seen = 0
    while True:
        _check_url(url, allowed)
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": accept,
            "Accept-Language": "en-GB,en;q=0.9",
        })
        try:
            resp = _opener.open(req, timeout=timeout or TIMEOUT)
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308):
                loc = e.headers.get("Location")
                if not loc:
                    raise Refused("redirect without Location")
                seen += 1
                if seen > MAX_REDIRECTS:
                    raise Refused("too many redirects")
                url = urllib.parse.urljoin(url, loc)
                continue
            raise
        with resp:
            ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            declared = resp.headers.get("Content-Length")
            if declared and int(declared) > max_bytes:
                raise Refused("content-length %s exceeds ceiling" % declared)
            body = resp.read(max_bytes + 1)
            if len(body) > max_bytes:
                raise Refused("body exceeds ceiling")
            return resp.geturl(), ctype, body


# ── Discovery ─────────────────────────────────────────────────────────────
IMG_RE = re.compile(r"https?://[^\s\"'\\<>]+?\.(?:jpg|jpeg|png|webp|avif)(?:\?[^\s\"'\\<>]*)?", re.I)
SRCSET_RE = re.compile(r"srcset\s*=\s*[\"']([^\"']+)[\"']", re.I)
HREF_RE = re.compile(r"<a[^>]+href\s*=\s*[\"']([^\"'#]+)[\"']", re.I)
OG_RE = re.compile(r"<meta[^>]+property=[\"']og:image[\"'][^>]+content=[\"']([^\"']+)[\"']", re.I)
JSONLD_RE = re.compile(r"<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", re.I | re.S)

# Methods where the page is *declaring this product's* media, as opposed to a
# blanket sweep of every image on the document.
AUTHORITATIVE_METHODS = {"json-ld", "og:image", "srcset", "request-seed", "cdn-probe",
                         # Located by Claude's research transport on a trusted
                         # product document, with that document recorded.
                         "research-evidence",
                         # An archived asset whose own path carries the article
                         # code identifies itself; the page that linked it is
                         # not needed to vouch for it.
                         "indexed-asset"}

# Paths that are editorial or chrome rather than product media. Belt and
# braces behind the method rule.
# Matches a whole path SEGMENT that begins with one of these words, so
# /banners_home/ and /banner-hp/ are caught as well as /banners/. The first
# version anchored on a trailing slash and let tradeinn's /banners_home/
# marketing panoramas through as candidate product media.
NON_PRODUCT_RE = re.compile(
    r"/(?:articles?|blog|news|banners?|promo|campaign|hero|cms|icons?|logos?|"
    r"sprites?|avatars?|placeholder|payment|social|flags?|categorias?|"
    r"categor(?:y|ies)|size[-_]?guides?|guia[-_]?tallas?|sizing)[^/]*/", re.I)

# A studio product photograph is roughly square to portrait. A 4:1 panorama is
# a page banner, a category strip or a lifestyle header — never the product
# shot this pipeline exists to acquire. Rejecting on shape is brand-agnostic
# and needs no allow-list to maintain.
# A search or listing route reflects our own query back at us: the article
# number appears in ?q= and in the rendered search box because WE put it there,
# never because the page asserts anything about an asset. Such a page is a
# discovery route — its value is the product links it yields, not its images.
# Treating its og:image as this product's is how a Scotch & Soda knitwear
# close-up was accepted as a Celest sneaker at OFFICIAL tier.
SEARCH_ROUTE_RE = re.compile(
    r"(?:/search\b|/catalogsearch\b|/results?\b|/find\b"
    r"|[?&](?:q|query|s|search|keyword|term)=)", re.I)


def is_search_route(url):
    """True when the URL is a search/listing route rather than a document
    about one product."""
    return bool(SEARCH_ROUTE_RE.search(url or ""))


MAX_ASPECT = 2.2


def _from_jsonld(html):
    out = []
    for blob in JSONLD_RE.findall(html):
        try:
            data = json.loads(blob.strip())
        except Exception:
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                img = node.get("image")
                if isinstance(img, str):
                    out.append((img, "json-ld"))
                elif isinstance(img, list):
                    out += [(u, "json-ld") for u in img if isinstance(u, str)]
                stack += list(node.values())
            elif isinstance(node, list):
                stack += node
    return out


SIZE_KEYS = ("size", "sizes", "productsize", "variantsize")


def sizes_from_jsonld(html):
    """Size labels the page itself declares for this product.

    Evidence only. PINK MALL availability comes from the user and from nothing
    else; this exists so that a user-supplied size can be checked against the
    scale the manufacturer actually offers, instead of being assumed to exist.
    A size the official scale does not contain is a size-identity question for
    a human, not something to publish quietly.
    """
    out = []
    for blob in JSONLD_RE.findall(html):
        try:
            data = json.loads(blob.strip())
        except Exception:
            continue
        # Document order, not stack order: the scale is meant to be read by a
        # human, and 36/37/38 reversed is a worse artefact than no artefact.
        queue = [data]
        while queue:
            node = queue.pop(0)
            if isinstance(node, dict):
                label = None
                for k, v in node.items():
                    if (k.lower().replace("_", "") in SIZE_KEYS
                            and isinstance(v, (str, int, float))):
                        label = str(v).strip()
                if label:
                    avail = node.get("availability")
                    avail = avail.rsplit("/", 1)[-1] if isinstance(avail, str) else ""
                    out.append((label, avail))
                queue += list(node.values())
            elif isinstance(node, list):
                queue += node
    seen, uniq = set(), []
    for lab, av in out:
        if lab and lab not in seen:
            seen.add(lab)
            uniq.append({"size": lab, "declared": av})
    return uniq


def outbound_links(html, base, sku):
    """Link targets on an indexed/official page that point at the exact SKU.

    A search or category page rarely carries the product's media itself; it
    carries the link to the page that does. Reading only <img> stops one hop
    short of the authority, which is how an official regional source gets
    misfiled as unreachable.
    """
    out = []
    for href in HREF_RE.findall(html):
        target = urllib.parse.urljoin(base, href.strip())
        if not target.lower().startswith(("http://", "https://")):
            continue
        if sku and sku.lower() in urllib.parse.unquote(target).lower():
            out.append(target)
    seen, uniq = set(), []
    for t in out:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq[:MAX_LINK_HOPS]


def discover_from_page(url, allowed, log, sku=None, ledger=None, route="DIRECT_OFFICIAL_PAGE",
                       collect_links=None, collect_sizes=None):
    """Pull image candidates out of one page. Returns
    [(url, method, source_page, page_has_sku)].

    page_has_sku matters as much as the images. A brand whose asset paths do
    not carry the style code can still be pinned to the exact SKU by the page
    the assets were found on — which is what makes a retailer page usable
    without opening the door to a neighbouring colourway.""" 
    try:
        final, ctype, body = http_get(url, allowed,
                                      max_bytes=MAX_PAGE_BYTES,
                                      accept="text/html,application/json,*/*")
    except Exception as e:
        err = "%s: %s" % (type(e).__name__, e)
        log.append({"stage": "discover", "url": url, "ok": False, "error": err})
        if ledger is not None:
            ledger.append({"route": route, "url": url, "result": "FAIL", "error": err,
                           "sku_evidence": False, "candidates": 0})
        return []
    # HTML and JSON are both fair game: a brand's product API is an approved
    # discovery route, and its payload carries the same asset URLs the page
    # would. The extractors below are tolerant of either — JSON-LD and og:image
    # simply find nothing in a JSON body, and the URL scan finds everything.
    if not any(t in (ctype or "") for t in ("html", "json", "javascript", "text")):
        log.append({"stage": "discover", "url": url, "ok": False,
                    "error": "unsupported type (%s)" % ctype})
        if ledger is not None:
            ledger.append({"route": route, "url": url, "result": "FAIL",
                           "error": "unsupported type (%s)" % ctype,
                           "sku_evidence": False, "candidates": 0})
        return []
    html = body.decode("utf-8", "replace")
    found = []
    found += _from_jsonld(html)
    found += [(u, "og:image") for u in OG_RE.findall(html)]
    for ss in SRCSET_RE.findall(html):
        for part in ss.split(","):
            u = part.strip().split(" ")[0]
            if u.startswith("http"):
                found.append((u, "srcset"))
    found += [(u, "html-scan") for u in IMG_RE.findall(html)]

    # Does the page itself name the exact SKU? Checked in its URL and body —
    # but never on a search route, where both are our own query echoed back.
    page_has_sku = bool(sku) and not is_search_route(final) and (
        sku.lower() in final.lower() or sku.lower() in html.lower())

    # One hop: hand back SKU-bearing link targets for the caller to follow.
    if collect_links is not None:
        links = outbound_links(html, final, sku)
        if links:
            log.append({"stage": "link-target", "url": final, "ok": True,
                        "targets": len(links), "sample": links[0][:140]})
        collect_links.extend(links)

    # Record the scale this page declares, but only when the page is actually
    # talking about our SKU — a category page's sizes belong to other products.
    if collect_sizes is not None and page_has_sku:
        declared = sizes_from_jsonld(html)
        if declared:
            collect_sizes.append({"page": final, "route": route, "sizes": declared})
            log.append({"stage": "size-scale", "url": final, "ok": True,
                        "declared": len(declared)})

    log.append({"stage": "discover", "url": final, "ok": True,
                "raw_candidates": len(found), "page_has_sku": page_has_sku})
    if ledger is not None:
        ledger.append({"route": route, "url": final, "result": "OK",
                       "sku_evidence": page_has_sku, "candidates": len(found)})
    return [(u, m, final, page_has_sku) for u, m in found]


# ── Indexed source evidence ───────────────────────────────────────────────
# A search engine is not source authority. But an *indexed snapshot of an
# identifiable source* carries that source's evidence: authority belongs to the
# destination (official manufacturer, official regional site, trusted
# retailer), and transport may be direct HTTP, an API, or a cached/archived
# document. A direct 403 or 404 says the runner could not fetch this URL now;
# it says nothing about whether the product exists or what the source said.
#
# Treating those as the same thing is what produced the PGS30614 false refusal:
# three official URLs 404'd, one retailer 403'd, and the run concluded "no
# reliable identity" while an indexed retailer product document with the exact
# reference, the full size ladder and seven SKU-named image files was sitting
# there unread.

WAYBACK_CDX = "https://web.archive.org/cdx/search/cdx"
# One archive refusing datacenter IPs must not end the route. These are
# independent public web archives with their own infrastructure; if the first
# will not talk to the runner, the second may. Each is an archive of the same
# identifiable sources, so authority is unchanged — only the transport is.
MEMENTO_TIMEMAP = "http://timetravel.mementoweb.org/timemap/link/"
ARQUIVO_CDX = "https://arquivo.pt/wayback/cdx"
# The id_ modifier returns the archived bytes verbatim — no Wayback banner and
# no URL rewriting — so extracted asset URLs are the source's own.
WAYBACK_SNAPSHOT = "https://web.archive.org/web/{ts}id_/{url}"
INDEX_HOSTS = frozenset(["web.archive.org", "archive.org",
                         "timetravel.mementoweb.org", "arquivo.pt"])
MAX_INDEXED_DOCS = 6
# The archive is slow, and indexed passes now fire for every page that failed
# direct fetch — across every manifest in a run. Without a ceiling one SKU's
# discovery can starve the whole job. A budget makes the cost bounded and,
# more importantly, makes exhaustion an explicit ledger fact rather than a
# silent truncation.
INDEX_CALL_BUDGET = 24
# A domain-scoped CDX query routinely takes far longer than a product-CDN
# fetch. Run 19 failed almost entirely on read timeouts at the 25s default and
# recorded them as "no archived capture" — reporting a transport failure as an
# evidence failure, one layer down from where that bug was just fixed.
INDEX_TIMEOUT = 45
INDEX_RETRIES = 1
# A call budget bounds the number of archive lookups but not their cost: 24
# calls that each burn a 90s timeout is half an hour. What actually has to be
# bounded is wall-clock, so the indexed phase gets a deadline and the job
# cannot be starved by a slow index.
INDEX_DEADLINE_S = 600
# The archive rate-limits by IP. In the last run the first domain query
# answered cleanly and the next four came back "Connection refused" within
# seconds — throttling, not an outage. Hammering it produces exactly the
# unreachable-route state the refusal gate then has to report. Space the calls
# out instead.
INDEX_MIN_INTERVAL_S = 7
_index_started = [None]
_index_last_call = [0.0]
_index_calls = [0]


def _index_budget_left():
    if _index_calls[0] >= INDEX_CALL_BUDGET:
        return False
    if _index_started[0] is not None:
        if time.time() - _index_started[0] > INDEX_DEADLINE_S:
            return False
    return True


def _index_budget_reason():
    if _index_calls[0] >= INDEX_CALL_BUDGET:
        return "index call budget exhausted (%d calls)" % INDEX_CALL_BUDGET
    return "index phase deadline reached (%ds)" % INDEX_DEADLINE_S


def _authority_tier(host, rule, request):
    """Which tier of the source hierarchy this domain belongs to.

    Authority is a property of the destination, never of the transport used to
    reach it. A snapshot of an official page is official-tier evidence.
    """
    h = (host or "").lower().lstrip(".")
    official = {x.lower().lstrip(".") for x in rule.get("allowed_hosts", [])}
    official |= {x.lower().lstrip(".") for x in request.get("officialHostSuffixes", [])}
    for o in official:
        if h == o or h.endswith("." + o):
            return "OFFICIAL"
    return "TRUSTED_RETAILER"


def _index_enabled(request=None):
    """Indexed transport can be switched off.

    The self-test must stay hermetic: it stands up a local fixture server and
    must not reach the public internet, let alone sit through archive timeouts.
    A request may also disable it explicitly.
    """
    if os.environ.get("PM_NO_INDEX"):
        return False
    if request is not None and request.get("indexedEvidence") is False:
        return False
    return True


def indexed_snapshots(target, limit=MAX_INDEXED_DOCS, match_type=None,
                      contains=None):
    """Archived captures of a URL, or of a whole domain, newest first.

    Returns (rows, error) where rows is [(timestamp, original_url)]. The error
    is returned rather than swallowed: "no archived capture" and "the index was
    unreachable" are completely different facts, and reporting the second as
    the first is the same class of mistake as reporting a 403 as an identity
    failure.

    match_type='domain' covers subdomains, which is how a product CDN is
    discovered from the storefront's own domain — cdn.<retailer>.com is found
    by asking about <retailer>.com, never by guessing the hostname.
    """
    params = [("url", target), ("output", "json"), ("limit", str(limit)),
              ("collapse", "urlkey"), ("fl", "timestamp,original"),
              ("filter", "statuscode:200")]
    if match_type:
        params.append(("matchType", match_type))
    if contains:
        params.append(("filter", "original:(?i).*%s.*" % re.escape(contains)))
    if not _index_enabled():
        return [], "indexed transport disabled (PM_NO_INDEX)"
    endpoints = [WAYBACK_CDX + "?" + urllib.parse.urlencode(params)]
    if not match_type:
        # arquivo.pt speaks the same CDX dialect for exact-URL lookups.
        endpoints.append(ARQUIVO_CDX + "?" + urllib.parse.urlencode(
            [(k, v) for k, v in params if k in ("url", "output", "limit", "fl")]))
    url = endpoints[0]
    if _index_started[0] is None:
        _index_started[0] = time.time()
    if not _index_budget_left():
        return [], _index_budget_reason()
    last_err = None
    rows = None
    for endpoint in endpoints:
        for _attempt in range(INDEX_RETRIES + 1):
            if not _index_budget_left():
                return [], last_err or _index_budget_reason()
            _index_calls[0] += 1
            gap = INDEX_MIN_INTERVAL_S - (time.time() - _index_last_call[0])
            if gap > 0:
                time.sleep(gap)
            _index_last_call[0] = time.time()
            try:
                _, _, body = http_get(endpoint, (INDEX_HOSTS, ()),
                                      max_bytes=MAX_PAGE_BYTES,
                                      accept="application/json,*/*",
                                      timeout=INDEX_TIMEOUT)
                text = body.decode("utf-8", "replace").strip()
                rows = json.loads(text) if text else []
                break
            except Exception as e:
                last_err = "%s: %s" % (type(e).__name__, e)
        if rows is not None:
            break
    if rows is None:
        return [], last_err
    out = []
    for row in rows:
        if not isinstance(row, list) or len(row) < 2:
            continue
        ts, original = row[0], row[1]
        if str(ts).lower() == "timestamp":
            continue
        out.append((str(ts), str(original)))
    out.sort(key=lambda r: r[0], reverse=True)
    return out, None


# An identifier the source itself uses for the same article: a retailer prefix,
# a colour suffix, or both (PGS30614 -> PPJ-PGS30614-327, pgs30614327).
# Expansion is only ever READ off an evidenced document — never generated and
# then assumed — so it cannot invent a neighbouring colourway.
def expand_identifiers(sku, text):
    base = re.escape(sku)
    pat = re.compile(r"[A-Za-z0-9]{0,6}[-_]?" + base + r"[-_]?[A-Za-z0-9]{0,6}", re.I)
    out = []
    for m in pat.findall(text or ""):
        token = m.strip("-_")
        if token.lower() == sku.lower():
            continue
        if not re.search(base, token, re.I):
            continue
        out.append(token)
    seen, uniq = set(), []
    for t in out:
        k = t.lower()
        if k not in seen:
            seen.add(k)
            uniq.append(t)
    return uniq[:8]


def discover_from_indexed(origin_url, allowed, log, sku, ledger, rule, request,
                          collect_links=None, collect_sizes=None,
                          observed_hosts=None, aliases=None):
    """Read an archived snapshot of one source URL.

    The snapshot is fetched from the archive, but every conclusion is attributed
    to the ORIGIN domain: its authority tier, its SKU evidence, its asset URLs.
    That is the whole point — transport changed, authority did not.

    Hosts seen inside an evidenced document are recorded as OBSERVED and become
    fetchable. That is not the same as guessing a CDN hostname: the source named
    it. Guessing is what wasted a whole A08745C run.
    """
    origin_host = urllib.parse.urlsplit(origin_url).netloc
    tier = _authority_tier(origin_host, rule, request)
    snaps, cdx_err = indexed_snapshots(origin_url, limit=3)
    log.append({"stage": "indexed-cdx", "url": origin_url,
                "captures": len(snaps), "error": cdx_err})
    if not snaps:
        if ledger is not None:
            ledger.append({"route": "INDEXED_SOURCE_EVIDENCE", "url": origin_url,
                           "result": "FAIL",
                           "error": cdx_err or "no archived capture",
                           "indexReachable": cdx_err is None,
                           "authorityTier": tier, "sku_evidence": False, "candidates": 0})
        return []

    ts, original = snaps[0]
    snap_url = WAYBACK_SNAPSHOT.format(ts=ts, url=original)
    try:
        _, ctype, body = http_get(snap_url, (INDEX_HOSTS, ()),
                                  max_bytes=MAX_PAGE_BYTES,
                                  accept="text/html,application/json,*/*")
    except Exception as e:
        err = "%s: %s" % (type(e).__name__, e)
        log.append({"stage": "indexed", "url": snap_url, "ok": False, "error": err})
        if ledger is not None:
            ledger.append({"route": "INDEXED_SOURCE_EVIDENCE", "url": origin_url,
                           "result": "FAIL", "error": err, "authorityTier": tier,
                           "sku_evidence": False, "candidates": 0})
        return []

    html = body.decode("utf-8", "replace")

    # Identifier expansion, read off the document rather than generated.
    found_aliases = expand_identifiers(sku, html) if sku else []
    if aliases is not None:
        for a in found_aliases:
            if a not in aliases:
                aliases.append(a)

    # Does this document actually name the article? Base code or an alias it
    # itself declares.
    hay = (original + " " + html).lower()
    page_has_sku = bool(sku) and not is_search_route(original) and (
        sku.lower() in hay or any(a.lower() in hay for a in found_aliases))

    found = []
    found += _from_jsonld(html)
    found += [(u, "og:image") for u in OG_RE.findall(html)]
    for ss in SRCSET_RE.findall(html):
        for part in ss.split(","):
            u = part.strip().split(" ")[0]
            if u.startswith("http"):
                found.append((u, "srcset"))
    found += [(u, "html-scan") for u in IMG_RE.findall(html)]

    # Strip archive rewriting if any survived, so candidates are origin URLs.
    cleaned = []
    for u, m in found:
        um = re.sub(r"^https?://web\.archive\.org/web/\d+(?:id_|im_)?/", "", u)
        if um.startswith("http"):
            cleaned.append((um, m))
    found = cleaned

    if collect_sizes is not None and page_has_sku:
        declared = sizes_from_jsonld(html)
        if declared:
            collect_sizes.append({"page": original, "route": "INDEXED_SOURCE_EVIDENCE",
                                  "authorityTier": tier, "indexedVia": "web.archive.org",
                                  "capturedAt": ts, "sizes": declared})

    if collect_links is not None:
        collect_links.extend(outbound_links(html, original, sku))

    # Observed hosts: named by an evidenced document from an allowed source.
    if observed_hosts is not None and page_has_sku:
        for u, _m in found:
            h = urllib.parse.urlsplit(u).netloc.lower()
            if h and h not in INDEX_HOSTS and h not in observed_hosts:
                observed_hosts.append(h)

    log.append({"stage": "indexed", "url": original, "ok": True, "capturedAt": ts,
                "raw_candidates": len(found), "page_has_sku": page_has_sku,
                "aliases": found_aliases})
    if ledger is not None:
        entry = {"route": "INDEXED_SOURCE_EVIDENCE", "url": original,
                 "result": "OK", "authorityTier": tier,
                 "indexedVia": "web.archive.org", "capturedAt": ts,
                 "aliases": found_aliases,
                 "exactProductDocument": bool(page_has_sku and found),
                 "sku_evidence": page_has_sku, "candidates": len(found)}
        ledger.append(entry)
        if tier == "TRUSTED_RETAILER":
            retail = dict(entry)
            retail["route"] = "TRUSTED_RETAILER_INDEXED_EVIDENCE"
            ledger.append(retail)
    return [(u, m, original, page_has_sku) for u, m in found]


ASSET_EXT_RE = re.compile(r"\.(?:jpg|jpeg|png|webp|avif)(?:\?|$)", re.I)


def indexed_asset_search(sku, aliases, allowed, log, ledger, rule, request,
                         observed_hosts=None):
    """Ask the index for archived ASSETS whose own path carries the article
    code, scoped to the domains this request already trusts.

    An image filename containing the exact reference identifies itself. It is
    the strongest identity signal this pipeline has and it survives the
    storefront being delisted, which is precisely the PGS30614 situation.

    Scoping matters: the query is per trusted domain with matchType=domain, so
    it covers that retailer's own CDN subdomain without ever searching the open
    web and without guessing a hostname.
    """
    out = []
    terms = []
    for t in [sku] + list(aliases or []):
        if t and t.lower() not in {x.lower() for x in terms}:
            terms.append(t)
    domains = [d.lower().lstrip(".") for d in
               (list(request.get("allowedHostSuffixes", []))
                + list(request.get("officialHostSuffixes", [])))]
    domains = sorted(set(domains))

    for domain in domains:
        for term in terms[:3]:
            rows, err = indexed_snapshots(domain, limit=100,
                                          match_type="domain", contains=term)
            hits = []
            for _ts, original in rows:
                if not ASSET_EXT_RE.search(original):
                    continue
                if NON_PRODUCT_RE.search(original):
                    continue
                host = urllib.parse.urlsplit(original).netloc.lower()
                if not host:
                    continue
                if observed_hosts is not None and host not in observed_hosts:
                    observed_hosts.append(host)
                hits.append(original)
            for u in hits[:24]:
                out.append((u, "indexed-asset", None, True))
            log.append({"stage": "indexed-asset", "domain": domain, "term": term,
                        "rows": len(rows), "hits": len(hits), "error": err})
            if ledger is not None:
                ledger.append({"route": "INDEXED_OUTBOUND_MEDIA",
                               "url": "%s (domain) ~ %s" % (domain, term),
                               "result": "OK" if hits else "FAIL",
                               "error": err,
                               "indexReachable": err is None,
                               "indexedVia": "web.archive.org",
                               "authorityTier": _authority_tier(domain, rule, request),
                               "exactProductDocument": bool(hits),
                               "sku_evidence": bool(hits), "candidates": len(hits)})
            if hits:
                break   # this domain answered; do not re-query it per alias
    return out


# ── Resolution upgrade ────────────────────────────────────────────────────
TRANSFORM_RE = re.compile(r"(/images/)([^/]*?w_)(\d+)([^/]*/)", re.I)


def _decode_transform(url):
    """adidas URLs sometimes arrive percent-encoded (w_500%2Cf_auto). Decode
    only the transform segment so the rest of the path is untouched."""
    return url.replace("%2C", ",").replace("%2c", ",")


QUERY_SIZE_RE = re.compile(r"([?&])(wid|hei|sw|sh)=(\d+)", re.I)

# Cloudflare Image Resizing puts its instructions in a path segment:
#   /cdn-cgi/image/h=785,w=628,fit=contain,.../product-vertical/<asset>.jpg
# Only that segment is ever rewritten, never the asset path after it, so the
# bytes that come back are the same photograph at a different size. Width and
# height move together so the native aspect ratio is preserved — this asks the
# CDN for a bigger copy, it does not scale anything up locally.
CF_SEG_RE = re.compile(r"(/cdn-cgi/image/)([^/]+)(/)", re.I)
CF_W_RE = re.compile(r"(\bw(?:%3D|=))(\d+)", re.I)
CF_H_RE = re.compile(r"(\bh(?:%3D|=))(\d+)", re.I)


def resolution_variants(url, ladder):
    """Same asset, larger. Only the sizing instruction changes — never the
    asset identifier — so this can never yield a different product or colorway.

    Two shapes are handled: a path transform segment (Cloudinary-style,
    /images/w_500,.../) and query sizing (Scene7-style, ?wid=440&hei=440)."""
    u = _decode_transform(url)
    out = []

    cf = CF_SEG_RE.search(u)
    if cf:
        seg = cf.group(2)
        mw, mh = CF_W_RE.search(seg), CF_H_RE.search(seg)
        if mw:
            cur_w = int(mw.group(2))
            cur_h = int(mh.group(2)) if mh else None
            for w in ladder:
                if w <= cur_w:
                    continue
                new_seg = CF_W_RE.sub(lambda x, w=w: x.group(1) + str(w), seg, count=1)
                if cur_h:
                    scaled = int(round(cur_h * (float(w) / cur_w)))
                    new_seg = CF_H_RE.sub(lambda x, h=scaled: x.group(1) + str(h),
                                          new_seg, count=1)
                out.append(u[:cf.start(2)] + new_seg + u[cf.end(2):])
            return out

    m = TRANSFORM_RE.search(u)
    if m:
        current = int(m.group(3))
        for w in ladder:
            if w <= current:
                continue
            out.append(TRANSFORM_RE.sub(
                lambda mm, w=w: "%s%s%d%s" % (mm.group(1), mm.group(2), w, mm.group(4)), u, count=1))
        return out

    sizes = QUERY_SIZE_RE.findall(u)
    if sizes:
        current = max(int(v) for _, _, v in sizes)
        for w in ladder:
            if w <= current:
                continue
            out.append(QUERY_SIZE_RE.sub(
                lambda mm, w=w: "%s%s=%d" % (mm.group(1), mm.group(2), w), u))
    return out


# ── Validation ────────────────────────────────────────────────────────────
def dhash(img, size=16):
    g = img.convert("L").resize((size + 1, size), Image.LANCZOS)
    px = list(g.getdata())
    bits = 0
    for r in range(size):
        for c in range(size):
            bits = (bits << 1) | (1 if px[r * (size + 1) + c] > px[r * (size + 1) + c + 1] else 0)
    return bits


def hamming(a, b):
    return bin(a ^ b).count("1")


def validate_bytes(body, ctype):
    """Decode and measure. Rejects an HTML error page saved with an image
    content-type, a truncated file, or anything Pillow cannot open."""
    if len(body) < MIN_BYTES:
        return None, "too small (%d B)" % len(body)
    head = body[:64].lstrip()[:15].lower()
    if head.startswith(b"<!doctype") or head.startswith(b"<html"):
        return None, "HTML served as image"
    try:
        img = Image.open(io.BytesIO(body))
        img.load()
    except Exception as e:
        return None, "undecodable: %s" % e
    w, h = img.size
    if w < 1 or h < 1:
        return None, "zero dimension"
    aspect = max(w, h) / float(min(w, h))
    if aspect > MAX_ASPECT:
        return None, "aspect %.1f:1 — banner shape, not a product photograph" % aspect
    fmt = (img.format or "").lower()
    mime = {"jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}.get(fmt, ctype or "")
    if mime not in OK_MIME:
        return None, "mime %r not allowed" % mime
    return {
        "width": w, "height": h, "longest_edge": max(w, h),
        "mime": mime, "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "dhash": "%064x" % dhash(img.convert("RGB")),
        "cutout": is_cutout(img),
        "_img": img.convert("RGB"),
    }, None


# Image CDNs in the Thumbor / imgproxy family put the real asset id inside
# parentheses and append a cosmetic, SEO-friendly slug after it:
#
#   https://img.eobuwie.cloud/product(<real-asset-id>)/<decorative-slug>.jpg
#
# The slug is chosen by the page, not by the asset. A page for one product can
# therefore serve a completely different product's bytes under a slug naming
# the SKU you asked for — which is exactly how a white-and-green Gazelle Bold
# was once accepted as evidence for the pink JR5952. Only the identifier
# counts.
TRANSFORM_WRAP_RE = re.compile(r"\(([^)]*)\)")


def asset_identity(url):
    """The part of a URL that actually identifies the bytes."""
    parts = urllib.parse.urlsplit(urllib.parse.unquote(url))
    wraps = TRANSFORM_WRAP_RE.findall(parts.path)
    if wraps:
        return (parts.netloc + " " + " ".join(wraps)).lower()
    return (parts.netloc + parts.path).lower()


def sku_signal(url, sku, aliases=None):
    """True only when the SKU, or an EVIDENCED alias of it, is in the asset's
    identifying portion.

    Aliases matter because a brand's own asset naming is not always the
    catalogue's. Colors of California's article HC.RBGLOW01 is stored as
    HC.F24.RBGLOW01-FUX-1.jpg — the season code is inserted into the MIDDLE of
    the article number, so a substring test on the article number alone fails
    on the manufacturer's own images. The alias machinery already existed and
    simply was not wired into the identity gate.

    Only evidenced aliases are accepted: they are read off documents the
    pipeline actually fetched, never generated, so this cannot loosen the gate
    into matching a neighbouring product.
    """
    ident = asset_identity(url)
    if sku.lower() in ident:
        return True
    for a in (aliases or []):
        a = str(a).strip().lower()
        if a and a in ident:
            return True
    return False


# A cut-out product PNG has no backdrop to detect, and flattening one produces
# whatever colour happened to sit in the palette — Puma 401489 reported a dark
# green #47704C from images that are 81% fully transparent. Publishing that as
# media.surface would paint a green field behind the product. Transparency is a
# better answer than a wrong colour: the storefront's own field shows through.
ALPHA_CUTOUT_RATIO = 0.30


def is_cutout(img, threshold=ALPHA_CUTOUT_RATIO):
    """Is this a transparent cut-out rather than a photograph on a backdrop?"""
    if img.mode not in ("RGBA", "LA", "P"):
        return False
    if img.mode == "P" and "transparency" not in img.info:
        return False
    a = img.convert("RGBA").getchannel("A")
    hist = a.histogram()
    clear = sum(hist[:8])
    return (clear / float(max(1, sum(hist)))) >= threshold


def backdrop(img, tol=6):
    """The studio backdrop colour, or None if there isn't one to detect.

    The storefront paints this behind a contained image so there is no visible
    seam around the photo. Detecting it here means a product never needs a
    hand-prepared canvas just to sit on the right background.

    A cut-out returns None: there is no backdrop, and inventing one is worse
    than leaving the storefront to use its own field.
    """
    if is_cutout(img):
        return None
    w, h = img.size
    inset = max(2, min(w, h) // 100)
    pts = [(inset, inset), (w - 1 - inset, inset),
           (inset, h - 1 - inset), (w - 1 - inset, h - 1 - inset)]
    cols = [img.getpixel(p) for p in pts]
    for ch in range(3):
        vals = [c[ch] for c in cols]
        if max(vals) - min(vals) > tol:
            return None
    avg = tuple(sum(c[ch] for c in cols) // len(cols) for ch in range(3))
    return "#%02X%02X%02X" % avg


# ── Variant confidence ────────────────────────────────────────────────────
# Two rules had already failed in opposite directions. "URL evidence -> PASS"
# accepted a page that misdeclared its own product. "This does not look pink
# enough -> reject" threw away correct official-matching imagery, because
# adidas's Almost Pink / Court Green / Gold Metallic is a pale upper with green
# stripes and reads nothing like the word "pink" on its own.
#
# So neither a single URL signal nor a single visual impression decides.
# Signals are fused, official image evidence outranks retailer image evidence,
# and a strong contradiction is surfaced rather than silently resolved.

# Chromatic terms are matched by hue, which is what actually separates green
# from blue; a plain RGB distance does not — a blue upper sits well inside any
# tolerance generous enough to accept real-world greens.
# hue is degrees, with a permitted window; sat/val floors keep near-greys out.
# Several terms cover more than one hue window. "Pink" is the clearest case:
# hot pink sits near magenta, but blush, dusty and "almost pink" are light,
# low-saturation tints in the red-orange arc. A single window centred on
# magenta reports "no pink in frame" for a plainly pink shoe — a false
# contradiction, which is worse than staying quiet.
HUE_TERMS = {
    "pink":     [(340, 35, 0.08, 0.55), (12, 28, 0.08, 0.62)],
    "rose":     [(345, 32, 0.08, 0.50), (12, 26, 0.08, 0.60)],
    "pembe":    [(340, 35, 0.08, 0.55), (12, 28, 0.08, 0.62)],
    "red":       (2, 18, 0.35, 0.25),
    "burgundy": (350, 22, 0.30, 0.12),
    "orange":   (28, 20, 0.35, 0.30),
    "gold":     (43, 18, 0.25, 0.30),
    "yellow":   (55, 18, 0.35, 0.40),
    "green":   (140, 45, 0.20, 0.15),
    "blue":    (220, 40, 0.20, 0.15),
    "purple":  (280, 35, 0.15, 0.15),
}
# Achromatic terms are matched on lightness and low saturation instead.
GREY_TERMS = {
    "white":  (0.86, 1.01, 0.16),
    "beige":  (0.68, 0.92, 0.30),
    "silver": (0.60, 0.85, 0.12),
    "grey":   (0.30, 0.70, 0.12),
    "gray":   (0.30, 0.70, 0.12),
    "black":  (0.00, 0.22, 0.35),
}
COLOUR_TERMS = dict.fromkeys(list(HUE_TERMS) + list(GREY_TERMS), True)


def palette(img, k=6):
    """Coarse dominant colours of the product area, background excluded."""
    im = img.convert("RGB").resize((64, 64), Image.LANCZOS)
    px = list(im.getdata())
    bg = im.getpixel((1, 1))
    keep = [p for p in px if sum(abs(a - b) for a, b in zip(p, bg)) > 40]
    if len(keep) < 40:
        keep = px
    buckets = {}
    for r, g, b in keep:
        key = (r // 48, g // 48, b // 48)
        acc = buckets.setdefault(key, [0, 0, 0, 0])
        acc[0] += r; acc[1] += g; acc[2] += b; acc[3] += 1
    top = sorted(buckets.values(), key=lambda a: -a[3])[:k]
    return [(a[0] // a[3], a[1] // a[3], a[2] // a[3], a[3]) for a in top]


def colour_terms_present(img, terms):
    """Which of the named colour terms are plausibly present in the image.

    Deliberately coarse. It exists to catch a flat contradiction — a colourway
    naming green with no green anywhere in frame — not to grade shades.
    """
    import colorsys
    pal = palette(img)
    total = sum(c[3] for c in pal) or 1
    hsv = [(colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255), c[3] / total)
           for c in pal]
    found = {}
    for term in terms:
        t = term.lower()
        if t in HUE_TERMS:
            windows = HUE_TERMS[t]
            if isinstance(windows, tuple):
                windows = [windows]
            found[term] = any(
                s >= smin and v >= vmin and share >= 0.04
                and min(abs(h * 360 - hue), 360 - abs(h * 360 - hue)) <= win
                for (h, s, v), share in hsv
                for hue, win, smin, vmin in windows)
        elif t in GREY_TERMS:
            lo, hi, smax = GREY_TERMS[t]
            found[term] = any(
                s <= smax and lo <= v < hi and share >= 0.04 for (h, s, v), share in hsv)
    return found


def variant_confidence(entries, official_colour, official_anchor_dhashes=None):
    """Fuse the signals into one of three states."""
    signals, conflicts = [], []

    sku_ok = bool(entries) and all(e.get("sku_evidence") for e in entries)
    if sku_ok:
        signals.append("exact-SKU evidence on every image")

    terms = re.findall(r"[A-Za-z]+", (official_colour or "").lower())
    terms = [t for t in terms if t in COLOUR_TERMS]

    if official_anchor_dhashes:
        agree = 0
        for e in entries:
            d = min(hamming(int(e["dhash"], 16), int(a, 16)) for a in official_anchor_dhashes)
            if d <= 40:
                agree += 1
        if agree:
            signals.append("%d/%d images agree perceptually with the official anchor"
                           % (agree, len(entries)))
        else:
            conflicts.append("no image agrees perceptually with the official anchor")

    if terms and entries:
        present = entries[0].get("_colour_terms") or {}
        missing = [t for t in terms if present.get(t) is False]
        hit = [t for t in terms if present.get(t) is True]
        if hit:
            signals.append("official colour term(s) present in frame: %s" % ", ".join(hit))
        if missing and not hit:
            conflicts.append("no official colour term found in frame (%s)" % ", ".join(missing))

    if conflicts and official_anchor_dhashes:
        state = "VARIANT_EVIDENCE_CONFLICT"
    elif conflicts:
        state = "HUMAN_VARIANT_REVIEW_REQUIRED"
    elif sku_ok and signals:
        state = "VARIANT_CONFIDENCE_PASS"
    else:
        state = "HUMAN_VARIANT_REVIEW_REQUIRED"
    return {"state": state, "signals": signals, "conflicts": conflicts,
            "officialColour": official_colour,
            "officialAnchor": bool(official_anchor_dhashes)}


# ── Size evidence semantics ───────────────────────────────────────────────
# The canonical sizing policy already says: exact-model scale NOT proven ->
# render only user-supplied sizes. So an empty size evidence set means the
# scale is unproven, which is the NORMAL case and the case the policy was
# written for. It must never mean "this size does not exist".
#
# Absence of evidence is not evidence of absence. PGS30614 was refused partly
# because empty sizeEvidence was read as a size problem; it was not.
#
# And retailer or manufacturer stock status never controls PINK MALL
# availability: the user is the only source of truth for what is in stock.

SIZE_SCALE_NOT_PROVEN = "SIZE_SCALE_NOT_PROVEN"
SIZE_CONFIRMED = "SIZE_CONFIRMED"
SIZE_IDENTITY_CONFLICT = "SIZE_IDENTITY_CONFLICT"
SIZE_CONFIRMATION_REQUIRED = "SIZE_CONFIRMATION_REQUIRED"


def _size_key(label):
    """Numeric key for a size label, or None if it is not numeric.

    Understands the three real EU footwear notations: whole (38), fractional
    (37 1/3) and decimal (37.5). Labels are compared, never rewritten.
    """
    t = str(label).strip()
    m = re.match(r"^(\d+)(?:\s+(\d+)/(\d+))?$", t)
    if m:
        whole = int(m.group(1))
        frac = (int(m.group(2)) / int(m.group(3))) if m.group(2) and m.group(3) else 0.0
        return whole + frac
    d = re.match(r"^(\d+)[.,](\d+)$", t)
    if d:
        try:
            return float(d.group(1) + "." + d.group(2))
        except ValueError:
            return None
    return None


def size_state(user_sizes, size_evidence):
    """Reconcile the sizes the user supplied against the scale sources declare.

    Returns {state, declaredScale, matched, missing, note}. This never decides
    PINK MALL availability — it only says how well evidenced the labels are.
    """
    user = [str(u).strip() for u in (user_sizes or []) if str(u).strip()]
    declared = []
    for block_ in (size_evidence or []):
        for entry in block_.get("sizes", []):
            lab = str(entry.get("size", "")).strip()
            if lab and lab not in declared:
                declared.append(lab)

    if not user:
        return {"state": SIZE_SCALE_NOT_PROVEN, "declaredScale": declared,
                "matched": [], "missing": [],
                "note": "no user sizes supplied"}

    if not declared:
        # The normal case. Publish exactly what the user gave, assert no
        # sold-out ladder, and do not treat this as a problem.
        return {"state": SIZE_SCALE_NOT_PROVEN, "declaredScale": [],
                "matched": [], "missing": [],
                "note": ("no source declared an exact size scale; user-supplied "
                         "sizes stand as availability truth and no sold-out "
                         "ladder is asserted")}

    dkeys = {}
    for lab in declared:
        k = _size_key(lab)
        if k is not None:
            dkeys.setdefault(round(k, 4), lab)
    dlabels = {l.lower() for l in declared}

    matched, missing, fuzzy = [], [], []
    for u in user:
        if u.lower() in dlabels:
            matched.append(u)
            continue
        k = _size_key(u)
        if k is not None and round(k, 4) in dkeys:
            matched.append(u)
            continue
        if k is None:
            # A non-numeric label against a numeric scale is a conversion
            # question, not a contradiction.
            fuzzy.append(u)
            continue
        missing.append(u)

    if fuzzy:
        return {"state": SIZE_CONFIRMATION_REQUIRED, "declaredScale": declared,
                "matched": matched, "missing": fuzzy,
                "note": "size label could not be compared to the declared scale"}
    if missing:
        return {"state": SIZE_IDENTITY_CONFLICT, "declaredScale": declared,
                "matched": matched, "missing": missing,
                "note": ("the declared exact scale does not contain %s"
                         % ", ".join(missing))}
    return {"state": SIZE_CONFIRMED, "declaredScale": declared,
            "matched": matched, "missing": [],
            "note": "every supplied size appears in the declared exact scale"}


# ── Refusal gate ──────────────────────────────────────────────────────────
# Refusing is an action with a cost. BLOCKED / UNRESOLVED / "please send me a
# link" may not be returned until the routes that could have answered were
# actually tried and actually failed.

REFUSAL_ROUTES = (
    "DIRECT_OFFICIAL_PAGE",
    "DIRECT_OFFICIAL_API",
    "OFFICIAL_REGIONAL_SEARCH",
    "SEARCH_INDEX_OFFICIAL",
    "INDEXED_SOURCE_EVIDENCE",
    "INDEXED_OUTBOUND_MEDIA",
    "OFFICIAL_CDN_PROBE",
    "TRUSTED_RETAILER_SEARCH",
    "TRUSTED_RETAILER_INDEXED_EVIDENCE",
    "IDENTIFIER_EXPANSION",
)


# A route that could not be reached did not answer the question. Treating
# "the archive refused the connection" as "the archive holds nothing" is the
# same conflation as treating a 403 as an identity failure — one level up.
TRANSPORT_FAILURE_RE = re.compile(
    r"timed out|timeout|connection refused|connection reset|handshake|"
    r"temporarily unavailable|budget exhausted|deadline reached|"
    r"HTTP Error (?:403|408|429|5\d\d)", re.I)


def _is_transport_failure(entry):
    """Did this route fail to be *reached*, as opposed to answering 'nothing'?

    A 404 is an answer: the host responded and that URL does not resolve. A
    timeout, a refused connection, a 403, a 5xx, or an exhausted budget is not
    an answer at all — the route never got to speak.
    """
    if entry.get("result") != "FAIL":
        return False
    if entry.get("indexReachable") is False:
        return True
    return bool(TRANSPORT_FAILURE_RE.search(str(entry.get("error") or "")))


def refusal_audit(ledger, aliases=None):
    """Machine-readable account of whether a refusal is permitted.

    Two facts decide it.

    exact_product_document: if any route returned a document from an allowed
    source naming this exact article with product fields, the identity is NOT
    unresolved, whatever happened elsewhere.

    transport failures: a route that timed out, was refused, or ran out of
    budget never answered. Counting it as "tried and empty" would let an
    infrastructure problem masquerade as evidence of absence — which is the
    entire failure mode this gate exists to prevent.
    """
    attempted, succeeded, exact, unreachable = {}, {}, [], {}
    for e in (ledger or []):
        r = e.get("route")
        if not r:
            continue
        attempted[r] = attempted.get(r, 0) + 1
        if e.get("result") == "N/A":
            continue
        if e.get("result") == "OK":
            succeeded[r] = succeeded.get(r, 0) + 1
        elif _is_transport_failure(e):
            unreachable.setdefault(r, []).append(str(e.get("error") or "unreachable")[:120])
        if e.get("exactProductDocument") or (e.get("sku_evidence") and e.get("candidates")):
            exact.append({"route": r, "url": e.get("url"),
                          "authorityTier": e.get("authorityTier"),
                          "candidates": e.get("candidates")})
    if aliases:
        attempted["IDENTIFIER_EXPANSION"] = attempted.get("IDENTIFIER_EXPANSION", 0) + 1
        succeeded["IDENTIFIER_EXPANSION"] = succeeded.get("IDENTIFIER_EXPANSION", 0) + 1

    untried = [r for r in REFUSAL_ROUTES if r not in attempted]
    # A route counts as exhausted only if it actually answered at least once.
    blocked = sorted(r for r in unreachable if r not in succeeded)

    if exact:
        why = "an exact product document was found — identity is established"
    elif untried:
        why = "routes not attempted: " + ", ".join(untried)
    elif blocked:
        why = ("route(s) never answered — transport failure, not evidence: "
               + ", ".join(blocked))
    else:
        why = ""

    return {
        "routesAttempted": sorted(attempted),
        "routesSucceeded": sorted(succeeded),
        "routesNotAttempted": untried,
        "routesUnreachable": {k: v for k, v in unreachable.items() if k in blocked},
        "exactProductDocuments": exact,
        "identifierAliases": list(aliases or []),
        # Honest only when nothing was left untried, nothing was merely
        # unreachable, and nothing exact was found.
        "refusalPermitted": (not exact) and (not untried) and (not blocked),
        "refusalBlockedBecause": why,
    }


# ── Research evidence handoff ─────────────────────────────────────────────
# Discovery and acquisition are different jobs with different transports.
#
# A GitHub runner is an excellent binary client — it fetches CDN bytes fast and
# reliably — and a poor research client: search indexes and public archives
# rate-limit or refuse its datacenter IP, which is what produced four
# consecutive DISCOVERY_TRANSPORT_BLOCKED runs for PGS30614.
#
# So research happens where research works (Claude's own investigation), and
# its findings are written into the manifest as structured evidence. The runner
# then does only what it is good at: validate the host, fetch the bytes,
# validate MIME and dimensions, reject banners and editorial assets, hash and
# dedupe, check variant confidence, build the contact sheet, preserve
# provenance. Archive lookups become a fallback for when research did not
# expose enough media, not a precondition for onboarding anything.
#
# Authority is unchanged by any of this. A research transport is not an
# authority; the underlying official or trusted-retailer source is.

# REVIEWER_VERIFIED: an independent reviewer transport read the live source
# document that this session could not reach. It is neither Claude's own
# research nor an unverified user assertion, and it is recorded as its own
# provenance class so the distinction survives into the approval package.
RESEARCH_TRANSPORTS = {"CLAUDE_RESEARCH", "REVIEWER_VERIFIED", "USER_SUPPLIED",
                       "INDEX_SNAPSHOT", "DIRECT_FETCH"}
EVIDENCE_LEVELS = {"A", "B", "C"}


def ingest_research_evidence(request, log, ledger):
    """Turn recorded research findings into acquisition inputs.

    Returns (candidates, observed_hosts, aliases, size_evidence, summary).
    Nothing here asserts a product fact: every media URL still has to survive
    host validation, byte validation, the banner and shape guards, the identity
    gate and variant confidence before it can reach an approval package.
    """
    candidates, observed_hosts, aliases, size_evidence = [], [], [], []
    summary = []

    for ev in (request.get("researchEvidence") or []):
        src = ev.get("sourceUrl") or ""
        tier = ev.get("authorityTier") or "TRUSTED_RETAILER"
        transport = ev.get("discoveryTransport") or "CLAUDE_RESEARCH"
        level = (ev.get("confidence") or "").upper()
        if transport not in RESEARCH_TRANSPORTS:
            log.append({"stage": "research", "url": src, "ok": False,
                        "error": "unknown discoveryTransport %r" % transport})
            continue
        if level and level not in EVIDENCE_LEVELS:
            log.append({"stage": "research", "url": src, "ok": False,
                        "error": "unknown confidence level %r" % level})
            continue

        for a in (ev.get("aliases") or []):
            if a and a not in aliases:
                aliases.append(a)

        scale = ev.get("sizeScale") or []
        if scale:
            # Accept a bare label as well as {"size": ..., "declared": ...},
            # exactly as mediaUrls just below accepts a bare URL. A size scale
            # is naturally written as ["36", "37", ...], and every manifest
            # before this one left the field empty, so the dict-only form had
            # never actually been exercised against real data.
            sizes = []
            for x in scale:
                if isinstance(x, dict):
                    label, declared = x.get("size"), x.get("declared", "")
                else:
                    label, declared = x, ""
                if label is None:
                    continue
                label = str(label).strip()
                if label:
                    sizes.append({"size": label, "declared": declared})
            size_evidence.append({
                "page": src, "route": "RESEARCH_EVIDENCE",
                "authorityTier": tier, "transport": transport,
                "capturedAt": ev.get("capturedAt"),
                "sizes": sizes,
            })

        media = ev.get("mediaUrls") or []
        for m in media:
            url = m.get("url") if isinstance(m, dict) else m
            if not url or not str(url).lower().startswith(("http://", "https://")):
                continue
            field = (m.get("field") if isinstance(m, dict) else None) or "research"
            candidates.append((url, "research-evidence", src, True))
            host = urllib.parse.urlsplit(url).netloc.lower()
            if host and host not in observed_hosts:
                observed_hosts.append(host)
            log.append({"stage": "research-media", "url": url, "field": field,
                        "sourcePage": src, "authorityTier": tier})

        for h in (ev.get("observedCdnHosts") or []):
            h = str(h).lower().lstrip(".")
            if h and h not in observed_hosts:
                observed_hosts.append(h)

        entry = {
            "route": "RESEARCH_EVIDENCE",
            "url": src,
            "result": "OK" if (media or scale or aliases) else "FAIL",
            "authorityTier": tier,
            "discoveryTransport": transport,
            "confidence": level or None,
            "capturedAt": ev.get("capturedAt"),
            "observedSku": ev.get("sku"),
            "model": ev.get("model"),
            "variant": ev.get("variant"),
            "aliases": ev.get("aliases") or [],
            "mediaUrls": len(media),
            "sizeLabels": len(scale),
            # Identity evidence and media evidence are separate claims and are
            # recorded separately. A source can pin the article precisely and
            # still expose no usable imagery.
            "exactProductDocument": bool(ev.get("sku") and (media or scale)),
            "sku_evidence": bool(ev.get("sku")),
            "candidates": len(media),
        }
        ledger.append(entry)
        summary.append({k: entry[k] for k in
                        ("url", "authorityTier", "discoveryTransport", "confidence",
                         "observedSku", "model", "variant", "mediaUrls", "sizeLabels")})

    if candidates or observed_hosts:
        log.append({"stage": "research", "seeded_candidates": len(candidates),
                    "observed_hosts": sorted(set(observed_hosts))})
    return candidates, observed_hosts, aliases, size_evidence, summary


# ── Main ──────────────────────────────────────────────────────────────────
def acquire(request, outroot, log):
    sku = request["manufacturerItemNo"].strip()
    brand = request["brand"].strip()
    rule = brand_rule(brand)

    allowed = (
        frozenset([h.lower() for h in rule["allowed_hosts"]] +
                  [h.lower() for h in request.get("allowedHosts", [])]),
        tuple(sorted({h.lower().lstrip(".") for h in request.get("allowedHostSuffixes", [])})),
    )
    ladder = request.get("resolution", {}).get("widthLadder") or rule["width_ladder"]

    # 1. DISCOVER ---------------------------------------------------------
    ledger = []
    candidates = []

    # Research evidence first. Media Claude already located from a trusted
    # product document is acquired directly; the runner does not go and
    # rediscover it through an archive.
    (research_candidates, research_hosts, research_aliases,
     research_sizes, research_summary) = ingest_research_evidence(request, log, ledger)
    candidates += research_candidates

    for seed in request.get("candidateMedia", []):
        u = seed["url"] if isinstance(seed, dict) else seed
        candidates.append((u, "request-seed", None, True))
        ledger.append({"route": "REQUEST_SEED", "url": u, "result": "OK",
                       "sku_evidence": True, "candidates": 1})

    # Official-CDN probing. Brands that publish under the style code expose a
    # predictable asset path; we try it and keep only what actually downloads,
    # decodes and carries the exact SKU. A probe is a lead, never evidence:
    # the variant is still confirmed visually before any approval package.
    probes = list(request.get("cdnProbe", [])) or rule.get("cdn_probe", [])
    views = request.get("cdnProbeViews") or rule.get("cdn_probe_views", [])
    for tpl in probes:
        for view in views:
            probe_url = tpl.format(sku=sku, sku_lower=sku.lower(),
                                   sku_upper=sku.upper(), view=view)
            candidates.append((probe_url, "cdn-probe", None, False))

    pages = list(request.get("discoveryPages", []))
    if request.get("officialProductPage"):
        pages.insert(0, request["officialProductPage"])
    for tpl in rule["page_templates"]:
        pages.append(tpl.format(sku=sku))
    routes = request.get("discoveryRoutes") or {}
    seen_pages = set()
    hop_targets = []
    size_evidence = []
    # hosts an evidenced document named — never guessed
    observed_hosts = list(research_hosts)
    aliases = list(research_aliases)          # identifiers the source itself uses
    size_evidence.extend(research_sizes)
    failed_pages = []

    # Research media is allow-listed immediately: the runner must be able to
    # fetch what research already found without waiting on any other route.
    if observed_hosts:
        allowed = (frozenset(set(allowed[0]) | {h.lower() for h in observed_hosts}),
                   allowed[1])
    for page in pages:
        if page in seen_pages:
            continue
        seen_pages.add(page)
        before = len(ledger)
        candidates += discover_from_page(page, allowed, log, sku=sku, ledger=ledger,
                                         route=routes.get(page, "DIRECT_OFFICIAL_PAGE"),
                                         collect_links=hop_targets,
                                         collect_sizes=size_evidence)
        # A direct fetch that failed, or succeeded without naming the article,
        # is a TRANSPORT outcome. The source may still have said plenty; ask
        # the index for its snapshot before concluding anything.
        entry = ledger[before] if len(ledger) > before else None
        if entry and (entry.get("result") != "OK" or not entry.get("sku_evidence")):
            failed_pages.append(page)

    # Second hop. The authority is the destination, not the page that linked to
    # it: a product page reached from an official category listing is official
    # media, and stays official even though the direct URL refuses the runner.
    def page_key(u):
        parts = urllib.parse.urlsplit(u)
        return (parts.netloc.lower(), parts.path.rstrip("/").lower())

    seen_keys = {page_key(p) for p in seen_pages}
    for target in hop_targets:
        key = page_key(target)
        if target in seen_pages or key in seen_keys:
            continue
        seen_pages.add(target)
        seen_keys.add(key)
        candidates += discover_from_page(target, allowed, log, sku=sku, ledger=ledger,
                                         route="INDEXED_OUTBOUND_MEDIA",
                                         collect_sizes=size_evidence)

    # Archived assets whose own path carries the article code. This runs FIRST,
    # ahead of the per-URL snapshot lookups, because it is the strongest
    # evidence available: a filename carrying the exact reference identifies
    # itself and survives the storefront being delisted. Ordering it last let
    # six per-URL lookups burn the whole indexed-phase deadline before the
    # highest-value route was ever attempted.
    # Archive lookup is a fallback for missing media — but only for media at
    # the SAME OR HIGHER tier. Skipping the routes that find official media
    # because retailer media was already supplied inverts the source hierarchy:
    # it lets a lower tier suppress the discovery of a higher one. PGS30614
    # did exactly that, publishing 1600px retailer imagery while the
    # manufacturer's own CDN sat undiscovered.
    research_official = any(
        _authority_tier(urllib.parse.urlsplit(u).netloc, rule, request) == "OFFICIAL"
        for u, _m, _p, _e in research_candidates)
    research_media_found = bool(research_candidates) and research_official
    if research_media_found:
        log.append({"stage": "index-skip",
                    "reason": "research evidence already exposed %d OFFICIAL media "
                              "URL(s); archive lookup is a fallback, not a "
                              "precondition" % len(research_candidates)})
    elif research_candidates:
        log.append({"stage": "index-continue",
                    "reason": "research evidence supplied %d retailer-tier media "
                              "URL(s); official routes still run so the source "
                              "hierarchy can be applied"
                              % len(research_candidates)})
    if (request.get("indexedAssetSearch", True) and _index_enabled(request)
            and not research_media_found):
        candidates += indexed_asset_search(sku, aliases, allowed, log, ledger, rule,
                                           request, observed_hosts=observed_hosts)

    # Indexed source evidence. Runs for every page the direct transport could
    # not turn into evidence — 403, 404, or a 200 that never named the article.
    for page in (failed_pages[:MAX_INDEXED_DOCS]
                 if (_index_enabled(request) and not research_media_found) else []):
        candidates += discover_from_indexed(page, allowed, log, sku, ledger, rule,
                                            request, collect_links=hop_targets,
                                            collect_sizes=size_evidence,
                                            observed_hosts=observed_hosts,
                                            aliases=aliases)

    # A route that cannot apply to this brand is not a route left untried.
    # Without this the audit reports "routes not attempted" forever and a
    # refusal becomes impossible even when one is warranted — the mirror image
    # of the false refusal this gate exists to prevent.
    def note_na(route, reason):
        if not any(e.get("route") == route for e in ledger):
            ledger.append({"route": route, "url": None, "result": "N/A",
                           "notApplicable": reason,
                           "sku_evidence": False, "candidates": 0})

    if not any("/api/" in t for t in rule.get("page_templates", [])):
        note_na("DIRECT_OFFICIAL_API", "brand registry declares no product API")
    if not any(r == "OFFICIAL_REGIONAL_SEARCH" for r in routes.values()):
        note_na("OFFICIAL_REGIONAL_SEARCH", "no official regional search entry point")
    if not any(r == "SEARCH_INDEX_OFFICIAL" for r in routes.values()):
        note_na("SEARCH_INDEX_OFFICIAL", "no official index entry point supplied")
    if not (request.get("cdnProbe") or rule.get("cdn_probe")):
        note_na("OFFICIAL_CDN_PROBE",
                "brand asset paths are not derivable from the style code")
    if not any(r == "TRUSTED_RETAILER_INDEXED_EVIDENCE" for r in
               [e.get("route") for e in ledger]):
        note_na("TRUSTED_RETAILER_INDEXED_EVIDENCE",
                "no trusted-retailer page reached indexed evaluation")
    note_na("IDENTIFIER_EXPANSION",
            "ran over every evidenced document; %d alias(es) found" % len(aliases))

    # Promote observed hosts into the allow-list. A host named by an evidenced
    # document from an allowed source is discovered, not guessed.
    if observed_hosts:
        allowed = (frozenset(set(allowed[0]) | {h.lower() for h in observed_hosts}),
                   allowed[1])
        log.append({"stage": "observed-hosts", "hosts": sorted(set(observed_hosts))})

    # normalise, de-dup by URL, keep discovery order
    ordered, seen_url = [], set()
    for u, method, src_page, page_sku in candidates:
        u = _decode_transform(u.strip())
        if not u.lower().startswith(("http://", "https://")):
            continue
        try:
            _check_url(u, allowed)
        except Refused as e:
            log.append({"stage": "filter", "url": u[:160], "ok": False, "error": str(e)})
            continue
        if u in seen_url:
            continue
        seen_url.add(u)
        ordered.append((u, method, src_page, page_sku))
    # Rank before capping. Following link targets multiplied the candidate pool
    # roughly fivefold, and a flat cap then truncated the real product images
    # out of the list entirely — discovery got better and acquisition got worse.
    # Authoritative declarations and SKU-evidenced pages go first, so the cap
    # trims the page sweep rather than the product.
    METHOD_RANK = {"research-evidence": 0, "request-seed": 0, "cdn-probe": 0,
                   "indexed-asset": 0,
                   "json-ld": 1, "og:image": 1, "srcset": 2, "html-scan": 3}
    ordered.sort(key=lambda c: (METHOD_RANK.get(c[1], 4), 0 if c[3] else 1))
    ordered = ordered[:MAX_CANDIDATES]
    log.append({"stage": "discover", "total_unique_candidates": len(ordered)})

    # 2. ACQUIRE (with resolution upgrade per asset) -----------------------
    def grab(u):
        """Download and validate one URL. Returns meta or None."""
        try:
            final, ctype, body = http_get(u, allowed, accept="image/*,*/*")
        except Exception as e:
            log.append({"stage": "acquire", "url": u[:160], "ok": False,
                        "error": "%s: %s" % (type(e).__name__, e)})
            return None
        meta, err = validate_bytes(body, ctype)
        if not meta:
            log.append({"stage": "validate", "url": u[:160], "ok": False, "error": err})
            return None
        meta["url"] = final
        meta["requested_url"] = u
        meta["_body"] = body
        return meta

    acquired = []
    for url, method, src_page, page_sku in ordered:
        # The discovered URL is the anchor: it is the image we actually found
        # on the source. Every larger variant is then checked against it.
        # Anchoring on "whichever variant downloaded first" would let a CDN
        # that serves something else at a different width slip through
        # unchecked, so the order here matters.
        anchor = grab(url)
        best = anchor
        notes = []
        if anchor is None:
            notes.append("anchor image unavailable; resolution variant accepted unverified")

        for variant in resolution_variants(url, ladder):
            meta = grab(variant)
            if meta is None:
                continue
            if anchor is not None:
                d = hamming(int(anchor["dhash"], 16), int(meta["dhash"], 16))
                if d > DUPLICATE_DISTANCE:
                    log.append({"stage": "resolution", "url": variant[:160], "ok": False,
                                "error": "variant differs from anchor (dHash %d); rejected" % d})
                    continue
            if best is None or meta["longest_edge"] > best["longest_edge"]:
                best = meta

        # Identity gate. A candidate is admissible when the exact SKU is
        # evidenced either by the asset URL itself, or by the page the asset
        # was discovered on.
        #
        # Requiring it in the asset URL alone was too narrow: adidas and New
        # Balance embed the style code in the path, but plenty of brands and
        # every retailer do not. Requiring nothing would be far too loose — a
        # category page for "pink Chuck Taylor Move" lists several distinct
        # SKUs, and substituting a neighbour is exactly the failure the
        # exact-variant rule exists to prevent.
        if best:
            asset_sku = sku_signal(best["url"], sku, aliases)
            if not (asset_sku or page_sku):
                log.append({"stage": "identity", "url": best["url"][:160], "ok": False,
                            "error": "neither asset URL nor source page evidences SKU %s" % sku})
                best = None
            elif not asset_sku and method not in AUTHORITATIVE_METHODS:
                # Source-page evidence alone is not enough for a blanket page
                # sweep. A retailer product page names the SKU and *also*
                # carries a sidebar of editorial thumbnails; every one of those
                # would otherwise inherit the page's identity and pass. When
                # the asset URL does not identify itself, the page must be
                # declaring the image as this product's — JSON-LD, og:image or
                # a gallery srcset — not merely containing it.
                log.append({"stage": "identity", "url": best["url"][:160], "ok": False,
                            "error": "source-page evidence requires an authoritative "
                                     "declaration; %s is a page sweep" % method})
                best = None
            elif not asset_sku and NON_PRODUCT_RE.search(best["url"]):
                log.append({"stage": "identity", "url": best["url"][:160], "ok": False,
                            "error": "editorial or chrome asset path; rejected"})
                best = None
            else:
                best["sku_evidence"] = "asset-url" if asset_sku else "source-page"

        if best:
            best["discovery_method"] = method
            best["acquired_at"] = now()
            best["sku_in_url"] = sku_signal(best["url"], sku, aliases)
            best["source_page"] = src_page
            best["anchor_url"] = url
            best["notes"] = notes
            acquired.append(best)
            log.append({"stage": "acquire", "url": best["url"][:160], "ok": True,
                        "size": "%dx%d" % (best["width"], best["height"]),
                        "bytes": best["bytes"],
                        "upgraded_from": None if best["requested_url"] == url else url[:160]})

    if not acquired:
        return None, acquired, ledger, size_evidence, aliases

    # 3. DEDUPE -----------------------------------------------------------
    acquired.sort(key=lambda m: (-m["longest_edge"], -m["bytes"]))
    unique = []
    for m in acquired:
        dup_of = None
        for k in unique:
            if m["sha256"] == k["sha256"]:
                dup_of = k
                break
            if hamming(int(m["dhash"], 16), int(k["dhash"], 16)) <= DUPLICATE_DISTANCE:
                dup_of = k
                break
        if dup_of:
            dup_of.setdefault("duplicates", []).append(
                {"url": m["url"], "size": "%dx%d" % (m["width"], m["height"]), "sha256": m["sha256"]})
        else:
            unique.append(m)

    # 4. SELECT -----------------------------------------------------------
    # A request may raise the keep limit for reconnaissance — sweeping one hero
    # view across an article's colour codes needs every colourway visible on
    # the contact sheet, not the first five. Bounded so it cannot become a way
    # to publish a sprawling gallery by accident.
    max_keep = min(int(request.get("maxKeep") or MAX_KEEP), 24)

    usable = [m for m in unique if m["longest_edge"] >= MIN_EDGE]

    # Authority tier decides before resolution does. The source hierarchy is a
    # locked rule — official manufacturer media outranks a trusted retailer —
    # but until now it only governed which pages were visited, never which
    # bytes were kept. A run that reached both could therefore publish retailer
    # imagery while official imagery sat in the same candidate pool.
    for m in usable:
        m["authorityTier"] = _authority_tier(
            urllib.parse.urlsplit(m["url"]).netloc, rule, request)
    TIER_RANK = {"OFFICIAL": 0, "TRUSTED_RETAILER": 1}
    if any(m["authorityTier"] == "OFFICIAL" for m in usable):
        official = [m for m in usable if m["authorityTier"] == "OFFICIAL"]
        if len(official) >= MIN_KEEP:
            # Enough official media to stand on its own: do not mix tiers in
            # one gallery, and never let a larger retailer copy displace it.
            log.append({"stage": "select", "tier": "OFFICIAL",
                        "note": "official media sufficient; retailer candidates "
                                "dropped to keep one authority tier per gallery",
                        "official": len(official),
                        "retailer_dropped": len(usable) - len(official)})
            usable = official

    usable.sort(key=lambda m: (TIER_RANK.get(m["authorityTier"], 2),
                               -m["longest_edge"], m["url"]))
    selected = usable[:max_keep]
    return selected, acquired, ledger, size_evidence, aliases


# The studio backdrop only has to agree, not be byte-identical. A set shot on
# one seamless can still return #DCDBD7 and #DDDCD8 from JPEG quantisation, and
# demanding exact equality threw the whole value away — leaving media.surface
# unset and a contained image sitting on a mismatched field.
BACKDROP_TOLERANCE = 8


def _hex_rgb(h):
    h = (h or "").lstrip("#")
    if len(h) != 6:
        return None
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def consensus_backdrop(entries, tolerance=BACKDROP_TOLERANCE):
    """One surface colour for the set, when the frames genuinely agree."""
    cols = [_hex_rgb(e.get("backdrop")) for e in (entries or [])]
    cols = [c for c in cols if c]
    if not cols or len(cols) != len(entries or []):
        return None
    ref = cols[0]
    if any(max(abs(a - b) for a, b in zip(c, ref)) > tolerance for c in cols):
        return None
    mid = tuple(sorted(v[i] for v in cols)[len(cols) // 2] for i in range(3))
    return "#%02X%02X%02X" % mid


# ── Output ────────────────────────────────────────────────────────────────
def view_key(url, view_re):
    """Brand-specific view token, used only for ordering. Unknown -> 99."""
    if not view_re:
        return 99
    m = re.search(view_re, urllib.parse.unquote(url), re.I)
    return int(m.group(1)) if m else 99


def contact_sheet(entries, header, out_path):
    """A real sheet: every tile is a downloaded asset. No placeholders."""
    from PIL import ImageDraw, ImageFont
    FD = "/usr/share/fonts/truetype/dejavu/"
    B = lambda s: ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", s)
    R = lambda s: ImageFont.truetype(FD + "DejaVuSans.ttf", s)
    BG, INK, MUTE = (255, 252, 253), (24, 20, 22), (120, 112, 116)
    PINK, WARN, LINE = (233, 86, 150), (176, 104, 0), (226, 218, 222)

    CELL, PAD, CAP, COLS = 460, 30, 150, 2
    TW, TH = CELL + PAD * 2, CELL + CAP + PAD * 2
    HEAD, FOOT = 176, 96
    rows = (len(entries) + COLS - 1) // COLS
    W, H = TW * COLS, HEAD + TH * rows + FOOT
    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)

    def wrap(t, f, mw):
        out, cur = [], ""
        for w in t.split(" "):
            c = (cur + " " + w).strip()
            if d.textlength(c, font=f) <= mw:
                cur = c
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
        return out

    def block(x, y, t, f, fill, mw, lh):
        for ln in wrap(t, f, mw):
            d.text((x, y), ln, font=f, fill=fill)
            y += lh
        return y

    d.rectangle([0, 0, W, HEAD - 1], fill=(255, 240, 246))
    d.line([0, HEAD - 1, W, HEAD - 1], fill=PINK, width=3)
    # Shrink the title until it fits; SKUs and brand names vary in length.
    tf = B(38)
    while d.textlength(header["title"], font=tf) > W - PAD * 2 and tf.size > 20:
        tf = B(tf.size - 2)
    d.text((PAD, 26 + (38 - tf.size) // 2), header["title"], font=tf, fill=INK)
    d.text((PAD, 82), header["line2"], font=R(21), fill=INK)
    d.text((PAD, 114), header["line3"], font=R(19), fill=MUTE)

    for i, e in enumerate(entries):
        ox, oy = (i % COLS) * TW, HEAD + (i // COLS) * TH
        im = Image.open(e["_preview_path"]).convert("RGB")
        im.thumbnail((CELL, CELL), Image.LANCZOS)
        px, py = ox + PAD + (CELL - im.width) // 2, oy + PAD + (CELL - im.height) // 2
        if e["role"] == "MAIN":
            d.rectangle([ox + PAD - 8, oy + PAD - 8, ox + PAD + CELL + 7, oy + PAD + CELL + 7],
                        outline=PINK, width=5)
        else:
            d.rectangle([ox + PAD - 1, oy + PAD - 1, ox + PAD + CELL, oy + PAD + CELL],
                        outline=LINE, width=1)
        sheet.paste(im, (px, py))

        x, y = ox + PAD, oy + PAD + CELL + 14
        label = "IMAGE %02d" % e["index"]
        d.text((x, y), label, font=B(26), fill=INK)
        if e["role"] == "MAIN":
            bx = x + int(d.textlength(label, font=B(26))) + 14
            tw = d.textlength("PROPOSED MAIN", font=B(17))
            d.rectangle([bx, y + 2, bx + tw + 20, y + 28], fill=PINK)
            d.text((bx + 10, y + 6), "PROPOSED MAIN", font=B(17), fill=(255, 255, 255))
        y += 34
        y = block(x, y, "%d x %d  ·  %s  ·  %.0f KB" % (
            e["width"], e["height"], e["mime"].split("/")[-1].upper(), e["bytes"] / 1024),
            R(18), INK, CELL, 24)
        y = block(x, y, "Source: %s  ·  %s" % (e["source_domain"], e["discovery_method"]),
                  R(15), MUTE, CELL, 20)
        y = block(x, y, "sha256 %s…" % e["sha256"][:24], R(14), MUTE, CELL, 20)
        if e.get("warnings"):
            block(x, y, "⚠ " + "; ".join(e["warnings"]), R(15), WARN, CELL, 20)

    fy = H - FOOT
    d.line([0, fy, W, fy], fill=LINE, width=2)
    y = block(PAD, fy + 14, header["footer1"], R(17), INK, W - PAD * 2, 23)
    block(PAD, y + 2, header["footer2"], R(15), MUTE, W - PAD * 2, 21)
    sheet.save(out_path, "WEBP", quality=92, method=6)
    return sheet.size


def write_outputs(request, selected, all_acquired, log, outroot, ledger=None,
                  size_evidence=None, aliases=None):
    sku = request["manufacturerItemNo"].strip()
    brand = request["brand"].strip()
    rule = brand_rule(brand)
    base = os.path.join(outroot, sku)
    src_dir, prev_dir = os.path.join(base, "source"), os.path.join(base, "preview")
    # Wipe the previous run's artefacts. These directories are fully
    # regenerated, and leaving stragglers behind is genuinely dangerous: the
    # PGS30614 folder still held 1920x460 .webp banners from the very first
    # run, sitting next to the real .jpg product images under near-identical
    # names. Nothing referenced them, but that is one careless glob away from
    # publishing a marketing banner as product media.
    for d in (src_dir, prev_dir):
        if os.path.isdir(d):
            for f in os.listdir(d):
                fp = os.path.join(d, f)
                if os.path.isfile(fp):
                    os.remove(fp)
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(prev_dir, exist_ok=True)

    selected.sort(key=lambda m: (view_key(m["url"], rule.get("view_re")), -m["longest_edge"]))

    entries = []
    for i, m in enumerate(selected, 1):
        ext = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}[m["mime"]]
        # Filenames are derived from SKU and index only — never from the
        # remote URL — so a hostile path can never escape the output dir.
        sfile = "%s-%02d-original.%s" % (re.sub(r"[^A-Za-z0-9_-]", "", sku), i, ext)
        pfile = "%s-%02d.webp" % (re.sub(r"[^A-Za-z0-9_-]", "", sku), i)
        spath, ppath = os.path.join(src_dir, sfile), os.path.join(prev_dir, pfile)
        with open(spath, "wb") as fh:
            fh.write(m["_body"])
        prev = m["_img"].copy()
        prev.thumbnail((1600, 1600), Image.LANCZOS)
        prev.save(ppath, "WEBP", quality=90, method=6)

        warnings = []
        if m["longest_edge"] < PREFERRED_EDGE:
            warnings.append("%dpx longest edge — below the %dpx preference"
                            % (m["longest_edge"], PREFERRED_EDGE))
        elif m["longest_edge"] < IDEAL_EDGE:
            warnings.append("%dpx longest edge — usable, %dpx ideal"
                            % (m["longest_edge"], IDEAL_EDGE))
        if not m["sku_in_url"]:
            warnings.append("SKU not present in asset URL")
        warnings += m.get("notes", [])

        terms = re.findall(r"[A-Za-z]+", (request.get("variant") or "").lower())
        terms = [t for t in terms if t in COLOUR_TERMS]
        entries.append({
            "_colour_terms": colour_terms_present(m["_img"], terms) if terms else {},
            "index": i,
            "role": "MAIN" if i == 1 else "gallery",
            "file": os.path.relpath(spath, base),
            "preview": os.path.relpath(ppath, base),
            "_preview_path": ppath,
            "source_url": m["url"],
            "requested_url": m["requested_url"],
            "anchor_url": m.get("anchor_url"),
            "source_domain": urllib.parse.urlsplit(m["url"]).hostname,
            "discovery_method": m["discovery_method"],
            "acquired_at": m["acquired_at"],
            "width": m["width"], "height": m["height"],
            "longest_edge": m["longest_edge"],
            "mime": m["mime"], "bytes": m["bytes"],
            "sha256": m["sha256"], "dhash": m["dhash"],
            "sku_in_url": m["sku_in_url"],
            "sku_evidence": m.get("sku_evidence"),
            "source_page": m.get("source_page"),
            # m["_img"] is already flattened to RGB, so backdrop() cannot see
            # alpha by then. The cut-out flag is recorded at validation time,
            # while the original image still has its alpha channel.
            "backdrop": None if m.get("cutout") else backdrop(m["_img"]),
            "duplicates_collapsed": m.get("duplicates", []),
            "authorityTier": m.get("authorityTier"),
            "cutout": m.get("cutout", False),
            "validation": "PASS",
            "warnings": warnings,
        })

    vc = variant_confidence(entries, request.get("variant"),
                            request.get("officialAnchorDHashes"))
    for e in entries:
        e.pop("_colour_terms", None)

    audit = refusal_audit(ledger, aliases)

    status = "PASS" if len(entries) >= MIN_KEEP else ("PARTIAL" if entries else "BLOCKED")
    # A run must not report PASS while variant evidence conflicts.
    if status == "PASS" and vc["state"] == "VARIANT_EVIDENCE_CONFLICT":
        status = "VARIANT_EVIDENCE_CONFLICT"
    elif status == "PASS" and vc["state"] == "HUMAN_VARIANT_REVIEW_REQUIRED":
        status = "HUMAN_VARIANT_REVIEW_REQUIRED"

    # The refusal gate. BLOCKED is a claim that nothing could be established,
    # and it may not stand while an exact product document from an allowed
    # source is sitting in the ledger, or while a route that could have
    # answered was never tried. Media may still be missing — that is
    # MEDIA_NOT_ACQUIRED, a media outcome — but identity is not unresolved.
    if status == "BLOCKED" and not audit["refusalPermitted"]:
        if audit["exactProductDocuments"]:
            status = "MEDIA_NOT_ACQUIRED_IDENTITY_EVIDENCED"
        elif audit["routesUnreachable"]:
            status = "DISCOVERY_TRANSPORT_BLOCKED"
        else:
            status = "ROUTES_NOT_EXHAUSTED"
    sheet_rel = None
    if entries:
        sheet_path = os.path.join(base, "CONTACT_SHEET.webp")
        best = max(e["longest_edge"] for e in entries)
        contact_sheet(entries, {
            "title": "PINK MALL — %s %s — ACQUIRED MEDIA" % (brand.upper(), sku),
            "line2": "%s  /  %s  /  %s" % (brand, request.get("model", "—"), request.get("variant", "—")),
            "line3": "Automated acquisition · %d unique images · best %dpx · NOT PUBLISHED" % (len(entries), best),
            "footer1": "Every tile is a downloaded asset. No placeholders, no generative edits, "
                       "no upscaling — only the CDN's own larger copy of the same photograph.",
            "footer2": "Proposed MAIN is a filename-order heuristic. Visual confirmation by the "
                       "onboarding skill is still required before approval.",
        }, sheet_path)
        sheet_rel = "CONTACT_SHEET.webp"

    for e in entries:
        e.pop("_preview_path", None)

    manifest = {
        "schemaVersion": 1,
        "status": status,
        "sku": sku,
        "brand": brand,
        "model": request.get("model"),
        "variant": request.get("variant"),
        "officialProductPage": request.get("officialProductPage"),
        "generatedAt": now(),
        "generatedBy": "tools/media_acquisition/acquire.py",
        "runner": os.environ.get("GITHUB_RUN_ID") and {
            "githubRunId": os.environ.get("GITHUB_RUN_ID"),
            "githubRepository": os.environ.get("GITHUB_REPOSITORY"),
            "githubSha": os.environ.get("GITHUB_SHA"),
        } or {"local": True},
        "counts": {
            "acquired": len(all_acquired),
            "unique_selected": len(entries),
            "duplicates_collapsed": sum(len(e["duplicates_collapsed"]) for e in entries),
        },
        "variantConfidence": vc,
        # Which tier of the source hierarchy the published gallery came from.
        # Stated plainly so an approval package can never overclaim it.
        "mediaTier": (entries[0].get("authorityTier") if entries else None),
        "mediaTierMixed": len({e.get("authorityTier") for e in entries}) > 1 if entries else False,
        "proposedMain": entries[0]["file"] if entries else None,
        # Shared backdrop across the whole set, when the images agree. The
        # storefront uses it as media.surface so a contained image sits on a
        # matching field instead of a mismatched one.
        "dominantBackdrop": consensus_backdrop(entries),
        # A transparent set has no backdrop by construction; the storefront
        # should use its own field rather than a colour invented from a flatten.
        "cutoutSet": bool(entries) and all(e.get("cutout") for e in entries),
        "contactSheet": sheet_rel,
        "images": entries,
        "discoveryLedger": ledger or [],
        # What the sources themselves say this article is offered in. Never
        # PINK MALL availability — that is the user's alone — but it is how a
        # supplied size gets checked against the real scale instead of assumed.
        "sizeEvidence": size_evidence or [],
        # How the supplied sizes reconcile with any declared scale. Never a
        # gate on availability — the user owns that — only on how well the
        # labels are evidenced.
        "sizeState": size_state(request.get("availableSizes"), size_evidence),
        "identifierAliases": list(aliases or []),
        "researchEvidence": request.get("researchEvidence") or [],
        # Whether a refusal would even be honest. Consulted before any BLOCKED
        # or UNRESOLVED conclusion is allowed to stand.
        "refusalAudit": audit,
        "log": log,
        "notes": [
            "Media is acquired but NOT published. Live assets live under "
            "assets/pink-mall/products/<PM-ID>/ and only after explicit approval.",
            "Resolution upgrades rewrite only the CDN transform segment of the same "
            "asset URL and are accepted only if perceptually identical to the base image.",
            "Images are delivered at their native aspect ratio. The storefront owns "
            "card and PDP fitting via media.fit; no per-SKU canvas is manufactured here.",
        ],
    }
    with open(os.path.join(base, "result.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return manifest, base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request", required=True)
    ap.add_argument("--out", default="docs/pink-mall/media-acquisition")
    args = ap.parse_args()

    with open(args.request, encoding="utf-8") as fh:
        request = json.load(fh)
    for k in ("brand", "manufacturerItemNo"):
        if not request.get(k):
            print("request is missing %r" % k, file=sys.stderr)
            return 2

    log = []
    selected, all_acquired, ledger, size_evidence, aliases = acquire(request, args.out, log)
    manifest, base = write_outputs(request, selected or [], all_acquired or [],
                                   log, args.out, ledger, size_evidence, aliases)
    print(json.dumps({"status": manifest["status"], "sku": manifest["sku"],
                      "selected": manifest["counts"]["unique_selected"],
                      "acquired": manifest["counts"]["acquired"],
                      "out": base}, indent=2))
    return 0 if manifest["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
