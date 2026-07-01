"""
Sequential execution engine for planned orchestrator tasks.
"""
from __future__ import annotations

import logging
from typing import Any

from src.agents.orchestrator.agent_registry import AgentRegistry
from src.agents.orchestrator.task import Task

log = logging.getLogger(__name__)


class Executor:
    """Runs planned tasks in order and records status/timing on each task."""

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    def run(self, tasks: list[Task], context: dict[str, Any]) -> dict[str, Any]:
        for task in tasks:
            attempts = task.retries + 1
            for attempt in range(1, attempts + 1):
                started_at = task.start()
                try:
                    task.input_data = self._snapshot_input(context)
                    context["current_task_name"] = task.name
                    print(
                        "[Orchestrator][Executor] Selected Agent: "
                        f"{task.agent} for task={task.name}"
                    )
                    print(f"[Orchestrator][Executor] Execution Started: {task.name}")
                    log.info(
                        "Executing orchestrator task=%s agent=%s attempt=%d",
                        task.name,
                        task.agent,
                        attempt,
                    )
                    output = self.registry.execute(task.agent, context)
                    task.complete(started_at, output)

                    if task.output_key:
                        context[task.output_key] = output

                    print(
                        "[Orchestrator][Executor] Execution Finished: "
                        f"{task.name} status={task.status} time_ms={task.execution_time_ms}"
                    )
                    print(
                        "[Orchestrator][Executor] Returned Object: "
                        f"{type(output).__name__}"
                    )
                    log.info(
                        "Completed orchestrator task=%s agent=%s time_ms=%.2f",
                        task.name,
                        task.agent,
                        task.execution_time_ms,
                    )
                    break
                except Exception as exc:
                    task.fail(started_at, exc)
                    print(
                        "[Orchestrator][Executor] Execution Failed: "
                        f"{task.name} agent={task.agent} error={exc}"
                    )
                    log.exception(
                        "Failed orchestrator task=%s agent=%s attempt=%d/%d",
                        task.name,
                        task.agent,
                        attempt,
                        attempts,
                    )

                    if attempt >= attempts:
                        if task.required:
                            raise
                        log.warning("Skipping optional failed task=%s: %s", task.name, exc)

        context.pop("current_task_name", None)
        return context

    def _snapshot_input(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "session_id": context.get("session_id"),
            "intent": context.get("intent"),
            "goal": context.get("goal"),
            "user_query": context.get("user_query"),
        }
