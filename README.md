# AI Resume Screener

Lightweight, local-first AI resume screener and portfolio generator. This repository contains a FastAPI backend and a Vite + React frontend that together parse resumes, extract skills, and match candidates to job descriptions. The project is designed to work with free-tier or local fallbacks for LLMs and transcription.

## Quick start (development)

Prerequisites:
- Python 3.9+
- Node.js 18+ (for frontend / Vite)
- (Optional) git, Docker

1. Backend: create and activate a virtual environment, install dependencies

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Frontend: install dependencies and run dev server

```powershell
cd frontend
npm install
npm run dev
```

3. Start backend (from repo root)

```powershell
# from repository root
python backend/app.py
# or: uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

Open the frontend URL shown by Vite (usually http://localhost:5173) and the backend API will be available at http://localhost:8000.

## Configuration

Copy `.env.example` (or create a `.env`) and set values for any optional integrations (LLM provider, transcription, S3, etc.). The project is designed to run in "local-only" mode when API keys are not provided.

Key environment variables (examples):

- `LLM_API_KEY`, `LLM_PROVIDER` — optional LLM provider; leave empty to use local stub
- `WHISPER_MODEL` — (optional) local Whisper model name
- `JWT_SECRET`, `BCRYPT_ROUNDS` — auth configuration for saved sessions
- `DATABASE_URL` — defaults to `sqlite:///./backend/data/app.db`

## Developer notes

- The backend is in `backend/` and exposes endpoints such as `/match` and `/match-llm`.
- The frontend is in `frontend/` and uses Vite + React.
- Sample resumes and job descriptions are included in `sample_data/`.
- New features and experimental code should be developed on `develop` branch and merged to `main` via PRs.

## Tests & CI

- Unit tests should be added under `tests/` (not present by default). We recommend GitHub Actions for CI.

## License

This project is provided as-is. Add a LICENSE file if you intend to publish or share widely.

---
If you'd like, I can also add a minimal `README` badge, CI workflow, or a CONTRIBUTING.md next.
