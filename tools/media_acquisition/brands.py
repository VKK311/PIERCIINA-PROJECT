"""Brand registry for PINK MALL media acquisition.

Each entry describes how to reach one manufacturer's official media, and how
to ask its CDN for a larger copy of the *same* asset. Nothing here decides
whether an image is the right product — that is the validator's job.

Adding a brand means adding one dict. No other file changes.
"""

BRANDS = {
    "adidas": {
        # Hosts the fetcher may talk to for this brand. Everything else is
        # refused before a socket is opened.
        "allowed_hosts": [
            "assets.adidas.com",
            "www.adidas.de", "adidas.de",
            "www.adidas.com", "adidas.com",
            "www.adidas.co.uk", "www.adidas.fr", "www.adidas.it",
            "www.adidas.es", "www.adidas.nl", "www.adidas.pl",
        ],
        # Product pages to try, in source-hierarchy order. {sku} is filled in.
        "page_templates": [
            "https://www.adidas.de/en/{sku}.html",
            "https://www.adidas.com/us/{sku}.html",
            "https://www.adidas.co.uk/{sku}.html",
        ],
        # adidas serves Cloudinary-style transform segments:
        #   /images/w_500,f_auto,q_auto/<hash>/<Name>_<SKU>_..._standard.jpg
        # The same asset is available at larger widths. We only ever rewrite
        # the transform segment, never the asset path, so the bytes we get
        # back are the same photograph at a different size.
        "cdn_hosts": ["assets.adidas.com"],
        "width_ladder": [1880, 1200, 1000, 840, 600],
        # The SKU normally appears in the asset filename. Used as one identity
        # signal among several, never on its own.
        "sku_in_url": True,
        # adidas encodes the view in the filename: _01_00_standard is the
        # lateral catalogue shot, then _02_, _03_, _04_. Used only to ORDER
        # candidates and propose a MAIN; a human still confirms visually.
        "view_re": r"_(\d{2})(?:_\d{2})?_standard",
    },
}

DEFAULT = {
    "allowed_hosts": [],
    "page_templates": [],
    "cdn_hosts": [],
    "width_ladder": [1880, 1600, 1200, 1000],
    "sku_in_url": True,
    "view_re": None,
}


def brand_rule(brand):
    return BRANDS.get((brand or "").strip().lower(), DEFAULT)
