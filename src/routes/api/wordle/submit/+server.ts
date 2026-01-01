import type { RequestHandler } from './$types';

const WORDLE_URL = 'http://127.0.0.1:5000/api/submit';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const { letters, colors } = await request.json();

    const r = await fetch(WORDLE_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ letters, colors })
    });

    const text = await r.text();
    return new Response(text, {
      status: r.status,
      headers: { 'Content-Type': r.headers.get('content-type') || 'application/json' }
    });
  } catch (err) {
    console.error('Wordle API error:', err);
    return new Response('Backend unavailable.', { status: 502 });
  }
};
