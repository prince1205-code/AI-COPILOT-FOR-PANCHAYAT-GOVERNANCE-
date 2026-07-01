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
from google.api_core.exceptions import DeadlineExceeded


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


        print("✅ Sahayak AI Initialized Successfully")


    def generate(self, context: str):

        """
        Send a message to Gemini.

        Parameters
        ----------
        user_question : str

        Returns
        -------
        AI Response
        """

        try:
            response = self.model.generate_content(context)
            return response.text

        except DeadlineExceeded:
            return (
                "The AI service timed out. "
                "Please try again."
            )

        except Exception as e:
            return f"Error : {e}"
        
        

    def ask(self, context: str):
        """
        Backward compatible wrapper.
        Existing agents can continue using ask().
        """

        return self.generate(context)
    

    
    def reset_chat(self):
        """
        Clears conversation history.
        """

        self.chat = self.model.start_chat(history=[])

        print("Stateless AI Engine. No chat history to reset")


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

        answer = ai.generate(question)

        print("\n🤖 Sahayak AI :")
        print(answer)
        print("-" * 60)