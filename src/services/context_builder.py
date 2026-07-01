"""
=========================================================
Sahayak AI - Context Builder
=========================================================

Purpose:
    Builds structured context for the LLM by combining:
    - System Prompt
    - Conversation History
    - Relevant Knowledge
    - Current User Query

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

from typing import List, Dict


class ContextBuilder:
    """
    Builds the final context that will be sent to the LLM.
    """

    def __init__(self, max_history: int = 10):

        self.max_history = max_history

    def _format_history(
        self,
        history: List[Dict]
    ) -> str:
        """
        Format conversation history.
        """

        if not history:
            return "No previous conversation."

        history = history[-self.max_history:]

        lines = []

        for message in history:

            role = message.get("role", "unknown").capitalize()

            content = message.get("content", "")

            lines.append(f"{role}: {content}")

        return "\n".join(lines)

    def _format_documents(
        self,
        documents: List[Dict]
    ) -> str:
        """
        Format retrieved RAG documents.
        """

        if not documents:
            return "No relevant documents retrieved."

        lines = []

        for i, item in enumerate(documents, start=1):

            doc = item["document"]

            lines.append(f"""
    -----------------------------
    Document {i}
    -----------------------------
    Title:
    {doc.get("title","")}

    Content:
    {doc.get("text","")}
    """)

        return "\n".join(lines)
    

    def build_context(
        self,
        system_prompt: str,
        user_query: str,
        conversation_history: List[Dict],
        retrieved_documents: List[Dict]
    ) -> str:
        """
        Build complete LLM context.
        """

        history = self._format_history(conversation_history)

        documents_text = self._format_documents(
        retrieved_documents
    )

        context = f"""
================ SYSTEM ================

{system_prompt}

================ HISTORY ===============

{history}

========= RETRIEVED DOCUMENTS =========

{documents_text}

========== CURRENT QUESTION ============

{user_query}

========================================
"""

        return context.strip()
    
if __name__ == "__main__":

    builder = ContextBuilder()

    history = [

        {
            "role": "user",
            "content": "Hello"
        },

        {
            "role": "assistant",
            "content": "Hello Prince!"
        },

        {
            "role": "user",
            "content": "Tell me about PMAY"
        }

    ]

    knowledge = {

        "scheme_name": "Pradhan Mantri Awas Yojana",

        "category": "Housing",

        "benefit": "Financial Assistance"

    }

    prompt = builder.build_context(

        system_prompt="You are Sahayak AI.",

        user_query="Tell me about PMAY",

        conversation_history=history,

        knowledge=knowledge

    )

    print(prompt)