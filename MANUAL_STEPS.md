# Manual Steps (Shopify Admin)

These steps require your Partners account and cannot be automated.

## Day 1 — Dev store and product

### Create development store (if not exists)

1. Go to [dev.shopify.com/dashboard](https://dev.shopify.com/dashboard)
2. Add store → Create development store
3. Name: `proof-test-dev` → `proof-test-dev.myshopify.com`
4. Start with Dawn, USD, timezone America/Los_Angeles
5. Add yourself as staff

### Authenticate CLI

```bash
export PATH="$HOME/.local/bin:$PATH"
cd proof-theme
shopify auth login
```

### Create test product

| Field | Value |
|-------|-------|
| Title | PROOF Display — Test |
| Handle | `proof-display-test` |
| Price | $499.00 |
| Cost | $200.00 |
| SKU | PROOF-TEST-001 |
| Inventory | 100 |
| Weight | 2.5 lbs |
| Status | Active |

### Verify theme (checklist items 1–2, 15)

1. Run `npm run dev` in `proof-theme/`
2. Open storefront → inspect header → `bg-proof-bg` = `#0a0a0a`
3. Change a Tailwind class, save → browser auto-reloads
4. Change product price in admin → storefront updates

---

## Day 2 — Apps and checkout

### Sales Pop (MakeProSimp)

- Position: bottom-left
- Background: `#1a1a2e`, text: `#f0f0f0`
- Real orders only, 5s duration

### Judge.me

- Dark widget, stars on product page, photo reviews
- Add one manual test review

### Abandoned checkout email

- Marketing → Automations → Abandoned checkout
- Trigger: 1 hour, subject: `Complete your PROOF Display order`
- Try **Send test** before waiting 1 hour

### Shopify Inbox

- Welcome: `Hi! Questions about PROOF?`
- 24/7, bottom-right

### Shopify Payments

- Activate test mode if possible; fall back to Bogus Gateway if identity verification blocks

### Test order

1. `/products/proof-display-test` → Add to cart → Checkout
2. Email: `test@example.com`, Portland OR 97201
3. Card: `4242 4242 4242 4242`, exp `12/25`, CVC `123`
4. Confirm order Paid in admin, Sales Pop on product page, confirmation email

---

## Day 3 — Webhook registration

After deploying `proof-api` to Vercel:

1. Admin → Settings → Notifications → Webhooks → Create webhook
2. Event: **Order payment**, Format: JSON
3. URL: `https://proof-webhook-dev.vercel.app/api/shopify/webhook` (your Vercel URL)
4. Copy signing secret → `vercel env add SHOPIFY_WEBHOOK_SECRET`
5. Redeploy: `npx vercel --prod`
6. Place test order → check Vercel logs + webhook Delivered status

### Setup page smoke test

Visit: `https://<vercel-url>/setup?token=test123`
