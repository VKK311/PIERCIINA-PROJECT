"""Brand registry for PINK MALL media acquisition.

Each entry describes how to reach one manufacturer's official media, and how
to ask its CDN for a larger copy of the *same* asset. Nothing here decides
whether an image is the right product — that is the validator's job.

Adding a brand means adding one dict. No other file changes.
"""

BRANDS = {
    "adidas": {
        # Manufacturer authority. Separate from allowed_hosts, which only
        # answers whether the fetcher may connect.
        "official_hosts": ["assets.adidas.com", "adidas.com", "adidas.de", "adidas.co.uk", "adidas.fr", "adidas.it", "adidas.es", "adidas.nl", "adidas.pl"],
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
            # Product API first: it returns the same asset URLs as the page and
            # is usually less aggressively protected than the rendered HTML.
            "https://www.adidas.com/api/products/{sku}",
            "https://www.adidas.de/api/products/{sku}",
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
        # Manufacturer authority. Separate from allowed_hosts, which only
        # answers whether the fetcher may connect.
        # nb.scene7.com is New Balance's own Scene7 tenancy — evidenced,
        # not assumed from the hostname.
        "official_hosts": ["newbalance.co.uk", "newbalance.eu", "newbalance.com", "nb.scene7.com"],
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

    "converse": {
        # Manufacturer authority. Separate from allowed_hosts, which only
        # answers whether the fetcher may connect.
        "official_hosts": ["converse.com", "converse.scene7.com"],
        "allowed_hosts": [
            "www.converse.com", "converse.com",
            "converse.scene7.com",
        ],
        "page_templates": [
            "https://www.converse.com/search?q={sku}",
            "https://www.converse.com/uk/en/search?q={sku}",
            "https://www.converse.com/nl/en/search?q={sku}",
            "https://www.converse.com/api/products/{sku}",
        ],
        "cdn_hosts": ["www.converse.com", "converse.scene7.com"],
        # No CDN probe. Converse image paths embed a per-product colour-code
        # folder that cannot be derived from the SKU, and guessing one would be
        # fabricating a path rather than discovering an asset.
        "cdn_probe": [],
        "cdn_probe_views": [],
        "width_ladder": [1600, 1200, 1000],
        "sku_in_url": True,
        "view_re": None,
    },

    "puma": {
        # Manufacturer authority. Separate from allowed_hosts, which only
        # answers whether the fetcher may connect.
        # images.puma.com is Puma's own Cloudinary delivery host.
        "official_hosts": ["puma.com", "images.puma.com"],
        "allowed_hosts": [
            "images.puma.com", "puma.com", "www.puma.com",
            "eu.puma.com", "us.puma.com", "de.puma.com", "fr.puma.com",
            "it.puma.com", "es.puma.com", "nl.puma.com", "pl.puma.com",
        ],
        "page_templates": [
            "https://eu.puma.com/eu/en/pd/{sku}",
            "https://us.puma.com/us/en/pd/{sku}",
        ],
        "cdn_hosts": ["images.puma.com"],
        # Puma publishes on Cloudinary under the article number and colour
        # code. These are PROBES, not assertions: a probe only becomes a
        # candidate if it downloads, decodes, and carries the exact article
        # number in its own path — so a wrong template costs a 404 and proves
        # nothing, while a right one is self-evidencing. The colour code is
        # supplied per request because it is the variant, and substituting a
        # neighbouring colourway is the one thing the exact-variant rule
        # exists to prevent.
        "cdn_probe": [],
        "cdn_probe_views": [],
        "width_ladder": [2000, 1600, 1200, 1000],
        "sku_in_url": True,
        "view_re": r"/sv(\d{2})/",
    },

    "pepe jeans": {
        # Manufacturer authority. Separate from allowed_hosts, which only
        # answers whether the fetcher may connect.
        "official_hosts": ["pepejeans.com"],
        "allowed_hosts": [
            "www.pepejeans.com", "pepejeans.com",
        ],
        # No page templates. Pepe Jeans product URLs are
        # /<locale>/<localised-slug>-<SKU><COLOUR>.html — the slug is written
        # per locale and cannot be derived from the style code, and their
        # search path is not known to us. Guessing either would be inventing a
        # URL rather than discovering one, so entry points come from the
        # request manifest, found by search used as a transport.
        "page_templates": [],
        # Left empty deliberately: the media host for this brand has not been
        # observed yet. It is filled in from a run's own rejection log, never
        # from a guess. (The A08745C run is the recorded reason for this rule.)
        "cdn_hosts": [],
        "cdn_probe": [],
        "cdn_probe_views": [],
        "width_ladder": [1600, 1200, 1000, 800],
        # The style code appears in the product URL; whether it reaches the
        # asset path is what the run tells us.
        "sku_in_url": True,
        "view_re": None,
    },

    "scotch & soda": {
        # Manufacturer authority. Separate from allowed_hosts, which only
        # answers whether the fetcher may connect.
        # cdn.shopify.com is deliberately ABSENT: it is a shared platform
        # host serving every Shopify merchant, so it carries no authority.
        "official_hosts": ["scotch-soda.eu", "scotchandsoda.com", "scotch-soda.com"],
        "allowed_hosts": [
            "scotch-soda.eu", "www.scotch-soda.eu",
            "scotchandsoda.com", "www.scotchandsoda.com",
            "scotch-soda.com", "www.scotch-soda.com",
            "cdn.shopify.com",
            # Trusted-retailer fallback: the MODIVO S.A. / eobuwie group.
            # The 8-digit article number the user works from is THIS GROUP'S
            # numbering, not Shopify's — the brand's own store indexes
            # 78-XXXX-XX style codes and its search returns nothing for the
            # 8-digit form. These are the group's country domains, which share
            # one catalogue and one URL grammar.
            "www.obuvki.bg", "obuvki.bg",
            "www.efootwear.eu", "efootwear.eu",
            "www.eskor.se", "eskor.se",
            "www.eobuwie.pl", "eobuwie.pl",
            "www.modivo.bg", "modivo.bg",
            # Added because the USER supplied an eMAG product URL for this
            # exact article after every MODIVO route 404'd the runner. eMAG is
            # the largest established e-commerce retailer in BG/RO and is the
            # user's own supplier here; it is not treated as an official
            # manufacturer source.
            "www.emag.bg", "emag.bg",
        ],
        # Scotch & Soda runs on Shopify, whose /search?q= route is part of the
        # platform rather than a URL we invented. Everything else comes from
        # the request manifest.
        "page_templates": [
            # Retailer search first: the article number is the retailer's own.
            # A search route yields LINK TARGETS, which is its whole value —
            # since the search-route fix it lends no identity to its own
            # images, so a fuzzy match costs nothing.
            "https://www.obuvki.bg/search?q={sku}",
            "https://www.efootwear.eu/search?q={sku}",
            "https://scotch-soda.eu/search?q={sku}",
            "https://scotchandsoda.com/search?q={sku}",
        ],
        # Left empty deliberately, on the Pepe Jeans precedent: the media host
        # for this brand has not been observed yet, and it is filled in from a
        # run's own rejection log rather than from a guess about Shopify.
        "cdn_hosts": [],
        # No probe. Shopify asset filenames are whatever the merchant uploaded;
        # they cannot be derived from the article number, and constructing one
        # would be fabricating a path rather than discovering an asset.
        "cdn_probe": [],
        "cdn_probe_views": [],
        "width_ladder": [2000, 1600, 1200, 1000],
        "sku_in_url": True,
        "view_re": None,
    },

    "stella mccartney": {
        # Manufacturer authority. Separate from allowed_hosts, which only
        # answers whether the fetcher may connect.
        # Everything else in allowed_hosts for this brand — Giglio,
        # Smallable, Farfetch, italist, Childrensalon — is a retailer we may
        # CONNECT to, not a manufacturer.
        "official_hosts": ["stellamccartney.com"],
        "allowed_hosts": [
            "www.stellamccartney.com", "stellamccartney.com",
            # Established kidswear/luxury retailers that index the WHOLESALE
            # style code. The brand's own site indexes K-codes such as
            # K03231PK02407203 instead, so these are the only observed route
            # from TU0A28Z0699 to a product document.
            "www.littletagsluxury.com", "littletagsluxury.com",
            "www.smallable.com", "smallable.com",
            "kids21.com", "www.kids21.com",
            "www.childrensalon.com", "childrensalon.com",
            "modesens.com", "www.modesens.com",
            # OBSERVED in pass 1's own rejection log, not guessed: Smallable
            # serves product media from these two hosts.
            "media.smallable.com", "staticv3.smallable.com",
            "cdn.modesens.com",
            # Aggregators of Italian boutiques that publish the manufacturer
            # style code on the product page, which the pure e-tailers above
            # do not. Used for IDENTITY; their media tier is recorded honestly.
            "www.italist.com", "italist.com",
            "www.farfetch.com", "farfetch.com",
            "cdn-images.farfetch-contents.com",
            # Giglio, an established Italian retailer (Palermo, 1996) that
            # publishes the DESIGNER code alongside its own product code.
            # img.giglio.com is its image CDN — reviewer-observed and
            # independently confirmed, not guessed.
            "www.giglio.com", "giglio.com", "img.giglio.com",
        ],
        # Search is a platform route and yields link targets only; since the
        # search-route fix it lends no identity to its own images.
        "page_templates": [
            "https://www.stellamccartney.com/us/en/search?q={sku}",
        ],
        # Left empty deliberately, on the Pepe Jeans precedent: this brand's
        # media host has not been observed yet and is filled in from a run's
        # own rejection log, never guessed.
        "cdn_hosts": [],
        "cdn_probe": [],
        "cdn_probe_views": [],
        "width_ladder": [2000, 1600, 1200, 1000],
        "sku_in_url": True,
        "view_re": None,
    },
}

DEFAULT = {
    "allowed_hosts": [],
    # No brand is official by default. An allowed host is a host we may talk
    # to, never a claim about who owns it.
    "official_hosts": [],
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
