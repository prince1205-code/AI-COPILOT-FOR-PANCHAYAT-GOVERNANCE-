"""
=========================================================
Sahayak AI - AI Engine
=========================================================

Purpose:
    This module initializes the Gemini model and provides
    functions to interact with Sahayak AI.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

# =====================================================
# Imports
# =====================================================

import google.generativeai as genai

from src.core.config import GEMINI_API_KEY, MODEL_NAME
from src.core.prompts import SYSTEM_PROMPT


# =====================================================
# Configure Gemini
# =====================================================

genai.configure(api_key=GEMINI_API_KEY)


# =====================================================
# AI Engine Class
# =====================================================

class SahayakAI:

    def __init__(self):
        """
        Initialize Gemini model and chat session.
        """

        self.model = genai.GenerativeModel(MODEL_NAME)

        self.chat = self.model.start_chat(history=[])

        print("✅ Sahayak AI Initialized Successfully")


    def ask(self, user_question: str):

        """
        Send a message to Gemini.

        Parameters
        ----------
        user_question : str

        Returns
        -------
        AI Response
        """

        prompt = f"""
{SYSTEM_PROMPT}

User:
{user_question}

Assistant:
"""

        try:

            response = self.chat.send_message(prompt)

            return response.text

        except Exception as e:

            return f"Error : {str(e)}"


    def reset_chat(self):
        """
        Clears conversation history.
        """

        self.chat = self.model.start_chat(history=[])

        print("✅ Chat history cleared.")


# =====================================================
# Standalone Testing
# =====================================================

if __name__ == "__main__":

    ai = SahayakAI()

    print()

    while True:

        question = input("👤 You : ")

        if question.lower() in ["exit", "quit"]:

            print("\n🤖 Sahayak AI : Goodbye!")
            break

        answer = ai.ask(question)

        print("\n🤖 Sahayak AI :")
        print(answer)
        print("-" * 60)