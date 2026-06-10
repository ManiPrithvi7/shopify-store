import { createHmac } from 'crypto';
import getRawBody from 'raw-body';

export const config = { api: { bodyParser: false } };

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const hmac = req.headers['x-shopify-hmac-sha256'];
  const topic = req.headers['x-shopify-topic'];
  const secret = process.env.SHOPIFY_WEBHOOK_SECRET;

  if (!secret) {
    console.error('SHOPIFY_WEBHOOK_SECRET is not configured');
    return res.status(500).json({ error: 'Webhook secret not configured' });
  }

  const rawBody = (await getRawBody(req)).toString('utf8');

  const hash = createHmac('sha256', secret)
    .update(rawBody, 'utf8')
    .digest('base64');

  if (hash !== hmac) {
    console.error('HMAC verification failed');
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (topic === 'orders/paid') {
    const order = JSON.parse(rawBody);
    console.log('Order received:', order.id, order.email);
    console.log('Webhook verified and processed successfully');
  }

  return res.status(200).json({ received: true });
}
