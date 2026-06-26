"""
=========================================================
Sahayak AI - AI Service
=========================================================

Provides a shared AI engine instance for all agents.

Author : Prince Kumar
=========================================================
"""

from src.core.ai_engine import SahayakAI


class AIService:

    _instance = None

    @classmethod
    def get_ai(cls):

        if cls._instance is None:

            cls._instance = SahayakAI()

        return cls._instance