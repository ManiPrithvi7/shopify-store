import { useRouter } from 'next/router';

export default function Setup() {
  const router = useRouter();
  const { token } = router.query;

  return (
    <div className="min-h-screen bg-proof-bg text-proof-text p-8">
      <h1 className="text-2xl font-bold">PROOF Display Setup</h1>
      <p className="mt-4 text-proof-muted">Token: {token || 'No token provided'}</p>
      {token && (
        <div className="mt-8">
          <p className="text-green-400">Token received successfully</p>
          <p className="mt-2">In production, this would:</p>
          <ul className="list-disc ml-6 mt-2 text-proof-muted">
            <li>Validate token against database</li>
            <li>Link to Shopify order</li>
            <li>Start device configuration</li>
          </ul>
        </div>
      )}
    </div>
  );
}
