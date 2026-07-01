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
from src.services.context_builder import ContextBuilder
from src.rag.retriever import Retriever
from src.core.prompts import SYSTEM_PROMPT

class SchemeAgent:

    def __init__(self):
        self.ai = AIService.get_ai()

        self.retriever = Retriever()

        self.context_builder = ContextBuilder()


    def process(self, user_query: str, history=None):

        if history is None:
            history = []

        # -----------------------------------------
        # Retrieve Top Documents
        # -----------------------------------------

        retrieved_documents = self.retriever.retrieve(

            user_query,

            top_k=5

        )

        # -----------------------------------------
        # Build Prompt
        # -----------------------------------------

        context = self.context_builder.build_context(

            system_prompt=SYSTEM_PROMPT,

            user_query=user_query,

            conversation_history=history,

            retrieved_documents=retrieved_documents

        )

        # -----------------------------------------
        # Ask Gemini
        # -----------------------------------------

        return self.ai.ask(context)

        prompt = f"""
You are Sahayak AI, an AI Assistant for Panchayat Governance.

You MUST answer ONLY using the scheme information given below.

If the answer is not available in the scheme information,
say clearly:

'I could not find this information in the official dataset.'

=========================
SCHEME INFORMATION
=========================

Name:
{scheme.get("scheme_name","")}

Category:
{scheme.get("category","")}

Level:
{scheme.get("level","")}

Description:
{scheme.get("description","")}

Benefits:
{scheme.get("benefits","")}

Eligibility:
{scheme.get("eligibility","")}

Application Process:
{scheme.get("application_process","")}

Required Documents:
{scheme.get("required_documents","")}

=========================
USER QUESTION
=========================

{user_query}

=========================
RULES
=========================

1. Never invent information.
2. Use only the above dataset.
3. Reply in simple English.
4. Use bullet points whenever appropriate.
5. If something is unavailable, explicitly mention it.
"""

        return self.ai.ask(prompt)


# ------------------------------------------------------
# Testing
# ------------------------------------------------------

if __name__ == "__main__":

    agent = SchemeAgent()

    history = []

    while True:

        query = input("\nUser : ")

        if query.lower() in ["exit", "quit"]:

            break

        response = agent.process(

            query,

            history

        )

        history.append({

            "role": "user",

            "content": query

        })

        history.append({

            "role": "assistant",

            "content": response

        })

        print("\nSahayak AI:\n")

        print(response)