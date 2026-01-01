import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

const FLASK_URL = 'http://127.0.0.1:5000/send-email';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const body = await request.json();
    const name = String(body?.name ?? '').trim();
    const email = String(body?.email ?? '').trim();
    const message = String(body?.message ?? '').trim();

    if (!name || !email || !message) {
      return new Response('Missing name, email, or message.', { status: 400 });
    }

    // Basic sanity check (not perfect validation, but enough to reduce junk)
    if (!email.includes('@') || email.length > 254) {
      return new Response('Invalid email address.', { status: 400 });
    }

    const r = await fetch(FLASK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, message })
    });

    if (!r.ok) {
      const text = await r.text().catch(() => '');
      return new Response(text || 'Flask service returned an error.', { status: 502 });
    }

    // If Flask returns JSON, pass it through; otherwise return ok.
    const ct = r.headers.get('content-type') || '';
    if (ct.includes('application/json')) {
      const data = await r.json();
      return json(data);
    }

    return new Response('ok', { status: 200 });
  } catch (err) {
    console.error('Contact API error:', err);
    return new Response('Server error.', { status: 500 });
  }
};
