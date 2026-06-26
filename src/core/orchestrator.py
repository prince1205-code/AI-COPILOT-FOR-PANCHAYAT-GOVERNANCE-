"""
=========================================================
Sahayak AI - Orchestrator
=========================================================

Purpose:
    Central controller of the Sahayak AI system.

Responsibilities:
    - Receive user query
    - Detect intent
    - Route request to correct agent
    - Return final response

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

# =====================================================
# Imports
# =====================================================

from src.agents.router import IntentRouter
from src.agents.chat_agent import ChatAgent
from src.agents.scheme_agent import SchemeAgent


# =====================================================
# Orchestrator
# =====================================================

class SahayakOrchestrator:

    def __init__(self):

        print("Initializing Sahayak AI Orchestrator...")

        self.router = IntentRouter()

        self.chat_agent = ChatAgent()

        self.scheme_agent = SchemeAgent()

        print("Orchestrator Ready.\n")


    def process(self, user_query: str):

        """
        Process user request.
        """

        intent = self.router.route_query(user_query)

        print(f"[Intent Detected] -> {intent}")

        if intent == "chat":

            return self.chat_agent.process(user_query)

        elif intent == "scheme":

            return self.scheme_agent.process(user_query)

        elif intent == "document":

            return (
                "🚧 Document Agent is under development."
            )

        elif intent == "knowledge":

            return (
                "🚧 Knowledge Agent is under development."
            )

        else:

            return (
                "Sorry, I couldn't understand your request."
            )


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    bot = SahayakOrchestrator()

    while True:

        query = input("\n👤 You : ").strip()

        if query.lower() in ["exit", "quit"]:

            print("\n👋 Goodbye!")
            break

        answer = bot.process(query)

        print("\n🤖 Sahayak AI:\n")

        print(answer)