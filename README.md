# PROOF Display — Test Store Validation

Architecture validation environment for the PROOF Display Shopify storefront.

## Projects

| Directory | Purpose |
|-----------|---------|
| [`proof-theme/`](proof-theme/) | Dawn + Vite + Tailwind v3 theme |
| [`proof-api/`](proof-api/) | Standalone Next.js webhook + setup handoff API |

## Quick start — Theme

```bash
export PATH="$HOME/.local/bin:$PATH"   # Shopify CLI installed to ~/.local/bin
cd proof-theme
shopify auth login
npm run dev -- --store=proof-test-dev
```

Note: Vite config is [`vite.config.mjs`](proof-theme/vite.config.mjs) (ESM required for `vite-plugin-shopify`).

Build production assets:

```bash
npm run vite:build
npm run deploy -- --store=proof-test-dev
```

## Quick start — API

```bash
cd proof-api
cp .env.example .env.local
# Set SHOPIFY_WEBHOOK_SECRET from Admin → Settings → Notifications → Webhooks
npm run dev
```

Deploy to Vercel:

```bash
npx vercel link    # project name: proof-webhook-dev
npx vercel env add SHOPIFY_WEBHOOK_SECRET
npx vercel --prod
```

## Manual steps

See [`MANUAL_STEPS.md`](MANUAL_STEPS.md) for Shopify Admin tasks (dev store, apps, webhook registration).

## Verification

Track all 15 gates in [`VERIFICATION.md`](VERIFICATION.md).
# shopify-store
