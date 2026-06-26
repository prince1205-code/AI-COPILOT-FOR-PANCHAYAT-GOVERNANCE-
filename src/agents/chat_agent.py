"""
=========================================================
Sahayak AI - Chat Agent
=========================================================

Purpose:
    Handles general conversations such as greetings,
    introductions, and casual user interactions.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

from src.services.ai_service import AIService


class ChatAgent:
    """
    Agent responsible for handling general conversations.
    """

    def __init__(self):
        """
        Initialize the AI Engine.
        """
        self.ai = AIService.get_ai()
        
    def process(self, user_query: str) -> str:
        """
        Process a general chat request.

        Parameters
        ----------
        user_query : str

        Returns
        -------
        str
            AI generated response.
        """

        return self.ai.ask(user_query)


# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    agent = ChatAgent()

    print("=" * 50)
    print("Chat Agent Started")
    print("=" * 50)

    while True:

        query = input("\nYou : ")

        if query.lower() in ["exit", "quit"]:
            print("\nChat Agent Closed.")
            break

        response = agent.process(query)

        print("\nSahayak AI :")
        print(response)