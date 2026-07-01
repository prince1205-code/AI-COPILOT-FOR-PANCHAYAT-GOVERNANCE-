"""
Task primitives for the Sahayak agentic orchestrator.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any
from uuid import uuid4


TaskStatus = str


@dataclass
class Task:
    """A single planned unit of work executed by one registered agent."""

    name: str
    agent: str
    input_key: str | None = None
    output_key: str | None = None
    label: str = ""
    retries: int = 0
    required: bool = True
    input_data: dict[str, Any] = field(default_factory=dict)
    output: Any = None
    status: TaskStatus = "pending"
    execution_time_ms: float = 0.0
    error: str | None = None
    task_id: str = field(default_factory=lambda: uuid4().hex[:12])

    def start(self) -> float:
        self.status = "running"
        self.error = None
        return perf_counter()

    def complete(self, started_at: float, output: Any) -> None:
        self.status = "completed"
        self.output = output
        self.execution_time_ms = round((perf_counter() - started_at) * 1000, 2)

    def fail(self, started_at: float, error: Exception) -> None:
        self.status = "failed"
        self.error = str(error)
        self.execution_time_ms = round((perf_counter() - started_at) * 1000, 2)

    def to_trace(self) -> dict[str, Any]:
        """Return a JSON-safe execution trace entry."""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "label": self.label or self.name.replace("_", " ").title(),
            "agent": self.agent,
            "status": self.status,
            "execution_time_ms": self.execution_time_ms,
            "error": self.error,
        }
