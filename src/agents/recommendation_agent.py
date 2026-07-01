"""
=========================================================
Sahayak AI - Recommendation Agent
=========================================================

Purpose:
    Generates personalized government scheme
    recommendations for citizens.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

from src.services.ai_service import AIService
from src.recommendation.profile_parser import ProfileParser
from src.recommendation.eligibility_engine import EligibilityEngine


class RecommendationAgent:
    """
    Personalized Government Scheme Recommendation Agent.
    """

    def __init__(self):

        self.ai = AIService.get_ai()

        self.profile_parser = ProfileParser()

        self.engine = EligibilityEngine()

    # --------------------------------------------------

    def process(self, user_query: str):

        """
        Generate personalized recommendations.
        """

        # Step 1
        profile = self.profile_parser.parse(user_query)

        # Step 2
        recommendations = self.engine.recommend(
            profile,
            top_k=5
        )

        # No recommendation
        if len(recommendations) == 0:

            return (
                "I couldn't identify enough profile information.\n\n"
                "Please tell me your:\n"
                "- Age\n"
                "- State\n"
                "- Occupation\n"
                "- Income"
            )

        # Step 3
        schemes = ""

        for i, scheme in enumerate(recommendations, start=1):

            schemes += f"""
Scheme {i}

Name:
{scheme['scheme_name']}

Category:
{scheme['category']}

Reason:
{scheme['reason']}

Score:
{scheme['score']}

------------------------------------
"""

        # Step 4
        prompt = f"""
You are Sahayak AI.

A citizen has provided the following profile.

Citizen Profile

{profile}

Recommended Government Schemes

{schemes}

Instructions

1. Explain why these schemes are suitable.
2. Use simple language.
3. Use bullet points.
4. Do NOT invent new schemes.
5. Recommend only the listed schemes.
6. Keep the answer concise.
"""

        return self.ai.generate(prompt)


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    agent = RecommendationAgent()

    print("=" * 60)
    print("Recommendation Agent")
    print("=" * 60)

    while True:

        query = input("\nUser : ")

        if query.lower() in ["exit", "quit"]:

            break

        response = agent.process(query)

        print("\nSahayak AI:\n")

        print(response)