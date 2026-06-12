# proof-theme — Dev setup

## If you see "don't have access to this dev store"

This is an **account permissions** issue, not a Vite/Tailwind bug.

### 1. Log in with the correct Shopify account

```bash
export PATH="$HOME/.local/bin:$PATH"
npm run auth
# or: shopify auth login
```

Use the email that **owns** the dev store or was added as **staff**.

### 2. Confirm the store in `shopify.theme.toml`

Edit `[environments.development]` → `store` to your real dev store URL:

```toml
store = "your-store.myshopify.com"
```

### 3. Start dev

```bash
npm run dev
```

Override store without editing files:

```bash
SHOPIFY_FLAG_STORE=your-store.myshopify.com npm run dev
```

### 4. No Partners / Stores access (403)?

Create your own dev store at [dev.shopify.com/dashboard](https://dev.shopify.com/dashboard), then set that URL in `shopify.theme.toml`.

You cannot develop against a store unless your logged-in account has CLI + staff access on it.

## V40 landing page (homepage)

The storefront homepage (`/`) uses the **V40** design — 13 Theme Editor sections on `theme.proof` layout.

| File | Purpose |
|------|---------|
| `layout/theme.proof.liquid` | Minimal layout, `<main>`, fonts, Lenis + landing JS |
| `sections/proof-chrome.liquid` | Ambient orbs + V40 nav (`#main-nav`) |
| `sections/proof-hero.liquid` … `proof-fcta.liquid` | **13 V40 sections** — add/reorder in Theme Editor |
| `sections/proof-app-zone.liquid` | App blocks zone (after testimonials, before pricing) |
| `snippets/proof-embed-rail.liquid` | Inbox / Sales Pop anchors (layout, not in section count) |
| `sections/proof-footer.liquid` | V40 footer |
| `sections/proof-product-apps.liquid` | Product page app block zone |
| `assets/proof-landing.css` | V40 design system + app embed styles |
| `assets/proof-landing.js` | Lenis, device tilt, FAQ, odometers |
| `assets/proof-motion.mp4` | Hero video (extracted from V40 HTML) |
| `snippets/proof-schema.liquid` | V40 JSON-LD (Product, FAQPage, Dataset) |
| `templates/index.json` | `"layout": "theme.proof"` + 13 sections |
| `archive/v23/` | Retired V23 sections (rollback only — not uploaded; Shopify forbids subfolders in `sections/`) |

### Nav anchor IDs (V40)

| Link | Target |
|------|--------|
| How it works | `#how-it-works` |
| Screens | `#screens` |
| Results | `#results` |
| Pricing | `#pricing` |
| FAQ | `#faq` |

**Checkout product:** Theme Editor → any PROOF section → **Checkout product**, or **Theme settings → PROOF → Default checkout product** (`proof-display-test` fallback).

**Preview with apps:** Use `http://127.0.0.1:9292` after `npm run dev` — not Vite-only `localhost:5173`.

## App embeds + app blocks (inside V40 design)

### Step 1 — Global embeds (Inbox, Sales Pop)

Theme Editor → **App embeds** → enable Shopify Inbox (+ Sales Pop).

- **PROOF Embed rail** shows labeled slots in the layout footer area.
- CSS keeps widgets clear of page content (no sticky buy bar in V40).

### Step 2 — App blocks on homepage

Theme Editor → Homepage → **PROOF App zone** (between Testimonials and Pricing) → **Add block** → Judge.me or Sales Pop preview.

### Step 3 — Product page reviews

Theme Editor → **Product** template → **PROOF Product apps** → **Add block** → Judge.me.

### Theme setting

**Theme settings → PROOF → Default checkout product** applies when a section has no product set.

## Content policy (V40 source of truth)

- **Guarantee:** 30-day pilot / money-back on hardware
- **Manufacturer:** Portland, OR
- **JSON-LD URLs:** Shopify canonical (`shop.url` + product path)

## Known launch gap

V40 hides desktop nav links below ~960px with **no hamburger menu**. Mobile users rely on scroll + final CTA. Add a mobile menu in a fast-follow if needed.

## Theme JSON mismatch (upload errors)

If you see `product-recommendations` or `badge_corner_radius` errors, restore Dawn files:

```bash
git checkout HEAD -- templates/product.json config/settings_data.json
```
