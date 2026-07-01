# 🏛️ AI Copilot for Panchayat Governance

AI-powered assistant and scheme recommendation platform for Indian panchayats — helps citizens discover eligible government schemes, complete voice-enabled applications, and get instant multilingual support.

## What this project does

- Helps citizens find government schemes that match their profile and eligibility.
- Lets users complete scheme applications using voice (speech-to-text) and multilingual input.
- Provides an AI assistant that answers scheme-related questions in the user's language.
- Generates downloadable PDF receipts for submitted applications.

Key user benefits: faster access to benefits, accessibility for low-literacy users, and support for multiple Indian languages.

## Tech preview

This repository contains a Python FastAPI backend and a Vite-powered React frontend. The backend hosts APIs for the AI agents, text-to-speech/voice routing, and recommendation logic. The frontend provides a modern, mobile-friendly UI with voice capture.

Primary technologies:
- Python 3.8+ (FastAPI)
- React + Vite (frontend)
- gTTS / TTS utilities
- FAISS vector store (local index under knowledge_base/vector_store)
- (Optional) MongoDB or other datastore for production deployment

## Project layout

The repository is organized to separate backend agents, API routes, and the frontend app:

```
README.md
requirements.txt
frontend/                # React + Vite frontend
knowledge_base/          # Scheme data and FAISS vector store
src/                     # Python backend (FastAPI) and AI agents
	├── api/               # FastAPI routes
	├── agents/            # Agent implementations
	├── core/              # Orchestration and engine
	└── rag/               # Retrieval-augmented generation helpers
``` 

## Quick start (local)

1. Clone the repository

```bash
git clone https://github.com/prince1205-code/AI-COPILOT-FOR-PANCHAYAT-GOVERNANCE-.git
cd AI-COPILOT-FOR-PANCHAYAT-GOVERNANCE-
```

2. Create a Python virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Start the backend (development)

```bash
# from repo root
uvicorn src.api.app:app --reload --port 8000
```

4. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Open the frontend in your browser (usually http://localhost:5173) and browse the API at http://localhost:8000/docs

## Contributing

Contributions, issue reports and pull requests are welcome. If you want to improve the README, code, or add new scheme data, please open a PR.

Suggested contribution steps:

1. Fork the repo and create a branch: `docs/readme-enhance` or `feature/<your-idea>`
2. Make changes, run unit tests (if any), and ensure the frontend builds
3. Open a pull request describing your change

## License

This project is licensed under the MIT License.

---

Made with ❤️ by Prince Kumar — built for accessible, multilingual civic services.
