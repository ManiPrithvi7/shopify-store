#!/usr/bin/env python3
import re
from pathlib import Path

theme = Path(__file__).resolve().parent.parent
main_path = theme / "sections/proof-landing-main.liquid"
raw = main_path.read_text(encoding="utf-8")

# Extract content between <main> and </main>
start = raw.index('<main id="main-content"')
end = raw.index('</main><!-- end #main-content -->')
text = raw[start:end]
text = re.sub(r'^<main[^>]*>\s*', '', text)

# Fix placement markup
text = text.replace(
    '<!-- ══ PLACEMENT ══ -->\n<section class="s placement" id="placement">\n\n<!-- ══ BEFORE / AFTER ══ -->',
    '<!-- ══ BEFORE / AFTER ══ -->',
)
text = text.replace(
    '<!-- ══ PLACEMENT ══ -->\n  <div class="inner">',
    '<!-- ══ PLACEMENT ══ -->\n<section class="s placement" id="placement">\n  <div class="inner">',
)

markers = [
    ("proof-hero", "PROOF Hero", "<!-- ══ HERO ══ -->", "<!-- LIVE TICKER -->"),
    ("proof-ticker-trust", "PROOF Ticker & trust", "<!-- LIVE TICKER -->", "<!-- ══ COUNTER STACK ══ -->"),
    ("proof-counter-stack", "PROOF Counter stack", "<!-- ══ COUNTER STACK ══ -->", "<!-- ══ VIDEO DEMO ══ -->"),
    ("proof-video", "PROOF Video", "<!-- ══ VIDEO DEMO ══ -->", "<!-- ══ VERTICALS ══ -->"),
    ("proof-verticals", "PROOF Verticals", "<!-- ══ VERTICALS ══ -->", "<!-- ══ WHY IT WORKS ══ -->"),
    ("proof-why", "PROOF Why it works", "<!-- ══ WHY IT WORKS ══ -->", "<!-- ══ GOLD BREAK — KEY METRICS ══ -->"),
    ("proof-gold-break", "PROOF Key metrics", "<!-- ══ GOLD BREAK — KEY METRICS ══ -->", "<!-- ══ PATTERN INTERRUPT ══ -->"),
    ("proof-pattern-interrupt", "PROOF Pattern interrupt", "<!-- ══ PATTERN INTERRUPT ══ -->", "<!-- ══ CATEGORY DEFINITION ══ -->"),
    ("proof-category", "PROOF Category", "<!-- ══ CATEGORY DEFINITION ══ -->", "<!-- ══ MECHANISM ══ -->"),
    ("proof-mechanism", "PROOF Mechanism", "<!-- ══ MECHANISM ══ -->", "<!-- ══ BEFORE / AFTER ══ -->"),
    ("proof-before-after", "PROOF Before after", "<!-- ══ BEFORE / AFTER ══ -->", "<!-- ══ COMPARISON TABLE ══ -->"),
    ("proof-comparison", "PROOF Comparison", "<!-- ══ COMPARISON TABLE ══ -->", "<!-- ══ PLACEMENT ══ -->"),
    ("proof-placement", "PROOF Placement", "<!-- ══ PLACEMENT ══ -->", "<!-- ══ 30 DAYS TIMELINE ══ -->"),
    ("proof-timeline", "PROOF Timeline", "<!-- ══ 30 DAYS TIMELINE ══ -->", "<!-- ══ ROI SIMULATOR ══ -->"),
    ("proof-simulator", "PROOF Simulator", "<!-- ══ ROI SIMULATOR ══ -->", "<!-- ══ IN THE WILD ══"),
    ("proof-customers", "PROOF Customers", "<!-- ══ IN THE WILD ══", "<!-- ══ PRICING ══ -->"),
    ("proof-pricing", "PROOF Pricing", "<!-- ══ PRICING ══ -->", "<!-- ══ RISK REVERSAL ══ -->"),
    ("proof-risk-reversal", "PROOF Risk reversal", "<!-- ══ RISK REVERSAL ══ -->", "<!-- ══ TESTIMONIALS ══ -->"),
    ("proof-testimonials", "PROOF Testimonials", "<!-- ══ TESTIMONIALS ══ -->", "<!-- ══ FAQ ══ -->"),
    ("proof-faq", "PROOF FAQ", "<!-- ══ FAQ ══ -->", "<!-- ══ AEO ANSWER BLOCKS ══ -->"),
    ("proof-aeo", "PROOF AEO", "<!-- ══ AEO ANSWER BLOCKS ══ -->", "<section class=\"fcta\">"),
    ("proof-fcta", "PROOF Final CTA", "<section class=\"fcta\">", None),
]

SCHEMA = '''{% schema %}
{
  "name": "{title}",
  "tag": "section",
  "class": "proof-section",
  "settings": [
    { "type": "product", "id": "product", "label": "Checkout product" },
    { "type": "url", "id": "demo_video_url", "label": "90-sec demo link" }
  ],
  "blocks": [{ "type": "@app" }],
  "presets": [{ "name": "{title}" }]
}
{% endschema %}
'''

HEAD = "{% render 'proof-checkout-url', section: section %}\n"
sections_dir = theme / "sections"
order = []

for slug, title, start_marker, end_marker in markers:
    si = text.index(start_marker)
    if end_marker:
        ei = text.index(end_marker, si)
        chunk = text[si:ei].strip()
    else:
        chunk = text[si:].strip()
        # fcta: from <section class="fcta"> to </section>
        close = chunk.index("</section>") + len("</section>")
        chunk = chunk[:close]

    body = HEAD + chunk + "\n"
    if slug == "proof-hero":
        body = HEAD + '<main id="main-content" role="main">\n' + chunk + "\n"
    if slug == "proof-fcta":
        body = HEAD + chunk + "\n</main>\n"

    body += SCHEMA.replace("{title}", title)
    (sections_dir / f"{slug}.liquid").write_text(body, encoding="utf-8")
    order.append(slug)
    print(slug, len(chunk))

# index.json
import json
index = {
    "layout": "theme.proof",
    "sections": {},
    "order": ["proof-chrome"]
    + order
    + ["proof-app-zone", "proof-footer", "proof-embed-rail"],
}
for sid in index["order"]:
    if sid == "proof-app-zone":
        index["sections"][sid] = {
            "type": "proof-app-zone",
            "settings": {
                "heading": "Trusted by merchants",
                "subheading": "Live reviews and social proof from your installed Shopify apps.",
                "layout": "single",
            },
        }
    else:
        index["sections"][sid] = {"type": sid, "settings": {}}

(theme / "templates/index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
print("sections:", len(order))
print("index order:", len(index["order"]))
