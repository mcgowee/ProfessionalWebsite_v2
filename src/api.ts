// Same-origin by default (production: https://earl-mcgowen.com)
// If you ever set VITE_API_URL (e.g., for local dev), it will prefix requests.
const API_BASE = import.meta.env.VITE_API_URL || "";

export async function generateText(
  prompt: string,
  maxTokens: number = 100,
  sessionId?: string
): Promise<string> {
  const res = await fetch(`${API_BASE}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt,
      max_tokens: maxTokens,
      // If undefined, backend will default to "default-session"
      session_id: sessionId,
    }),
  });

  const data: any = await res.json().catch(() => ({}));

  if (!res.ok) {
    // Prefer backend error message if present
    throw new Error(data?.error || `Request failed (HTTP ${res.status})`);
  }

  // Backend returns both "generated_text" and "reply"
  return data.generated_text ?? data.reply ?? "No response";
}
