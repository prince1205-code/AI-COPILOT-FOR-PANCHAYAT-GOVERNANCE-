"""
=========================================================
Sahayak AI - Configuration Module
=========================================================

Purpose:
    This module manages all project configurations.

Responsibilities:
    - Load environment variables
    - Configure API keys
    - Define project directories
    - Store model configuration

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

# =========================
# Import Libraries
# =========================

import os
from pathlib import Path

from dotenv import load_dotenv


# =========================
# Load Environment Variables
# =========================

load_dotenv()

 
# =========================
# Project Root Directory
# =========================

# src/config.py -> project root
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = BASE_DIR / ".env"

print("Loading .env from:", dotenv_path)

load_dotenv(dotenv_path=dotenv_path)

print("API Key Loaded:", os.getenv("GEMINI_API_KEY"))

# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

dotenv_path = PROJECT_ROOT / ".env"

print("Project Root:", PROJECT_ROOT)
print("Loading .env from:", dotenv_path)

load_dotenv(dotenv_path=dotenv_path)

print("API Key Loaded:", os.getenv("GEMINI_API_KEY"))

DATA_DIR = PROJECT_ROOT / "data"
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"
DOCUMENTS_DIR = PROJECT_ROOT / "documents"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"



# =========================
# Gemini Configuration
# =========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-flash"


# =========================
# Application Configuration
# =========================

APP_NAME = "Sahayak AI"

APP_VERSION = "1.0.0"

SUPPORTED_LANGUAGES = [
    "English",
    "Hindi"
]


# =========================
# Configuration Validation
# =========================

def validate_config():
    """
    Validate required configuration values.
    """

    if not GEMINI_API_KEY:
        raise ValueError(
            "❌ GEMINI_API_KEY not found. Please check your .env file."
        )

    print("✅ Configuration Loaded Successfully")


# =========================
# Run Directly
# =========================

if __name__ == "__main__":

    validate_config()

    print("\n========== Project Configuration ==========\n")

    print("App Name :", APP_NAME)
    print("Version :", APP_VERSION)
    print("Model :", MODEL_NAME)

    print("\nProject Root :", BASE_DIR)

    print("\nData Folder :", DATA_DIR)
    print("Knowledge Base :", KNOWLEDGE_BASE_DIR)
    print("Documents :", DOCUMENTS_DIR)
    print("Outputs :", OUTPUTS_DIR)
    print("Models :", MODELS_DIR)
    print("Logs :", LOGS_DIR)