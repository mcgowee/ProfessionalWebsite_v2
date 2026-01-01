import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';

// DEV: use your VPS host/port because Windows doesn't have Flask on 127.0.0.1:5000
// Use VITE_API_URL from environment or default to localhost
const BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';
const DEV_FLASK_URL = `${BASE}/api/solve`;

export const POST: RequestHandler = async ({ request }) => {
  try {
    const payload = await request.json();

    // In DEV, easiest is to allow passing a key via env if you want,
    // but if you don't want keys locally, temporarily disable auth on Flask /solve (not recommended).
    const apiKey = process.env.FLASK_API_KEY ?? '';

    const r = await fetch(DEV_FLASK_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {})
      },
      body: JSON.stringify(payload)
    });

    const text = await r.text();
    return new Response(text, {
      status: r.status,
      headers: { 'Content-Type': r.headers.get('content-type') || 'application/json' }
    });
  } catch (err) {
    console.error('Wordle dev proxy error:', err);
    return json({ error: 'Dev proxy failed to reach Flask.' }, { status: 502 });
  }
};
