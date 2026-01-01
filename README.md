# Earl McGowen — Professional Website

A modern, incrementally maintained personal/professional website for [earl-mcgowen.com](https://earl-mcgowen.com), built with [SvelteKit](https://kit.svelte.dev/) (frontend) and a Python [Flask](https://flask.palletsprojects.com/) backend for AI, demo, and utility services.

---

## Features

- **Informational Pages:** Home, About, Contact (with live email form).
- **Wordle Solver:** Accurate solver UI, powered by Flask backend.
- **Chat Demo:** Multiple chat modes and AI analysis features.
- **Modular UI:** Clean, accessible (a11y-conscious), and SSR-safe Svelte components.
- **Traditional CSS:** No Tailwind or CSS frameworks—component-scoped or minimal global CSS only.

---

## Architecture Overview

```
ProfessionalWebsite_v2/
│
├── src/
│   ├── routes/              # SvelteKit pages & endpoints (+page.svelte, about/, contact/, wordle/, api/)
│   ├── components/          # Reusable Svelte components (Header, ChatMenu, etc.)
│
├── static/                  # Public assets (favicon, images, etc.)
├── .continue/               # Project-specific migration rules & guidance
│
├── backend/                 # (If included) Flask backend sources, or managed externally
```

- **Frontend:** SvelteKit (latest, static adapter)
- **Backend:** Flask + Gunicorn, managed by systemd (127.0.0.1:5000)
- **Reverse Proxy:** Nginx (TLS with Let’s Encrypt, proxies 443/80 → 127.0.0.1:3000)
- **Deployment:** Hostinger VPS (Ubuntu)

---

## Development

### Prerequisites

- Node.js (18.x or later)
- Python 3.8+ (for backend services)
- NPM or Yarn

### Install & Run Frontend

```bash
npm install
npm run dev
```

- SvelteKit serves on http://localhost:5173 (dev) or port 3000 (prod).

### Build for Production

```bash
npm run build
npm run preview
```

_Note: SvelteKit uses the static adapter, suitable for reverse proxy setup._

### Backend (Flask)

- The Flask app is deployed separately (systemd service + Gunicorn), listening on 127.0.0.1:5000.
- **Env vars** (e.g., `FLASK_API_KEY`) should be set via `/etc/my_flask_app/env`.
- Do not hardcode secrets; always use authorized headers for API requests.

---

## API Endpoints

### SvelteKit API (src/routes/api)

- Used for client-facing AJAX/XHR from SvelteKit; may proxy to Flask backend as needed.

### Flask Backend Endpoints

- `/send-email` — Contact form (protected, requires Bearer token)
- `/solve` — Wordle solver API
- `/chat` — General chatbot (other endpoints available as per backend)
- All sensitive endpoints require: `Authorization: Bearer <FLASK_API_KEY>`

---

## Coding & Style Guide

- **No Tailwind, no CSS frameworks.** Use traditional, component-scoped CSS in `.svelte` files.
- **SSR Safety:** Avoid `window`/`document` in modules that run server-side.
- **Accessibility:** Follow a11y best-practices for all user-facing UI (ARIA attributes, semantic tags, labels, focus styling).
- **Incremental Changes:** Make small, drop-in refactors—never break working production code in migration.
- **Security:** Do not log/store credentials. All auth flows use environment variables and secure headers.

---

## Deployment

See [.continue/rules.md](.continue/rules.md) for detailed legacy migration and deployment expectations.

Basic steps:
1. Build frontend (`npm run build`).
2. Deploy (via systemd) to Hostinger VPS.
3. Ensure nginx reverse-proxy and SSL config is current.
4. Systemd manages Node and Gunicorn/Flask services.

---

## Contributing

- Follow rules and migration constraints outlined in [.continue/rules.md](.continue/rules.md).
- Ask before large refactors.
- PRs should explain purpose and approach.
- Do **not** introduce Tailwind, Next.js, or FastAPI (per project rules).

---

## License

(C) Earl McGowen, MIT License or as specified.

---
