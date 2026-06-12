#!/usr/bin/env python3
"""Generate V40 Shopify theme sections from PROOF_Display_V40.html extracts."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
HTML = REPO / "PROOF_Display_V40.html"
SECTIONS = ROOT / "sections"
SNIPPETS = ROOT / "snippets"
ASSETS = ROOT / "assets"

SCHEMA_BASE = '''{% schema %}
{
  "name": "__NAME__",
  "tag": "div",
  "class": "proof-section",
  "settings": [
    { "type": "product", "id": "product", "label": "Checkout product" },
    { "type": "url", "id": "demo_video_url", "label": "Demo / video link" }
  ],
  "blocks": [{ "type": "@app" }],
  "presets": [{ "name": "__NAME__" }]
}
{% endschema %}
'''


def schema(name: str) -> str:
    return SCHEMA_BASE.replace("__NAME__", name)

HEAD = "{% render 'proof-checkout-url', section: section %}\n"


def extract_css() -> str:
    raw = HTML.read_text(encoding="utf-8")
    parts = re.findall(r"<style>(.*?)</style>", raw, re.DOTALL)
    if not parts:
        raise SystemExit("CSS not found")
    css = "\n\n".join(p.strip() for p in parts)
    shopify_css = """
/* ── Shopify app integration (V40) ── */
.skip-link {
  position: absolute; left: -9999px; top: auto; width: 1px; height: 1px; overflow: hidden;
}
.skip-link:focus {
  position: fixed; left: 16px; top: 16px; width: auto; height: auto;
  padding: 12px 20px; background: var(--gold); color: var(--ink);
  font-family: var(--font-mono); font-size: 12px; z-index: 1000;
}
.proof-app-zone {
  padding: clamp(60px, 8vw, 100px) 40px;
  background: var(--ink);
  border-top: 0.5px solid var(--warm-border);
}
.proof-app-zone .inner { max-width: 960px; margin: 0 auto; }
.proof-app-zone .eyebrow {
  font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.28em;
  text-transform: uppercase; color: var(--gold); margin-bottom: 16px; display: block;
}
.proof-app-zone__sub {
  color: var(--text-secondary); margin-bottom: 32px; max-width: 560px;
}
.proof-app-zone__grid { display: grid; gap: 24px; }
.proof-app-zone__grid--single { grid-template-columns: 1fr; }
.proof-app-zone__grid--split { grid-template-columns: repeat(2, 1fr); }
.proof-app-zone__card {
  padding: 28px; border: 0.5px solid var(--warm-border); border-radius: 4px;
  background: rgba(20, 18, 16, 0.6);
}
.proof-app-zone__placeholder {
  padding: 40px; text-align: center; border: 1px dashed var(--warm-border);
  border-radius: 4px; color: var(--text-muted);
}
.proof-app-zone__placeholder-title {
  font-family: var(--font-serif); font-size: 20px; color: var(--cream); margin-bottom: 8px;
}
.proof-app-zone--pdp { padding: 60px 24px; }
.proof-app-zone__pdp-heading {
  font-family: var(--font-serif); font-size: clamp(24px, 3vw, 32px);
  color: var(--cream); margin-bottom: 24px;
}
.proof-embed-rail {
  position: fixed; bottom: 24px; left: 24px; right: 24px; z-index: 250;
  pointer-events: none; display: flex; justify-content: space-between; align-items: flex-end; gap: 16px;
}
.proof-embed-rail__inner { display: contents; }
.proof-embed-slot {
  pointer-events: auto; max-width: 220px; padding: 12px 14px;
  background: rgba(11, 10, 8, 0.92); border: 0.5px solid var(--warm-border);
  border-radius: 4px; backdrop-filter: blur(12px);
}
.proof-embed-slot__icon { color: var(--gold); margin-right: 6px; }
.proof-embed-slot__label {
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--cream);
}
.proof-embed-slot__hint {
  display: block; font-size: 10px; color: var(--text-muted); margin-top: 4px; line-height: 1.4;
}
.proof-embed-slot.is-active { border-color: var(--gold); }
.proof-embed-slot.is-active .proof-embed-slot__hint { color: var(--gold); }
@media (max-width: 720px) {
  .proof-embed-rail { flex-direction: column; align-items: stretch; }
  .proof-embed-slot { max-width: none; }
  .proof-embed-slot__hint { display: none; }
}
@media (max-width: 960px) {
  .proof-app-zone__grid--split { grid-template-columns: 1fr; }
}
/* Legacy aliases for PDP */
:root {
  --surface-base: var(--ink);
  --surface-raised: var(--warm-mid);
  --neutral-100: var(--cream);
  --neutral-500: var(--text-secondary);
  --brand-primary: var(--gold);
  --font-display: var(--font-serif);
  --font-body: var(--font-sans);
  --charcoal: var(--ink);
  --white: var(--cream);
  --fog: var(--text-secondary);
}
"""
    return css + shopify_css


def wire_urls(html: str) -> str:
    html = html.replace(
        "https://proofnexus.com/products/proof-display",
        "{{ product_url }}",
    )
    html = html.replace('href="#" class="nav-logo"', 'href="/" class="nav-logo"')
    return html


def write_css():
    out = ASSETS / "proof-landing.css"
    out.write_text(extract_css(), encoding="utf-8")
    print(f"Wrote {out}")


def write_snippets():
    device = """<!-- 3D PROOF device mock — V40 -->
<div class="hero-device-wrap">
  <div class="device-scene" id="deviceScene">
    <div class="device-3d" id="device3d">
      <div class="device-flag">
        <div class="flag-panel"><span class="flag-text">PROOF</span></div>
        <div class="flag-pole"></div>
      </div>
      <div class="device-body">
        <div class="device-screen">
          <div class="screen-content">
            <div class="screen-label">Google Reviews</div>
            <div class="screen-stars">
              <span class="star">★</span><span class="star">★</span><span class="star">★</span><span class="star">★</span><span class="star">★</span>
            </div>
            <div class="screen-rating">4.9</div>
            <div class="screen-count">Based on 91 reviews</div>
            <div class="screen-divider"></div>
            <div class="screen-google">Google · Verified</div>
          </div>
        </div>
        <div class="device-led"></div>
        <div class="device-nfc">
          <div class="nfc-ring"></div>
          <div class="nfc-ring"></div>
          <div class="nfc-ring"></div>
          <div class="nfc-dot"></div>
        </div>
      </div>
      <div class="device-side-right"></div>
      <div class="device-side-bottom"></div>
      <div class="device-base">
        <div class="base-shadow"></div>
        <div class="base-top">
          <div class="base-insert base-insert-tl"></div>
          <div class="base-insert base-insert-tr"></div>
          <div class="base-insert base-insert-bl"></div>
          <div class="base-insert base-insert-br"></div>
          <div class="base-nfc-slot"></div>
          <div class="base-engraving">PROOF</div>
        </div>
        <div class="base-front"></div>
      </div>
      <div class="device-reflection"></div>
    </div>
  </div>
</div>
"""
    (SNIPPETS / "proof-device-3d.liquid").write_text(device, encoding="utf-8")

    section_header = """{%- comment -%}
  label, heading, subheading — pass as render params
{%- endcomment -%}
<span class="section-label reveal">{{ label }}</span>
<h2 class="section-h2 reveal reveal-delay-1"{% if heading_id != blank %} id="{{ heading_id }}"{% endif %}>{{ heading }}</h2>
{%- if subheading != blank -%}
  <p class="section-sub reveal reveal-delay-2">{{ subheading }}</p>
{%- endif -%}
"""
    (SNIPPETS / "proof-section-header.liquid").write_text(section_header, encoding="utf-8")

    print("Wrote snippets")


def write_chrome():
    body = HEAD + """<div class="ambient-bg" aria-hidden="true">
  <div class="ambient-orb ambient-orb-1"></div>
  <div class="ambient-orb ambient-orb-2"></div>
  <div class="ambient-orb ambient-orb-3"></div>
</div>

<a href="#main-content" class="skip-link">Skip to main content</a>
<nav id="main-nav" role="navigation" aria-label="Main navigation">
  <a href="/" class="nav-logo">
    <div class="nav-logo-mark"><span>P</span></div>
    PROOF
  </a>
  <ul class="nav-links">
    <li><a href="#how-it-works">How it works</a></li>
    <li><a href="#screens">Screens</a></li>
    <li><a href="#results">Results</a></li>
    <li><a href="#pricing">Pricing</a></li>
    <li><a href="#faq">FAQ</a></li>
    <li><a href="{{ product_url }}" class="nav-cta">Order Now — $499</a></li>
  </ul>
</nav>
"""
    (SECTIONS / "proof-chrome.liquid").write_text(
        body + schema("PROOF Chrome"), encoding="utf-8"
    )


def write_hero():
    body = HEAD + """<section class="hero" id="hero" aria-label="Hero — PROOF Display">
  <div class="hero-eyebrow" id="speakable-hero">NFC Review Display · Countertop Trust Device · Portland Pilot Open</div>
  <h1 class="hero-h1">
    <span class="shimmer-text">Your Reputation.</span>
  </h1>
  <h1 class="hero-h1-sub">Live on Your Counter.</h1>
  <p class="hero-sub">
    Most of your happy customers never leave a review. PROOF displays your reputation live — and gives every satisfied customer one tap to add to it.
  </p>
  <div class="hero-ctas">
    <a href="{{ product_url }}" class="btn-primary">
      <span class="btn-primary-inner">Order Now — $499 ↗</span>
    </a>
    <a href="#how-it-works" class="btn-secondary">See how it works</a>
  </div>
  {% render 'proof-device-3d' %}
</section>
"""
    (SECTIONS / "proof-hero.liquid").write_text(
        body + schema("PROOF Hero"), encoding="utf-8"
    )


def write_video():
    body = HEAD + """<section class="proof-motion" aria-label="PROOF Display in motion">
  <div class="pm-ambient"></div>
  <div class="pm-grain"></div>
  <div class="pm-inner">
    <div class="pm-eyebrow reveal">
      <span class="pm-eyebrow-line"></span>
      <span>PROOF in motion</span>
      <span class="pm-eyebrow-line"></span>
    </div>
    <h2 class="pm-headline reveal reveal-delay-1">
      Eight seconds. <em>One tap.</em> Everything changes.
    </h2>
    <div class="pm-frame reveal reveal-delay-2">
      <div class="pm-corner pm-tl"></div>
      <div class="pm-corner pm-tr"></div>
      <div class="pm-corner pm-bl"></div>
      <div class="pm-corner pm-br"></div>
      <div class="pm-video-wrap">
        <video class="pm-video" autoplay muted loop playsinline preload="auto"
          poster="{{ 'proof-motion-poster.jpg' | asset_url }}"
          aria-label="Close-up of PROOF Display on a café counter">
          <source src="{{ 'proof-motion.mp4' | asset_url }}" type="video/mp4">
        </video>
        <div class="pm-vignette"></div>
        <div class="pm-scan"></div>
        <div class="pm-caption">
          <span class="pm-rec"><span class="pm-rec-dot"></span>LIVE</span>
          <span class="pm-cap-text">PROOF Display · Foxtail Coffee · 02:14 PM</span>
          <span class="pm-cap-tc">00:00:08:00</span>
        </div>
      </div>
    </div>
    <div class="pm-meta reveal reveal-delay-3">
      <div class="pm-meta-col"><div class="pm-meta-k">Tap latency</div><div class="pm-meta-v">~140ms</div></div>
      <div class="pm-meta-col"><div class="pm-meta-k">Customer steps</div><div class="pm-meta-v">1</div></div>
      <div class="pm-meta-col"><div class="pm-meta-k">Staff involvement</div><div class="pm-meta-v">0</div></div>
      <div class="pm-meta-col"><div class="pm-meta-k">Outcome</div><div class="pm-meta-v">~1 review / day</div></div>
    </div>
  </div>
</section>
"""
    schema = """{% schema %}
{
  "name": "PROOF in motion",
  "tag": "div",
  "class": "proof-section",
  "settings": [
    { "type": "product", "id": "product", "label": "Checkout product" },
    { "type": "url", "id": "demo_video_url", "label": "Fallback demo link" }
  ],
  "presets": [{ "name": "PROOF in motion" }]
}
{% endschema %}
"""
    (SECTIONS / "proof-video.liquid").write_text(body + schema, encoding="utf-8")


def read_body_slice(start_marker: str, end_marker: str | None) -> str:
    raw = HTML.read_text(encoding="utf-8")
    si = raw.index(start_marker)
    if end_marker:
        ei = raw.index(end_marker, si)
        chunk = raw[si:ei].strip()
    else:
        chunk = raw[si:].strip()
    return wire_urls(chunk)


def write_from_html(filename: str, start: str, end: str | None, schema_name: str):
    chunk = read_body_slice(start, end)
    (SECTIONS / filename).write_text(
        HEAD + chunk + "\n" + schema(schema_name),
        encoding="utf-8",
    )


def write_footer():
    body = HEAD + """<footer>
  <div class="footer-brand">PROOF</div>
  <ul class="footer-links">
    <li><a href="#how-it-works">How it works</a></li>
    <li><a href="#screens">Screens</a></li>
    <li><a href="#results">Results</a></li>
    <li><a href="#pricing">Pricing</a></li>
    <li><a href="#faq">FAQ</a></li>
    <li><a href="mailto:hello@proofnexus.com">Contact</a></li>
  </ul>
  <div class="footer-copy">© {{ 'now' | date: '%Y' }} Proof Nexus Inc. Portland, OR</div>
</footer>
"""
    (SECTIONS / "proof-footer.liquid").write_text(
        body + schema("PROOF Footer"), encoding="utf-8"
    )


def write_faq():
    chunk = read_body_slice(
        '<section class="faq-section" id="faq"',
        "<!-- ESTABLISH MODE + OBJECTIONS -->",
    )
    chunk = chunk.replace('onclick="toggleFaq(this)"', 'type="button"')
    chunk = re.sub(
        r'<button class="faq-q" type="button"',
        '<button class="faq-q" type="button" aria-expanded="false"',
        chunk,
    )
    (SECTIONS / "proof-faq.liquid").write_text(
        HEAD + chunk + "\n" + schema("PROOF FAQ"), encoding="utf-8"
    )


def write_fcta():
    chunk = read_body_slice(
        '<section class="final-cta" id="order"',
        "<style>",
    )
    (SECTIONS / "proof-fcta.liquid").write_text(
        HEAD + chunk + "\n" + schema("PROOF Final CTA"), encoding="utf-8"
    )


def write_new_sections():
    write_from_html(
        "proof-ticker-trust.liquid",
        '<div class="ticker-section">',
        "<!-- RESULTS -->",
        "PROOF Ticker",
    )
    write_from_html(
        "proof-results.liquid",
        '<section class="results-section" id="results"',
        "<!-- QR FRICTION vs PROOF -->",
        "PROOF Results",
    )
    write_from_html(
        "proof-how-it-works.liquid",
        '<section class="qr-section" id="how-it-works"',
        "<!-- SCREENS -->",
        "PROOF How it works",
    )
    write_from_html(
        "proof-screens.liquid",
        '<section class="screens-section" id="screens"',
        "<!-- TESTIMONIALS -->",
        "PROOF Screens",
    )
    write_from_html(
        "proof-testimonials.liquid",
        '<section class="testimonials-section" id="testimonials"',
        "<!-- PRICING -->",
        "PROOF Testimonials",
    )
    write_from_html(
        "proof-pricing.liquid",
        '<section class="pricing-section" id="pricing"',
        "<!-- QUICK ANSWERS / AEO -->",
        "PROOF Pricing",
    )


def write_checkout_url():
    content = """{%- liquid
  assign proof_product = nil
  if section.settings.product != blank
    assign proof_product = section.settings.product
  elsif settings.proof_checkout_product != blank
    assign proof_product = settings.proof_checkout_product
  endif

  if proof_product != blank
    assign product_url = proof_product.url
  else
    assign product_url = '/products/proof-display-test'
  endif

  if section.settings.demo_video_url != blank
    assign demo_url = section.settings.demo_video_url
  else
    assign demo_url = '#how-it-works'
  endif
-%}
"""
    (SNIPPETS / "proof-checkout-url.liquid").write_text(content, encoding="utf-8")


def main():
    write_css()
    write_snippets()
    write_checkout_url()
    write_chrome()
    write_hero()
    write_video()
    write_new_sections()
    write_faq()
    write_fcta()
    write_footer()
    print("V40 theme build complete")


if __name__ == "__main__":
    main()
