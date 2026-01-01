# Project Rules / Context (Continue AI)

You are assisting with a **professional personal website** migration and incremental modernization.

## What this project is
- A professional/personal website for **earl-mcgowen.com**
- Frontend: **SvelteKit (latest)**, traditional CSS (NO Tailwind)
- Backend services: a separate **Flask + Gunicorn** app on the same VPS (used for contact email + wordle + some demo pages)
- Deployment target: **Hostinger VPS (Ubuntu)** with **nginx + systemd**
- The website is live and changes must be safe and incremental.

## Key constraints
- **No Tailwind** and do not introduce CSS frameworks.
- Prefer component-scoped CSS and a small set of global variables (if needed).
- Respect SSR boundaries (no `document`/`window` during server render).
- Avoid adding new dependencies unless clearly beneficial.
- Provide **drop-in replacements** when suggesting file changes.
- Prefer small PR-style refactors: one file/feature at a time.

## SvelteKit structure
- `src/routes` contains pages and API routes.
- `/static` is used for images and public assets (logo, favicon, etc.).
- Some pages call the Flask backend over HTTP.

## VPS / Production architecture (important)
- Domain: **earl-mcgowen.com** (+ www)
- nginx terminates TLS (Let’s Encrypt already installed).
- nginx reverse proxies the site to **127.0.0.1:3000**
- SvelteKit service runs via systemd:
  - `/etc/systemd/system/earl-site.service`
  - Node serves the app on port 3000

Flask backend on VPS:
- Gunicorn binds to **127.0.0.1:5000**
- Managed by systemd: `/etc/systemd/system/flask_app.service`
- Env file: `/etc/my_flask_app/env`
- Flask endpoints used by the site:
  - POST `/send-email` (contact form)
  - POST `/solve` (wordle solver)
  - Other endpoints may exist but are secondary.

Security:
- Some Flask endpoints require `Authorization: Bearer <FLASK_API_KEY>`
- Keys live only in env files; do not hardcode secrets.

## Current work focus (what to help with)
- Migrating old SvelteKit pages/components into this new SvelteKit project
- Fixing and modernizing UI behavior (a11y + SSR safety)
- Wordle page UI improvements (duplicate-letter accurate solver already fixed server-side)
- Updating/cleaning demo sections (chat pages etc.) but they are not the core purpose

## Output expectations
When asked to change something:
- Prefer exact commands and exact file paths
- Provide complete drop-in file contents when requested
- If uncertain, ask for the current file before suggesting edits
- Keep solutions production-safe and easy to deploy
