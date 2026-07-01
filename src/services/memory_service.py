"""
=========================================================
Sahayak AI - Memory Service
=========================================================

Purpose:
    Manages conversation history for every session.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

from typing import Dict, List, Optional
from datetime import datetime

class MemoryService:

    def __init__(self, max_history: int = 20):

        self.max_history = max_history

        self.sessions: Dict[str, List[dict]] = {}

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        intent: str = "unknown",
        metadata: Optional[dict] = None
    ):

        if session_id not in self.sessions:
            self.sessions[session_id] = []

        message = {

            "role": role,

            "content": content,

            "intent": intent,

            "timestamp": datetime.now().isoformat(),

            "metadata": metadata or {}

        }

        self.sessions[session_id].append(message)

        if len(self.sessions[session_id]) > self.max_history:
            self.sessions[session_id] = self.sessions[session_id][-self.max_history:]

            
    def get_history(self,
                    session_id: str):

        return self.sessions.get(session_id, [])

    def clear_history(self,
                      session_id: str):

        if session_id in self.sessions:

            del self.sessions[session_id]

    def print_history(self,
                      session_id: str):

        history = self.get_history(session_id)

        print("\n========== Conversation ==========\n")

        for msg in history:

            print(f"""
                    Role      : {msg['role']}
                    Intent    : {msg['intent']}
                    Message   : {msg['content']}
                    Time      : {msg['timestamp']}
                    """)

        print("\n==================================")

if __name__ == "__main__":

    memory = MemoryService()

    SESSION = "prince"

    memory.add_message(
        SESSION,
        "user",
        "Hello",
        intent="chat"
    )

    memory.add_message(
        SESSION,
        "assistant",
        "Hello Prince!",
        intent="chat"
    )

    memory.add_message(
        SESSION,
        "user",
        "Tell me about PMAY.",
        intent="scheme"
    )

    memory.print_history(SESSION)