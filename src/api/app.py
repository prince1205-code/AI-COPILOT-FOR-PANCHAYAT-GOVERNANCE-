"""
Sahayak AI - FastAPI Application
Run: uvicorn src.api.app:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes          import router
from src.api.voice_routes    import router as voice_router
from src.api.language_routes import router as language_router
from src.api.tts_routes      import router as tts_router
from src.core.config      import APP_NAME, APP_VERSION

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI Copilot for Panchayat Governance — Scheme Recommendation API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router,       prefix="/api/v1")
app.include_router(voice_router,    prefix="/api/v1")
app.include_router(language_router, prefix="/api/v1")
app.include_router(tts_router,      prefix="/api/v1")


@app.get("/", tags=["Root"])
def root():
    return {"message": f"Welcome to {APP_NAME} API", "version": APP_VERSION, "docs": "/docs"}
