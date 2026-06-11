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

## V23 landing page (homepage)

The storefront homepage (`/`) uses the custom V23 design, not Dawn defaults.

| File | Purpose |
|------|---------|
| `layout/theme.proof.liquid` | Minimal layout — no Dawn header/footer; keeps `content_for_header` for apps |
| `sections/proof-chrome.liquid` | Sticky buy bar + nav |
| `sections/proof-hero.liquid` … `proof-fcta.liquid` | **22 V23 sections** — add/reorder in Theme Editor |
| `sections/proof-app-zone.liquid` | Dedicated **App blocks** zone |
| `sections/proof-embed-rail.liquid` | Visual anchors for Inbox / Sales Pop embeds |
| `sections/proof-footer.liquid` | V23 footer |
| `sections/proof-product-apps.liquid` | Product page app block zone |
| `assets/proof-landing.css` | V23 design system + app embed offsets |
| `assets/proof-landing.js` | Simulator, sticky bar, FAQ, scroll reveal |
| `snippets/proof-schema.liquid` | JSON-LD structured data |
| `templates/index.json` | `"layout": "theme.proof"` + `proof-landing` section |

**Checkout product:** Theme Editor → Homepage → PROOF Landing → set **Checkout product** to `proof-display-test` (fallback URL: `/products/proof-display-test`).

**Preview with apps:** Use `http://127.0.0.1:9292` after `npm run dev` — not Vite-only `localhost:5173`.

## App embeds + app blocks (inside V23 design)

Homepage is split into **multiple Theme Editor sections** — you can add/reorder sections and drop app blocks into **PROOF App zone**.

### Step 1 — Global embeds (Inbox, Sales Pop)

Theme Editor → **App embeds** → enable Shopify Inbox (+ Sales Pop).

- **PROOF Embed rail** section shows labeled slots; they highlight when widgets load.
- CSS in `proof-landing.css` keeps widgets clear of the sticky buy bar.

### Step 2 — App blocks on homepage

Theme Editor → Homepage → **PROOF App zone** → **Add block** → pick an app (e.g. Judge.me preview widget if available).

Blocks render inside a gold-bordered card matching V23 tokens.

### Step 3 — Product page reviews

Theme Editor → **Product** template → **PROOF Product apps** section → **Add block** → Judge.me.

(You can also add Judge.me to `main-product` blocks if you prefer inline with buy box.)

### Theme setting

**Theme settings → PROOF → Default checkout product** applies to all PROOF sections when a section has no product set.

After enabling, save. Do not `theme pull` Horizon JSON into this repo.

## Theme JSON mismatch (upload errors)

If you see `product-recommendations` or `badge_corner_radius` errors, restore Dawn files:

```bash
git checkout HEAD -- templates/product.json config/settings_data.json
```
