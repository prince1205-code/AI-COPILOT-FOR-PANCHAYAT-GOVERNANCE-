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

from typing import Dict, List


class MemoryService:

    def __init__(self, max_history: int = 20):

        self.max_history = max_history

        self.sessions: Dict[str, List[dict]] = {}

    def add_message(self,
                    session_id: str,
                    role: str,
                    content: str):

        if session_id not in self.sessions:

            self.sessions[session_id] = []

        self.sessions[session_id].append({

            "role": role,

            "content": content

        })

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

            print(f"{msg['role']} : {msg['content']}")

        print("\n==================================")

if __name__ == "__main__":

    memory = MemoryService()

    SESSION = "prince"

    memory.add_message(

        SESSION,

        "user",

        "Hello"

    )

    memory.add_message(

        SESSION,

        "assistant",

        "Hello Prince!"

    )

    memory.add_message(

        SESSION,

        "user",

        "Tell me about PMAY."

    )

    memory.print_history(SESSION)