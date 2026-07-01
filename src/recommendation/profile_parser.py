"""
=========================================================
Sahayak AI - Profile Parser
=========================================================

Purpose:
    Extract citizen profile information from
    natural language user input.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

import re


class ProfileParser:
    """
    Extracts structured profile information
    from user's natural language input.
    """

    def __init__(self):

        self.states = [

            "andhra pradesh",
            "arunachal pradesh",
            "assam",
            "bihar",
            "chhattisgarh",
            "goa",
            "gujarat",
            "haryana",
            "himachal pradesh",
            "jharkhand",
            "karnataka",
            "kerala",
            "madhya pradesh",
            "maharashtra",
            "manipur",
            "meghalaya",
            "mizoram",
            "nagaland",
            "odisha",
            "punjab",
            "rajasthan",
            "sikkim",
            "tamil nadu",
            "telangana",
            "tripura",
            "uttar pradesh",
            "uttarakhand",
            "west bengal",
            "delhi"
        ]

        self.occupations = [

            "farmer",
            "student",
            "labour",
            "labor",
            "teacher",
            "worker",
            "business",
            "shopkeeper",
            "employee",
            "driver",
            "doctor",
            "engineer",
            "unemployed",
            "housewife"

        ]

    # --------------------------------------------------

    def parse(self, text: str) -> dict:

        """
        Extract profile fields from user text.
        """

        text = text.lower()

        profile = {

            "age": None,
            "state": None,
            "occupation": None,
            "income": None,
            "gender": None

        }

        # -----------------------------------------
        # Age
        # -----------------------------------------

        age = re.search(r"\b(\d{1,3})\s*(years?|yrs?)?\b", text)

        if age:

            value = int(age.group(1))

            if 0 < value < 120:

                profile["age"] = value

        # -----------------------------------------
        # Income
        # -----------------------------------------

        income = re.search(r"(\d+(?:\.\d+)?)\s*(lakh|lakhs)", text)

        if income:

            value = float(income.group(1))

            profile["income"] = int(value * 100000)

        else:

            income = re.search(r"₹?\s*(\d{4,10})", text)

            if income:

                profile["income"] = int(income.group(1))

        # -----------------------------------------
        # Gender
        # -----------------------------------------

        if "female" in text:
            profile["gender"] = "female"
        elif "male" in text:
            profile["gender"] = "male"

        # -----------------------------------------
        # State
        # -----------------------------------------

        for state in self.states:

            if state in text:

                profile["state"] = state.title()

                break

        # -----------------------------------------
        # Occupation
        # -----------------------------------------

        for occupation in self.occupations:

            if occupation in text:

                profile["occupation"] = occupation.title()

                break

        return profile


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    parser = ProfileParser()

    print("=" * 60)
    print("Profile Parser")
    print("=" * 60)

    while True:

        query = input("\nEnter Profile : ")

        if query.lower() in ["exit", "quit"]:

            break

        profile = parser.parse(query)

        print("\nExtracted Profile\n")

        for key, value in profile.items():

            print(f"{key:12}: {value}")