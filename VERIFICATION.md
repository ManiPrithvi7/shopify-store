# PROOF Test Store — Verification Checklist

Mark each gate after testing. **All 15 must pass** before full development.

| # | Feature | Test method | Expected result | Status |
|---|---------|-------------|-----------------|--------|
| 1 | Tailwind in Liquid | Inspect header element | `bg-proof-bg` applied, color `#0a0a0a` | ☐ Agent: code ready — **you verify on live store** |
| 2 | Vite hot reload | Change CSS class, save | Browser auto-refreshes | ☐ Agent: toolchain ready — **you verify with `npm run dev`** |
| 3 | Sales Pop | Visit product page after order | Popup shows real purchase | ☐ **Manual** — install app + test order |
| 4 | Judge.me Reviews | Visit product page | Stars + review visible | ☐ **Manual** — install app + add review |
| 5 | Abandoned cart email | Abandon cart with email | Email received (test-send or 1h) | ☐ **Manual** — configure automation |
| 6 | Shopify Inbox | Click chat bubble | Chat opens, message in admin | ☐ **Manual** — enable Inbox |
| 7 | Shopify Payments | Proceed to checkout | Test card accepted | ☐ **Manual** — test order |
| 8 | Shop Pay | Checkout page | Shop Pay button visible | ☐ **Manual** — depends on Payments setup |
| 9 | Apple/Google Pay | Mobile / Chrome checkout | Buttons visible | ☐ **Manual** — depends on Payments setup |
| 10 | Order confirmation | Complete test order | Email received | ☐ **Manual** — test order |
| 11 | Webhook fires | Place order, check Vercel logs | POST `/api/shopify/webhook` 200 | ☐ **Manual** — after Vercel deploy + webhook register |
| 12 | HMAC verification | Check Vercel logs | "Webhook verified and processed successfully" | ☐ Local test passed (200 + valid HMAC) — **confirm on Vercel after deploy** |
| 13 | Dashboard setup URL | Visit `/setup?token=test123` | Page loads, token displayed | ☐ Local test passed (HTTP 200) — **confirm on Vercel after deploy** |
| 14 | Mobile responsive | iPhone / Android | No horizontal scroll | ☐ **Manual** — test on device |
| 15 | Dynamic product data | Change price in admin | Storefront updates | ☐ **Manual** — after product created |

## Agent-completed implementation

| Item | Status |
|------|--------|
| Shopify CLI installed (`~/.local/bin`, v4.1.0) | ✅ |
| `proof-theme/` Dawn + Vite 5 + Tailwind v3 | ✅ |
| PROOF color tokens in `tailwind.config.cjs` | ✅ |
| `vite-tag` wired in `theme.liquid` | ✅ |
| `bg-proof-bg` on header | ✅ |
| `vite build` produces hashed assets | ✅ |
| MCP `validate_theme` — header + vite-tag | ✅ |
| `proof-api/` webhook with raw-body HMAC | ✅ |
| `proof-api/` `/setup` page with PROOF tokens | ✅ |
| `proof-api` production build | ✅ |
| Webhook HMAC local smoke test (`scripts/test-webhook-hmac.mjs`) | ✅ |
| `/setup?token=test123` local smoke test | ✅ |
| Vercel deploy (`proof-webhook-dev`) | ⏳ Run `vercel login` then `npx vercel --prod` |

## Decision gate

| Criteria | Pass / Fail | Action if fail |
|----------|-------------|----------------|
| All 15 verification checks pass | ☐ | Investigate and fix |
| Test order completes in < 2 minutes | ☐ | Optimize checkout flow |
| Webhook delivers in < 5 seconds | ☐ | Check Vercel cold start |
| Apps load without console errors | ☐ | Check app compatibility |
| Mobile experience functional | ☐ | Fix responsive issues |

**If all pass:** Proceed to full theme development.  
**If any fail:** Debug before committing resources.
