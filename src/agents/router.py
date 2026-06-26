"""
=========================================================
Sahayak AI - Intent Router
=========================================================

Purpose:
    Detect the user's intent and route the request
    to the appropriate AI agent.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

import re


class IntentRouter:
    """
    Rule-based intent router for Sahayak AI.
    """

    def __init__(self):

        self.intent_keywords = {

            "chat": [
                "hi",
                "hello",
                "hey",
                "good morning",
                "good evening",
                "who are you",
                "how are you"
            ],

            "scheme": [
                "scheme",
                "yojana",
                "pm awas",
                "pm kisan",
                "scholarship",
                "benefit",
                "eligibility",
                "subsidy"
            ],

            "document": [
                "certificate",
                "application",
                "notice",
                "letter",
                "draft",
                "pdf",
                "income certificate",
                "caste certificate"
            ],

            "knowledge": [
                "panchayat",
                "gram sabha",
                "rule",
                "act",
                "government",
                "constitution",
                "policy"
            ]
        }

    def route_query(self, user_query: str) -> str:
        """
        Returns the detected intent.

        Returns:
            chat
            scheme
            document
            knowledge
            unknown
        """

        query = user_query.lower().strip()

        query = re.sub(r"[^\w\s]", "", query)

        for intent, keywords in self.intent_keywords.items():

            for keyword in keywords:

                if keyword in query:
                    return intent

        return "unknown"


# --------------------------------------------------------
# Testing
# --------------------------------------------------------

if __name__ == "__main__":

    router = IntentRouter()

    while True:

        question = input("\nEnter Query : ")

        if question.lower() == "exit":
            break

        intent = router.route_query(question)

        print(f"Detected Intent : {intent}")