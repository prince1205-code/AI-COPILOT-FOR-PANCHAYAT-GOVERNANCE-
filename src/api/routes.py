"""
Sahayak AI - API Routes
"""
from fastapi import APIRouter, Depends, HTTPException

from src.api.models import (
    ProfileRequest, RecommendResponse,
    NLProfileRequest, NLProfileResponse,
    ChatRequest, ChatResponse,
    SchemeRequest, SchemeResponse,
    HistoryResponse, MessageRecord,
    HealthResponse, SchemeResult,
)
from src.api.dependencies import (
    get_engine, get_chat_agent, get_memory, get_parser,
    get_orchestrator,
)
from src.core.orchestrator                  import SahayakOrchestrator
from src.recommendation.eligibility_engine import EligibilityEngine
from src.agents.chat_agent                 import ChatAgent
from src.services.memory_service           import MemoryService
from src.recommendation.profile_parser     import ProfileParser
from src.core.config                       import APP_VERSION

router = APIRouter()


# ----------------------------------------------------------
# Helper — build "Why this scheme?" bullets from reason str
# ----------------------------------------------------------

def _build_why(reason: str, profile: dict) -> list[str]:
    bullets = []
    r = reason.lower()

    if profile.get("occupation") and "scheme" in r or "welfare" in r or "support" in r:
        bullets.append(f"You are a {profile['occupation'].lower()}")
    if "state match" in r and profile.get("state"):
        bullets.append(f"Your state ({profile['state']}) is covered by this scheme")
    if "low income" in r and profile.get("income"):
        bullets.append(f"Your income (₹{profile['income']:,}) is within the supported range")
    if "gender match" in r and profile.get("gender"):
        bullets.append(f"This scheme targets {profile['gender']} beneficiaries")
    if "senior citizen" in r:
        bullets.append("You qualify as a senior citizen (age ≥ 60)")
    if "youth scheme" in r:
        bullets.append("You qualify under the youth category (age ≤ 30)")
    if "flagship" in r:
        bullets.append("This is a high-priority flagship government scheme")

    # keyword boost lines like "+35: pm kisan"
    for part in reason.split(","):
        part = part.strip()
        if part.startswith("+") and ":" in part:
            kw = part.split(":", 1)[1].strip()
            bullets.append(f"Scheme is directly related to: {kw}")

    return bullets if bullets else ["Matches your profile criteria"]


# ----------------------------------------------------------
# GET /health
# ----------------------------------------------------------

@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health(engine: EligibilityEngine = Depends(get_engine)):
    return HealthResponse(
        status="ok",
        schemes_loaded=len(engine.schemes),
        version=APP_VERSION,
    )


# ----------------------------------------------------------
# POST /recommend
# ----------------------------------------------------------

@router.post("/recommend", response_model=RecommendResponse, tags=["Recommendation"])
def recommend(
    body:   ProfileRequest,
    engine: EligibilityEngine = Depends(get_engine),
):
    profile = {
        "age":        body.age,
        "state":      body.state or "",
        "occupation": body.occupation or "",
        "income":     body.income,
        "gender":     (body.gender or "").lower(),
    }
    raw     = engine.recommend(profile, top_k=body.top_k)
    results = [SchemeResult(**r, why=_build_why(r["reason"], profile)) for r in raw]
    return RecommendResponse(total=len(results), profile=profile, results=results)


# ----------------------------------------------------------
# POST /profile/recommend  (natural language → profile → recommend)
# ----------------------------------------------------------

@router.post("/profile/recommend", response_model=NLProfileResponse, tags=["Recommendation"])
def profile_recommend(
    body:   NLProfileRequest,
    engine: EligibilityEngine = Depends(get_engine),
    parser: ProfileParser     = Depends(get_parser),
):
    profile = parser.parse(body.text)
    # normalise None → empty string for engine
    clean = {
        "age":        profile.get("age"),
        "state":      profile.get("state") or "",
        "occupation": profile.get("occupation") or "",
        "income":     profile.get("income"),
        "gender":     (profile.get("gender") or "").lower(),
    }
    raw     = engine.recommend(clean, top_k=body.top_k)
    results = [SchemeResult(**r, why=_build_why(r["reason"], clean)) for r in raw]
    return NLProfileResponse(extracted_profile=clean, total=len(results), results=results)


# ----------------------------------------------------------
# POST /chat
# ----------------------------------------------------------

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(
    body:   ChatRequest,
    agent:  ChatAgent     = Depends(get_chat_agent),
    memory: MemoryService = Depends(get_memory),
):
    memory.add_message(body.session_id, "user", body.message, intent="chat")
    reply = agent.process(body.message)
    memory.add_message(body.session_id, "assistant", reply, intent="chat")
    return ChatResponse(session_id=body.session_id, reply=reply, intent="chat")


# ----------------------------------------------------------
# POST /scheme
# ----------------------------------------------------------

@router.post("/scheme", response_model=SchemeResponse, tags=["Scheme"])
def scheme(
    body:   SchemeRequest,
    orchestrator: SahayakOrchestrator = Depends(get_orchestrator),
):
    print(f"[API][/scheme] Execution Started: session={body.session_id} query={body.query}")
    result = orchestrator.process_with_trace(body.query, body.session_id)
    print(f"[API][/scheme] Final Response: {result.answer[:300]}")
    return SchemeResponse(
        session_id=result.session_id,
        query=result.query,
        answer=result.answer,
        intent=result.intent,
        goal=result.goal,
        detected_language=result.detected_language,
        execution_time_ms=result.execution_time_ms,
        execution_trace=result.execution_trace,
        tts=result.tts,
    )


# ----------------------------------------------------------
# GET /history/{session_id}
# ----------------------------------------------------------

@router.get("/history/{session_id}", response_model=HistoryResponse, tags=["Chat"])
def history(
    session_id: str,
    memory:     MemoryService = Depends(get_memory),
):
    msgs = memory.get_history(session_id)
    if not msgs:
        raise HTTPException(status_code=404, detail=f"No history found for session '{session_id}'")
    records = [MessageRecord(**{k: m[k] for k in ("role", "content", "intent", "timestamp")}) for m in msgs]
    return HistoryResponse(session_id=session_id, total=len(records), messages=records)
