"""Extra pages for landlordsafetyfirst.uk: new services, bundles, booking, the landlord guide, reviews and legal pages."""


def pages(b, H):
    C, t, price, ptx, esc, icon = b.CFG, b.t, b.price, b.price_txt, b.esc, b.icon
    page_head, in_short, side, related = H.page_head, H.in_short, H.side, H.related
    R = C["base"]["radius_miles"]
    MIN = b.MIN_TXT
    PICKJS = {"pricing": b.picker_js()}
    sb = C["sister_brand"]
    P = []

    def svc_page(path, crumb, title, desc, h1, lede, body, faqs, side_html, preselect, schema_name, schema_desc, price_key, stype, book=None):
        trail = [("Home", "/"), ("Services", "/services/"), (crumb, path)]
        html = page_head(trail, h1, lede, book=book) + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap layout-side"><div class="prose">
{body}
{b.faq_html(faqs, f"{crumb} questions", "svc-faq")}
{b.reviewed_line()}
</div>
{side_html}
</div></section>'''
        P.append(dict(path=path, title=title, description=desc, body=html, crumbs=trail, preselect=preselect,
                      schema=[b.service_schema(schema_name, path, schema_desc, price_key, stype), b.faq_schema(faqs)]))

    # ======================================================================== BOILER SERVICE
    boiler_faqs = [
        ("Is a boiler service a legal requirement for landlords?",
         "No. The legal requirement is the annual gas safety check. But landlords must keep heating and hot water in working order, and most boiler warranties need a service every 12 months, so most landlords book both together."),
        ("What's the difference between a service and a gas safety check?",
         "The gas safety check confirms every appliance is safe to use and gives you the certificate. A service goes further on the boiler itself: opening it up, cleaning, checking parts and adjusting it so it runs efficiently."),
        ("How long does it take?",
         "Around an hour for the service, on top of the gas safety check if you book both."),
        ("Can you repair the boiler if you find a fault?",
         "We tell you exactly what's wrong and price the repair before doing anything. Small fixes can often be done on the same visit."),
    ]
    svc_page("/boiler-service/", "Boiler service",
             f"Boiler Service for Landlords East London | Add to Your Gas Check",
             f"Annual boiler service by a Gas Safe engineer, {ptx('boiler_service')} when added to your landlord gas safety check. Keeps the warranty valid and the tenant warm.",
             "Boiler service for landlords",
             f"An annual service keeps the boiler running, efficient and inside its warranty. {ptx('boiler_service')} when you add it to your gas safety check.",
             f'''{in_short("Do landlords need a boiler service?", f"It isn't a legal requirement, but landlords must keep heating and hot water working, and most boiler warranties need an annual service. Booked with the gas safety check, a service costs {ptx('boiler_service')}. On its own, the minimum visit charge of {MIN} applies.")}
<h2>What's included</h2>
<ul>
<li>Visual check of the boiler, flue and controls</li>
<li>Case removed, burner and heat exchanger inspected and cleaned where needed</li>
<li>Combustion analysis with a flue gas analyser</li>
<li>Gas pressure and flow checked and adjusted</li>
<li>Seals, condensate pipe and safety devices checked</li>
<li>A service record for your files and the warranty</li>
</ul>
<h2>Why book it with the gas check</h2>
<p>The engineer is already there, with the boiler isolated and the tools out. Adding the service costs much less than a second visit, and your tenant only lets us in once.</p>
<h2>Tenant reporting no heating?</h2>
<p>Give us their number. We'll arrange a visit, find the fault and price the repair before we start.</p>''',
             boiler_faqs,
             side("Add a boiler service", "boiler_service", ["Booked with your gas safety check", "Service record for the warranty", "Repairs priced before we start"], b.book_href("flat", 2, ["gas", "boiler"]), "Book gas check + service"),
             "Boiler service", "Boiler service", "Annual boiler servicing for rented homes by a Gas Safe registered engineer.", "boiler_service", "Boiler maintenance",
             book=b.book_href("flat", 2, ["gas", "boiler"]))

    # ======================================================================== FIRE ALARM
    fire_faqs = [
        ("What smoke and CO alarms does a rental need?",
         "In England, a smoke alarm on every storey used as living accommodation, and a carbon monoxide alarm in every room with a fixed combustion appliance, such as a gas boiler or wood burner. Gas cookers are excluded. Landlords must check alarms work on the first day of each new tenancy, and repair or replace them when told they're faulty."),
        ("Does my HMO need a fire alarm system?",
         "Most HMOs need an interlinked, mains-powered system. Larger ones need a more extensive system to BS 5839-6. Your licence conditions and fire risk assessment say exactly what's required. We'll check yours and tell you what fits."),
        ("How often should a fire alarm system be tested?",
         "Larger systems in HMOs and blocks are usually serviced every six months by a competent person, with a certificate each time. Tenants or managers test them weekly in between, and log it."),
        ("Do you install alarms as well as test them?",
         f"Yes. We fit hard-wired smoke, heat and CO alarms and repair existing systems, from {ptx('smoke_co_alarms')} per property."),
    ]
    svc_page("/fire-alarm/", "Fire alarm testing",
             "HMO Fire Alarm Testing & Certificates | East London",
             f"Fire alarm testing and certificates for HMOs and blocks in East London from {ptx('fire_alarm_test')}, plus smoke and CO alarms fitted to the 2022 regulations.",
             "Fire alarm testing for landlords",
             f"Smoke and CO alarms for single lets, and fire alarm systems tested and certified for HMOs. From {ptx('fire_alarm_test')}, done on the same visit as your other certificates.",
             f'''<p class="todo">TODO: confirm with the client exactly which fire safety work he does (testing only, or install too; any BAFE / FIA accreditation).</p>
{in_short("What fire safety does a landlord need?", f"Every rental in England needs a smoke alarm on each storey, and a carbon monoxide alarm in any room with a fixed combustion appliance. HMOs usually also need a mains-powered, interlinked fire alarm system, as set by the licence and fire risk assessment. We test and certify systems from {ptx('fire_alarm_test')}.")}
<h2>What different properties need</h2>
<table><thead><tr><th>Property</th><th>Usually needs</th></tr></thead><tbody>
<tr><td>Single-household let</td><td>Smoke alarm on every storey; CO alarm in rooms with a fixed combustion appliance</td></tr>
<tr><td>Small HMO (3–4 people)</td><td>Interlinked mains smoke and heat alarms, as set by licence conditions</td></tr>
<tr><td>Larger HMO or block</td><td>Fire alarm system to BS 5839-6 or BS 5839-1, <a href="/emergency-lighting/">emergency lighting</a> where required, six-monthly servicing</td></tr>
</tbody></table>
<p>This is a guide. Your licence conditions and <a href="/fire-risk-assessment/">fire risk assessment</a> are what count. Send us both and we'll tell you what your property needs.</p>
<h2>What we do</h2>
<ul>
<li>Test and certify fire alarm systems</li>
<li>Fit and replace hard-wired smoke, heat and CO alarms</li>
<li>Find the cause of systems that keep false-alarming</li>
<li>Combine it with your <a href="/eicr/">EICR</a> and <a href="/gas-safety-certificate/">gas check</a> in one visit</li>
</ul>''',
             fire_faqs,
             side("Book a fire alarm test", "fire_alarm_test", ["Certificate emailed to you", "Alarms fitted to the 2022 regulations", "Done alongside your EICR and gas check"], b.book_href("hmo", 5, ["fire_alarm"])),
             "Fire alarm test", "Fire alarm testing and certification", "Testing, certification and installation of fire alarm systems and smoke/CO alarms in rented homes and HMOs.", "fire_alarm_test", "Fire alarm inspection",
             book=b.book_href("hmo", 5, ["fire_alarm"]))

    # ======================================================================== EMERGENCY LIGHTING
    el_faqs = [
        ("Does my rental need emergency lighting?",
         "Most single lets don't. HMOs and blocks with longer or more complex escape routes often do, and your fire risk assessment or licence conditions will say so."),
        ("How often does emergency lighting need testing?",
         "A short function test every month, which a manager or tenant can do, and a full-duration test once a year, usually three hours, by a competent person. Both should be written in a log book."),
        ("What if some lights fail the test?",
         "We list each failed fitting, usually a battery or the fitting itself, and price the replacement. We can often fit replacements on the same visit."),
        ("Can it be done with the fire alarm test?",
         "Yes. Most landlords book both together, with the EICR, so there's one visit and one set of paperwork."),
    ]
    svc_page("/emergency-lighting/", "Emergency lighting",
             "Emergency Lighting Testing for HMOs | East London",
             f"Annual emergency lighting test and certificate to BS 5266 for HMOs and blocks, from {ptx('emergency_lighting')}. Failed fittings priced and replaced.",
             "Emergency lighting testing",
             f"The annual full-duration test that HMO licences and fire risk assessments ask for, with a certificate for your records. From {ptx('emergency_lighting')}.",
             f'''{in_short("What is an emergency lighting test?", f"Emergency lights must stay on when the mains power fails, so people can get out safely. Under BS 5266-1 they need a short function test every month and a full-duration test, usually three hours, once a year. We do the annual test, record each fitting and give you a certificate, from {ptx('emergency_lighting')}.")}
<h2>Who needs it</h2>
<p>Emergency lighting is usually needed in HMOs and blocks where the escape route has no natural light, or is long or complicated. Your <a href="/fire-risk-assessment/">fire risk assessment</a> or licence conditions say whether yours does.</p>
<h2>What we do</h2>
<ul>
<li>Full-duration discharge test of every fitting</li>
<li>Check each fitting lights the escape route as it should</li>
<li>Record results in your log book and issue a certificate</li>
<li>List and price any failed batteries or fittings</li>
</ul>
<h2>Plan around your tenants</h2>
<p>After a three-hour test, the batteries need time to recharge, so we test during the day when the lights aren't needed and tell your tenants in advance.</p>''',
             el_faqs,
             side("Book an emergency lighting test", "emergency_lighting", ["Certificate and log book entry", "Failed fittings priced before replacing", "Combine with your fire alarm test"], b.book_href("hmo", 5, ["em_light", "fire_alarm"])),
             "Emergency lighting test", "Emergency lighting testing", "Annual full-duration emergency lighting testing and certification to BS 5266 for HMOs and blocks.", "emergency_lighting", "Emergency lighting inspection",
             book=b.book_href("hmo", 5, ["em_light", "fire_alarm"]))

    # ======================================================================== FIRE RISK ASSESSMENT
    fra_faqs = [
        ("Who needs a fire risk assessment?",
         "The person responsible for the common parts of an HMO or block of flats, and anyone running non-domestic premises such as a shop or office. Single-household lets don't usually need one, though fire safety rules still apply."),
        ("How often should it be reviewed?",
         "Regularly, and whenever something changes, such as new tenants, building work or a change in how the property is used. Many landlords review it every year."),
        ("Does it have to be written down?",
         "Yes. Since October 2023, all responsible persons in England must record their full fire risk assessment in writing, whatever the size of the business."),
        ("What happens after the assessment?",
         "You get a written report with an action plan, ranked by priority. We can carry out the electrical and alarm actions ourselves and quote for them."),
    ]
    svc_page("/fire-risk-assessment/", "Fire risk assessment",
             "Fire Risk Assessment for HMOs & Landlords | East London",
             f"Fire risk assessments for HMOs, common parts of blocks and small commercial premises in East London, from {ptx('fra')}. Written report with a clear action plan.",
             "Fire risk assessment for landlords",
             f"A written fire risk assessment for HMOs, the common parts of blocks and small commercial premises, with a clear action plan. From {ptx('fra')}.",
             f'''<p>{t("fra_scope")}</p>
{in_short("What is a fire risk assessment?", f"A fire risk assessment looks at what could start a fire, who is at risk and how they get out, then sets out what needs doing. Under the Regulatory Reform (Fire Safety) Order 2005 it's a legal requirement for HMOs, the common parts of blocks of flats and business premises. Ours start at {ptx('fra')} for a small HMO.")}
<h2>What we look at</h2>
<ul>
<li>Sources of ignition and fuel, including the electrical installation</li>
<li>Escape routes, fire doors and signage</li>
<li>Fire detection, alarms and <a href="/emergency-lighting/">emergency lighting</a></li>
<li>Who lives there, and anyone who needs extra help to get out</li>
<li>How fire safety is managed: testing, logs and information for tenants</li>
</ul>
<h2>What you get</h2>
<p>A written report with each finding ranked by priority, and an action plan you can give to the council if they ask. Where the actions are electrical or alarm work, we can quote for them on the spot.</p>
<h2>Do it with your other certificates</h2>
<p>HMO landlords usually book the fire risk assessment with the EICR, gas safety check, fire alarm and emergency lighting tests. See the <a href="/landlord-bundles/">HMO bundle</a>.</p>''',
             fra_faqs,
             side("Book a fire risk assessment", "fra", ["Written report and action plan", "Ranked by priority", "Electrical actions quoted on the spot"], b.book_href("hmo", 5, ["fra"])),
             "Fire risk assessment", "Fire risk assessment", "Fire risk assessments for HMOs, common parts of residential blocks and small commercial premises.", "fra", "Fire risk assessment",
             book=b.book_href("hmo", 5, ["fra"]))

    # ======================================================================== EPC
    epc_faqs = [
        ("Do I need an EPC to rent out a property?",
         "Yes. You need a valid EPC before you advertise the property, and you must give your tenants a copy. It lasts 10 years."),
        ("What rating does a rental need?",
         "In England, a privately rented home must be rated E or above, unless it has a valid exemption registered. Councils can fine landlords up to £5,000 per property for breaches."),
        ("How long does an EPC take?",
         "Usually under an hour for a flat. The assessor measures the property, records the heating, insulation, windows and lighting, and lodges the certificate on the national register."),
        ("Why is it cheaper with other certificates?",
         f"Because we're already there. On its own, the minimum visit charge of {MIN} applies. Added to an EICR or gas check, an EPC costs {ptx('epc')}."),
    ]
    svc_page("/epc/", "EPC",
             "EPC for Landlords East London | Energy Performance Certificate",
             f"Energy Performance Certificates for rentals in East London, {ptx('epc')} when added to your EICR or gas safety check. Rentals must rate E or above.",
             "EPC for landlords",
             f"The energy certificate you need before you advertise a rental. {ptx('epc')} when added to another certificate on the same visit.",
             f'''<p>{t("epc_scope")}</p>
{in_short("What is an EPC and do landlords need one?", f"An Energy Performance Certificate rates a property's energy efficiency from A to G. Landlords in England need a valid EPC before they advertise, must give tenants a copy, and the property must be rated E or above. It's valid for 10 years. Added to another visit, ours cost {ptx('epc')}.")}
<h2>What the assessment covers</h2>
<ul>
<li>Property size and construction</li>
<li>Heating system and controls, and hot water</li>
<li>Loft, wall and floor insulation</li>
<li>Windows and glazing</li>
<li>Lighting</li>
</ul>
<h2>If your property rates F or G</h2>
<p>You can't grant a new tenancy until it reaches E, unless you register an exemption. The certificate lists recommended improvements and their rough cost. Better heating controls, LED lighting and loft insulation are often the cheapest gains.</p>
<h2>Do it with your other certificates</h2>
<p>An EPC is part of the <a href="/landlord-bundles/">Full Compliance bundle</a>, with the EICR, gas safety check and alarm check, all in one visit before a new tenancy.</p>''',
             epc_faqs,
             side("Add an EPC", "epc", ["Lodged on the national register", "Valid for 10 years", "Part of the Full Compliance bundle"], b.book_href("flat", 2, ["eicr", "gas", "epc"]), "Book with EICR + gas",
                  price_note=f"Added to another visit. On its own, the minimum visit charge of {MIN} applies."),
             "EPC", "Energy Performance Certificate", "Energy Performance Certificates for privately rented homes.", "epc", "Energy assessment",
             book=b.book_href("flat", 2, ["eicr", "gas", "epc"]))

    # ======================================================================== PAT TESTING
    pat_faqs = [
        ("Is PAT testing a legal requirement for landlords?",
         "It isn't named in law, but you must make sure any electrical appliances you supply are safe. PAT testing is the usual way to show that, and many HMO licences ask for it."),
        ("How often should appliances be tested?",
         "There's no fixed rule. Most landlords test at the start of each tenancy, or every year in HMOs where appliances get heavy use."),
        ("What counts as an appliance?",
         "Anything with a plug that you provide: fridges, washing machines, microwaves, kettles, lamps, heaters and extension leads. The tenant's own items aren't your responsibility."),
        ("What if something fails?",
         "We label it, tell you why it failed, and advise whether to repair or replace it. It shouldn't be used until it's sorted."),
    ]
    svc_page("/pat-testing/", "PAT testing",
             "PAT Testing for Landlords East London | Furnished Lets & HMOs",
             f"PAT testing for furnished lets and HMOs in East London, {ptx('pat')} for up to 10 appliances when added to your EICR or gas check.",
             "PAT testing for landlords",
             f"Safety checks on the appliances you supply in a furnished let or HMO. {ptx('pat')} for up to 10 items, added to another certificate on the same visit.",
             f'''{in_short("What is PAT testing?", f"PAT (portable appliance) testing checks that plug-in appliances are safe: a visual inspection plus electrical tests on the lead, plug and casing. Landlords must make sure appliances they supply are safe, and PAT testing is the usual way to prove it. Added to another visit, we test up to 10 items for {ptx('pat')}.")}
<h2>What we check</h2>
<ul>
<li>Plugs, leads and casings for damage and overheating</li>
<li>The fuse is the right rating</li>
<li>Earth continuity and insulation resistance</li>
<li>Each item labelled pass or fail, with a record for your files</li>
</ul>
<h2>Do it with your EICR</h2>
<p>We're already testing the fixed wiring, so adding the appliances takes little extra time and saves a second visit.</p>''',
             pat_faqs,
             side("Add PAT testing", "pat", ["Up to 10 appliances", "Every item labelled", "Record emailed to you"], b.book_href("flat", 2, ["eicr", "pat"]), "Book with an EICR",
                  price_note=f"Added to another visit. On its own, the minimum visit charge of {MIN} applies."),
             "PAT testing", "PAT testing", "Portable appliance testing for furnished rentals and HMOs.", "pat", "Portable appliance testing",
             book=b.book_href("flat", 2, ["eicr", "pat"]))

    # ======================================================================== COMMERCIAL
    com_faqs = [
        ("How often does a commercial property need an EICR?",
         "For most shops and offices, industry guidance recommends at least every five years, and at every change of occupier. Your insurer or landlord may ask for it more often."),
        ("Does my business need a fire risk assessment?",
         "Yes. Anyone responsible for non-domestic premises in England must have a written fire risk assessment under the Regulatory Reform (Fire Safety) Order 2005."),
        ("Can you work outside opening hours?",
         "Yes. Testing means switching circuits off, so we often work early, late or at weekends to keep your business running."),
        ("Do you do commercial gas work?",
         b.todo("Confirm whether the engineer holds commercial gas qualifications. If not, say so here.")),
    ]
    svc_page("/commercial/", "Commercial properties",
             "Commercial EICR & Fire Safety Certificates | East London",
             f"EICRs, emergency lighting, fire alarm testing and fire risk assessments for shops, offices and small commercial premises in East London. EICRs from {ptx('eicr_commercial')}.",
             "Safety certificates for small businesses",
             f"Commercial EICRs, emergency lighting, fire alarm testing and fire risk assessments for shops, offices and small premises. Worked around your opening hours.",
             f'''{in_short("What safety certificates does a small business need?", f"Most small commercial premises need an EICR at least every five years, a written fire risk assessment, and, depending on that assessment, a tested fire alarm and emergency lighting. We do all of these, priced by size. Commercial EICRs start at {ptx('eicr_commercial')}.")}
<h2>What we do for businesses</h2>
<ul>
<li>Commercial EICRs, with remedial work quoted from the report</li>
<li><a href="/emergency-lighting/">Emergency lighting</a> testing and certificates</li>
<li><a href="/fire-alarm/">Fire alarm</a> testing and certificates</li>
<li><a href="/fire-risk-assessment/">Fire risk assessments</a></li>
<li>PAT testing for office equipment</li>
</ul>
<h2>Working around your business</h2>
<p>We agree a time that keeps disruption low, often early morning or after closing, and tell you in advance which circuits will be off and for how long.</p>
<h2>Landlords of commercial units</h2>
<p>If you let a shop or office, check the lease for who is responsible for the electrics and fire safety. We'll work with you or your tenant, whichever the lease says.</p>''',
             com_faqs,
             side("Get a commercial quote", "eicr_commercial", ["Priced by size and circuit count", "Out-of-hours testing available", "One engineer for electrical and fire"], "#quote", "Get a quote"),
             "Commercial property", "Commercial electrical and fire safety certificates", "EICRs, emergency lighting, fire alarm testing and fire risk assessments for small commercial premises.", "eicr_commercial", "Commercial electrical inspection",
             book="#quote")

    # ======================================================================== BUNDLES
    bun_faqs = [
        ("How does the bundle saving work?",
         "Book two certificates for the same visit and save 10% on them. Three or more saves 15%. Add-ons like an EPC, PAT testing or an alarm check are already priced lower because we're there anyway."),
        ("Can I get one renewal date for everything?",
         "Mostly, yes. Gas safety is yearly and can be renewed up to two months early without losing the date. If you line your EICR up with a gas check, they fall on the same visit every fifth year, and we remind you before each one."),
        ("Can I change what's in a bundle?",
         "Yes. Use the price picker to tick exactly what you need. The saving applies automatically."),
        ("What if something fails?",
         "We tell you on the day, price the fix, and with your OK do small repairs before we leave. Bigger jobs get a written quote."),
    ]
    bun_body = page_head([("Home", "/"), ("Landlord bundles", "/landlord-bundles/")], "Landlord bundles: every certificate in one visit",
                         "Your tenant lets us in once, you get one set of paperwork, and you save 10–15% on the certificates.", buttons=False) + f'''
<section class="section" style="padding-top:3.5rem"><div class="wrap">{H.bundle_cards()}</div></section>
<section class="section section-alt" id="price" aria-labelledby="price-h"><div class="wrap">
<div class="section-head"><h2 id="price-h">Need something different?</h2>
<p class="section-lede">Tick exactly what your property needs. The saving applies automatically.</p></div>
{H.picker_home()}
</div></section>
{H.faq_section(bun_faqs, "Bundle questions")}'''
    P.append(dict(path="/landlord-bundles/", title="Landlord Certificate Bundles East London | Gas + EICR + EPC",
                  description=f"Landlord bundles: gas safety + EICR from {b.money(b.quote_calc('flat', 2, ['eicr', 'gas'])['total_inc'])} for a 2-bed flat. Full compliance and HMO packs. One visit, one engineer, save 10–15%.",
                  body=bun_body, js_extra=PICKJS, crumbs=[("Home", "/"), ("Landlord bundles", "/landlord-bundles/")], preselect="Landlord bundle", quote_heading="Questions before you book?"))

    # ======================================================================== BOOK
    embed = C.get("booking_embed_url")
    slots = "".join(f'<label class="opt-card"><input type="radio" name="time_slot" value="{v}"{" checked" if i == 0 else ""}><span>{n}</span><small>{s}</small></label>'
                    for i, (v, n, s) in enumerate((("any", "Any time", "Fastest slot"), ("morning", "Morning", "8am–12pm"), ("afternoon", "Afternoon", "12pm–4pm"))))
    if embed:
        book_main = f'''<div class="two"><div class="picker card" data-picker data-read-url><div class="picker-main">{H.picker_controls("bk")}</div>{H.picker_summary(book=False).replace('<button class="btn btn-primary" type="submit">', '<a class="btn btn-primary" href="#calendar">').replace('Send booking request</span></button>', 'Choose a time below</span></a>')}</div></div>
<h2 id="calendar" style="margin-top:3rem">Choose a time</h2><iframe class="embed" src="{esc(embed)}" title="Booking calendar" loading="lazy"></iframe>'''
    else:
        book_main = f'''<form class="book-grid" data-form="booking" data-picker data-read-url novalidate aria-label="Booking request">
<div>
<div class="card picker-main" style="margin-bottom:1.25rem">{H.picker_controls("bk")}</div>
<fieldset class="group"><legend>When suits you?</legend>
<div class="row"><div class="field"><label for="b-date">Preferred date</label><input id="b-date" name="preferred_date" type="date" data-min-tomorrow required></div>
<div class="field"><label for="b-date2">Back-up date <span class="opt">(optional)</span></label><input id="b-date2" name="backup_date" type="date" data-min-tomorrow></div></div>
<div class="field"><span class="label">Time of day</span><div class="slot-grid">{slots}</div></div>
<p class="small">{t("slot_confirm_line")}.</p>
</fieldset>
<fieldset class="group"><legend>The property</legend>
<div class="row"><div class="field"><label for="b-addr">First line of address</label><input id="b-addr" name="address" autocomplete="address-line1" required></div>
<div class="field"><label for="b-pc">Postcode</label><input id="b-pc" name="postcode" autocomplete="postal-code" required></div></div>
<div class="field"><label for="b-access">Who will let us in?</label><select id="b-access" name="access"><option>My tenant</option><option>I will</option><option>Keys from me or a key safe</option></select></div>
<div class="row"><div class="field"><label for="b-tname">Tenant's name <span class="opt">(optional)</span></label><input id="b-tname" name="tenant_name"></div>
<div class="field"><label for="b-tphone">Tenant's phone <span class="opt">(optional)</span></label><input id="b-tphone" name="tenant_phone" type="tel"></div></div>
<div class="field"><label for="b-notes">Anything we should know? <span class="opt">(optional)</span></label><textarea id="b-notes" name="message" rows="3" placeholder="e.g. combi boiler plus gas hob, consumer unit in the hall cupboard, EICR due on 3 March"></textarea></div>
</fieldset>
<fieldset class="group"><legend>Your details</legend>
<div class="row"><div class="field"><label for="b-name">Name</label><input id="b-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="b-phone">Phone</label><input id="b-phone" name="phone" type="tel" autocomplete="tel" required></div></div>
<div class="field"><label for="b-email">Email (for your certificates)</label><input id="b-email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="b-who">I am a</label><select id="b-who" name="customer_type"><option>Landlord</option><option>Homeowner</option><option>Business</option></select></div>
</fieldset>
<fieldset class="group"><legend>Payment</legend>
<div class="field"><label for="b-pay">How would you like to pay?</label><select id="b-pay" name="payment"><option>Card payment link when the slot is confirmed</option><option>Pay on the day</option></select></div>
<p class="small">{t("payment_line")}</p>
</fieldset>
<label class="tick"><input type="checkbox" name="start_within_14_days" value="yes" id="b-14" data-label="the 14-day cancellation box" required><span>I'd like the work done within the 14-day cancellation period. I understand I'll pay for any work already carried out if I cancel, and lose my right to cancel once it's complete.</span></label>
<label class="tick"><input type="checkbox" name="terms" value="accepted" id="b-terms" data-label="the terms box" required><span>I agree to the <a href="/terms/">terms and conditions</a> and <a href="/privacy/">privacy notice</a>.</span></label>
<div class="hp" aria-hidden="true"><label for="b-url">Leave empty</label><input id="b-url" name="company_url" tabindex="-1" autocomplete="off"></div>
</div>
<aside class="book-sum">{H.picker_summary(book=False)}</aside>
</form>'''
    book_body = page_head([("Home", "/"), ("Book", "/book/")], "Book your certificates",
                          f"Choose what you need and a day that suits. {t('slot_confirm_line')}, and we can arrange access with your tenant.", buttons=False) + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap">{book_main}
<p class="small" style="margin-top:2rem">Rather talk it through? Call <a href="{b.phone_href()}">{t("phone_display")}</a> or <a href="{esc(b.wa_href())}">send a WhatsApp</a>. Commercial premises: <a href="/commercial/#quote">ask for a quote</a>.</p>
</div></section>'''
    P.append(dict(path="/book/", title="Book a Landlord Safety Certificate Online | Landlord Safety First",
                  description="Book your gas safety certificate, EICR, EPC or fire safety check online. See the price before you book. One engineer, one visit.",
                  body=book_body, js_extra=PICKJS, crumbs=[("Home", "/"), ("Book", "/book/")], quote=False))

    # ======================================================================== GUIDE
    cert_rows = [
        ("Gas safety certificate (CP12)", "Every rental with a gas appliance, flue or pipework you provide", "Every 12 months", "Gas Safety (Installation and Use) Regulations 1998", "Copy to tenants within 28 days of the check, and to new tenants before they move in. Keep records for 2 years.", "/gas-safety-certificate/"),
        ("EICR", "Every private rental in England", "At least every 5 years", "Electrical Safety Standards in the Private Rented Sector (England) Regulations 2020", "Copy to tenants within 28 days. Fix C1, C2 and FI items within 28 days. Fines up to £30,000.", "/eicr/"),
        ("Smoke and CO alarms", "Every rental", "Checked on day one of each tenancy", "Smoke and Carbon Monoxide Alarm (England) Regulations 2015, amended 2022", "Smoke alarm on every storey; CO alarm in rooms with a fixed combustion appliance. Fines up to £5,000.", "/fire-alarm/"),
        ("EPC", "Every rental, before it's advertised", "Every 10 years", "Energy Performance of Buildings Regulations; minimum energy efficiency standards", "Must be rated E or above unless exempt. Give tenants a copy.", "/epc/"),
        ("Fire alarm system", "Most HMOs, as set by licence and fire risk assessment", "Serviced typically every 6 months", "Housing Act 2004 licence conditions; BS 5839-6", "Tenants or manager test weekly and keep a log.", "/fire-alarm/"),
        ("Emergency lighting", "HMOs and blocks where the fire risk assessment says so", "Monthly function test; annual full-duration test", "BS 5266-1", "Results kept in a log book.", "/emergency-lighting/"),
        ("Fire risk assessment", "HMOs, common parts of blocks, business premises", "Review regularly and after changes", "Regulatory Reform (Fire Safety) Order 2005", "Must be recorded in writing.", "/fire-risk-assessment/"),
        ("PAT testing", "Furnished lets and HMOs where you supply appliances", "Usually each tenancy or yearly", "Duty to supply safe appliances", "Often a licence condition for HMOs.", "/pat-testing/"),
    ]
    table = ('<div class="table-scroll"><table class="cert-table"><thead><tr><th>Certificate</th><th>Who needs it</th><th>How often</th><th>The law</th><th>What else you must do</th></tr></thead><tbody>'
             + "".join(f'<tr><th scope="row"><a href="{h}">{n}</a></th><td>{w}</td><td>{f}</td><td>{l}</td><td>{x}</td></tr>' for n, w, f, l, x, h in cert_rows) + "</tbody></table></div>")
    guide_faqs = [
        ("What certificates does a landlord legally need?",
         "In England, every private rental needs a valid EICR (every 5 years), a gas safety certificate if there's any gas appliance (every 12 months), an EPC rated E or above (every 10 years), and working smoke and CO alarms. HMOs usually need more, set by the licence."),
        ("What happens if I don't have them?",
         "Councils can fine landlords up to £30,000 for EICR breaches and up to £5,000 for alarm and EPC breaches, and gas safety failures are a criminal offence. Missing certificates can also block a licence application."),
        ("Who has to keep track of renewal dates?",
         "You do, as the landlord, even if an agent manages the property. Our free reminder service emails you 30 days before each one expires."),
    ]
    guide_body = page_head([("Home", "/"), ("Landlord compliance guide", "/landlord-compliance-guide/")], "The landlord compliance guide",
                           "Which safety certificates the law asks for, how often, and what else you have to do. Written for private landlords in England, in plain English.", buttons=False, eyebrow="Updated November 2026") + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap layout-side"><div class="prose" style="max-width:none">
<nav class="toc card" aria-label="On this page"><strong>On this page</strong><ol>
<li><a href="#at-a-glance">Certificates at a glance</a></li><li><a href="#single">A single-household let</a></li>
<li><a href="#hmo">HMOs</a></li><li><a href="#licensing">Licensing in East London</a></li>
<li><a href="#new-tenancy">Before a new tenancy</a></li><li><a href="#changes">What's changing</a></li></ol></nav>
<h2 id="at-a-glance" style="margin-top:2rem">Certificates at a glance</h2>
{table}
<p class="small">This is a guide, not legal advice. Check the rules for your property with your council or on GOV.UK.</p>
<h2 id="single">A single-household let</h2>
<p>For a flat or house let to one household, you need:</p>
<ul>
<li>A gas safety certificate every 12 months, if there's any gas appliance</li>
<li>An EICR at least every five years</li>
<li>An EPC rated E or above</li>
<li>A smoke alarm on every storey, and a CO alarm in any room with a fixed combustion appliance, tested on the first day of the tenancy</li>
</ul>
<p>The first three can be done in one visit. That's our <a href="/landlord-bundles/">Full Compliance bundle</a>.</p>
<h2 id="hmo">HMOs</h2>
<p>A house in multiple occupation (three or more people from two or more households, sharing facilities) needs everything above, plus whatever its licence and fire risk assessment set. That usually means:</p>
<ul>
<li>An interlinked, mains-powered <a href="/fire-alarm/">fire alarm system</a>, serviced and certified</li>
<li><a href="/emergency-lighting/">Emergency lighting</a> where the escape route needs it</li>
<li>A written <a href="/fire-risk-assessment/">fire risk assessment</a> for the common parts</li>
<li>Fire doors, and sometimes <a href="/pat-testing/">PAT testing</a></li>
</ul>
<h2 id="licensing">Licensing in East London</h2>
<p>Most East London boroughs run licensing schemes, and licence applications usually ask for a current EICR and gas safety certificate. See our guides for <a href="/areas/tower-hamlets/">Tower Hamlets</a>, <a href="/areas/hackney/">Hackney</a> and <a href="/areas/newham/">Newham</a>.</p>
<h2 id="new-tenancy">Before a new tenancy: checklist</h2>
<ol>
<li>Gas safety certificate in date, with a copy ready for the tenant</li>
<li>EICR in date, with a copy ready for the tenant</li>
<li>EPC rated E or above, with a copy ready for the tenant</li>
<li>Smoke and CO alarms tested on move-in day</li>
<li>Any licence the property needs, applied for or granted</li>
</ol>
<h2 id="changes">What's changing</h2>
<p>The Renters' Rights Act 2025 is coming in over several stages. The first changes to tenancies started on 1 May 2026. A national private rented sector database and a landlord ombudsman are being set up, and the Decent Homes Standard is being extended to private rentals. Keeping your certificates in one place, with renewal dates tracked, will make each step easier. Check GOV.UK for the latest dates.</p>
{b.faq_html(guide_faqs, "Quick answers", "guide-faq")}
{b.reviewed_line()}
</div>
<div style="position:sticky;top:100px">{side("Get compliant in one visit", "eicr_flat", ["Gas, electrical and alarms together", "One engineer, no subcontractors", "Free renewal reminders"], "/landlord-bundles/", "See landlord bundles", quote_href="/contact/#quote")}</div>
</div></section>'''
    P.append(dict(path="/landlord-compliance-guide/", title="Landlord Safety Certificates Guide 2026: What You Legally Need",
                  description="Which safety certificates landlords in England need, how often, and what the law says: gas safety, EICR, EPC, smoke and CO alarms, HMO fire safety. Plain-English guide.",
                  body=guide_body, crumbs=[("Home", "/"), ("Landlord compliance guide", "/landlord-compliance-guide/")], cta=True, quote=False,
                  schema=[{"@type": "Article", "headline": "The landlord compliance guide", "dateModified": C["last_reviewed"], "author": {"@id": b.BIZ_ID}, "publisher": {"@id": b.BIZ_ID}},
                          b.faq_schema(guide_faqs)]))

    # ======================================================================== REVIEWS
    if C["reviews"]:
        rv = "".join(f'<figure class="review card">{H.stars()}<blockquote>“{esc(r["text"])}”</blockquote><figcaption>{esc(r["name"])}, {esc(r["area"])}{" · " + esc(r["service"]) if r.get("service") else ""}</figcaption></figure>' for r in C["reviews"])
        rv_main = f'<div class="reviews">{rv}</div>'
    else:
        leave = (f'<a class="btn btn-primary" href="{esc(C["google_reviews_url"])}" rel="noopener">{icon("star")}<span>Leave a review on Google</span></a>' if C["google_reviews_url"]
                 else b.todo("Add the Google review link (google_reviews_url) once the Business Profile is live."))
        rv_main = f'''<div class="card empty-state"><div class="badge-ic amber">{icon("star")}</div>
<h2>Be one of our first reviews</h2>
<p class="section-lede" style="margin:0 auto 1.5rem">We're new on Google. If we've done work for you, a short review helps other landlords find an engineer they can trust.</p>
<div class="btn-row" style="justify-content:center">{leave}</div></div>'''
    rev_body = page_head([("Home", "/"), ("Reviews", "/reviews/")], "Reviews from landlords",
                         "Every review here is from a real customer, shown with their permission. We never write our own.", buttons=False) + f'''
<section class="section" style="padding-top:2.5rem"><div class="wrap">{rv_main}</div></section>'''
    P.append(dict(path="/reviews/", title="Reviews | Landlord Safety First",
                  description="Reviews from landlords, homeowners and businesses who have used Landlord Safety First for gas, electrical and fire safety certificates.",
                  body=rev_body, crumbs=[("Home", "/"), ("Reviews", "/reviews/")], cta=True, quote=False))

    # ======================================================================== LEGAL
    def legal(path, crumb, h1, lede, body, title, desc):
        html = page_head([("Home", "/"), (crumb, path)], h1, lede, buttons=False) + f'<section class="section" style="padding-top:2.5rem"><div class="wrap prose">{body}<p class="small">Last updated {C["last_reviewed"]}.</p></div></section>'
        P.append(dict(path=path, title=title, description=desc, body=html, crumbs=[("Home", "/"), (crumb, path)], quote=False))

    legal("/privacy/", "Privacy", "Privacy notice", "How we use the details you send us.", f'''
<p class="todo">TODO: confirm the data controller details, the CRM / form provider (e.g. GoHighLevel), payment provider and hosting before launch.</p>
<h2>Who we are</h2><p>{t("legal_line")}. ICO registration no. {t("ico_number")}. Contact: <a href="mailto:{esc(C["email"])}">{esc(C["email"])}</a>.</p>
<h2>What we collect</h2><p>When you call, message, book or use a form: your name, phone number, email, the property address or postcode, details of the job, and your tenant's name and number if you give them to us to arrange access. If you send an EICR or photos, we keep those too. If you sign up for a reminder, we keep the certificate type and expiry date.</p>
<h2>Why we use it</h2><p>To reply to you, quote, book and carry out the work, take payment and send certificates. Our lawful basis is taking steps to enter into, and perform, a contract with you. We also keep records we're legally required to keep, such as gas safety records. Reminders are sent because you asked for them, and you can stop them at any time.</p>
<h2>Cookies and analytics</h2><p>We only use analytics and advertising cookies if you accept them. See our <a href="/cookies/">cookie policy</a>.</p>
<h2>Who we share it with</h2><p>Only the services we use to run the business: our booking and customer system, email and messaging providers, our payment provider, our website host, and Google (analytics and ads, only with your consent). We never sell your details.</p>
<h2>How long we keep it</h2><p>Enquiries that don't become jobs: 12 months. Job records and certificates: at least 6 years for tax and safety purposes. Reminder details: until you unsubscribe.</p>
<h2>Your rights</h2><p>You can ask to see, correct or delete your data, or object to how we use it, by emailing us. You can complain to the Information Commissioner's Office at <a href="https://ico.org.uk" rel="noopener">ico.org.uk</a>.</p>''',
          "Privacy Notice | Landlord Safety First", "How Landlord Safety First uses the personal details you send us.")

    legal("/cookies/", "Cookies", "Cookie policy", "What we store on your device, and how to change your choice.", '''
<h2>Cookies we always use</h2><p>None that track you. If our cookie banner is shown, we store your choice (accept or reject) in your browser so we don't ask again.</p>
<h2>Cookies we only use if you accept</h2>
<table><thead><tr><th>Provider</th><th>Purpose</th><th>Examples</th></tr></thead><tbody>
<tr><td>Google Analytics</td><td>Counting visits and seeing which pages bring enquiries</td><td>_ga, _ga_*</td></tr>
<tr><td>Google Ads</td><td>Measuring which adverts lead to calls, messages and bookings</td><td>_gcl_au</td></tr>
</tbody></table>
<h2>Changing your choice</h2><p><button class="btn btn-ghost" type="button" data-reset-consent>Change my cookie choice</button></p>
<p>You can also clear cookies and site data in your browser settings.</p>''',
          "Cookie Policy | Landlord Safety First", "The cookies Landlord Safety First uses and how to change your choice.")

    legal("/terms/", "Terms", "Terms and conditions", "The terms for bookings, payment, cancellations and our work. Short and in plain English.", f'''
<p class="todo">TODO: draft terms. Have these checked (a solicitor, or the electrical scheme's member advice line) and confirm every fee before launch.</p>
<h2>1. Who we are</h2><p>{t("legal_line")}. Contact: <a href="mailto:{esc(C["email"])}">{esc(C["email"])}</a>.</p>
<h2>2. Prices</h2><p>Prices on this website include VAT. Certificate prices are fixed for the property described when you book. If the property turns out to be different (for example, more bedrooms or appliances than described), we'll tell you the new price before starting. The minimum charge for a visit is {MIN}.</p>
<h2>3. Payment</h2><p>{t("payment_line")} Remedial and repair work is quoted in writing and only started once you accept the quote.</p>
<h2>4. Access</h2><p>You're responsible for making sure we can get into the property at the agreed time, including arranging access with your tenant if you ask us not to. If we can't get in, a failed-visit charge of {b.todo("£X")} may apply.</p>
<h2>5. Changing or cancelling a booking</h2><p>You can change or cancel a booking free of charge up to {b.todo("24 hours")} before the appointment. After that, a late cancellation charge of {b.todo("£X")} may apply.</p>
<h2>6. Your right to cancel</h2><p>If you're booking as a consumer, online or by phone, you have the right to cancel within 14 days of booking without giving a reason. If you ask us to carry out the work within those 14 days and then cancel, you'll pay for work already done. Once the work is complete, the right to cancel ends. To cancel, email or call us; you can use the model cancellation form from GOV.UK but you don't have to.</p>
<h2>7. What an inspection covers</h2><p>An inspection reports on the condition of the installation on the day. It isn't a repair. Anything that needs fixing is listed on the report and quoted separately. If we find something immediately dangerous, we're required to make it safe, which can mean isolating a circuit or disconnecting a gas appliance, and we'll explain why.</p>
<h2>8. Certificates</h2><p>Certificates and reports are emailed to the address you give us. We keep copies so we can send you another if you lose yours.</p>
<h2>9. Our responsibility</h2><p>We carry out our work with reasonable care and skill, and we're insured ({t("insurance_line")}). Nothing in these terms limits your legal rights as a consumer.</p>
<h2>10. Complaints</h2><p>If something isn't right, tell us first and we'll put it right. You can also contact our registration scheme ({t("electrical_scheme")} for electrical work, Gas Safe Register for gas work).</p>
<h2>11. Law</h2><p>These terms are governed by the law of England and Wales.</p>''',
          "Terms and Conditions | Landlord Safety First", "Booking, payment, cancellation and access terms for Landlord Safety First.")

    return P
