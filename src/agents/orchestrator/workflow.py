"""
Agentic workflow entry point for Sahayak AI.
"""
from __future__ import annotations

from dataclasses import dataclass
import logging
from time import perf_counter
from typing import Any

from src.agents.orchestrator.executor import Executor
from src.agents.orchestrator.planner import Planner

log = logging.getLogger(__name__)


@dataclass
class WorkflowResult:
    session_id: str
    query: str
    answer: str
    intent: str
    goal: str
    detected_language: str
    execution_trace: list[dict[str, Any]]
    execution_time_ms: float
    tts: dict[str, Any]


class AgenticWorkflow:
    """Plans, executes, validates, and returns a final response."""

    def __init__(self, planner: Planner, executor: Executor):
        self.planner = planner
        self.executor = executor

    def run(self, user_query: str, session_id: str) -> WorkflowResult:
        started_at = perf_counter()
        plan = self.planner.create_plan(user_query)
        print(f"[Orchestrator][Workflow] Detected Intent: {plan.intent}")
        print(f"[Orchestrator][Workflow] Selected Workflow: {plan.goal}")
        log.info("Workflow selected intent=%s goal=%s", plan.intent, plan.goal)
        context: dict[str, Any] = {
            "session_id": session_id,
            "user_query": user_query,
            "intent": plan.intent,
            "goal": plan.goal,
        }

        context = self.executor.run(plan.tasks, context)
        answer = context.get("final_response")
        if not isinstance(answer, str) or not answer.strip():
            raise RuntimeError("Agentic workflow completed without a valid final response.")

        print(f"[Orchestrator][Workflow] Final Response: {answer[:300]}")
        log.info("Workflow final response chars=%d", len(answer))

        language = (context.get("language") or {}).get("detected_language", "English")
        tts = context.get("tts") or {"ready": bool(answer), "language": language, "text": answer}

        return WorkflowResult(
            session_id=session_id,
            query=user_query,
            answer=answer,
            intent=plan.intent,
            goal=plan.goal,
            detected_language=language,
            execution_trace=[task.to_trace() for task in plan.tasks],
            execution_time_ms=round((perf_counter() - started_at) * 1000, 2),
            tts=tts,
        )
