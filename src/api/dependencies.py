"""
Sahayak AI - API Dependencies
Shared singleton instances injected into routes.
"""
from functools import lru_cache
from src.recommendation.eligibility_engine import EligibilityEngine
from src.agents.chat_agent                 import ChatAgent
from src.agents.language.detector          import LanguageDetector
from src.agents.language.language_agent    import LanguageAgent
from src.agents.scheme_agent               import SchemeAgent
from src.core.orchestrator                 import SahayakOrchestrator
from src.services.memory_service           import MemoryService
from src.recommendation.profile_parser     import ProfileParser


@lru_cache(maxsize=1)
def get_engine() -> EligibilityEngine:
    return EligibilityEngine()

@lru_cache(maxsize=1)
def get_chat_agent() -> ChatAgent:
    return ChatAgent()

@lru_cache(maxsize=1)
def get_scheme_agent() -> SchemeAgent:
    return SchemeAgent()

@lru_cache(maxsize=1)
def get_memory() -> MemoryService:
    return MemoryService()

@lru_cache(maxsize=1)
def get_parser() -> ProfileParser:
    return ProfileParser()

@lru_cache(maxsize=1)
def get_language_detector() -> LanguageDetector:
    return LanguageDetector()

def get_language_agent() -> LanguageAgent:
    return LanguageAgent(detector=get_language_detector(), memory=get_memory())

@lru_cache(maxsize=1)
def get_orchestrator() -> SahayakOrchestrator:
    scheme_agent = get_scheme_agent()
    return SahayakOrchestrator(
        chat_agent=get_chat_agent(),
        scheme_agent=scheme_agent,
        memory=get_memory(),
        language_agent=get_language_agent(),
        parser=get_parser(),
        engine=get_engine(),
        retriever=scheme_agent.retriever,
    )
