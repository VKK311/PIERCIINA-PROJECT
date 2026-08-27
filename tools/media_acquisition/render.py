"""Bounded JavaScript rendering for client-side product pages.

Some storefronts serve a small bootstrap shell and assemble the real document —
gallery included — in the browser. Giglio returned ~2.4 kB for a page that
genuinely named the article in its body and exposed no image reference in any
form. An HTTP-only fetcher cannot see that gallery. That is a capability limit,
not evidence of absence.

This module is NOT a crawler and NOT a search engine. It renders ONE already
evidenced product URL and reports the image URLs that page exposes. It approves
nothing: every URL it returns goes through the same acquisition and identity
validation as any other candidate.

The caller decides whether rendering is allowed. See should_render().
"""

import os
import re
import time
import urllib.parse

# Bounds. A render that has not produced a gallery inside these is a transport
# failure, reported as such, and never read as evidence of absence.
NAV_TIMEOUT_S = 20
HYDRATE_TIMEOUT_S = 12
TOTAL_TIMEOUT_S = 45
MAX_IMAGE_URLS = 400

IMAGE_EXT_RE = re.compile(r"\.(?:jpg|jpeg|png|webp|avif)(?:\?|$)", re.I)

# Rendering is only ever pointed at a page the pipeline already vetted.
RENDERABLE_TIERS = {"OFFICIAL", "TRUSTED_RETAILER"}


def should_render(*, authority_tier, http_ok, sku_where, media_found,
                  shell_suspected, host_allowed):
    """Every condition must hold. Any one false means do not render.

    The important exclusion: a page whose only SKU match is in the URL WE
    requested has not identified itself, so rendering an arbitrary search
    result because the article appears in its query string is refused here.
    """
    return bool(
        host_allowed
        and http_ok
        and (authority_tier in RENDERABLE_TIERS)
        and (sku_where in ("body", "body-only"))
        and not media_found
        and shell_suspected
    )


def _chromium_path():
    for env in ("PM_CHROMIUM", "PLAYWRIGHT_CHROMIUM"):
        p = os.environ.get(env)
        if p and os.path.exists(p):
            return p
    for p in ("/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
              "/opt/pw-browsers/chromium/chrome-linux/chrome"):
        if os.path.exists(p):
            return p
    return None


def render_page(url, log=None, nav_timeout=NAV_TIMEOUT_S,
                hydrate_timeout=HYDRATE_TIMEOUT_S,
                total_timeout=TOTAL_TIMEOUT_S):
    """Render one URL. Returns (image_urls, rendered_html, error).

    error is non-None only for TRANSPORT failures — no browser, navigation
    timeout, crash. An empty gallery from a page that rendered fine is not an
    error; it is an answer.
    """
    log = log if log is not None else []
    started = time.time()
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:                              # noqa: BLE001
        return [], "", "playwright unavailable: %s" % exc

    exe = _chromium_path()
    origin_host = urllib.parse.urlsplit(url).netloc.lower()
    seen, html = [], ""

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=True,
                executable_path=exe or None,
                args=["--disable-dev-shm-usage", "--no-sandbox"])
            ctx = browser.new_context(
                viewport={"width": 1400, "height": 1600},
                accept_downloads=False,                   # no downloads
                java_script_enabled=True)
            ctx.set_default_timeout(nav_timeout * 1000)
            page = ctx.new_page()

            # No popups or new-window traversal: close anything that opens.
            page.on("popup", lambda p: p.close())

            # Never leave the page we were told to render. Sub-resources load
            # normally — that is how the gallery appears, and how we observe
            # the CDN host — but a main-frame navigation to another origin is
            # crawling, which this is not.
            def _guard(route, request):
                try:
                    if request.is_navigation_request() and request.frame == page.main_frame:
                        h = urllib.parse.urlsplit(request.url).netloc.lower()
                        if h and h != origin_host and request.url != url:
                            return route.abort()
                except Exception:                          # noqa: BLE001
                    pass
                return route.continue_()
            page.route("**/*", _guard)

            # Image URLs the product page actually requested.
            def _on_response(resp):
                try:
                    ct = (resp.headers or {}).get("content-type", "")
                    if ct.lower().startswith("image/") and len(seen) < MAX_IMAGE_URLS:
                        if resp.url not in seen:
                            seen.append(resp.url)
                except Exception:                          # noqa: BLE001
                    pass
            page.on("response", _on_response)

            page.goto(url, wait_until="domcontentloaded",
                      timeout=nav_timeout * 1000)
            # Wait only long enough for the application to hydrate.
            try:
                page.wait_for_load_state("networkidle",
                                         timeout=hydrate_timeout * 1000)
            except Exception:                              # noqa: BLE001
                pass                                       # hydration is best-effort
            if time.time() - started > total_timeout:
                raise TimeoutError("render exceeded %ss" % total_timeout)

            html = page.content()
            # Whatever the rendered DOM declares, including lazy attributes.
            dom_urls = page.eval_on_selector_all(
                "img, source",
                """els => els.flatMap(e => [
                     e.currentSrc, e.src, e.getAttribute('src'),
                     e.getAttribute('data-src'), e.getAttribute('data-original'),
                     e.getAttribute('data-zoom-image'), e.getAttribute('srcset'),
                     e.getAttribute('data-srcset')
                   ]).filter(Boolean)""") or []
            for raw in dom_urls:
                for part in str(raw).split(","):
                    u = part.strip().split(" ")[0]
                    if not u:
                        continue
                    u = urllib.parse.urljoin(url, u)
                    if u.lower().startswith(("http://", "https://")) \
                       and IMAGE_EXT_RE.search(u) and u not in seen \
                       and len(seen) < MAX_IMAGE_URLS:
                        seen.append(u)
            ctx.close()
            browser.close()
    except Exception as exc:                               # noqa: BLE001
        log.append({"stage": "js-render", "url": url, "ok": False,
                    "error": "%s: %s" % (type(exc).__name__, str(exc)[:160])})
        return [], html, "%s: %s" % (type(exc).__name__, str(exc)[:160])

    log.append({"stage": "js-render", "url": url, "ok": True,
                "images": len(seen), "html_bytes": len(html or ""),
                "elapsed_s": round(time.time() - started, 1)})
    return seen, html, None
