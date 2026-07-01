"""
Agent registry for the Sahayak agentic orchestrator.

This file adapts existing agents and services into small callable units. It
does not change their internal behavior.
"""
from __future__ import annotations

import logging
from typing import Any, Callable

from src.agents.chat_agent import ChatAgent
from src.agents.language.language_agent import LanguageAgent
from src.agents.scheme_agent import SchemeAgent
from src.recommendation.eligibility_engine import EligibilityEngine
from src.recommendation.profile_parser import ProfileParser
from src.rag.retriever import Retriever
from src.services.memory_service import MemoryService

log = logging.getLogger(__name__)

AgentHandler = Callable[[dict[str, Any]], Any]


class AgentRegistry:
    """Maps task agent names to executable handlers."""

    def __init__(
        self,
        *,
        chat_agent: ChatAgent,
        scheme_agent: SchemeAgent,
        memory: MemoryService,
        language_agent: LanguageAgent | None,
        parser: ProfileParser,
        engine: EligibilityEngine,
        retriever: Retriever | None = None,
    ):
        self.chat_agent = chat_agent
        self.scheme_agent = scheme_agent
        self.memory = memory
        self.language_agent = language_agent
        self.parser = parser
        self.engine = engine
        self.retriever = retriever

        self._handlers: dict[str, AgentHandler] = {
            "language_agent": self._detect_language,
            "memory_agent": self._memory,
            "profile_agent": self._extract_profile,
            "recommendation_agent": self._recommend,
            "rag_retrieval_agent": self._retrieve,
            "scheme_agent": self._scheme_response,
            "chat_agent": self._chat_response,
            "validation_agent": self._validate,
            "tts_agent": self._prepare_tts,
        }

    def execute(self, agent_name: str, context: dict[str, Any]) -> Any:
        print(f"[Orchestrator][Registry] Agent Registry Lookup: {agent_name}")
        log.info("Agent Registry Lookup: %s", agent_name)
        handler = self._handlers.get(agent_name)
        if not handler:
            registered = ", ".join(sorted(self._handlers))
            raise ValueError(
                f"Agent '{agent_name}' is not registered. "
                f"Registered agents: {registered}"
            )
        output = handler(context)
        print(f"[Orchestrator][Registry] Returned Object: {type(output).__name__}")
        log.info("Agent %s returned object type=%s", agent_name, type(output).__name__)
        return output

    def _detect_language(self, context: dict[str, Any]) -> dict[str, Any]:
        if not self.language_agent:
            return {"detected_language": "English", "confidence": 0.0, "method": "default"}
        return self.language_agent.detect_and_store(context["user_query"], context["session_id"])

    def _memory(self, context: dict[str, Any]) -> Any:
        task_name = context["current_task_name"]
        session_id = context["session_id"]

        if task_name == "load_memory":
            return [
                {"role": m["role"], "content": m["content"]}
                for m in self.memory.get_history(session_id)
                if m.get("intent") != "language_detection"
            ]

        if task_name == "update_memory_user":
            self.memory.add_message(
                session_id=session_id,
                role="user",
                content=context["user_query"],
                intent=context["intent"],
                metadata={"goal": context["goal"]},
            )
            return {"saved": True, "role": "user"}

        if task_name == "update_memory_assistant":
            final_response = context.get("final_response", "")
            if final_response:
                self.memory.add_message(
                    session_id=session_id,
                    role="assistant",
                    content=final_response,
                    intent=context["intent"],
                    metadata={"goal": context["goal"]},
                )
            return {"saved": bool(final_response), "role": "assistant"}

        raise ValueError(f"Unsupported memory task '{task_name}'")

    def _extract_profile(self, context: dict[str, Any]) -> dict[str, Any]:
        profile = self.parser.parse(context["user_query"])
        return {
            "age": profile.get("age"),
            "state": profile.get("state") or "",
            "occupation": profile.get("occupation") or "",
            "income": profile.get("income"),
            "gender": (profile.get("gender") or "").lower(),
        }

    def _recommend(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        print("[Orchestrator][RecommendationAgent] Execution Started")
        log.info("RecommendationAgent execution started")
        profile = context.get("profile") or self._extract_profile(context)
        recommendations = self.engine.recommend(profile, top_k=5)
        print(
            "[Orchestrator][RecommendationAgent] Execution Finished: "
            f"{len(recommendations)} recommendations"
        )
        log.info("RecommendationAgent execution finished results=%d", len(recommendations))
        return recommendations

    def _retrieve(self, context: dict[str, Any]) -> list[dict[str, Any]]:
        if not self.retriever:
            log.info("RAG retriever unavailable; skipping retrieval task.")
            return []

        query = context["user_query"]
        recommendations = context.get("recommendations") or []
        if recommendations:
            names = ", ".join(r.get("scheme_name", "") for r in recommendations[:3])
            query = f"{query}. Official details for: {names}"

        return self.retriever.retrieve(query, top_k=5)

    def _scheme_response(self, context: dict[str, Any]) -> str:
        print("[Orchestrator][SchemeAgent] Execution Started")
        log.info("SchemeAgent execution started")
        history = context.get("history") or []
        user_query = context["user_query"]

        if context["intent"] == "recommendation":
            recommendations = context.get("recommendations") or []
            if not recommendations:
                return (
                    "I couldn't identify enough profile information.\n\n"
                    "Please tell me your age, state, occupation, income, and gender."
                )

            rec_lines = []
            for index, item in enumerate(recommendations, start=1):
                rec_lines.append(
                    f"{index}. {item.get('scheme_name')} "
                    f"({item.get('category')}) - {item.get('reason')} "
                    f"[confidence: {item.get('confidence')}]"
                )
            user_query = (
                f"{context['user_query']}\n\n"
                "Planner selected these recommendation results. Explain only these schemes, "
                "why they match, and what the citizen should check next:\n"
                + "\n".join(rec_lines)
            )

        response = self.scheme_agent.process(user_query, history=history)
        print(
            "[Orchestrator][SchemeAgent] Execution Finished: "
            f"{len(response or '')} chars"
        )
        log.info("SchemeAgent execution finished chars=%d", len(response or ""))
        return response

    def _chat_response(self, context: dict[str, Any]) -> str:
        return self.chat_agent.process(context["user_query"])

    def _validate(self, context: dict[str, Any]) -> dict[str, Any]:
        response = (context.get("final_response") or "").strip()
        if not response:
            raise ValueError("Final response is empty.")
        return {
            "valid": True,
            "checks": ["non_empty_response"],
            "language": (context.get("language") or {}).get("detected_language", "English"),
        }

    def _prepare_tts(self, context: dict[str, Any]) -> dict[str, Any]:
        language = (context.get("language") or {}).get("detected_language", "Hindi")
        return {
            "ready": bool(context.get("final_response")),
            "language": language,
            "text": context.get("final_response", ""),
        }
