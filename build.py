#!/usr/bin/env python3
"""Static site generator for landlordsafetyfirst.uk.

    python3 build.py               # build to dist/, list TODOs
    python3 build.py --production  # refuse to build while TODOs remain

No dependencies. Edit site.config.json for business facts and prices, content.py / content_more.py for page copy.
"""
import html, json, math, re, shutil, sys
from pathlib import Path
from urllib.parse import quote as urlquote

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
CFG = json.loads((ROOT / "site.config.json").read_text())
TODOS = set()

# ------------------------------------------------------------------ helpers
def is_todo(v):
    return isinstance(v, str) and v.startswith("TODO")

def t(key):
    """Config value for HTML. TODO values render highlighted so they can't slip through unseen."""
    v = CFG[key]
    if is_todo(v):
        TODOS.add(f"{key}: {v[5:].strip()}")
        return f'<span class="todo">{html.escape(v[5:].strip())}</span>'
    return html.escape(str(v))

def plain(key, fallback=""):
    """Config value for meta/schema/plain text. TODO → fallback."""
    v = CFG[key]
    if is_todo(v):
        TODOS.add(f"{key}: {v[5:].strip()}")
    return fallback if is_todo(v) or v in ("", None) else str(v)

def todo(text):
    """An inline TODO note written in page copy."""
    TODOS.add(f"content: {text}")
    return f'<span class="todo">{html.escape(text)}</span>'

def money(n):
    return f"£{n:,.0f}" if float(n).is_integer() else f"£{n:,.2f}"

def with_vat(ex):
    return round(ex * (1 + CFG["vat_rate"]))

def inc(key):
    return with_vat(CFG["prices"][key]["ex"])

def price(key, from_=True):
    p = CFG["prices"][key]
    f = '<span class="from">from</span>' if from_ else ""
    return f'<span class="price">{f}<span class="amt">{money(inc(key))}</span><span class="ex">{money(p["ex"])} + VAT</span></span>'

def price_txt(key):
    """Inline text form: '£180 inc. VAT'."""
    return f"{money(inc(key))} inc. VAT"

def esc(s):
    return html.escape(s, quote=True)

def phone_href():
    return f"tel:{CFG['phone_e164']}" if CFG["phone_e164"] else "/contact/#quote"

def wa_href(text="Hi, I'm a landlord and I'd like a price for my property."):
    if not CFG["whatsapp_e164"]:
        return "/contact/#quote"
    return f"https://wa.me/{CFG['whatsapp_e164'].lstrip('+')}?text={urlquote(text)}"

MIN_EX = CFG["picker"]["minimum_ex"]
MIN_TXT = f"{money(with_vat(MIN_EX))} inc. VAT"

# ------------------------------------------------------------------ icons (Lucide-style, MIT)
_P = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "check": '<path d="M4 12.5l5 5L20 6.5"/>',
    "check-circle": '<circle cx="12" cy="12" r="10"/><path d="m8 12.5 2.8 2.8L16.5 9.5"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4.1 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/>',
    "bulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6M10 22h4"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.7 9a1 1 0 0 1-.6 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.2-2.7a1.2 1.2 0 0 1 1.6 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6C9.5 14.5 12 13 13 12"/>',
    "plug": '<path d="M12 22v-5M9 8V2M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9l-3.8 3.8z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    "box": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18M10 12v2h4v-2"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-9 5.7a2 2 0 0 1-2 0L2 7"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m9 15 2 2 4-4"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "alert": '<path d="m21.7 18-8-14a2 2 0 0 0-3.5 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3"/><path d="M12 9v4M12 17h.01"/>',
    "star": '<path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    "home": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .7-1.5l7-6a2 2 0 0 1 2.6 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "pound": '<path d="M18 7c0-5.3-8-5.3-8 0v10M6 13h8M6 21h12"/>',
    "bolt-file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m12.5 11-2.5 4h4l-2.5 4"/>',
}
_WA = '<path fill="currentColor" stroke="none" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.3-.4.8-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1 2.7.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/>'

def icon(name, cls="ic"):
    body = _WA if name == "wa" else _P[name]
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'

ICON = {k: icon(k) for k in ("phone", "check", "wa")}

LOGO = ('<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true">'
        '<rect width="32" height="32" rx="8" fill="#0B2A21"/>'
        '<path d="M16 5.5 24.5 8.6v6.1c0 5.3-3.6 9.2-8.5 11.6-4.9-2.4-8.5-6.3-8.5-11.6V8.6Z" fill="#F5A524"/>'
        '<path d="m11.9 15.6 2.9 2.9 5.4-5.9" fill="none" stroke="#0B2A21" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
        '</svg>')

def btn(href, label, cls="btn-primary", ic=None, extra=""):
    i = icon(ic) if ic else ""
    return f'<a class="btn {cls}" href="{esc(href)}"{extra}>{i}<span>{label}</span></a>'

def call_btn(cls="btn-ghost", label=None):
    lbl = label or (f"Call {esc(CFG['phone_display'])}" if not is_todo(CFG["phone_display"]) else "Call us")
    return btn(phone_href(), lbl, cls, "phone")

def wa_btn(cls="btn-ghost", text=None, label="WhatsApp us"):
    h = wa_href(text) if text else wa_href()
    extra = ' rel="noopener"' if h.startswith("http") else ""
    return btn(h, label, cls, "wa", extra)

def book_btn(cls="btn-primary", label="Book now", href="/book/"):
    return btn(href, label, cls, "calendar")

def quote_btn(cls="btn-ghost", label="Get a quote"):
    return btn("#quote", label, cls)

# ------------------------------------------------------------------ pricing (mirrors main.js)
def _res(v):
    return CFG["prices"][v]["ex"] if isinstance(v, str) else v

PICK = {}
for it in CFG["picker"]["items"]:
    r = {"id": it["id"], "label": it["label"], "cert": bool(it.get("cert"))}
    base = it["base"]
    r["base"] = {k: _res(base if isinstance(base, (str, int, float)) else base[k]) for k in ("flat", "house", "hmo")}
    r["incl"] = {k: (it.get("incl_beds") or {}).get(k, 99) for k in ("flat", "house", "hmo")}
    r["per"] = {k: _res((it.get("per_bed") or {}).get(k, 0)) for k in ("flat", "house", "hmo")}
    PICK[it["id"]] = r

def round_to(x):
    n = CFG["picker"]["round_to"]
    return math.floor(x / n + 0.5) * n

def quote_calc(ptype, beds, ids):
    lines, certs, addons = [], 0, 0
    for i in ids:
        it = PICK[i]
        ex = it["base"][ptype] + max(0, beds - it["incl"][ptype]) * it["per"][ptype]
        lines.append((it["label"], ex))
        if it["cert"]: certs += ex
        else: addons += ex
    n = sum(1 for i in ids if PICK[i]["cert"])
    rate = 0
    for k, r in CFG["picker"]["tiers"]:
        if n >= k: rate = r
    sub = certs + addons
    total = round_to(certs * (1 - rate) + addons) if rate else sub
    floored = total < MIN_EX
    total = max(total, MIN_EX)
    return {"lines": lines, "subtotal": sub, "saving": max(0, sub - total) if not floored else 0, "rate": rate,
            "total_ex": total, "total_inc": with_vat(total), "floored": floored}

def book_href(ptype, beds, ids):
    return f"/book/?type={ptype}&beds={beds}&items={','.join(ids)}"

def picker_js():
    return {"items": list(PICK.values()), "min": MIN_EX, "round": CFG["picker"]["round_to"], "tiers": CFG["picker"]["tiers"], "vat": CFG["vat_rate"]}

# ------------------------------------------------------------------ geography
BASE = CFG["base"]
def miles(lat, lng):
    dx = (lng - BASE["lng"]) * math.cos(math.radians(BASE["lat"])) * 69.17
    dy = (lat - BASE["lat"]) * 69.17
    return math.hypot(dx, dy)

TOWNS = [  # name, lat, lng, slug-or-None (only boroughs with their own page get a slug)
    ("Stratford", 51.5413, -0.0033, "newham"), ("Hackney", 51.5450, -0.0553, "hackney"),
    ("Bow", 51.5290, -0.0200, "tower-hamlets"), ("Canary Wharf", 51.5054, -0.0235, "tower-hamlets"),
    ("Islington", 51.5362, -0.1033, None), ("Camden", 51.5390, -0.1426, None),
    ("Westminster", 51.4975, -0.1357, None), ("Walthamstow", 51.5830, -0.0200, None),
    ("Ilford", 51.5590, 0.0741, None), ("Barking", 51.5362, 0.0798, None),
    ("Romford", 51.5768, 0.1801, None), ("Enfield", 51.6523, -0.0807, None),
    ("Greenwich", 51.4826, 0.0077, None), ("Lewisham", 51.4452, -0.0209, None),
    ("Bromley", 51.4060, 0.0136, None), ("Croydon", 51.3762, -0.0982, None),
    ("Wembley", 51.5560, -0.2796, None), ("Ealing", 51.5130, -0.3089, None),
    ("Richmond", 51.4613, -0.3037, None), ("Kingston", 51.4123, -0.3007, None),
    ("Watford", 51.6565, -0.3903, None), ("St Albans", 51.7520, -0.3360, None),
    ("Hertford", 51.7959, -0.0778, None), ("Harlow", 51.7730, 0.1023, None),
    ("Epping", 51.6995, 0.1110, None), ("Brentwood", 51.6214, 0.3050, None),
    ("Basildon", 51.5761, 0.4887, None), ("Grays", 51.4785, 0.3230, None),
    ("Dartford", 51.4462, 0.2169, None), ("Gravesend", 51.4416, 0.3707, None),
    ("Sevenoaks", 51.2724, 0.1909, None), ("Epsom", 51.3360, -0.2670, None),
    ("Heathrow", 51.4700, -0.4543, None), ("Slough", 51.5105, -0.5950, None),
]
TOWNS = [x for x in TOWNS if miles(x[1], x[2]) <= BASE["radius_miles"]]

THAMES = [(51.43,-0.51),(51.41,-0.37),(51.41,-0.31),(51.46,-0.30),(51.467,-0.215),(51.48,-0.16),
          (51.50,-0.123),(51.507,-0.088),(51.504,-0.06),(51.50,-0.035),(51.488,-0.012),(51.50,0.005),
          (51.497,0.03),(51.495,0.07),(51.505,0.12),(51.48,0.18),(51.465,0.26),(51.47,0.32),
          (51.445,0.37),(51.47,0.45),(51.50,0.55)]

def map_svg(highlight=None):
    W, R = 460, 190
    c = W / 2
    s = R / BASE["radius_miles"]
    def xy(lat, lng):
        dx = (lng - BASE["lng"]) * math.cos(math.radians(BASE["lat"])) * 69.17
        dy = (lat - BASE["lat"]) * 69.17
        return c + dx * s, c - dy * s
    river = " ".join(f"{x:.1f},{y:.1f}" for x, y in (xy(a, b) for a, b in THAMES))
    r10 = 10 * s
    parts = [f'<svg class="map-svg" viewBox="0 0 {W} {W}" role="img" aria-labelledby="map-t map-d">',
             f'<title id="map-t">Area covered: {BASE["radius_miles"]} miles from {BASE["area_name"]}</title>',
             f'<desc id="map-d">A circle centred on {BASE["area_name"]}, East London, reaching {", ".join(n for n,*_ in TOWNS[-8:])} and everywhere in between.</desc>',
             '<defs><clipPath id="mc"><circle cx="%s" cy="%s" r="%s"/></clipPath></defs>' % (c, c, R + 20),
             f'<circle cx="{c}" cy="{c}" r="{R}" fill="#FFFFFF" stroke="#F5A524" stroke-opacity=".55" stroke-width="9"/>',
             f'<circle cx="{c}" cy="{c}" r="{R}" fill="none" stroke="#0B2A21" stroke-width="1.25"/>',
             f'<circle cx="{c}" cy="{c}" r="{r10:.1f}" fill="#EEF4F0" stroke="#0B2A21" stroke-width=".75" stroke-dasharray="3 3"/>',
             f'<polyline clip-path="url(#mc)" points="{river}" fill="none" stroke="#BCD3C6" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>']
    taken = [(c + 8, c - 24, c + 8 + 7.6 * len(BASE["area_name"]), c - 6),
             (c + R * 0.62 - 2, c + R * 0.86 - 12, c + R * 0.62 + 52, c + R * 0.86 + 3)]
    def free(box):
        x1, y1, x2, y2 = box
        return 6 < x1 and x2 < W - 6 and all(x2 < a or x1 > c2 or y2 < b_ or y1 > d for a, b_, c2, d in taken)
    for name, lat, lng, slug in sorted(TOWNS, key=lambda z: -miles(z[1], z[2])):
        x, y = xy(lat, lng)
        hl = highlight and slug == highlight
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4 if hl else 2.6}" fill="{"#0B2A21" if hl else "#5E7268"}"/>')
        w = 6.0 * len(name) + 2
        for anchor, box in (("start", (x + 5, y - 7, x + 6 + w, y + 6)), ("end", (x - 6 - w, y - 7, x - 5, y + 6)),
                            ("middle", (x - w / 2, y - 19, x + w / 2, y - 6))):
            if free(box):
                taken.append(box)
                tx = {"start": x + 6, "end": x - 6, "middle": x}[anchor]
                ty = y - 9 if anchor == "middle" else y + 4
                parts.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}"{" class=\"base-label\"" if hl else ""}>{esc(name)}</text>')
                break
    parts.append(f'<circle cx="{c}" cy="{c}" r="6" fill="#0B2A21" stroke="#FFFFFF" stroke-width="2"/>'
                 f'<text class="base-label" x="{c+11}" y="{c-9}">{esc(BASE["area_name"])} (E1)</text>'
                 f'<text x="{c+R*0.62:.0f}" y="{c+R*0.86:.0f}">{BASE["radius_miles"]} miles</text></svg>')
    return "".join(parts)

# ------------------------------------------------------------------ schema
SITE = CFG["site_url"].rstrip("/")
BIZ_ID = f"{SITE}/#business"

def business_schema():
    days = [{"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"], "opens": h["opens"], "closes": h["closes"]} for h in CFG["hours"]]
    offers = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": p["label"]},
               "priceSpecification": {"@type": "PriceSpecification", "minPrice": inc(k), "priceCurrency": "GBP", "valueAddedTaxIncluded": True}}
              for k, p in CFG["prices"].items()]
    b = {
        "@type": "Electrician", "@id": BIZ_ID, "name": CFG["business_name"], "url": SITE + "/",
        "description": f"Landlord safety certificates in East London: EICRs, gas safety certificates, fire alarm and emergency lighting tests, EPCs and remedial work, carried out by a qualified electrician and Gas Safe engineer, within {BASE['radius_miles']} miles of Whitechapel.",
        "logo": f"{SITE}/logo.png", "image": f"{SITE}/og.png", "priceRange": "££",
        "email": CFG["email"],
        "address": {"@type": "PostalAddress", "addressLocality": BASE["locality"], "postalCode": BASE["postcode_area"], "addressRegion": "Greater London", "addressCountry": "GB"},
        "geo": {"@type": "GeoCoordinates", "latitude": BASE["lat"], "longitude": BASE["lng"]},
        "areaServed": [{"@type": "GeoCircle", "geoMidpoint": {"@type": "GeoCoordinates", "latitude": BASE["lat"], "longitude": BASE["lng"]}, "geoRadius": round(BASE["radius_miles"] * 1609.34)}]
                      + [{"@type": "Place", "name": n} for n, *_ in TOWNS],
        "openingHoursSpecification": days,
        "knowsAbout": ["EICR", "Electrical Safety Standards in the Private Rented Sector (England) Regulations 2020", "BS 7671",
                       "Landlord gas safety record (CP12)", "Gas Safety (Installation and Use) Regulations 1998",
                       "Smoke and Carbon Monoxide Alarm (Amendment) Regulations 2022", "Fire alarm testing BS 5839-6",
                       "Emergency lighting BS 5266", "Energy Performance Certificates", "PAT testing", "Consumer unit replacement"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Landlord safety certificates and electrical work", "itemListElement": offers},
    }
    if CFG["phone_e164"]: b["telephone"] = CFG["phone_e164"]
    same = [u for u in CFG["same_as"] + [CFG["google_business_profile_url"]] if u]
    if same: b["sameAs"] = same
    cred = []
    if not is_todo(CFG["gas_safe_number"]): cred.append({"@type": "EducationalOccupationalCredential", "name": f"Gas Safe Register no. {CFG['gas_safe_number']}", "recognizedBy": {"@type": "Organization", "name": "Gas Safe Register"}})
    if not is_todo(CFG["electrical_scheme"]): cred.append({"@type": "EducationalOccupationalCredential", "name": f"{CFG['electrical_scheme']} registered", "recognizedBy": {"@type": "Organization", "name": CFG["electrical_scheme"]}})
    if cred: b["hasCredential"] = cred
    if not is_todo(CFG["engineer_name"]):
        b["employee"] = {"@type": "Person", "name": CFG["engineer_name"], "jobTitle": "Electrician and Gas Safe engineer"}
    return b

def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail)]}

def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}

def service_schema(name, path, desc, price_key=None, service_type=None):
    s = {"@type": "Service", "@id": f"{SITE}{path}#service", "name": name, "serviceType": service_type or name, "description": desc,
         "provider": {"@id": BIZ_ID}, "url": SITE + path,
         "areaServed": {"@type": "GeoCircle", "geoMidpoint": {"@type": "GeoCoordinates", "latitude": BASE["lat"], "longitude": BASE["lng"]}, "geoRadius": round(BASE["radius_miles"] * 1609.34)},
         "audience": {"@type": "Audience", "audienceType": "Private landlords, homeowners and small businesses"}}
    if price_key:
        s["offers"] = {"@type": "Offer", "priceCurrency": "GBP", "price": inc(price_key),
                       "priceSpecification": {"@type": "PriceSpecification", "minPrice": inc(price_key), "priceCurrency": "GBP", "valueAddedTaxIncluded": True}}
    return s

# ------------------------------------------------------------------ navigation
SERVICE_MENU = [
    ("Electrical", "zap", [("EICR certificate", "/eicr/"), ("EICR remedial works", "/eicr-remedial-works/"),
                           ("Consumer unit replacement", "/consumer-unit-replacement/"), ("Fault finding", "/electrical-fault-finding/"),
                           ("PAT testing", "/pat-testing/")]),
    ("Gas", "flame", [("Gas safety certificate", "/gas-safety-certificate/"), ("Boiler service", "/boiler-service/")]),
    ("Fire", "bell", [("Fire alarm testing", "/fire-alarm/"), ("Emergency lighting", "/emergency-lighting/"),
                      ("Fire risk assessment", "/fire-risk-assessment/")]),
    ("Energy and business", "leaf", [("EPC", "/epc/"), ("Commercial properties", "/commercial/"),
                                       ("All services", "/services/"), ("Prices", "/prices/")]),
]
NAV = [("Bundles", "/landlord-bundles/"), ("Areas", "/areas/"), ("Guide", "/landlord-compliance-guide/"),
       ("Reviews", "/reviews/"), ("Contact", "/contact/")]

def topbar():
    sb = CFG["sister_brand"]
    phone_lbl = t("phone_display")
    return f'''<div class="topbar"><div class="wrap topbar-in">
<div class="topbar-contact"><a href="{phone_href()}">{icon("phone")}{phone_lbl}</a><a href="{esc(wa_href())}"{' rel="noopener"' if wa_href().startswith("http") else ""}>{icon("wa")}WhatsApp</a></div>
<a class="topbar-emergency" href="{esc(sb["url"])}" rel="noopener">{icon("alert")}<span>{esc(sb["line"])}</span> <strong>{esc(sb["name"])}</strong></a>
</div></div>'''

def header(path):
    in_svc = any(path == h for _, _, links in SERVICE_MENU for _, h in links)
    groups = "".join(
        f'<div class="mega-col"><p class="mega-h">{icon(ic)}{esc(g)}</p><ul>'
        + "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if path == h else ""}>{esc(n)}</a></li>' for n, h in links)
        + "</ul></div>" for g, ic, links in SERVICE_MENU)
    items = "".join(f'<li><a class="nav-link" href="{h}"{" aria-current=\"page\"" if path.startswith(h) else ""}>{n}</a></li>' for n, h in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
{topbar()}
<header class="site-head"><div class="wrap head-in">
<a class="logo" href="/" aria-label="{esc(CFG["business_name"])} home">{LOGO}<span>Landlord<b>Safety First</b></span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">{icon("menu")}<span>Menu</span></button>
<nav class="nav" id="nav" aria-label="Main"><ul class="nav-list">
<li class="has-mega"><button class="nav-link mega-btn{" is-current" if in_svc else ""}" type="button" aria-expanded="false" aria-controls="mega">Services{icon("chev")}</button>
<div class="mega" id="mega">{groups}</div></li>
{items}
</ul>
<a class="btn btn-primary nav-book" href="/book/">{icon("calendar")}<span>Book now</span></a>
</nav>
</div></header>'''

SERVICE_OPTIONS = ["Not sure yet", "Landlord bundle", "EICR (electrical certificate)", "EICR remedial works", "Consumer unit replacement",
                   "Fault finding / repair", "Gas safety certificate", "Boiler service", "Fire alarm test", "Emergency lighting test",
                   "Fire risk assessment", "EPC", "PAT testing", "Smoke and CO alarms", "Commercial property"]
PROPERTY_TYPES = ["Flat", "House", "HMO", "Commercial", "Other"]

def quote_block(preselect=None, heading="Get a fixed quote", lede=None):
    opts = "".join(f'<option{" selected" if o == preselect else ""}>{esc(o)}</option>' for o in SERVICE_OPTIONS)
    ptypes = "".join(f"<option>{p}</option>" for p in PROPERTY_TYPES)
    lede = lede or "Tell us about the property and what you need. Got an EICR with codes on it? Attach a photo on WhatsApp and we'll price the work from the report."
    return f'''<section class="section section-navy" id="quote" aria-labelledby="quote-h"><div class="wrap quote">
<div class="quote-copy">
<h2 id="quote-h">{heading}</h2>
<p class="lede">{lede}</p>
<ul class="quote-contact">
<li><a href="{phone_href()}">{icon("phone")}{t("phone_display")}</a></li>
<li><a href="{esc(wa_href())}"{' rel="noopener"' if wa_href().startswith("http") else ""}>{icon("wa")}WhatsApp us a photo of your report</a></li>
<li><a href="mailto:{esc(CFG["email"])}">{icon("mail")}{esc(CFG["email"])}</a></li>
<li>{icon("clock")}<span>{t("hours_display")}</span></li>
</ul>
<p class="quote-alt">Know what you need? <a href="/book/">Book online</a>.</p>
</div>
<form class="card form" data-form="quote" novalidate>
<div class="row">
<div class="field"><label for="q-name">Name</label><input id="q-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="q-phone">Phone</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" required></div>
</div>
<div class="row">
<div class="field"><label for="q-email">Email <span class="opt">(optional)</span></label><input id="q-email" name="email" type="email" autocomplete="email"></div>
<div class="field"><label for="q-pc">Property postcode</label><input id="q-pc" name="postcode" autocomplete="postal-code"></div>
</div>
<div class="row">
<div class="field"><label for="q-type">Property type</label><select id="q-type" name="property_type">{ptypes}</select></div>
<div class="field"><label for="q-date">Preferred date <span class="opt">(optional)</span></label><input id="q-date" name="preferred_date" type="date" data-min-tomorrow></div>
</div>
<div class="field"><label for="q-svc">What do you need?</label><select id="q-svc" name="service">{opts}</select></div>
<div class="field"><label for="q-msg">Details <span class="opt">(optional)</span></label><textarea id="q-msg" name="message" rows="3" placeholder="e.g. 2-bed flat in E3, gas cert due next month, tenant works from home"></textarea></div>
<div class="hp" aria-hidden="true"><label for="q-url">Leave empty</label><input id="q-url" name="company_url" tabindex="-1" autocomplete="off"></div>
<p class="consent">We only use your details to reply to this request. See our <a href="/privacy/">privacy notice</a>.</p>
<button class="btn btn-primary btn-block" type="submit">{icon("send")}<span>Send my request</span></button>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>
</div></section>'''

def cta_band(heading="Need your certificates sorted?", sub=None):
    sub = sub or f"Pick a slot online, call, or send a WhatsApp. {t('slot_confirm_line')}."
    return f'''<section class="cta-band" aria-labelledby="cta-h"><div class="wrap"><div class="cta-in" data-reveal>
<img class="cta-bg" src="/img/street.webp" alt="" width="1600" height="900" loading="lazy" decoding="async">
<div><p class="tag light">Book today</p><h2 id="cta-h">{heading}</h2><p>{sub}</p></div>
<div class="btn-row">{book_btn("btn-primary", "Book online")}{call_btn("btn-light")}{wa_btn("btn-light")}</div>
</div></div></section>'''

def footer():
    yr = CFG["last_reviewed"][:4]
    sb = CFG["sister_brand"]
    socials = "".join(f'<li><a href="{esc(u)}" rel="noopener">{esc(re.sub(r"^https?://(www\.)?", "", u).split("/")[0])}</a></li>' for u in CFG["same_as"])
    col = lambda title, links: f'<div><h2>{title}</h2><ul>' + "".join(f'<li><a href="{h}">{esc(n)}</a></li>' for n, h in links) + "</ul></div>"
    return f'''<footer class="site-foot"><div class="wrap">
<div class="foot-grid">
<div class="foot-brand">
<a class="logo logo-light" href="/">{LOGO}<span>Landlord<b>Safety First</b></span></a>
<p>Gas, electrical and fire safety certificates for landlords, homeowners and small businesses, within {BASE["radius_miles"]} miles of {BASE["area_name"]}.</p>
<address>
<strong>{esc(CFG["business_name"])}</strong><br>
{BASE["area_name"]}, {BASE["locality"]} {BASE["postcode_area"]}<br>
<a href="{phone_href()}">{t("phone_display")}</a><br>
<a href="mailto:{esc(CFG["email"])}">{esc(CFG["email"])}</a>
</address>
<p class="foot-hours">{icon("clock")}{t("hours_display")}</p>
</div>
{col("Certificates", [("EICR", "/eicr/"), ("Gas safety certificate", "/gas-safety-certificate/"), ("Fire alarm testing", "/fire-alarm/"), ("Emergency lighting", "/emergency-lighting/"), ("Fire risk assessment", "/fire-risk-assessment/"), ("EPC", "/epc/"), ("PAT testing", "/pat-testing/")])}
{col("Work and repairs", [("EICR remedial works", "/eicr-remedial-works/"), ("Consumer unit replacement", "/consumer-unit-replacement/"), ("Fault finding", "/electrical-fault-finding/"), ("Boiler service", "/boiler-service/"), ("Commercial properties", "/commercial/"), ("Landlord bundles", "/landlord-bundles/"), ("Prices", "/prices/")])}
{col("Areas", [("Tower Hamlets", "/areas/tower-hamlets/"), ("Hackney", "/areas/hackney/"), ("Newham", "/areas/newham/"), ("All areas", "/areas/")])}
{col("Company", [("About", "/about/"), ("Reviews", "/reviews/"), ("Landlord guide", "/landlord-compliance-guide/"), ("FAQ", "/faq/"), ("Contact", "/contact/"), ("Book online", "/book/")])}
</div>
<a class="foot-emergency" href="{esc(sb["url"])}" rel="noopener">{icon("alert")}<span>{esc(sb["line"])} Our sister company <strong>{esc(sb["name"])}</strong> handles urgent electrical repairs.</span></a>
{('<ul class="foot-social">' + socials + '</ul>') if socials else ''}
<div class="foot-legal">
<p>Gas Safe Register no. {t("gas_safe_number")} · {t("electrical_scheme")} no. {t("electrical_scheme_number")} · {t("insurance_line")} · ICO no. {t("ico_number")}</p>
<p>© {yr} {esc(CFG["business_name"])}. {t("legal_line")}</p>
<p><a href="/privacy/">Privacy</a> · <a href="/cookies/">Cookies</a> · <a href="/terms/">Terms</a> · <a href="/sitemap.xml">Sitemap</a></p>
</div>
</div></footer>'''

def action_bar():
    return (f'<nav class="action-bar" aria-label="Quick contact">'
            f'<a href="{phone_href()}">{icon("phone")}<span>Call</span></a>'
            f'<a class="ab-book" href="/book/">{icon("calendar")}<span>Book</span></a>'
            f'<a href="{esc(wa_href())}"{" rel=\"noopener\"" if wa_href().startswith("http") else ""}>{icon("wa")}<span>WhatsApp</span></a></nav>')

def consent_bar():
    if not (CFG["analytics"]["ga4_id"] or CFG["analytics"]["google_ads_id"]):
        return ""
    return '''<div class="consent-bar" id="consent" role="region" aria-label="Cookie choice">
<p>We'd like to use cookies to see which pages and adverts bring enquiries. Nothing is set unless you accept. <a href="/cookies/">Cookie policy</a>.</p>
<div class="btn-row"><button class="btn btn-primary" data-consent="granted">Accept</button><button class="btn btn-ghost" data-consent="denied">Reject</button></div></div>'''

def head_analytics():
    a = CFG["analytics"]
    ids = [i for i in (a["ga4_id"], a["google_ads_id"]) if i]
    if not ids:
        return ""
    cfg_lines = "".join(f"gtag('config','{i}');" for i in ids)
    return (f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}"
            f"gtag('consent','default',{{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500}});"
            f"gtag('js',new Date());{cfg_lines}</script>"
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={ids[0]}"></script>')

CSS = (ROOT / "src/styles.css").read_text()
JS = (ROOT / "src/main.js").read_text()

def minify_css(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    s = re.sub(r"\s+", " ", s)
    return re.sub(r"\s*([{};,>])\s*", r"\1", s).replace(";}", "}").strip()

def page_js_config(extra=None):
    a = CFG["analytics"]
    phone_link = f'<a href="{phone_href()}">{esc(plain("phone_display", "us"))}</a>'
    cfg = {"formEndpoint": CFG["form_endpoint"], "adsId": a["google_ads_id"], "labelCall": a["ads_label_call"],
           "labelWhatsapp": a["ads_label_whatsapp"], "labelForm": a["ads_label_form"], "labelBooking": a.get("ads_label_booking", ""),
           "analytics": bool(a["ga4_id"] or a["google_ads_id"]), "phoneLink": phone_link,
           "responsePromise": plain("response_promise", "We'll be in touch shortly.")}
    if extra: cfg.update(extra)
    return "window.LSF=" + json.dumps(cfg, ensure_ascii=False) + ";"

def layout(p):
    """p: dict(path, title, description, body, schema=[...], crumbs=[(name,path)], js_extra=None, noindex=False, quote=True, preselect=None, cta=True)"""
    path = p["path"]
    graph = [business_schema()] + p.get("schema", [])
    if p.get("crumbs"): graph.append(crumbs_schema(p["crumbs"]))
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    canonical = SITE + path
    robots = '<meta name="robots" content="noindex">' if p.get("noindex") else '<meta name="robots" content="index,follow,max-image-preview:large">'
    quote = quote_block(p.get("preselect"), p.get("quote_heading", "Get a fixed quote"), p.get("quote_lede")) if p.get("quote", True) else ""
    cta = cta_band() if p.get("cta", False) else ""
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["description"])}">
<link rel="canonical" href="{canonical}">
{robots}
<meta name="theme-color" content="#0B2A21">
<meta property="og:type" content="website"><meta property="og:site_name" content="{esc(CFG["business_name"])}">
<meta property="og:title" content="{esc(p["title"])}"><meta property="og:description" content="{esc(p["description"])}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/og.png"><meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
<script>document.documentElement.classList.add('js')</script>
<style>{minify_css(CSS)}</style>
{head_analytics()}
<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(path)}
<main id="main">
{p["body"]}
{quote}
{cta}
</main>
{footer()}
{action_bar()}
{consent_bar()}
<script>{page_js_config(p.get("js_extra"))}{JS}</script>
</body>
</html>'''

def breadcrumbs_html(trail):
    lis = "".join(f'<li><a href="{h}">{esc(n)}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{esc(n)}</li>'
                  for i, (n, h) in enumerate(trail))
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'

def faq_html(faqs, heading="Questions landlords ask", hid="faq-h", lede=None):
    items = "".join(f'<details><summary>{esc(q)}{icon("chev")}</summary><div class="answer"><p>{a}</p></div></details>' for q, a in faqs)
    ld = f'<p class="section-lede">{lede}</p>' if lede else ""
    return f'<h2 id="{hid}">{heading}</h2>{ld}<div class="faq">{items}</div>'

def reviewed_line():
    from datetime import date
    d = date.fromisoformat(CFG["last_reviewed"])
    return f'<p class="reviewed">{icon("user")}<span>Written and checked by {t("engineer_name")}, {t("electrical_scheme")} registered electrician and Gas Safe engineer (no. {t("gas_safe_number")}). Last reviewed {d.day} {d.strftime("%B %Y")}.</span></p>'

# ------------------------------------------------------------------ build
def write(path, content):
    out = DIST / path.lstrip("/")
    if path.endswith("/"):
        out = out / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content)

def main():
    production = "--production" in sys.argv
    import content
    pages = content.pages(sys.modules[__name__])
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    for p in pages:
        write(p["path"] if p["path"] != "/404" else "/404.html", layout(p))
    shutil.copytree(ROOT / "src/fonts", DIST / "fonts")
    shutil.copytree(ROOT / "src/img", DIST / "img")
    for f in (ROOT / "src/static").glob("*"):
        shutil.copy(f, DIST / f.name)
    urls = [p for p in pages if not p.get("noindex")]
    sm = "".join(f"<url><loc>{SITE}{p['path']}</loc><lastmod>{CFG['last_reviewed']}</lastmod></url>" for p in urls)
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    (DIST / "llms.txt").write_text(content.llms_txt(sys.modules[__name__], urls))
    # Vercel reads vercel.json from the repo root. The built site in dist/ is committed and served as-is (no build step on Vercel).
    (ROOT / "vercel.json").write_text(json.dumps({
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "framework": None, "outputDirectory": "dist",
        "trailingSlash": True, "cleanUrls": False,
        "headers": [
            {"source": "/fonts/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/img/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=2592000"}]},
            {"source": "/(.*)", "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"}]}],
        "redirects": [{"source": "/index.html", "destination": "/", "permanent": True},
                      {"source": "/fire-alarm-emergency-lighting/", "destination": "/fire-alarm/", "permanent": True}]}, indent=2))
    unconfirmed = not CFG.get("prices_confirmed", False)
    print(f"Built {len(pages)} pages → {DIST}")
    blockers = sorted(TODOS) + (["prices: set \"prices_confirmed\": true once the client signs off every price"] if unconfirmed else [])
    for k in ("phone_e164", "whatsapp_e164", "form_endpoint"):
        if not CFG[k]: blockers.append(f"{k}: empty")
    if blockers:
        print("\nStill to fill in:")
        for b in blockers: print("  -", b)
        if production:
            print("\n--production: refusing to finish while these remain.")
            sys.exit(1)

if __name__ == "__main__":
    main()
