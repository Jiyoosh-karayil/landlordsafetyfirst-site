"""Page copy for landlordsafetyfirst.uk. Business facts and prices come from site.config.json via the build helpers (b.*).
Core pages live here; extra service, booking and legal pages live in content_more.py."""
from types import SimpleNamespace


def helpers(b):
    """Shared page pieces, passed to content_more.py as H."""
    C, t, price, ptx, esc, icon = b.CFG, b.t, b.price, b.price_txt, b.esc, b.icon
    HOURLY = ptx("hourly")

    def page_head(trail, h1, lede, buttons=True, book=None, eyebrow=None):
        btns = ""
        if buttons:
            btns = (f'<div class="btn-row">{b.book_btn("btn-primary", "Book now", book or "/book/")}{b.call_btn("btn-ghost")}</div>'
                    f'<p class="head-alt">Prefer it in writing? <a href="#quote">Get a fixed quote</a> or <a href="{esc(b.wa_href())}">send a WhatsApp</a>.</p>')
        meta = f'<p class="page-meta">{eyebrow}</p>' if eyebrow else ""
        return f'<section class="page-head"><div class="wrap">{b.breadcrumbs_html(trail)}<h1>{h1}</h1><p class="lede">{lede}</p>{meta}{btns}</div></section>'

    def in_short(q, a):
        return f'<div class="in-short"><h2>{q}</h2><p>{a}</p></div>'

    def side(title, price_key, bullets, book=None, label="Book now", price_note=None, quote_href="#quote"):
        lis = "".join(f"<li>{icon('check')}<span>{x}</span></li>" for x in bullets)
        pn = f'<p class="small">{price_note}</p>' if price_note else ""
        return f'''<aside class="side card" aria-label="Book">
<h2>{title}</h2>
{price(price_key)}
{pn}
{b.book_btn("btn-primary", label, book or "/book/")}
{b.btn(quote_href, "Get a quote first", "btn-ghost")}
{b.wa_btn("btn-ghost")}
<ul>{lis}</ul>
</aside>'''

    def related(links):
        return '<h2 style="font-size:1.25rem;margin-top:2.5rem">Related</h2><ul class="related">' + "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in links) + "</ul>"

    def price_board(rows):
        out = []
        for key, title, desc, href in rows:
            h = f'<a href="{href}">{esc(title)}</a>' if href else esc(title)
            out.append(f'<div class="price-row"><h3>{h}</h3>{price(key)}<p>{desc}</p></div>')
        return '<div class="price-board">' + "".join(out) + "</div>"

    def creds_block():
        return f'''<dl class="creds">
<div class="cred"><dt>Electrical registration</dt><dd>{t("electrical_scheme")}<br>No. {t("electrical_scheme_number")}</dd></div>
<div class="cred"><dt>Gas Safe Register</dt><dd>No. {t("gas_safe_number")}</dd></div>
<div class="cred"><dt>Insurance</dt><dd>{t("insurance_line")}</dd></div>
<div class="cred"><dt>Experience</dt><dd>{t("years_trading")} years</dd></div>
</dl>'''

    def stars():
        return '<div class="stars" aria-hidden="true">' + icon("star") * 5 + "</div>"

    def reviews_block(heading="What landlords say"):
        if not C["reviews"]:
            return ""
        items = "".join(f'<figure class="review card">{stars()}<blockquote>“{esc(r["text"])}”</blockquote><figcaption>{esc(r["name"])}, {esc(r["area"])}{" · " + esc(r["service"]) if r.get("service") else ""}</figcaption></figure>' for r in C["reviews"])
        more = f'<p style="margin-top:1.5rem"><a href="{esc(C["google_reviews_url"])}" rel="noopener">Read all our reviews on Google</a></p>' if C["google_reviews_url"] else ""
        return f'<section class="section section-alt" aria-labelledby="rev-h"><div class="wrap"><div class="section-head"><h2 id="rev-h">{heading}</h2></div><div class="reviews">{items}</div>{more}</div></section>'

    def faq_section(faqs, heading="Questions landlords ask", lede=None, hid="faq-h", alt=False):
        ld = lede or "Straight answers. If yours isn't here, call or send a WhatsApp."
        items = "".join(f'<details><summary>{esc(q)}{icon("chev")}</summary><div class="answer"><p>{a}</p></div></details>' for q, a in faqs)
        return f'''<section class="section{" section-alt" if alt else ""}" aria-labelledby="{hid}"><div class="wrap faq-wrap">
<div class="faq-intro"><h2 id="{hid}">{heading}</h2><p class="section-lede">{ld}</p>
<div class="btn-row" style="margin-top:1.5rem">{b.call_btn("btn-ghost")}{b.wa_btn("btn-ghost")}</div></div>
<div class="faq">{items}</div>
</div></section>'''

    # ---------------- price picker ----------------
    TYPES = [("flat", "Flat", "building"), ("house", "House", "home"), ("hmo", "HMO", "users"), ("commercial", "Commercial", "box")]

    def picker_controls(pfx, ptype="flat", beds=2, items=("eicr", "gas")):
        seg = "".join(f'<label class="opt-card"><input type="radio" name="ptype" value="{v}"{" checked" if v == ptype else ""}><span>{n}</span></label>' for v, n, ic in TYPES)
        bopts = "".join(f'<option value="{i}"{" selected" if i == beds else ""}>{"Studio / 0" if i == 0 else i}</option>' for i in range(0, 13))
        chks = ""
        for it in b.PICK.values():
            ex = it["base"][ptype] + max(0, beds - it["incl"][ptype]) * it["per"][ptype]
            chks += (f'<label class="chk"><input class="vh" type="checkbox" name="item" value="{it["id"]}"{" checked" if it["id"] in items else ""}>'
                     f'<span class="chk-box">{icon("check")}</span><span class="chk-name">{esc(it["label"])}</span>'
                     f'<span class="chk-price tnum" data-price-for="{it["id"]}">{b.money(b.with_vat(ex))}</span></label>')
        return f'''<fieldset class="pick-step"><legend><span class="step-n">1</span>What kind of property?</legend><div class="seg">{seg}</div></fieldset>
<div class="pick-step"><label class="pick-label" for="{pfx}-beds"><span class="step-n">2</span><span data-beds-label>Bedrooms</span></label>
<div class="beds"><select id="{pfx}-beds" name="beds">{bopts}</select></div></div>
<fieldset class="pick-step"><legend><span class="step-n">3</span>Which certificates?</legend><div class="chks">{chks}</div></fieldset>
<p class="picker-note">Book two certificates together and save 10%. Three or more, save 15%. Minimum visit {b.MIN_TXT}. Prices include VAT.</p>'''

    def picker_summary(ptype="flat", beds=2, items=("eicr", "gas"), book=True):
        q = b.quote_calc(ptype, beds, list(items))
        lines = "".join(f'<li><span>{esc(l)}</span><span class="tnum">{b.money(b.with_vat(ex))}</span></li>' for l, ex in q["lines"])
        sav = b.with_vat(q["subtotal"]) - q["total_inc"]
        bedtxt = "studio" if beds == 0 else f"{beds} bedrooms"
        book_html = (f'<a class="btn btn-primary" data-sum="book" href="{b.book_href(ptype, beds, list(items))}">{icon("calendar")}<span>Book this</span></a>'
                     f'<p class="sum-alt">or <a href="/contact/#quote">ask a question first</a></p>') if book else \
                    f'<button class="btn btn-primary" type="submit">{icon("send")}<span>Send booking request</span></button><div class="form-msg" role="status" aria-live="polite"></div>'
        return f'''<div class="sum" aria-live="polite">
<h3>Your price</h3>
<p class="sum-prop" data-sum="prop">{ptype.title()}, {bedtxt}</p>
<ul class="sum-lines" data-sum="lines">{lines}</ul>
<p class="sum-saving" data-sum="saving"{"" if q["saving"] else " hidden"}><span>Bundle saving ({round(q["rate"]*100)}%)</span><span class="tnum">−{b.money(sav)}</span></p>
<div class="sum-total" data-sum="total"><span>Total</span><span class="sum-amt tnum" data-sum="amt">{b.money(q["total_inc"])}</span></div>
<p class="sum-ex tnum" data-sum="ex">{b.money(q["total_ex"])} + VAT</p>
<p class="sum-min" data-sum="min" hidden>Minimum visit charge applied. Add another certificate at no extra call-out.</p>
<p class="sum-min" data-sum="commercial" hidden>Commercial premises are priced by size and circuit count. Send the details and we'll quote the same day.</p>
<input type="hidden" name="quote_total" value="">
{book_html}
</div>'''

    def picker_home():
        return f'''<div class="picker card" data-picker>
<div class="picker-main">{picker_controls("pk")}</div>
{picker_summary()}
</div>'''

    def picker_sheet():
        """The home hero: the working price picker set as a register sheet."""
        return f'''<div class="sheet picker" data-picker id="price" role="region" aria-label="Instant price">
<div class="sheet-head"><h3>Your price</h3><p>VAT included. Fixed before you book.</p></div>
<div class="picker-main">{picker_controls("pk")}</div>
{picker_summary()}
</div>'''

    # ---------------- bundles ----------------
    def bundle_cards():
        out = []
        for bd in C["bundles"]:
            q = b.quote_calc(bd["type"], bd["beds"], bd["items"])
            sav = b.with_vat(q["subtotal"]) - q["total_inc"]
            basis = f'{bd["beds"]}-bed flat' if bd["type"] == "flat" else (f'{bd["beds"]}-room HMO' if bd["type"] == "hmo" else f'{bd["beds"]}-bed house')
            incl = "".join(f'<li>{icon("check-circle")}<span>{esc(b.PICK[i]["label"])}</span></li>' for i in bd["items"])
            pop = bd.get("popular")
            out.append(f'''<article class="bundle card{" popular" if pop else ""}">
<h3>{esc(bd["name"])}{'<span class="bundle-flag">Most popular</span>' if pop else ""}</h3>
<p class="bundle-for">{esc(bd["for"])}</p>
<div class="bundle-price"><span class="from">from</span><span class="amt tnum">{b.money(q["total_inc"])}</span>{f'<span class="save">Save {b.money(sav)}</span>' if sav > 0 else ""}</div>
<p class="bundle-meta tnum">{b.money(q["total_ex"])} + VAT · {basis}</p>
<p class="blurb">{esc(bd["blurb"])}</p>
<ul class="incl">{incl}</ul>
{b.book_btn("btn-primary" if pop else "btn-ghost", "Book this bundle", b.book_href(bd["type"], bd["beds"], bd["items"]))}
</article>''')
        flag = "" if C.get("prices_confirmed") else f'<p class="small" style="margin-top:1rem">{b.todo("Bundle prices are placeholders until the client confirms them.")}</p>'
        return '<div class="bundles">' + "".join(out) + "</div>" + flag

    # ---------------- service cards ----------------
    def svc_card(ic, name, href, desc, price_key=None, price_txt=None):
        pr = price_txt or (f'<span class="svc-from">from</span> {b.money(b.inc(price_key))}' if price_key else "")
        return f'''<li class="svc"><h4><a class="stretch" href="{href}">{esc(name)}</a></h4><p>{desc}</p><span class="svc-price tnum">{pr}</span></li>'''

    return SimpleNamespace(**locals())


def pages(b):
    C, t, price, ptx, esc, icon = b.CFG, b.t, b.price, b.price_txt, b.esc, b.icon
    H = helpers(b)
    page_head, in_short, side, related, price_board, creds_block = H.page_head, H.in_short, H.side, H.related, H.price_board, H.creds_block
    R = C["base"]["radius_miles"]
    HOURLY = ptx("hourly")

    # ---------------------------------------------------------- EICR code checker data
    codes = {
        "C1": dict(result="Unsatisfactory", colour="#B42318",
                   means="Danger present. Someone could be hurt now, for example exposed live parts.",
                   deadline="Make safe immediately. The inspector should isolate it before leaving.",
                   action="We make it safe on the first visit where we can, do the permanent repair, and give you the written confirmation your tenants and council need.",
                   cost=f"Usually one visit, from {HOURLY} for the first hour"),
        "C2": dict(result="Unsatisfactory", colour="#B85400",
                   means="Potentially dangerous. Not dangerous this minute, but could become so, for example no RCD on sockets that could power something outdoors.",
                   deadline="Fix within 28 days, or sooner if the report says so.",
                   action="Send us the report. We price each C2 item separately, fix them, and issue the certificate plus written confirmation the work is done.",
                   cost=f"Most single items take 1–2 hours, from {HOURLY}"),
        "C3": dict(result="Does not fail the report", colour="#2560A8",
                   means="Improvement recommended. Below today's standard but not unsafe.",
                   deadline="No legal deadline.",
                   action="We list them in your quote so you can fix them while we're already there, with no separate call-out.",
                   cost="Quoted alongside other work"),
        "FI": dict(result="Unsatisfactory", colour="#6B4FA0",
                   means="Further investigation needed. The inspector found something they couldn't fully test, such as a circuit they couldn't trace.",
                   deadline="Investigate within 28 days, or sooner if the report says so.",
                   action="We trace it, tell you exactly what it is, and price any repair before we start it.",
                   cost=f"Usually 1–2 hours, from {HOURLY}"),
        "OK": dict(result="Satisfactory", colour="#157A45",
                   means="No C1, C2 or FI codes. You're compliant until the next inspection date on the report, five years at most.",
                   deadline="Give your tenants a copy within 28 days.",
                   action="We note your next due date and remind you before it comes round.",
                   cost=f"Next EICR from {ptx('eicr_flat')}"),
    }
    for k, d in codes.items():
        if k in ("C1", "C2", "FI"):
            d["cta"] = f'<a class="btn btn-primary" href="/eicr-remedial-works/#quote">Get these fixed</a>{b.wa_btn("btn-ghost", "Hi, my EICR has " + k + " codes. Can I send you the report?", "Send us the report")}'
        elif k == "C3":
            d["cta"] = '<a class="btn btn-ghost" href="#quote">Add them to a quote</a>'
        else:
            d["cta"] = '<a class="btn btn-ghost" href="/book/?type=flat&beds=2&items=eicr">Book your next EICR</a>'

    def verdict_static(k):
        d = codes[k]
        row = lambda a, v: f'<div class="verdict-row"><dt>{a}</dt><dd>{v}</dd></div>'
        return (f'<dl>{row("Result", f"<span class=status style=background:{d['colour']}>{d['result']}</span>")}'
                f'{row("Means", d["means"])}{row("Deadline", d["deadline"])}{row("What we do", d["action"])}{row("Typical cost", d["cost"])}</dl>'
                f'<div class="cta btn-row">{d["cta"]}</div>')

    def checker(heading_tag="h2"):
        btns = "".join(
            f'<button type="button" class="code-btn" data-code="{k}" aria-pressed="{"true" if k == "C2" else "false"}">{k if k != "OK" else "Pass"}<small>{lbl}</small></button>'
            for k, lbl in (("C1", "Danger"), ("C2", "Urgent"), ("C3", "Advisory"), ("FI", "Investigate"), ("OK", "Satisfactory")))
        return f'''<div class="checker" id="checker"><div class="checker-stripe"></div><div class="checker-in">
<{heading_tag}>Got your EICR back?</{heading_tag}>
<p class="checker-q">Pick the worst code on your report to see what you have to do, and by when.</p>
<div class="codes" role="group" aria-label="EICR observation codes">{btns}</div>
<div class="verdict" id="verdict" aria-live="polite">{verdict_static("C2")}</div>
</div></div>'''

    PICKJS = {"pricing": b.picker_js()}
    CODESJS = {"codes": codes, "pricing": b.picker_js()}

    P = []

    # ======================================================================== HOME
    home_faqs = [
        ("How often does a rental property need an EICR?",
         "At least every five years, or sooner if the last report says so. Some HMO licences ask for it more often. You must give a copy to your tenants within 28 days of the inspection."),
        ("How often do I need a gas safety certificate?",
         "Every 12 months, for every gas appliance, flue and pipe you provide. You can have the check done up to two months before the old one runs out and keep the same renewal date."),
        ("What happens if my property fails?",
         "If the EICR has C1, C2 or FI codes, you have 28 days (or less, if the report says so) to fix them. We price each item from the report and can often fix small items on the same visit, with your OK. If a gas appliance is unsafe, we tell you exactly why and quote the repair."),
        ("Do I need to be there for the inspection?",
         "No. Most landlords aren't. Give us your tenant's number and we'll arrange a time with them directly, or we can collect keys. You get the certificates by email."),
        ("How fast do I get my certificate?",
         f"{t('cert_turnaround')}. If anything fails, we send the report the same way with a price for the work."),
        ("Can you do gas, electrical and fire checks in one visit?",
         "Yes. The same qualified engineer does the gas safety check, the EICR and the alarm checks, so your tenant only gives access once. Booking two or more certificates together saves 10–15%."),
        ("What does an HMO need?",
         "Most HMOs need a licence from the council, plus the usual EICR and gas safety certificate. Licence conditions usually add an interlinked fire alarm system, and sometimes emergency lighting and a fire risk assessment. Send us your licence conditions and we'll tell you what applies."),
        ("Do I need an EPC to rent out a property?",
         "Yes. You need a valid EPC before you advertise, you must give a copy to your tenants, and in England a rental must be rated E or above unless it has a registered exemption. An EPC lasts 10 years."),
        ("What smoke and carbon monoxide alarms does a rental need?",
         "In England, a smoke alarm on every storey used as living accommodation, and a carbon monoxide alarm in every room with a fixed combustion appliance, such as a gas boiler. You must check they work on the first day of each new tenancy."),
        ("Are your prices fixed?",
         f"Certificates have fixed prices, shown before you book. Remedial work is priced item by item from the report, and nothing starts until you say yes. The minimum charge for a visit is {b.MIN_TXT}."),
        ("Which areas do you cover?",
         f"Anywhere within {R} miles of Whitechapel: all of East and Central London, most of Greater London, and nearby towns like Romford, Brentwood, Harlow, Dartford and Watford. See <a href=\"/areas/\">areas we cover</a>."),
        ("Do you work for homeowners and businesses too?",
         "Yes. Homeowners book us for EICRs, consumer units and boiler checks, and small shops and offices for <a href=\"/commercial/\">commercial EICRs, emergency lighting and fire alarm testing</a>."),
    ]

    engineer_photo = C.get("engineer_photo")
    pack_rows = [("Gas safety record (CP12)", "12 months", "Passed"),
                 ("EICR", "Up to 5 years", "Satisfactory"),
                 ("Smoke and CO alarms", "Checked on the day", "Working"),
                 ("EPC", "10 years", "Lodged")]
    pack = f'''<figure class="extract">
<figcaption class="extract-h"><strong>Example pack</strong><span>2-bed flat in London E3</span></figcaption>
<table class="extract-t"><thead><tr><th scope="col">Certificate</th><th scope="col">Valid for</th><th scope="col">Result</th></tr></thead><tbody>
{"".join(f'<tr><th scope="row">{n}</th><td>{v}</td><td><span class="mark-ok">{icon("check")}{ok}</span></td></tr>' for n, v, ok in pack_rows)}
</tbody></table>
<p class="extract-foot">{icon("bell")}<span>Reminder set for 30 days before the gas check is due.</span></p>
</figure>'''
    photo = (f'<img class="visit-photo" src="/{esc(engineer_photo)}" alt="{esc(b.plain("engineer_name", "Our engineer"))}, the engineer who carries out every inspection" width="800" height="1000" loading="lazy">' if engineer_photo else "")

    creds = [f"Gas Safe registered, no. {t('gas_safe_number')}",
             f"{t('electrical_scheme')} registered",
             t("insurance_line"),
             "Fixed price before you book"]
    if C["google_reviews_url"] and C["reviews"]:
        rating = esc(C["google_rating"]) if C["google_rating"] else "Reviews"
        creds[3] = f'<a href="{esc(C["google_reviews_url"])}" rel="noopener">{rating} on Google</a>'
    creds_html = '<ul class="hero-creds">' + "".join(f"<li>{icon('check')}<span>{c}</span></li>" for c in creds) + "</ul>"

    groups = [
        ("Electrical", [H.svc_card("zap", "EICR certificate", "/eicr/", "The electrical safety report every rental needs at least every five years.", "eicr_flat"),
                        H.svc_card("wrench", "EICR remedial works", "/eicr-remedial-works/", "Failed report? We fix the C1, C2 and FI codes inside your 28 days.", "hourly")]),
        ("Gas", [H.svc_card("flame", "Gas safety certificate", "/gas-safety-certificate/", "The annual CP12 check on every gas appliance, flue and pipe.", "gas_safety"),
                 H.svc_card("wrench", "Boiler service", "/boiler-service/", "Keeps the boiler efficient and its warranty valid. Best done with the gas check.", "boiler_service")]),
        ("Fire", [H.svc_card("bell", "Fire alarm testing", "/fire-alarm/", "Tests and certificates for HMO alarm systems, plus smoke and CO alarms.", "fire_alarm_test"),
                  H.svc_card("bulb", "Emergency lighting", "/emergency-lighting/", "The annual three-hour test HMO licences and fire risk assessments ask for.", "emergency_lighting")]),
        ("Energy", [H.svc_card("leaf", "EPC", "/epc/", "The energy certificate you need before you advertise. Rentals must rate E or above.", "epc"),
                    H.svc_card("plug", "PAT testing", "/pat-testing/", "Checks on the appliances you supply in a furnished let or HMO.", "pat")]),
    ]
    svc_html = '<div class="ledger">' + "".join(
        f'<div class="ledger-group"><h3>{g}</h3><ul class="ledger-list">{"".join(cs)}</ul></div>' for g, cs in groups) + "</div>"

    yes = lambda s: f'<span class="yes">{icon("check")}{s}</span>'
    no = lambda s: f'<span class="no">{icon("x")}{s}</span>'
    compare_rows = [
        ("Who turns up", yes("The engineer you booked"), no("Whoever is free")),
        ("Who you speak to", yes("The engineer, directly"), no("A central booking line")),
        ("Who does the work", yes("Us. No subcontractors"), no("Often a contractor network")),
        ("If something fails", yes("Fixed on the day, with your OK"), no("Usually a second booking")),
        ("Gas, electrical and fire", yes("One qualified person"), no("Often separate visits")),
    ]
    compare = ('<table class="compare"><caption class="sr">How we compare with large booking platforms</caption><thead><tr><th scope="col"><span class="sr">Question</span></th>'
               '<th scope="col" class="us">Landlord Safety First</th><th scope="col">Large booking platforms</th></tr></thead><tbody>'
               + "".join(f'<tr><th scope="row">{q}</th><td class="us">{u}</td><td>{th}</td></tr>' for q, u, th in compare_rows) + "</tbody></table>")

    reminder = f'''<div class="reminder">
<div><h2 id="rem-h">Never miss a renewal date</h2>
<p class="section-lede">Tell us when your certificate runs out. We'll remind you 30 days before, by email or text. It's free, whoever did the last one.</p></div>
<form class="form" data-form="reminder" novalidate aria-labelledby="rem-h">
<div class="row">
<div class="field"><label for="r-cert">Certificate</label><select id="r-cert" name="certificate"><option>Gas safety certificate</option><option>EICR</option><option>EPC</option><option>Fire alarm service</option><option>Emergency lighting test</option></select></div>
<div class="field"><label for="r-date">Expiry date</label><input id="r-date" name="expiry_date" type="date" required></div>
</div>
<div class="row">
<div class="field"><label for="r-email">Email</label><input id="r-email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="r-phone">Mobile <span class="opt">(optional)</span></label><input id="r-phone" name="phone" type="tel" autocomplete="tel"></div>
</div>
<div class="field"><label for="r-pc">Property postcode <span class="opt">(optional)</span></label><input id="r-pc" name="postcode" autocomplete="postal-code"></div>
<div class="hp" aria-hidden="true"><label for="r-url">Leave empty</label><input id="r-url" name="company_url" tabindex="-1" autocomplete="off"></div>
<p class="consent">We'll only use this to send the reminder and, if you want, a price. Unsubscribe any time. <a href="/privacy/">Privacy notice</a>.</p>
<button class="btn btn-navy btn-block" type="submit">{icon("bell")}<span>Set my reminder</span></button>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>
</div>'''

    area_rows = "".join(
        f'<li class="area-row"><h3><a class="stretch" href="/areas/{s}/">{n}</a></h3><p>{pc}</p><span class="tnum">{tm} from E1</span></li>'
        for n, s, pc, tm in (("Tower Hamlets", "tower-hamlets", "E1, E1W, E2, E3, E14", "5–20 min"),
                             ("Hackney", "hackney", "E5, E8, E9, N1, N16", "15–25 min"),
                             ("Newham", "newham", "E6, E7, E12, E13, E15, E16", "15–30 min")))

    arrow_ic = icon("arrow", "ic arrow-ic")
    q_home = b.quote_calc("flat", 2, ["eicr", "gas"])
    max_save = round(max(r for _, r in C["picker"]["tiers"]) * 100)

    def photo_card(img, name, href, desc, price_key=None, price_txt=None, d=0):
        pr = price_txt or (f'<span class="from">from</span> {b.money(b.inc(price_key))}' if price_key else "")
        return (f'<li class="svc-card" data-reveal style="--d:{d}s"><img src="/img/{img}.webp" alt="" width="900" height="1000" loading="lazy" decoding="async">'
                f'<div class="svc-body"><h3><a class="stretch" href="{href}">{esc(name)}</a></h3><p class="svc-desc">{desc}</p><span class="svc-price tnum">{pr}</span></div>'
                f'<span class="svc-go" aria-hidden="true">{icon("arrow")}</span></li>')

    svc_cards = "".join([
        photo_card("svc-eicr", "EICR certificate", "/eicr/", "The electrical safety report every rental needs at least every five years.", "eicr_flat", d=0),
        photo_card("svc-gas", "Gas safety certificate", "/gas-safety-certificate/", "The annual CP12 check on every gas appliance, flue and pipe.", "gas_safety", d=.08),
        photo_card("svc-fire", "Fire alarm testing", "/fire-alarm/", "Tests and certificates for HMO alarm systems, plus smoke and CO alarms.", "fire_alarm_test", d=.16),
        photo_card("svc-remedial", "EICR remedial works", "/eicr-remedial-works/", "Failed report? We fix the C1, C2 and FI codes inside your 28 days.", "hourly", d=0),
        photo_card("svc-cu", "Consumer unit replacement", "/consumer-unit-replacement/", "A metal, RCD-protected board, tested, certified and notified. Usually done in a day.", "consumer_unit", d=.08),
        photo_card("svc-epc", "EPC", "/epc/", "The energy certificate you need before you advertise. Rentals must rate E or above.", "epc", d=.16),
    ])
    more_svcs = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in (
        ("Boiler service", "/boiler-service/"), ("Emergency lighting", "/emergency-lighting/"), ("Fire risk assessment", "/fire-risk-assessment/"),
        ("PAT testing", "/pat-testing/"), ("Fault finding", "/electrical-fault-finding/"), ("Commercial properties", "/commercial/")))

    whys = [
        ("user", "The engineer you booked turns up", f"Big platforms send whoever is free. We're {esc(C['team_size_line'])}."),
        ("pound", "Fixed prices, VAT included", f"You see the full price before you book. Remedial work is priced item by item, and nothing starts until you say yes."),
        ("wrench", "Small faults fixed on the day", "With your OK, we fix what we can on the same visit. No second booking, no second access request to your tenant."),
        ("zap", "Gas, electrical and fire in one visit", f"One qualified person does the lot, so your tenant lets us in once. Book two or more and save up to {max_save}%."),
    ]
    why_html = "".join(f'<article class="why" data-reveal style="--d:{i % 2 * .1}s"><div class="why-ic">{icon(ic)}</div><h3>{h}</h3><p>{p}</p></article>' for i, (ic, h, p) in enumerate(whys))

    town_names = ["Whitechapel"] + [x[0] for x in b.TOWNS]
    mq = "".join(f"<span>{esc(n)}</span>" for n in town_names)
    marquee = (f'<section class="marquee" aria-label="Areas we cover"><div class="marquee-track">'
               f'<div class="marquee-set">{mq}</div><div class="marquee-set" aria-hidden="true">{mq}</div></div></section>')

    reg_line = f"Gas Safe &amp; {t('electrical_scheme')} registered"

    home_body = f'''
<section class="hero"><div class="hero-card">
<picture class="hero-bg"><source media="(max-width: 700px)" srcset="/img/hero-m.webp"><img src="/img/hero.webp" alt="" width="1800" height="1200" fetchpriority="high"></picture>
<div class="wrap hero-in">
<div class="hero-top"><p class="hero-badge hero-fade" style="--d:.2s"><span class="badge-mark">{icon("shield")}</span><span><strong>{reg_line}</strong>One engineer for gas, electrical and fire</span></p></div>
<div class="hero-main">
<div class="hero-copy">
<h1 data-split>Landlord safety certificates in <em>East London</em></h1>
<p class="lede hero-fade" style="--d:.75s">Gas, electrical and fire safety for your rental, done by a qualified engineer, not a call centre. The engineer who books you is the engineer who turns up.</p>
<div class="btn-row hero-fade" style="--d:.9s"><a class="btn btn-primary" href="#price"><span>See your price</span>{arrow_ic}</a>{b.call_btn("btn-glass")}</div>
</div>
<div class="hero-side hero-fade" style="--d:1.05s">
<div class="hero-price"><span>EICR + gas safety, 2-bed flat</span><strong class="tnum">{b.money(q_home["total_inc"])}</strong><small>Fixed price, VAT included</small></div>
<p class="hero-area">{icon("pin")}<span>Based in Whitechapel, E1. Covering {R} miles.</span></p>
</div>
</div>
</div>
</div></section>

<section class="section" aria-labelledby="price-h"><div class="wrap price-wrap">
<div class="price-copy" data-reveal>
<p class="tag">Instant price</p>
<h2 id="price-h">Tick what you need. See the price you pay.</h2>
<p class="section-lede">The price you see is the price you pay, VAT included. Pick the property and the certificates, then book a slot that suits you.</p>
{creds_html.replace('class="hero-creds"', 'class="checks"')}
<div class="btn-row">{b.call_btn("btn-ghost")}{b.wa_btn("btn-ghost")}</div>
</div>
<div data-reveal style="--d:.1s">{H.picker_sheet()}</div>
</div></section>

<section class="section section-soft" aria-labelledby="about-h"><div class="wrap">
<div class="intro" data-reveal><p class="tag">About us</p><div>
<h2 id="about-h" class="statement">A local engineer, not a booking platform. One qualified person for gas, electrical and fire, one visit, and a fixed price before you book.</h2>
<a class="btn btn-dark" href="/about/"><span>More about us</span>{arrow_ic}</a></div></div>
<figure class="feature" data-reveal="zoom"><img src="/img/testing.webp" alt="An engineer testing a consumer unit with a voltage tester" width="1800" height="900" loading="lazy" decoding="async">
<div class="stats">
<p class="stat"><strong><span data-count="{R}">{R}</span><i> mi</i></strong>covered from Whitechapel, E1</p>
<p class="stat"><strong><span data-count="1">1</span><i> visit</i></strong>for gas, electrical and fire checks</p>
<p class="stat"><strong><span data-count="{max_save}">{max_save}</span><i>%</i></strong>off when you book three or more</p>
<p class="stat"><strong><span data-count="30">30</span><i> days</i></strong>notice before each renewal is due</p>
</div></figure>
</div></section>

<section class="section" aria-labelledby="svc-h"><div class="wrap">
<div class="intro" data-reveal><p class="tag">Our services</p><div>
<h2 id="svc-h">Every certificate a rental needs, done by the engineer who books you</h2>
<a class="btn btn-dark" href="/services/"><span>View all services</span>{arrow_ic}</a></div></div>
<ul class="svc-grid">{svc_cards}</ul>
<ul class="chips" data-reveal><li class="chips-label">Also:</li>{more_svcs}</ul>
</div></section>

<section class="section section-soft" aria-labelledby="why-h"><div class="wrap">
<div class="intro" data-reveal><p class="tag">Why us</p><div>
<h2 id="why-h">Booked once, done properly, priced up front</h2></div></div>
<div class="why-grid">{why_html}</div>
</div></section>

<section class="section" aria-labelledby="bun-h"><div class="wrap">
<div class="intro" data-reveal><p class="tag">Landlord bundles</p><div>
<h2 id="bun-h">One visit, every certificate, less to pay</h2>
<p class="section-lede">Your tenant lets us in once, and you get one set of paperwork and one renewal date to remember.</p></div></div>
<div data-reveal>{H.bundle_cards()}</div>
</div></section>

{marquee}

<section class="section" aria-labelledby="how-h"><div class="wrap how">
<div class="how-media" data-reveal="left"><img src="/img/engineer.webp" alt="An electrician working on a consumer unit" width="1000" height="1150" loading="lazy" decoding="async">{pack}</div>
<div data-reveal="right">
<p class="tag">How it works</p>
<h2 id="how-h">From booking to certificate in four steps</h2>
<ol class="steps">
<li><h3>Book online</h3><p>Pick your certificates and a day that suits. Or call or WhatsApp if you'd rather talk.</p></li>
<li><h3>We confirm your slot</h3><p>{t("slot_confirm_line")}. We can arrange access with your tenant directly.</p></li>
<li><h3>Inspection</h3><p>One visit for gas, electrical and alarms. Small faults fixed on the day if you approve.</p></li>
<li><h3>Certificate and reminder</h3><p>Certificates emailed to you, and a reminder set before each one expires.</p></li>
</ol>
{b.book_btn("btn-primary", "Book an inspection")}
</div>
</div></section>

<section class="section section-soft" aria-labelledby="area-h"><div class="wrap">
<div class="intro" data-reveal><p class="tag">Areas we cover</p><div>
<h2 id="area-h">Based in Whitechapel, covering {R} miles</h2>
<p class="section-lede">East London gets the quickest appointments. We go anywhere inside the circle, from Watford to Basildon and Enfield to Croydon.</p></div></div>
<div class="two areas-home">
<div data-reveal><ul class="area-rows">{area_rows}</ul>
<p><a class="more" href="/areas/">All areas we cover {icon("arrow")}</a></p></div>
<div class="map" data-reveal="zoom" style="--d:.1s">{b.map_svg()}</div>
</div>
</div></section>

<section class="section" aria-label="Free certificate reminder"><div class="wrap" data-reveal>{reminder}</div></section>

{H.reviews_block()}

{H.faq_section(home_faqs, "Questions landlords ask us", alt=True)}
'''
    P.append(dict(path="/", title="Landlord Safety Certificates East London | Gas, EICR & Fire",
                  description=f"Gas safety, EICR and fire safety certificates for landlords within {R} miles of Whitechapel. One qualified engineer, one visit. EICR + gas from {b.money(b.quote_calc('flat', 2, ['eicr', 'gas'])['total_inc'])}.",
                  body=home_body, js_extra=PICKJS, quote=False, cta=True,
                  schema=[{"@type": "WebSite", "@id": f"{b.SITE}/#website", "url": b.SITE + "/", "name": C["business_name"], "publisher": {"@id": b.BIZ_ID}, "inLanguage": "en-GB"},
                          b.faq_schema(home_faqs)]))

    # ======================================================================== SERVICES HUB
    def group_board(title, ic, rows):
        return f'<h2 class="price-group-h">{icon(ic)}{title}</h2>' + price_board(rows)
    svc_body = page_head([("Home", "/"), ("Services", "/services/")], "Safety certificates and electrical work",
                         "Everything a rental needs from an electrician and Gas Safe engineer, apart from full rewires. Book them on their own or together to save.") + f'''
<section class="section" style="padding-top:2rem"><div class="wrap">
{group_board("Electrical", "zap", [
    ("eicr_flat", "EICR (electrical safety certificate)", "Required at least every 5 years for every private rental in England.", "/eicr/"),
    ("hourly", "EICR remedial works", "Clearing C1, C2 and FI codes so your property passes, with written confirmation for tenants and council.", "/eicr-remedial-works/"),
    ("consumer_unit", "Consumer unit replacement", "Old fuse box out, new RCD-protected metal unit in, tested and notified.", "/consumer-unit-replacement/"),
    ("hourly", "Fault finding and repairs", "Tripping RCDs, dead circuits, sockets, lights and burning smells.", "/electrical-fault-finding/"),
    ("pat", "PAT testing", "Appliance checks for furnished lets and HMOs, added to another visit.", "/pat-testing/"),
])}
{group_board("Gas", "flame", [
    ("gas_safety", "Gas safety certificate (CP12)", "Required every 12 months for every rental with a gas appliance.", "/gas-safety-certificate/"),
    ("boiler_service", "Boiler service", "Annual service to keep the boiler efficient and its warranty valid.", "/boiler-service/"),
])}
{group_board("Fire", "bell", [
    ("fire_alarm_test", "Fire alarm testing", "Tests and certificates for HMO and block alarm systems.", "/fire-alarm/"),
    ("smoke_co_alarms", "Smoke and CO alarms fitted", "Checked, fitted or replaced to meet the 2022 alarm regulations.", "/fire-alarm/"),
    ("emergency_lighting", "Emergency lighting test", "Annual full-duration test and certificate.", "/emergency-lighting/"),
    ("fra", "Fire risk assessment", "For HMOs, common parts of blocks and small commercial premises.", "/fire-risk-assessment/"),
])}
{group_board("Energy and commercial", "leaf", [
    ("epc", "EPC (energy certificate)", "Needed before you advertise. Rentals must rate E or above.", "/epc/"),
    ("eicr_commercial", "Commercial properties", "EICRs, emergency lighting and fire alarm testing for shops and offices.", "/commercial/"),
])}
<p class="note" style="margin-top:2rem">Prices include VAT. Items under {b.MIN_TXT} are add-ons to another visit; on their own, the minimum visit charge applies. We don't take on full rewires.</p>
</div></section>'''
    P.append(dict(path="/services/", title="Landlord Certificates & Electrical Services | East London",
                  description="EICRs, gas safety certificates, fire alarm and emergency lighting tests, EPCs, PAT testing, remedial works and consumer units for landlords in East London.",
                  body=svc_body, crumbs=[("Home", "/"), ("Services", "/services/")]))

    # ======================================================================== EICR
    eicr_faqs = [
        ("How often does a rental property need an EICR?",
         "At least every five years, or sooner if the last report says so. HMO licences sometimes set a shorter period. A new tenancy doesn't need a new EICR if the current one is still in date."),
        ("Do I need to be there for the EICR?",
         "No. Most landlords aren't. We arrange access with your tenant or collect keys, and email you the report afterwards."),
        ("Will the power be off during the test?",
         "Yes, in short spells while each circuit is tested. Let your tenant know so they can save work on computers and keep the fridge closed."),
        ("Can I use an Electrical Installation Certificate instead?",
         "If the property was fully rewired, or newly built, and has an Electrical Installation Certificate less than five years old, that counts until it's five years old. After that you need an EICR."),
        ("What happens if my EICR is unsatisfactory?",
         "You have 28 days, or less if the report says so, to have the C1, C2 and FI items fixed. Then you send written confirmation of the work to your tenants and council within 28 days of it being done. We can do the repairs, often on the same visit."),
        ("Do HMOs cost more?",
         f"Yes, because there are usually more circuits and more rooms to test. We add {ptx('eicr_hmo_room')} per lettable room to the house price. The <a href=\"/#price\">price picker</a> works it out for you."),
    ]
    eicr_body = page_head([("Home", "/"), ("Services", "/services/"), ("EICR", "/eicr/")], "EICR for landlords in East London",
                          f"The electrical safety report every private landlord in England needs at least every five years. From {ptx('eicr_flat')} for a flat, with the report emailed to you.",
                          book=b.book_href("flat", 2, ["eicr"])) + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap layout-side"><div class="prose">
{in_short("What is an EICR and what does it cost?", f"An EICR (Electrical Installation Condition Report) is a full inspection and test of a property's fixed wiring, carried out by a qualified electrician. Private landlords in England must have one at least every five years. A flat takes about 2–3 hours and costs from {ptx('eicr_flat')}. A house of up to 3 bedrooms takes 3–4 hours and costs from {ptx('eicr_house')}.")}

<h2>What the law asks of landlords</h2>
<p>The Electrical Safety Standards in the Private Rented Sector (England) Regulations 2020 say you must:</p>
<ul>
<li>have the electrical installation inspected and tested by a qualified person at least every five years</li>
<li>give a copy of the report to existing tenants within 28 days of the inspection</li>
<li>give a copy to new tenants before they move in</li>
<li>give a copy to the council within 7 days if they ask for one</li>
<li>complete any remedial work or further investigation within 28 days, or less if the report says so</li>
<li>send written confirmation that the work is done to your tenants and the council within 28 days of finishing it</li>
</ul>
<p>Councils can fine landlords up to £30,000 for breaches. Many London boroughs also ask for a current EICR when you apply for a property licence.</p>

<h2>What we test</h2>
<ul>
<li>The consumer unit (fuse board), its protective devices and RCD trip times</li>
<li>Earthing and the bonding to gas and water pipes</li>
<li>Every circuit: insulation resistance, continuity and polarity</li>
<li>Sockets, switches, light fittings and fixed appliances such as showers and cookers</li>
<li>Signs of overheating, damage, wear and DIY work</li>
</ul>

<h2>How long it takes and what it costs</h2>
<table><thead><tr><th>Property</th><th>Time on site</th><th>From</th></tr></thead><tbody>
<tr><td>Studio or 1–2 bed flat</td><td>2–3 hours</td><td>{ptx("eicr_flat")}</td></tr>
<tr><td>House, up to 3 bedrooms</td><td>3–4 hours</td><td>{ptx("eicr_house")}</td></tr>
<tr><td>HMO</td><td>Half to full day</td><td>House price + {ptx("eicr_hmo_room")} per room</td></tr>
</tbody></table>

<h2>What the codes on your report mean</h2>
<table><thead><tr><th>Code</th><th>Meaning</th><th>Fails the report?</th></tr></thead><tbody>
<tr><td><span class="code-chip c1">C1</span></td><td>Danger present. Immediate action needed.</td><td>Yes</td></tr>
<tr><td><span class="code-chip c2">C2</span></td><td>Potentially dangerous. Urgent remedial action needed.</td><td>Yes</td></tr>
<tr><td><span class="code-chip fi">FI</span></td><td>Further investigation needed without delay.</td><td>Yes</td></tr>
<tr><td><span class="code-chip c3">C3</span></td><td>Improvement recommended.</td><td>No</td></tr>
</tbody></table>
<p>One C1, C2 or FI makes the whole report unsatisfactory. If yours fails, see <a href="/eicr-remedial-works/">EICR remedial works</a>.</p>

<h2>EICR and gas safety in one visit</h2>
<p>The engineer is Gas Safe registered as well, so your <a href="/gas-safety-certificate/">gas safety certificate</a> can be done on the same day. Your tenant gives access once, and the two together cost {b.money(b.quote_calc("flat", 2, ["eicr", "gas"])["total_inc"])} for a 2-bed flat. See <a href="/landlord-bundles/">landlord bundles</a>.</p>

{b.faq_html(eicr_faqs, "EICR questions", "eicr-faq")}
{b.reviewed_line()}
{related([("EICR remedial works", "/eicr-remedial-works/"), ("Consumer unit replacement", "/consumer-unit-replacement/"), ("Gas safety certificate", "/gas-safety-certificate/"), ("Landlord bundles", "/landlord-bundles/")])}
</div>
{side("Book an EICR", "eicr_flat", ["Report emailed to you", "Access arranged with your tenant", "Repairs quoted from the report"], b.book_href("flat", 2, ["eicr"]))}
</div></section>
<section class="section section-alt" aria-label="Code checker"><div class="wrap two"><div><h2>What do the codes on your report mean?</h2><p class="lede">Pick the worst code on your report. The checker tells you what it means, your deadline and what the fix usually costs.</p></div>{checker("h3")}</div></section>'''
    P.append(dict(path="/eicr/", title=f"Landlord EICR East London from {b.money(b.inc('eicr_flat'))} | Landlord Safety First",
                  description=f"Landlord EICR in East London from {ptx('eicr_flat')}. Report emailed to you, access arranged with your tenant, and any repairs quoted from the report.",
                  body=eicr_body, js_extra=CODESJS, crumbs=[("Home", "/"), ("Services", "/services/"), ("EICR", "/eicr/")], preselect="EICR (electrical certificate)",
                  schema=[b.service_schema("EICR (Electrical Installation Condition Report) for landlords", "/eicr/", "Inspection and testing of fixed electrical installations in privately rented homes, as required every five years by the 2020 regulations.", "eicr_flat", "Electrical inspection"), b.faq_schema(eicr_faqs)]))

    # ======================================================================== REMEDIAL
    rem_faqs = [
        ("Do I have to use the electrician who did my EICR?",
         "No. Any qualified electrician can do the remedial work. Many landlords get a second quote, especially when the original inspector's repair quote looks high."),
        ("What if I think a C2 has been over-graded?",
         "Send us the report. If an item looks over-coded, we'll explain why. If we agree it doesn't need the work quoted, we'll tell you. We won't invent work."),
        ("What paperwork do I get?",
         "A Minor Electrical Installation Works Certificate or an Electrical Installation Certificate, depending on the job, plus written confirmation that each item on the report has been put right. Send that confirmation, with the original report, to your tenants and the council."),
        ("Do I need a whole new EICR after the repairs?",
         "Not by law. The regulations ask for written confirmation that the remedial work is done. Some councils, licences or letting arrangements ask for a fresh satisfactory report. We can do one if you need it."),
        ("Can you fix the codes on the same day as the inspection?",
         "Often, yes. If we're doing the EICR and the faults are small, such as a damaged socket or missing bonding, we can usually fix them before we leave with your approval."),
        ("Do you charge a diagnostic fee?",
         f"No separate diagnostic fee. Remedial work is priced item by item from the report before we start. Labour is {HOURLY} per hour, one-hour minimum."),
    ]
    rem_body = page_head([("Home", "/"), ("Services", "/services/"), ("EICR remedial works", "/eicr-remedial-works/")], "EICR remedial works in East London",
                         "Failed EICR? Send us the report. We price each C1, C2 and FI item, fix them inside your 28 days, and give you the written confirmation the law asks for.", book="#quote") + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap layout-side"><div class="prose">
{in_short("What are EICR remedial works?", f"Remedial works are the repairs needed to clear the C1, C2 and FI codes that make an EICR unsatisfactory. Landlords must complete them within 28 days of the inspection, or sooner if the report says, and then send written confirmation to tenants and the council. We charge from {HOURLY}, and most single items take one to two hours.")}

<h2>The 28-day rule</h2>
<p>The clock starts on the day of the inspection, not the day you read the report. If the report gives a shorter deadline, that applies. Once the work is finished, you have another 28 days to send written confirmation from the electrician to your tenants and the council. Send us the report on the day you get it and we can usually start within the week.</p>

<h2>Common C2 items we fix</h2>
<ul>
<li>No RCD protection on sockets that could power equipment outdoors</li>
<li>Missing or undersized main bonding to gas and water pipes</li>
<li>No earth on lighting circuits feeding metal fittings</li>
<li>Cracked or scorched sockets, switches and ceiling roses</li>
<li>Exposed or damaged cables, and cables without proper protection</li>
<li>Bathroom issues: wrong fittings in the wrong zone, missing supplementary bonding</li>
<li>An old consumer unit that can't take RCD protection, which needs a <a href="/consumer-unit-replacement/">consumer unit replacement</a></li>
</ul>

<h2>How we price it</h2>
<p>We go through the report line by line and price each item, so you can see where the money goes. There's no lump sum covering work you can't check, and no separate diagnostic fee. Small items are charged at {ptx("hourly")} per hour, one-hour minimum. Bigger jobs such as a new consumer unit get a fixed price.</p>
<p>Any C3 items are listed separately. You don't have to do them, but adding them while we're already there costs less than a second visit.</p>

<h2>A second opinion on your report</h2>
<p>Cheap EICRs are sometimes followed by expensive repair quotes. If a code doesn't look right, ask us. We'll look at the photos and the observation, and tell you honestly whether the work is needed.</p>

<h2>What we don't do</h2>
<p>Full rewires. We focus on repairs, upgrades and consumer units. If a report shows the wiring needs replacing throughout, we'll tell you rather than patching it.</p>

{b.faq_html(rem_faqs, "Remedial works questions", "rem-faq")}
{b.reviewed_line()}
{related([("EICR", "/eicr/"), ("Consumer unit replacement", "/consumer-unit-replacement/"), ("Fault finding", "/electrical-fault-finding/"), ("Prices", "/prices/")])}
</div>
{side("Send us your report", "hourly", ["Every item priced separately", "No separate diagnostic fee", "Written confirmation for tenants and council"], "#quote", "Get a remedial quote")}
</div></section>
<section class="section section-alt" aria-label="Code checker"><div class="wrap two"><div><h2>Not sure what your codes mean?</h2><p class="lede">Pick the worst code on your report. The checker tells you what it means, your deadline and what the fix usually costs.</p></div>{checker("h3")}</div></section>'''
    P.append(dict(path="/eicr-remedial-works/", title="EICR Remedial Works East London | Fix C1, C2 & FI Codes",
                  description=f"Failed EICR? We price every C1, C2 and FI item, fix it inside your 28 days and give you written confirmation for tenants and council. From {HOURLY}.",
                  body=rem_body, js_extra=CODESJS, crumbs=[("Home", "/"), ("Services", "/services/"), ("EICR remedial works", "/eicr-remedial-works/")], preselect="EICR remedial works",
                  quote_heading="Send us your EICR for a quote",
                  schema=[b.service_schema("EICR remedial works", "/eicr-remedial-works/", "Repairs to clear C1, C2 and FI observations on an unsatisfactory EICR, with written confirmation for tenants and the local authority.", "hourly", "Electrical repair"), b.faq_schema(rem_faqs)]))

    # ======================================================================== CONSUMER UNIT
    cu_faqs = [
        ("How long does a consumer unit replacement take?",
         "Most of a working day for a typical flat or house. The power is off for about 4–6 hours while we change the board and test every circuit."),
        ("Does a consumer unit change need Building Regulations approval?",
         f"Yes. It's notifiable work under Part P. We notify it through our scheme ({t('electrical_scheme')}), and you get a Building Regulations compliance certificate in the post, as well as our Electrical Installation Certificate."),
        ("Why might the price change on the day?",
         "An old fuse box can hide faults that the new RCDs will detect, such as a damaged cable or a neutral-to-earth fault. If testing finds one, we stop, show you, and price it before carrying on."),
        ("RCBOs or a dual-RCD board?",
         "RCBOs give every circuit its own protection, so one fault only switches off one circuit. For rented property we recommend RCBOs because a single fault doesn't leave the tenant without lights and sockets. A dual-RCD board costs less."),
        ("Can my tenants stay in during the work?",
         "Yes, but they'll have no power for part of the day. We agree the time with them in advance and tell them to keep the fridge and freezer closed."),
        ("Will a new consumer unit make my EICR satisfactory?",
         "It clears codes about the board itself and missing RCD protection. Other items on the report, like damaged accessories or missing bonding, need fixing separately. We'll quote them together."),
    ]
    cu_body = page_head([("Home", "/"), ("Services", "/services/"), ("Consumer unit replacement", "/consumer-unit-replacement/")], "Consumer unit replacement for landlords",
                        f"Replacing the old fuse box is the fix for many failed EICRs. From {ptx('consumer_unit')}, usually done in a day, certified and notified to Building Control.", book="#quote") + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap layout-side"><div class="prose">
{in_short("How much is a consumer unit replacement in London?", f"With us, replacing a consumer unit (fuse box) starts at {ptx('consumer_unit')} for up to 8 ways. That includes the new metal unit with RCD protection, testing every circuit, an Electrical Installation Certificate and Building Regulations notification. Most jobs take a day, with the power off for about 4–6 hours.")}

<h2>Signs your rental needs a new consumer unit</h2>
<ul>
<li>Rewireable fuses (the old ceramic carriers with fuse wire)</li>
<li>No RCD protection, often coded C2 on an EICR</li>
<li>Scorch marks, a burning smell or a hot board</li>
<li>A cracked or damaged plastic unit, or one with missing blanks that leave live parts exposed</li>
<li>Breakers tripping with no clear cause</li>
</ul>

<h2>What's included</h2>
<ul>
<li>A metal (non-combustible) consumer unit, which has been required for homes since 2016</li>
<li>RCBOs or RCD protection for every circuit, plus surge protection where required</li>
<li>Testing every circuit before and after the change</li>
<li>Clear circuit labelling, so your tenant knows which switch does what</li>
<li>An Electrical Installation Certificate</li>
<li>Building Regulations notification through our scheme</li>
<li>Removal of the old board</li>
</ul>

<h2>Why the price can change</h2>
<p>An old board with fuses doesn't detect some faults that an RCD will. When the new unit goes in, a damaged cable that the fuses have been living with can start tripping it. We test before we start, so most surprises show up early. If something turns up mid-job, we stop, show you and price it. Nothing extra happens without your yes.</p>

<h2>Planning around your tenant</h2>
<p>We agree the date with your tenant directly, give them a time the power will be off, and get the essential circuits (fridge, lights) back on first.</p>

{b.faq_html(cu_faqs, "Consumer unit questions", "cu-faq")}
{b.reviewed_line()}
{related([("EICR remedial works", "/eicr-remedial-works/"), ("EICR", "/eicr/"), ("Fault finding", "/electrical-fault-finding/"), ("Prices", "/prices/")])}
</div>
{side("Replace your consumer unit", "consumer_unit", ["Fixed price before we book", "Done in a day", "Certificate and Building Regs notification included"], "#quote", "Get a fixed price")}
</div></section>'''
    P.append(dict(path="/consumer-unit-replacement/", title=f"Consumer Unit Replacement London from {b.money(b.inc('consumer_unit'))} | Fuse Box",
                  description=f"Consumer unit (fuse box) replacement for landlords and homeowners from {ptx('consumer_unit')}. Metal RCD-protected board, tested, certified and notified. Usually done in a day.",
                  body=cu_body, crumbs=[("Home", "/"), ("Services", "/services/"), ("Consumer unit replacement", "/consumer-unit-replacement/")], preselect="Consumer unit replacement",
                  schema=[b.service_schema("Consumer unit replacement", "/consumer-unit-replacement/", "Replacement of old fuse boxes with metal RCD/RCBO consumer units, fully tested, certified and notified under Part P.", "consumer_unit", "Consumer unit installation"), b.faq_schema(cu_faqs)]))

    # ======================================================================== FAULT FINDING
    sb = C["sister_brand"]
    ff_faqs = [
        ("Why does my RCD keep tripping?",
         "Usually a fault on one circuit or one appliance: moisture in an outdoor socket, a failing kettle or immersion heater, or a damaged cable. Unplugging everything and resetting tells you whether it's an appliance or the wiring. If it trips with everything unplugged, it's the wiring and needs an electrician."),
        ("How much does fault finding cost?",
         f"{ptx('hourly')} for the first hour, then charged per half hour. Most faults in flats are found within the first hour. Parts are extra and we tell you before fitting them."),
        ("Is it an emergency?",
         f"If there's burning, smoke or sparking, switch off at the consumer unit and keep clear. For urgent call-outs, our sister company <a href=\"{esc(sb['url'])}\" rel=\"noopener\">{esc(sb['name'])}</a> handles emergency electrical repairs."),
        ("Can you speak to my tenant directly?",
         "Yes. Give us their number and we'll arrange access, ask the right questions before we arrive, and update you when it's fixed."),
    ]
    ff_body = page_head([("Home", "/"), ("Services", "/services/"), ("Fault finding and repairs", "/electrical-fault-finding/")], "Electrical fault finding and repairs",
                        f"Tripping RCD, a dead circuit, a burning smell. We trace the fault, make it safe and fix it, usually in one visit. {HOURLY} for the first hour.", book="#quote") + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap layout-side"><div class="prose">
{in_short("How much does an electrician charge to find a fault?", f"We charge {ptx('hourly')} for the first hour, then per half hour. That's {b.money(C['prices']['hourly']['ex'])} + VAT. Most faults in rented flats are found and fixed in a single visit. If something is dangerous, we make it safe before we leave and price the permanent repair.")}
<p class="note">{icon("alert")} <strong>Emergency right now?</strong> Our sister company <a href="{esc(sb["url"])}" rel="noopener">{esc(sb["name"])}</a> handles urgent electrical call-outs.</p>

<h2>Faults we find and fix</h2>
<ul>
<li>RCDs or breakers that keep tripping</li>
<li>Sockets, lights or a whole circuit that's gone dead</li>
<li>Burning smells, buzzing, or warm sockets and switches</li>
<li>Flickering lights</li>
<li>Electric showers, cookers and immersion heaters not working</li>
<li>Water damage from a leak upstairs</li>
</ul>

<h2>What to tell your tenant right now</h2>
<ol>
<li>If there's burning, smoke or sparking, switch off the main switch on the consumer unit and keep away from it.</li>
<li>If something keeps tripping, unplug everything on that circuit and try resetting it.</li>
<li>If it resets, plug things back in one at a time. The one that trips it is the faulty appliance.</li>
<li>If it trips with everything unplugged, leave it off and call us. It's a wiring fault.</li>
</ol>

<h2>How we keep it simple for landlords</h2>
<p>Give us your tenant's number. We arrange the visit, find the fault, and send you a short note with what we found, what we fixed and a photo. If it needs a part or more time, we price it and ask you first.</p>

{b.faq_html(ff_faqs, "Fault finding questions", "ff-faq")}
{b.reviewed_line()}
{related([("EICR remedial works", "/eicr-remedial-works/"), ("Consumer unit replacement", "/consumer-unit-replacement/"), ("EICR", "/eicr/")])}
</div>
{side("Report a fault", "hourly", ["We contact your tenant", "Made safe before we leave", "Parts priced before fitting"], "#quote", "Book a visit")}
</div></section>'''
    P.append(dict(path="/electrical-fault-finding/", title="Electrical Fault Finding East London | Landlord Safety First",
                  description=f"Tripping RCD, dead circuit or burning smell in a rental? {HOURLY} for the first hour. We contact your tenant and fix it, usually in one visit.",
                  body=ff_body, crumbs=[("Home", "/"), ("Services", "/services/"), ("Fault finding and repairs", "/electrical-fault-finding/")], preselect="Fault finding / repair",
                  schema=[b.service_schema("Electrical fault finding and repairs", "/electrical-fault-finding/", "Tracing and repairing electrical faults in rented homes: tripping RCDs, dead circuits, damaged accessories.", "hourly", "Electrical repair"), b.faq_schema(ff_faqs)]))

    # ======================================================================== GAS SAFETY
    gas_faqs = [
        ("How often do landlords need a gas safety certificate?",
         "Every 12 months. You can have the check done up to two months before the current one expires and keep the original expiry date, so you don't lose time."),
        ("Is a gas safety check the same as a boiler service?",
         "No. The safety check confirms appliances are safe to use. A service cleans and adjusts the boiler to keep it working well. Many landlords book both together. Your boiler warranty may require an annual service."),
        ("What happens if an appliance fails?",
         "If it's classed as 'Immediately Dangerous' we have to disconnect it, with the tenant's permission. If it's 'At Risk' we'll advise turning it off. We tell you exactly what's wrong and price the repair."),
        ("How long do I keep gas safety records?",
         "At least two years. Give a copy to existing tenants within 28 days of the check, and to new tenants before they move in."),
        ("Why don't you do £30 gas certificates?",
         "A proper check takes time: tightness test, flue and combustion checks on every appliance, ventilation and safety devices. We'd rather do it properly than fast. Book it with your EICR and the bundle saving brings the price down."),
    ]
    gas_body = page_head([("Home", "/"), ("Services", "/services/"), ("Gas safety certificate", "/gas-safety-certificate/")], "Landlord gas safety certificate (CP12)",
                         f"The annual gas check every rental with a gas appliance needs, by a Gas Safe registered engineer. From {ptx('gas_safety')}, or with your EICR in one visit.",
                         book=b.book_href("flat", 2, ["gas"])) + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap layout-side"><div class="prose">
{in_short("What is a landlord gas safety certificate?", f"A landlord gas safety record, often called a CP12, confirms that every gas appliance, flue and pipe in a rented property has been checked by a Gas Safe registered engineer in the last 12 months. It's a legal requirement under the Gas Safety (Installation and Use) Regulations 1998. Ours start at {ptx('gas_safety')} for a boiler and up to two other appliances.")}

<h2>What the law asks of landlords</h2>
<ul>
<li>A gas safety check on every appliance and flue you provide, every 12 months</li>
<li>The check done by a Gas Safe registered engineer</li>
<li>A copy of the record to existing tenants within 28 days</li>
<li>A copy to new tenants before they move in</li>
<li>Records kept for at least two years</li>
</ul>

<h2>What we check</h2>
<ul>
<li>Gas tightness of the installation</li>
<li>Each appliance's burner pressure or gas rate</li>
<li>Flue flow and spillage tests, and ventilation</li>
<li>Safety devices working correctly</li>
<li>Flue terminals and their position</li>
</ul>

<h2>Do it with your EICR</h2>
<p>The engineer is an electrician as well, so the gas check and <a href="/eicr/">EICR</a> can be done in one visit. Your tenant gives access once, and you get both certificates together. For a 2-bed flat that's {b.money(b.quote_calc("flat", 2, ["eicr", "gas"])["total_inc"])} inc. VAT with the bundle saving.</p>

<h2>Add a boiler service</h2>
<p>A <a href="/boiler-service/">boiler service</a> on the same visit adds {ptx("boiler_service")}. It's not a legal requirement, but most boiler warranties need one every year.</p>

<h2>Smoke and carbon monoxide alarms</h2>
<p>While we're there, we can check your alarms meet the 2022 regulations: a smoke alarm on every storey, and a CO alarm in any room with a fixed combustion appliance such as a gas boiler. See <a href="/fire-alarm/">fire alarm testing</a>.</p>

{b.faq_html(gas_faqs, "Gas safety questions", "gas-faq")}
{b.reviewed_line()}
{related([("EICR", "/eicr/"), ("Boiler service", "/boiler-service/"), ("Fire alarm testing", "/fire-alarm/"), ("Landlord bundles", "/landlord-bundles/")])}
</div>
{side("Book a gas safety check", "gas_safety", [f"Gas Safe no. {t('gas_safe_number')}", "Certificate emailed to you", "Add a boiler service for " + ptx("boiler_service")], b.book_href("flat", 2, ["gas"]))}
</div></section>'''
    P.append(dict(path="/gas-safety-certificate/", title=f"Landlord Gas Safety Certificate (CP12) East London from {b.money(b.inc('gas_safety'))}",
                  description=f"Gas Safe registered landlord gas safety checks (CP12) in East London from {ptx('gas_safety')}. Book with your EICR in one visit and save.",
                  body=gas_body, crumbs=[("Home", "/"), ("Services", "/services/"), ("Gas safety certificate", "/gas-safety-certificate/")], preselect="Gas safety certificate",
                  schema=[b.service_schema("Landlord gas safety certificate (CP12)", "/gas-safety-certificate/", "Annual landlord gas safety checks and records by a Gas Safe registered engineer.", "gas_safety", "Gas safety inspection"), b.faq_schema(gas_faqs)]))

    # ======================================================================== PRICES
    all_rows = [(k, p["label"], p["note"], None) for k, p in C["prices"].items()]
    price_faqs = [
        ("Do your prices include VAT?",
         f"Yes. Every price on this site includes VAT at {int(C['vat_rate']*100)}%. The figure before VAT is shown underneath."),
        ("Is there a minimum charge?",
         f"Yes. The minimum charge for a visit is {b.MIN_TXT}. Smaller items, like an EPC, PAT testing or an alarm check, cost less when you add them to another certificate."),
        ("Is there a call-out charge?",
         b.todo("Confirm with the client whether there is a call-out charge on top of the minimum visit.")),
        ("Do you give fixed quotes?",
         "Yes. For certificates and consumer units we give a fixed price for your property. For remedial work we price each item from your report. Fault finding is charged by the hour, because nobody can know how long a fault takes to find until they look."),
        ("Do you offer discounts for several properties?",
         "Yes. Tell us how many properties you have and when their certificates are due, and we'll quote for the lot."),
    ]
    prices_body = page_head([("Home", "/"), ("Prices", "/prices/")], "Prices",
                            "'From' prices for every job, including VAT. Your fixed price depends on the size of the property, and booking certificates together saves 10–15%.", buttons=False) + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap">
{"" if C.get("prices_confirmed") else '<p class="todo">Prices are placeholders until the client confirms them.</p>'}
<div class="btn-row" style="margin-bottom:2rem">{b.btn("/#price", "Work out your exact price", "btn-primary", "pound")}{b.btn("/landlord-bundles/", "See landlord bundles", "btn-ghost")}</div>
{price_board(all_rows)}
<div class="two" style="margin-top:3rem">
<div class="prose"><h2>Included in every job</h2><ul>
<li>A fixed price agreed before we book</li>
<li>Access arranged with your tenant if you want</li>
<li>Certificates and reports emailed to you</li>
<li>Photos of anything we find or fix</li>
<li>A reminder before each certificate expires</li>
</ul></div>
<div class="prose"><h2>What changes a price</h2><ul>
<li>Property size and number of circuits</li>
<li>HMOs and extra lettable rooms</li>
<li>Access problems, such as a consumer unit behind fitted units</li>
<li>Faults found during the work, always priced and agreed first</li>
</ul></div>
</div>
<div style="margin-top:3rem">{b.faq_html(price_faqs, "Price questions", "price-faq")}</div>
</div></section>'''
    P.append(dict(path="/prices/", title="Landlord Certificate Prices East London | Landlord Safety First",
                  description=f"EICR from {ptx('eicr_flat')}, gas safety from {ptx('gas_safety')}, fire alarm tests from {ptx('fire_alarm_test')}. Bundle two or more and save 10–15%. All prices include VAT.",
                  body=prices_body, crumbs=[("Home", "/"), ("Prices", "/prices/")], schema=[b.faq_schema([f for f in price_faqs if "todo" not in f[1]])]))

    # ======================================================================== AREAS HUB + BOROUGHS
    boroughs = [
        dict(slug="tower-hamlets", name="Tower Hamlets", postcodes=["E1", "E1W", "E2", "E3", "E14"], travel="5–20 minutes",
             h1="Landlord safety certificates in Tower Hamlets",
             lede="We're based in Whitechapel, so Tower Hamlets is home ground. Gas, electrical and fire certificates from Aldgate to the Isle of Dogs.",
             short="Landlords in Tower Hamlets need an EICR at least every five years and an annual gas safety record, like everywhere in England. HMOs with three or more people from two or more households also need an additional HMO licence across the whole borough. We're based in E1, so most Tower Hamlets properties are 5–20 minutes away.",
             licensing="""<h2>Licensing in Tower Hamlets</h2>
<ul>
<li><strong>Additional HMO licensing</strong> covers all 20 wards from 1 April 2024 to 31 March 2029. It applies to properties with three or more people forming two or more households who share facilities, including flats in purpose-built blocks.</li>
<li><strong>Mandatory HMO licensing</strong> applies to HMOs with five or more people, as everywhere in England.</li>
<li><strong>Selective licensing</strong> has applied in Weavers, Whitechapel and Spitalfields &amp; Banglatown. Licences granted there run until they expire, so check the council's site for what applies to your property now.</li>
</ul>
<p>HMO licence applications usually ask for a current EICR and gas safety record, and set fire alarm standards. Getting them done together saves time.</p>""",
             stock="""<h2>What we see in Tower Hamlets properties</h2>
<p>The housing here is mixed: Victorian terraces in Bow and Stepney, ex-council flats across Poplar and Shadwell, and new-build blocks around Canary Wharf, Aldgate and Wapping. Older conversions often fail on missing RCD protection and old consumer units. Newer flats tend to pass, but can have consumer units hidden behind kitchen units.</p>""",
             places="Whitechapel, Stepney, Bow, Mile End, Poplar, Limehouse, Wapping, Shadwell, Bethnal Green, Spitalfields, Canary Wharf, Isle of Dogs",
             council="https://www.towerhamlets.gov.uk/lgnl/housing/Private-tenants-landlords-and-homeowners/Private-Landlords/Selective_Licensing.aspx"),
        dict(slug="hackney", name="Hackney", postcodes=["E2", "E5", "E8", "E9", "N1", "N16"], travel="15–25 minutes",
             h1="Landlord safety certificates in Hackney",
             lede="Hackney brought in new licensing schemes in May 2026, and most private lets now need a licence. We do the EICRs, gas checks and fire safety work they ask for.",
             short="Since 1 May 2026, Hackney has run selective licensing in 17 of its wards and additional HMO licensing across the whole borough, both for five years. That means most private landlords in Hackney need a licence for each property, on top of the usual five-yearly EICR and annual gas safety record. Most Hackney properties are 15–25 minutes from our base in E1.",
             licensing="""<h2>Licensing in Hackney</h2>
<ul>
<li><strong>Selective licensing</strong> from 1 May 2026, for five years, in 17 wards including Hackney Central, Dalston, Homerton, Hackney Downs, Hackney Wick, Brownswood, Cazenove, Clissold and De Beauvoir. It covers homes let to a single household or two sharers.</li>
<li><strong>Additional HMO licensing</strong> borough-wide over the same period, for homes with three or more people forming two or more households.</li>
<li><strong>Mandatory HMO licensing</strong> for HMOs with five or more people.</li>
</ul>
<p>Licence applications and conditions usually require a valid EICR and gas safety record and working smoke and CO alarms. If your EICR is close to expiring, renew it before you apply.</p>""",
             stock="""<h2>What we see in Hackney properties</h2>
<p>Hackney is mostly Victorian and Edwardian terraces split into flats, plus large estates and new blocks around Hackney Wick and Dalston. Conversions are where EICRs most often fail: shared supplies, old consumer units, missing bonding, and circuits nobody can trace after decades of DIY.</p>""",
             places="Hackney Central, Dalston, Homerton, Clapton, Stoke Newington, Stamford Hill, Hackney Wick, Shoreditch, Hoxton, De Beauvoir, London Fields, Haggerston",
             council="https://hackney.gov.uk/check-which-property-licence-you-need"),
        dict(slug="newham", name="Newham", postcodes=["E6", "E7", "E12", "E13", "E15", "E16", "E20"], travel="15–30 minutes",
             h1="Landlord safety certificates in Newham",
             lede="Newham licenses almost every private rental in the borough. We keep your EICR, gas safety and alarms in order so your licence conditions are met.",
             short="Newham has run selective licensing across most of the borough since 1 June 2023, for five years, alongside additional HMO licensing. Licensed properties still need an EICR at least every five years and an annual gas safety record. Most Newham properties are 15–30 minutes from our base in E1.",
             licensing="""<h2>Licensing in Newham</h2>
<ul>
<li><strong>Selective licensing</strong> since 1 June 2023, for five years, across most of the borough's wards.</li>
<li><strong>Additional HMO licensing</strong> for homes with three or more people forming two or more households.</li>
<li><strong>Mandatory HMO licensing</strong> for HMOs with five or more people.</li>
</ul>
<p>Newham enforces its licence conditions actively, and they include keeping gas and electrical certificates current and providing them on request. We can remind you before each one is due.</p>""",
             stock="""<h2>What we see in Newham properties</h2>
<p>Lots of Victorian and inter-war terraces in Forest Gate, Manor Park, East Ham and Plaistow, many split into flats or let as HMOs, plus new developments in Stratford and the Royal Docks. Older terraces are where we fit the most consumer units and fix the most bonding and RCD-related C2s.</p>""",
             places="Stratford, Forest Gate, Manor Park, East Ham, West Ham, Plaistow, Upton Park, Canning Town, Custom House, Beckton, Silvertown, Royal Docks",
             council="https://newham.gov.uk/landlords-newham/rented-property-licensing/7"),
    ]
    bcards = "".join(
        f'<article class="area-card card card-link"><div><h3><a class="stretch" href="/areas/{bo["slug"]}/">{bo["name"]}</a></h3><p>{", ".join(bo["postcodes"])} · {bo["travel"]} from E1</p></div>{icon("arrow")}</article>'
        for bo in boroughs)
    areas_body = page_head([("Home", "/"), ("Areas", "/areas/")], f"Areas we cover: {R} miles from Whitechapel",
                           "We're based in E1. East London gets the quickest appointments, and we cover anywhere inside the circle.") + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap two">
<div class="map">{b.map_svg()}</div>
<div>
<h2>Borough guides</h2>
<p>Each borough has its own licensing rules, and they change which certificates you need and when. Our guides explain what applies where.</p>
<div class="area-cards">{bcards}</div>
<h2 style="margin-top:2rem">Towns and areas</h2>
<ul class="areas-list">{"".join(f"<li>{esc(n)}</li>" for n, *_ in b.TOWNS)}</ul>
<p class="small">Not listed? If you're within {R} miles of Whitechapel, we cover you. Send your postcode in the form below.</p>
</div>
</div></section>'''
    P.append(dict(path="/areas/", title=f"Areas Covered: {R} Miles from Whitechapel | Landlord Safety First",
                  description=f"Landlord gas, electrical and fire certificates up to {R} miles from Whitechapel: Tower Hamlets, Hackney, Newham, Romford, Ilford, Watford and more.",
                  body=areas_body, crumbs=[("Home", "/"), ("Areas", "/areas/")]))

    for bo in boroughs:
        path = f"/areas/{bo['slug']}/"
        trail = [("Home", "/"), ("Areas", "/areas/"), (bo["name"], path)]
        q = f"What do landlords in {bo['name']} need?"
        bf = [(q, bo["short"]),
              (f"How quickly can you get to {bo['name']}?", f"Most {bo['name']} properties are {bo['travel']} from our base in Whitechapel, depending on traffic. Certificates can usually be booked within a few working days."),
              (f"Do you cover all of {bo['name']}?", f"Yes: {bo['places']}.")]
        pcs = "".join(f"<li>{p}</li>" for p in bo["postcodes"])
        body = page_head(trail, bo["h1"], bo["lede"]) + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap layout-side"><div class="prose">
{in_short(q, bo["short"])}
<h2>Postcodes and travel time</h2>
<p>We cover every {bo["name"]} postcode, including:</p>
<ul class="postcodes">{pcs}</ul>
<p>Typical drive from our base in E1: <strong>{bo["travel"]}</strong>, depending on traffic.</p>
<h2>A recent job in {bo["name"]}</h2>
<p>{b.todo(f"One real job done in {bo['name']}: the area (not the address), what was found and what was fixed. Add a photo if the landlord agrees.")}</p>
{bo["licensing"]}
<p class="small">Licensing details checked November 2026. Always confirm with <a href="{bo["council"]}" rel="noopener">{bo["name"]} Council</a> before applying.</p>
{bo["stock"]}
<h2>Services in {bo["name"]}</h2>
<ul>
<li><a href="/eicr/">EICR</a> from {ptx("eicr_flat")}</li>
<li><a href="/gas-safety-certificate/">Gas safety certificate</a> from {ptx("gas_safety")}</li>
<li><a href="/landlord-bundles/">Landlord bundles</a>, saving 10–15%</li>
<li><a href="/eicr-remedial-works/">EICR remedial works</a> from {HOURLY}</li>
<li><a href="/fire-alarm/">HMO fire alarm testing</a> from {ptx("fire_alarm_test")}</li>
</ul>
<h2>Areas in {bo["name"]}</h2>
<p>{bo["places"]}.</p>
{b.faq_html(bf, f"{bo['name']} questions", "b-faq")}
{b.reviewed_line()}
</div>
<div><div class="map" style="margin-bottom:1.25rem">{b.map_svg(bo["slug"])}</div>
{side(f"Book in {bo['name']}", "eicr_flat", [f"{bo['travel']} from our base", "Access arranged with your tenant", "Certificates emailed to you"], b.book_href("flat", 2, ["eicr", "gas"]))}</div>
</div></section>'''
        P.append(dict(path=path, title=f"Landlord Certificates {bo['name']} | EICR, Gas Safety & Fire",
                      description=f"EICRs from {ptx('eicr_flat')}, gas safety and fire safety certificates for landlords in {bo['name']} ({', '.join(bo['postcodes'][:4])}). Licensing rules explained. {bo['travel']} from our base.",
                      body=body, crumbs=trail, schema=[b.faq_schema(bf)]))

    # ======================================================================== ABOUT
    photo = (f'<img class="hero-photo" src="/{esc(engineer_photo)}" alt="{esc(b.plain("engineer_name", "Our engineer"))}" width="800" height="1000" loading="lazy">' if engineer_photo
             else f'<div class="photo-slot">{icon("user")}<p>{b.todo("Add a real photo of the engineer and the van here (set engineer_photo in site.config.json).")}</p></div>')
    about_body = page_head([("Home", "/"), ("About", "/about/")], "The engineer who books you is the engineer who turns up",
                           f"Landlord Safety First is a small team led by {t('engineer_name')}, a qualified electrician who is also Gas Safe registered and fire safety trained.", buttons=False) + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap two">
<div class="prose">
<p class="todo">TODO: one paragraph in the engineer's own words: how long he's been qualified, where he trained, why he works with landlords.</p>
<h2>How we work</h2>
<ul>
<li><strong>Direct.</strong> You speak to the engineer, not a call centre or an agency.</li>
<li><strong>One person, three trades.</strong> Gas, electrical and fire checks in one visit, by one qualified engineer.</li>
<li><strong>Priced up front.</strong> A fixed price or an item-by-item quote before any work.</li>
<li><strong>Honest about what's needed.</strong> If a code looks over-graded or a job isn't worth doing, we say so.</li>
<li><strong>Paperwork sorted.</strong> Certificates emailed, and a reminder before the next one is due.</li>
</ul>
<h2>What we don't do</h2>
<p>Full rewires. We'd rather do certificates, repairs and upgrades well than stretch into everything. For urgent electrical call-outs, our sister company <a href="{esc(sb["url"])}" rel="noopener">{esc(sb["name"])}</a> is on hand.</p>
</div>
<div>{photo}<div style="margin-top:1.25rem">{creds_block()}</div><p class="small" style="margin-top:1rem">Check our registration on the <a href="https://www.gassaferegister.co.uk/" rel="noopener">Gas Safe Register</a> and the {t("electrical_scheme")} website.</p></div>
</div></section>
{H.reviews_block()}'''
    P.append(dict(path="/about/", title="About Us | Landlord Safety First, Whitechapel E1",
                  description="Landlord Safety First is a Whitechapel-based electrician and Gas Safe engineer working directly with landlords across East London. No call centre, no subcontractors.",
                  body=about_body, crumbs=[("Home", "/"), ("About", "/about/")], cta=True, quote=False,
                  schema=[{"@type": "AboutPage", "url": b.SITE + "/about/", "about": {"@id": b.BIZ_ID}}]))

    # ======================================================================== CONTACT
    contact_body = page_head([("Home", "/"), ("Contact", "/contact/")], "Contact us",
                             f"Call, WhatsApp or use the form. {t('response_promise')}.", buttons=False) + f'''
<section class="section" style="padding:2.5rem 0 0"><div class="wrap two">
<div class="prose">
<h2>Phone</h2><p><a href="{b.phone_href()}" style="font-size:1.5rem;font-weight:700">{t("phone_display")}</a></p>
<h2>Email</h2><p><a href="mailto:{esc(C["email"])}">{esc(C["email"])}</a></p>
<h2>Hours</h2><p>{t("hours_display")}</p>
</div>
<div class="prose">
<h2>Where we work</h2><p>Based in Whitechapel, London {esc(C["base"]["postcode_area"])}. We cover anywhere within {R} miles. <a href="/areas/">See the map</a>.</p>
<h2>Sending an EICR?</h2><p>A photo or PDF of every page is ideal, especially the observations page. We price remedial work straight from it.</p>
<h2>Electrical emergency?</h2><p>Our sister company <a href="{esc(sb["url"])}" rel="noopener">{esc(sb["name"])}</a> handles urgent call-outs.</p>
</div>
</div></section>'''
    P.append(dict(path="/contact/", title="Contact | Landlord Safety First, Whitechapel E1",
                  description=f"Get a price for an EICR, gas safety certificate, fire alarm test or remedial works. Based in Whitechapel, covering {R} miles.",
                  body=contact_body, crumbs=[("Home", "/"), ("Contact", "/contact/")], quote_heading="Send us a message",
                  schema=[{"@type": "ContactPage", "url": b.SITE + "/contact/", "about": {"@id": b.BIZ_ID}}]))

    # ======================================================================== FAQ HUB
    faq_all = home_faqs + [eicr_faqs[3], rem_faqs[1], rem_faqs[3], cu_faqs[1], gas_faqs[1], ff_faqs[0]]
    faq_body = page_head([("Home", "/"), ("Landlord FAQ", "/faq/")], "Landlord safety certificate FAQ",
                         "Straight answers to the questions landlords ask us most.", buttons=False) + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap prose" style="max-width:860px">{b.faq_html(faq_all, "Questions and answers", "all-faq")}{b.reviewed_line()}</div></section>'''
    P.append(dict(path="/faq/", title="Landlord Safety Certificate FAQ | Landlord Safety First",
                  description="How often landlords need an EICR and gas safety certificate, the 28-day rule, HMO and EPC requirements, smoke and CO alarm rules, and what it all costs.",
                  body=faq_body, crumbs=[("Home", "/"), ("Landlord FAQ", "/faq/")], schema=[b.faq_schema(faq_all)]))

    # ======================================================================== the rest
    import content_more
    P += content_more.pages(b, H)

    # ======================================================================== 404
    P.append(dict(path="/404", title="Page not found | Landlord Safety First", description="This page doesn't exist.", noindex=True,
                  body=f'''<section class="page-head"><div class="wrap"><h1>That page doesn't exist</h1>
<p class="lede">It may have moved. Try one of these, or call {t("phone_display")}.</p>
<ul class="related" style="margin-top:1.5rem"><li><a href="/">Home</a></li><li><a href="/landlord-bundles/">Bundles</a></li><li><a href="/eicr/">EICR</a></li><li><a href="/gas-safety-certificate/">Gas safety</a></li><li><a href="/contact/">Contact</a></li></ul></div></section>''',
                  quote=False))
    return P


def llms_txt(b, pages):
    C = b.CFG
    R = C["base"]["radius_miles"]
    p = lambda k: b.price_txt(k)
    phone = b.plain("phone_display", "see website")
    lines = [
        f"# {C['business_name']}",
        "",
        f"> Landlord safety certificates in East London, by a qualified electrician who is also Gas Safe registered, based in Whitechapel (London E1) and covering anywhere within {R} miles. "
        "Services: EICRs, gas safety certificates (CP12), boiler servicing, fire alarm and emergency lighting tests, fire risk assessments, EPCs, PAT testing, EICR remedial works, consumer unit replacement and fault finding. "
        "Customers: private landlords, homeowners and small businesses. Does not do full rewires.",
        "",
        "## Key facts",
        f"- Phone: {phone}",
        f"- Email: {C['email']}",
        f"- Base: Whitechapel, London {C['base']['postcode_area']}; service radius {R} miles",
        f"- Gas Safe Register number: {b.plain('gas_safe_number', 'pending')}",
        f"- Electrical scheme: {b.plain('electrical_scheme', 'pending')}",
        f"- Sister company for emergency electrical repairs: {C['sister_brand']['name']} ({C['sister_brand']['url']})",
        "",
        "## Prices (from, including VAT)",
        f"- EICR, flat: {p('eicr_flat')}",
        f"- EICR, house: {p('eicr_house')}",
        f"- Gas safety certificate (CP12): {p('gas_safety')}",
        f"- EICR + gas safety for a 2-bed flat, one visit: {b.money(b.quote_calc('flat', 2, ['eicr', 'gas'])['total_inc'])}",
        f"- Fire alarm test: {p('fire_alarm_test')}",
        f"- Emergency lighting test: {p('emergency_lighting')}",
        f"- Electrical work / remedial works: {p('hourly')} per hour, one-hour minimum",
        f"- Minimum visit: {b.MIN_TXT}. Booking 2 certificates together saves 10%, 3 or more saves 15%.",
        "",
        "## Pages",
    ]
    for pg in pages:
        lines.append(f"- [{pg['title'].split(' | ')[0]}]({b.SITE}{pg['path']}): {pg['description']}")
    return "\n".join(lines) + "\n"
