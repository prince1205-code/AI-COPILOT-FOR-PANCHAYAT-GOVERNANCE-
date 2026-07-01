"""
Sahayak AI - Agentic Orchestrator

Compatibility wrapper around the planner/executor workflow. The public
`process()` method still returns a plain response string for older callers.
"""
from __future__ import annotations

import logging

from src.agents.chat_agent import ChatAgent
from src.agents.language.detector import LanguageDetector
from src.agents.language.language_agent import LanguageAgent
from src.agents.orchestrator.agent_registry import AgentRegistry
from src.agents.orchestrator.executor import Executor
from src.agents.orchestrator.planner import Planner
from src.agents.orchestrator.workflow import AgenticWorkflow, WorkflowResult
from src.agents.scheme_agent import SchemeAgent
from src.recommendation.eligibility_engine import EligibilityEngine
from src.recommendation.profile_parser import ProfileParser
from src.rag.retriever import Retriever
from src.services.memory_service import MemoryService

log = logging.getLogger(__name__)


class SahayakOrchestrator:
    """Agentic planner that coordinates existing Sahayak agents."""

    def __init__(
        self,
        *,
        chat_agent: ChatAgent | None = None,
        scheme_agent: SchemeAgent | None = None,
        memory: MemoryService | None = None,
        language_agent: LanguageAgent | None = None,
        parser: ProfileParser | None = None,
        engine: EligibilityEngine | None = None,
        retriever: Retriever | None = None,
        session_id: str = "default",
    ):
        self.session_id = session_id
        self.memory = memory or MemoryService()

        registry = AgentRegistry(
            chat_agent=chat_agent or ChatAgent(),
            scheme_agent=scheme_agent or SchemeAgent(),
            memory=self.memory,
            language_agent=language_agent or LanguageAgent(LanguageDetector(), self.memory),
            parser=parser or ProfileParser(),
            engine=engine or EligibilityEngine(),
            retriever=retriever,
        )
        self.workflow = AgenticWorkflow(
            planner=Planner(),
            executor=Executor(registry),
        )

    def process(self, user_query: str) -> str:
        """Backward-compatible response-only API."""
        return self.process_with_trace(user_query, self.session_id).answer

    def process_with_trace(self, user_query: str, session_id: str | None = None) -> WorkflowResult:
        """Run the agentic workflow and return answer plus execution trace."""
        active_session = session_id or self.session_id
        print(
            "[Orchestrator][Core] Execution Started: "
            f"session={active_session} query={user_query}"
        )
        log.info("Orchestrator execution started session=%s", active_session)
        result = self.workflow.run(user_query, active_session)
        print(f"[Orchestrator][Core] Final Response: {result.answer[:300]}")
        log.info("Orchestrator execution finished session=%s chars=%d", active_session, len(result.answer))
        return result


if __name__ == "__main__":
    bot = SahayakOrchestrator()

    while True:
        query = input("\nYou: ").strip()
        if query.lower() in {"exit", "quit"}:
            break

        result = bot.process_with_trace(query)
        print("\nSahayak AI:\n")
        print(result.answer)
        print("\nExecution Trace:")
        for step in result.execution_trace:
            print(f"- {step['label']}: {step['status']} ({step['execution_time_ms']} ms)")
