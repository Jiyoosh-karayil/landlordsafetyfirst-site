# landlordsafetyfirst.uk

A static site with no framework, database or plugins. `dist/` is the website.

## Change something
- **Business facts, prices, picker rules, bundles, phone, form, tracking:** edit `site.config.json`
- **Page wording:** `content.py` (home, core services, areas, about, contact, FAQ) and `content_more.py` (boiler, fire, EPC, PAT, commercial, bundles, booking, guide, reviews, legal)
- **Look:** edit `src/styles.css` ("on site": dark photo hero, rounded cards, amber #F5A524 accent, Manrope; stand-in photos in src/img). Rules in `DESIGN.md`.
- **Behaviour (menu, price picker, forms):** `src/main.js`. The picker maths is mirrored in `build.py` (`quote_calc`), so bundle cards and the picker always agree.

Then rebuild:

    python3 build.py               # builds dist/ and lists anything still TODO (on Windows: set PYTHONUTF8=1 first)
    python3 build.py --production  # refuses to build while any TODO is left

## Go live (Vercel)
1. Build locally (`PYTHONUTF8=1 python build.py`), commit (including `dist/`) and push to GitHub.
2. Vercel → New Project → import the repo. `vercel.json` already sets Framework: Other and Output directory: `dist`; leave the build command empty. Every push to `main` redeploys.
   Before launch, run `python build.py --production` locally: it refuses to build while any TODO is left.
3. Add the domain landlordsafetyfirst.uk in Vercel, then point the Namecheap DNS records at it (Vercel shows the exact A/CNAME values).
4. Google Search Console: add the domain, submit `https://landlordsafetyfirst.uk/sitemap.xml`.

## Before launch, fill in `site.config.json`
- `phone_display` + `phone_e164` (e.g. "+447700900123"), `whatsapp_e164`
- `gas_safe_number`, `electrical_scheme`, `electrical_scheme_number`, `insurance_line`
- `engineer_name`, `years_trading`, `legal_line`, `hours_display`, `response_promise`
- Every price in `prices` (ex-VAT), then set `"prices_confirmed": true`
- `form_endpoint`: GoHighLevel inbound webhook (or n8n / Formspree). Every form POSTs JSON with `form_type` = quote, booking or reminder, plus page and submitted_at
- `booking_embed_url` (optional): a GHL / Cal.com calendar URL to embed on /book/ instead of the built-in booking request form
- `cert_turnaround`, `slot_confirm_line`, `payment_line`, `ico_number`, `epc_scope`, `fra_scope`
- `engineer_photo`: a real photo in `src/static/` (the hero switches from the example certificate pack to the photo)
- `analytics.ga4_id` / `google_ads_id` + conversion labels. The consent banner appears automatically once an ID is set.
- `google_business_profile_url`, `google_reviews_url`, and real `reviews` once you have them (the reviews section stays hidden until then)

Also replace the highlighted TODO paragraphs in `content.py`: the About page bio and the fire-safety scope note.

## What's built in for SEO and AI answers
- An Electrician (LocalBusiness) schema on every page: 25-mile GeoCircle service area, opening hours, an offer catalogue with prices, and credentials once the numbers are filled in
- Service, FAQPage and BreadcrumbList schema on each service page
- An "In short" 40–60 word direct answer at the top of each service page, plus question-style H2s
- `llms.txt` summarising the business, prices and pages for AI crawlers
- `sitemap.xml`, `robots.txt`, canonical URLs, Open Graph image, self-hosted fonts, inline CSS (no render-blocking requests)
- Call, WhatsApp and form-submit events tracked as GA4 events and Google Ads conversions (after consent)
- Borough pages for Tower Hamlets, Hackney and Newham, each with that council's licensing rules (checked Nov 2026)

## Adding commercial work later
Add a page block in `content.py` (copy the consumer unit page pattern), add a link in the footer in `build.py`, and rebuild.
