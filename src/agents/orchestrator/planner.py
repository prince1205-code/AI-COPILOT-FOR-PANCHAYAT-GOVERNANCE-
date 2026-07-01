"""
Deterministic goal detection and bounded task planning.
"""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass

from src.agents.orchestrator.task import Task
from src.agents.router import IntentRouter

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Plan:
    goal: str
    intent: str
    tasks: list[Task]


class Planner:
    """Converts a user request into a finite execution plan."""

    _RECOMMENDATION_TERMS = (
        "which schemes",
        "recommend",
        "eligible",
        "apply for",
        "suitable",
        "for me",
        "i am",
        "my income",
        "farmer",
        "student",
        "labour",
        "labor",
        "worker",
    )
    _DOCUMENT_TERMS = ("document", "documents", "required", "certificate", "proof")

    def __init__(self, router: IntentRouter | None = None):
        self.router = router or IntentRouter()

    def create_plan(self, user_query: str) -> Plan:
        query = user_query.strip()
        intent = self._detect_intent(query)
        goal = self._detect_goal(query, intent)

        print(f"[Orchestrator][Planner] Detected Intent: {intent}")
        print(f"[Orchestrator][Planner] Goal: {goal}")
        log.info("Detected Intent: %s", intent)
        log.info("Detected Goal: %s", goal)

        tasks = [
            Task(
                name="detect_language",
                agent="language_agent",
                output_key="language",
                label="Detecting Language",
                retries=1,
            ),
            Task(
                name="load_memory",
                agent="memory_agent",
                output_key="history",
                label="Loading Memory",
            ),
            Task(
                name="update_memory_user",
                agent="memory_agent",
                label="Updating Memory",
            ),
        ]

        if intent == "recommendation":
            tasks.extend(self._recommendation_tasks())
        elif intent in {"scheme", "documents"}:
            tasks.extend(self._scheme_tasks(intent))
        else:
            tasks.extend(self._chat_tasks())

        tasks.extend(
            [
                Task(
                    name="validate_result",
                    agent="validation_agent",
                    output_key="validation",
                    label="Validating Results",
                ),
                Task(
                    name="update_memory_assistant",
                    agent="memory_agent",
                    label="Saving Response",
                ),
                Task(
                    name="prepare_tts",
                    agent="tts_agent",
                    output_key="tts",
                    label="Preparing Speech",
                    required=False,
                ),
            ]
        )

        print(
            "[Orchestrator][Planner] Selected Workflow: "
            + " -> ".join(f"{task.name}:{task.agent}" for task in tasks)
        )
        log.info("Selected Workflow: %s", [(task.name, task.agent) for task in tasks])

        return Plan(goal=goal, intent=intent, tasks=tasks)

    def _detect_intent(self, query: str) -> str:
        lowered = query.lower()
        if any(term in lowered for term in self._RECOMMENDATION_TERMS):
            return "recommendation"
        if any(term in lowered for term in self._DOCUMENT_TERMS):
            return "documents"

        routed = self.router.route_query(query)
        if routed == "scheme":
            return "scheme"
        if routed in {"chat", "knowledge", "document"}:
            return routed
        return "chat"

    def _detect_goal(self, query: str, intent: str) -> str:
        normalized = re.sub(r"\s+", " ", query).strip()
        if intent == "recommendation":
            return f"Recommend suitable government schemes for: {normalized}"
        if intent == "documents":
            return f"Find required documents from official scheme data for: {normalized}"
        if intent == "scheme":
            return f"Answer scheme question using official dataset for: {normalized}"
        return f"Respond conversationally to: {normalized}"

    def _recommendation_tasks(self) -> list[Task]:
        return [
            Task(
                name="extract_profile",
                agent="profile_agent",
                output_key="profile",
                label="Extracting Profile",
            ),
            Task(
                name="run_recommendations",
                agent="recommendation_agent",
                output_key="recommendations",
                label="Searching Schemes",
                retries=1,
            ),
            Task(
                name="retrieve_scheme_details",
                agent="rag_retrieval_agent",
                output_key="retrieved_documents",
                label="Verifying Information",
                retries=1,
                required=False,
            ),
            Task(
                name="generate_recommendation_response",
                agent="scheme_agent",
                output_key="final_response",
                label="Generating Response",
                retries=1,
            ),
        ]

    def _scheme_tasks(self, intent: str) -> list[Task]:
        label = "Checking Documents" if intent == "documents" else "Searching Schemes"
        return [
            Task(
                name="retrieve_scheme_details",
                agent="rag_retrieval_agent",
                output_key="retrieved_documents",
                label=label,
                retries=1,
            ),
            Task(
                name="generate_scheme_response",
                agent="scheme_agent",
                output_key="final_response",
                label="Generating Response",
                retries=1,
            ),
        ]

    def _chat_tasks(self) -> list[Task]:
        return [
            Task(
                name="generate_chat_response",
                agent="chat_agent",
                output_key="final_response",
                label="Generating Response",
                retries=1,
            )
        ]
