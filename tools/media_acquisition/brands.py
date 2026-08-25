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

    "new balance": {
        "allowed_hosts": [
            "www.newbalance.co.uk", "newbalance.co.uk",
            "www.newbalance.eu", "newbalance.eu",
            "nl.newbalance.eu", "at.newbalance.eu", "de.newbalance.eu",
            "fr.newbalance.eu", "si.newbalance.eu", "ie.newbalance.eu",
            "www.newbalance.com", "newbalance.com",
            "nb.scene7.com",
        ],
        "page_templates": [
            "https://www.newbalance.co.uk/search?q={sku}",
            "https://www.newbalance.eu/search?q={sku}",
            "https://www.newbalance.com/search?q={sku}",
        ],
        "cdn_hosts": ["nb.scene7.com"],
        # New Balance publishes on Scene7 under the style code itself. These are
        # probes, not assertions: a probe only becomes a candidate if it
        # downloads, decodes, and carries the exact SKU in its own path — and a
        # human still confirms the variant visually on the contact sheet.
        "cdn_probe": [
            "https://nb.scene7.com/is/image/NB/{sku_lower}_nb_{view}_i?$pdpflexf2$&wid=1600&hei=1600",
        ],
        "cdn_probe_views": ["02", "03", "04", "05", "06", "07", "08"],
        "width_ladder": [1600, 1200, 1000],
        "sku_in_url": True,
        "view_re": r"_nb_(\d{2})_i",
    },
}

DEFAULT = {
    "allowed_hosts": [],
    "page_templates": [],
    "cdn_hosts": [],
    "width_ladder": [1880, 1600, 1200, 1000],
    "sku_in_url": True,
    "view_re": None,
    "cdn_probe": [],
    "cdn_probe_views": [],
}


def brand_rule(brand):
    return BRANDS.get((brand or "").strip().lower(), DEFAULT)
