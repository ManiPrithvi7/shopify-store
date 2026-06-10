# Deploy proof-api to Vercel

Deployment requires Vercel authentication (not available in automated setup).

## Steps

```bash
cd proof-api
npx vercel login
npx vercel link          # project name: proof-webhook-dev
npx vercel env add SHOPIFY_WEBHOOK_SECRET production
npx vercel env add SHOPIFY_WEBHOOK_SECRET preview
npx vercel --prod
```

## Webhook secret

1. Shopify Admin → Settings → Notifications → Webhooks → Create webhook
2. Event: Order payment, Format: JSON
3. URL: `https://proof-webhook-dev.vercel.app/api/shopify/webhook`
4. Copy the signing secret shown at creation → use for `SHOPIFY_WEBHOOK_SECRET`
5. Redeploy after setting env var

## Verify

```bash
# After deploy
curl "https://<your-vercel-url>/setup?token=test123"

# Place test order, then check Vercel → Project → Logs
```

## Local test (before deploy)

```bash
SHOPIFY_WEBHOOK_SECRET=test_webhook_secret npm run dev
# In another terminal:
SHOPIFY_WEBHOOK_SECRET=test_webhook_secret node scripts/test-webhook-hmac.mjs
```
