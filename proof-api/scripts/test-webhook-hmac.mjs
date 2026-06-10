#!/usr/bin/env node
/**
 * Local smoke test for webhook HMAC verification.
 * Usage: SHOPIFY_WEBHOOK_SECRET=testsecret node scripts/test-webhook-hmac.js
 */
import { createHmac } from 'crypto';
import http from 'http';

const secret = process.env.SHOPIFY_WEBHOOK_SECRET || 'test_webhook_secret';
const body = JSON.stringify({ id: 1001, email: 'test@example.com' });
const hmac = createHmac('sha256', secret).update(body, 'utf8').digest('base64');

const req = http.request(
  {
    hostname: 'localhost',
    port: 3000,
    path: '/api/shopify/webhook',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-shopify-hmac-sha256': hmac,
      'x-shopify-topic': 'orders/paid',
      'x-shopify-shop-domain': 'proof-test-dev.myshopify.com',
    },
  },
  (res) => {
    let data = '';
    res.on('data', (chunk) => { data += chunk; });
    res.on('end', () => {
      console.log('Status:', res.statusCode);
      console.log('Body:', data);
      process.exit(res.statusCode === 200 ? 0 : 1);
    });
  }
);

req.on('error', (err) => {
  console.error('Request failed. Is `npm run dev` running?', err.message);
  process.exit(1);
});

req.write(body);
req.end();
