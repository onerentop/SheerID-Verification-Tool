# Repository Guidelines

## Project Structure & Module Organization

This repository is a collection of small, mostly self-contained tools:

- `anti_detect.py`: shared anti-detection helpers used by multiple Python tools.
- `*-verify-tool/`: Python CLI tools (each typically has a `main.py` and `README.md`).
- `veterans-extension/` and `veterans-autofill/`: browser extensions (Manifest V3) and related assets.
- `docs/`: documentation and translated READMEs used by GitHub Pages.
- `_deprecated_auto-verify-tool/`: legacy Node-based automation (kept for reference; avoid expanding unless necessary).

## Build, Test, and Development Commands

Python tools are run directly (no central build step):

- Create a virtual environment (recommended): `python -m venv .venv`
- Activate on Windows: `.\.venv\Scripts\activate`
- Install shared deps: `pip install -r requirements.txt`
- Run a tool (example): `cd spotify-verify-tool` then `python main.py "YOUR_SHEERID_URL"`
- Optional anti-detection deps (when needed): `pip install curl_cffi cloudscraper`

Tool-specific dependencies may exist (example: `pip install -r canva-teacher-tool/requirements.txt`).

Browser extensions are loaded unpacked (no bundler):

- Chrome: open `chrome://extensions/` → enable Developer mode → “Load unpacked” → select `veterans-extension/`.

## Coding Style & Naming Conventions

- Python: 4-space indentation, keep scripts runnable as `python main.py ...`, and prefer clear/defensive error handling over cleverness.
- Naming: use folder patterns (`*-verify-tool`, `*-extension`) and keep entrypoints as `main.py` to match existing tools.

## Testing Guidelines

There is no dedicated automated test suite today. For changes, do a quick validation:

- Syntax check: `python -m compileall .`
- Smoke run: execute the relevant tool’s `main.py` (use a non-sensitive URL/token) and confirm CLI args still work.
- Extensions: load the unpacked folder and check the browser console for errors.

## Commit & Pull Request Guidelines

- Commits follow a Conventional Commits style (examples seen in history): `feat(scope): ...`, `fix(scope): ...`, `docs: ...`, `refactor: ...`.
- PRs should follow `.github/pull_request_template.md`: include a clear description, testing notes, and screenshots for UI/extension changes.

## Security & Configuration Tips

- Do not commit secrets (tokens, IMAP passwords, proxy credentials). Prefer `*.example.*` files and local-only configs (e.g., `config.json` copied from `config.example.json`).
- `.env` is git-ignored; use it for local configuration when applicable.
