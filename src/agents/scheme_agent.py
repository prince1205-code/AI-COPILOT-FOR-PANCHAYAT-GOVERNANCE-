"""
=========================================================
Sahayak AI - Scheme Agent
=========================================================

Purpose:
    Handles all Government Scheme related queries.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

import json

from src.services.ai_service import AIService
from src.services.knowledge_loader import KnowledgeLoader


class SchemeAgent:

    def __init__(self):

        self.ai = AIService.get_ai()

        self.loader = KnowledgeLoader()


    def process(self, user_query: str):

        """
        Process Government Scheme Queries.
        """

        scheme = self.loader.search_scheme(user_query)

        if scheme is None:

            return (
                "Sorry! I couldn't find any matching scheme "
                "in the knowledge base."
            )

        prompt = f"""
You are Sahayak AI.

Use ONLY the following official scheme information.

Scheme Information:

{json.dumps(scheme, indent=4)}

User Question:

{user_query}

Instructions:

1. Answer using only the above information.
2. Use simple language.
3. If the answer is not present, clearly say so.
4. Don't invent facts.
"""

        return self.ai.ask(prompt)


# ------------------------------------------------------
# Testing
# ------------------------------------------------------

if __name__ == "__main__":

    agent = SchemeAgent()

    print("=" * 60)
    print("Scheme Agent Started")
    print("=" * 60)

    while True:

        query = input("\nUser : ")

        if query.lower() == "exit":
            break

        response = agent.process(query)

        print("\nSahayak AI:\n")

        print(response)