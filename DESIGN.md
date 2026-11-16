---
world: on-site
colors:
  dark: "#0B2A21"        # forest green: header, hero tint, dark cards, footer (trust, "passed", safety)
  accent: "#F5A524"      # amber from the logo: ONLY things to click (book, see price) plus small markers
  soft: "#F7F3EA"        # warm ivory: alternate sections; the third colour that makes it feel premium
  accent-50: "#FDF3DF"
  ink: "#10201A"
  muted: "#4F5D56"
  line: "#E8E3D7"
type:
  family: "Manrope (variable, self-hosted), 600 for headings, 700-800 for prices and UI"
  scale: "h1 clamp(2.5rem→5rem) lh 1.02 tracking -.035em; h2 clamp(1.9rem→3rem); body 1.0625rem/1.65"
radius: { xl: 28px, lg: 20px, md: 14px, sm: 10px, buttons: pill }
---

# Design: on site

A photographic, premium trade look in three colours: forest green for structure, amber (the logo colour) only for actions,
and warm ivory sections alternating with white. Generous white space: sections are 5.5-9.5rem tall in padding.

## Rules

- **Sections open with an intro row**: a small amber-square label (`.tag`) on the left and the heading on the right (`.intro`).
- **Photos carry the page.** Hero, feature photo with stats, service photo cards, how-it-works photo, CTA band. Stand-ins are listed in `src/img/CREDITS.txt`; swap for real photos when available.
- **Buttons are pills.** Amber = the main action (book, see price). Dark pills for secondary links. Glass pills on photos.
- **Never invent facts.** Stats and counters only use numbers from `site.config.json` or the copy (radius, bundle saving, reminder days).

## Motion (all off under prefers-reduced-motion)

- Hero: photo slow zoom-out, headline words rise in one by one (`[data-split]`), the rest fades up (`.hero-fade`).
- Scroll reveals: add `data-reveal` (or `="zoom" | "left" | "right"`), stagger with `style="--d:.1s"`.
- Count-ups: `<span data-count="25">25</span>` inside a revealed block.
- Service cards: image zoom plus an amber panel sliding up on hover/focus. Areas marquee in a dark band.
- Header turns translucent with blur after 24px of scroll.

## Files

- Tokens and components: `src/styles.css`. Motion JS at the end of `src/main.js`. Markup: `build.py`, `content.py`, `content_more.py`.
- Fonts: `src/fonts/manrope.woff2` (SIL Open Font License, licence alongside). Photos: `src/img/`.
