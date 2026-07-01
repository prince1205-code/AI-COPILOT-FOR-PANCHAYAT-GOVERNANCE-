"""
Sahayak AI - Language Detector
Two-stage detection:
  1. Unicode script analysis (fast, no API call)
  2. Gemini confirmation for Latin-script languages (Hindi/English/Bhojpuri/Awadhi)
"""
import re
import json
from google import genai
from google.genai import types
from src.core.config import GEMINI_API_KEY

# ── Unicode script ranges ──────────────────────────────────────────────────────
_SCRIPT_RANGES = {
    "Hindi":     (r"[\u0900-\u097F]", "Devanagari"),
    "Bengali":   (r"[\u0980-\u09FF]", "Bengali"),
    "Gujarati":  (r"[\u0A80-\u0AFF]", "Gujarati"),
    "Punjabi":   (r"[\u0A00-\u0A7F]", "Gurmukhi"),
    "Tamil":     (r"[\u0B80-\u0BFF]", "Tamil"),
    "Telugu":    (r"[\u0C00-\u0C7F]", "Telugu"),
    "Kannada":   (r"[\u0C80-\u0CFF]", "Kannada"),
    "Malayalam": (r"[\u0D00-\u0D7F]", "Malayalam"),
    "Urdu":      (r"[\u0600-\u06FF]", "Arabic/Urdu"),
}

# Latin-script languages that need Gemini to distinguish
_LATIN_LANGS = ["English", "Hindi", "Bhojpuri", "Awadhi", "Marathi"]

_GEMINI_PROMPT = (
    "Identify the language of the following text. "
    "Choose ONLY from: English, Hindi, Bhojpuri, Awadhi, Bengali, Marathi, "
    "Gujarati, Punjabi, Tamil, Telugu, Kannada, Malayalam, Urdu. "
    "Respond with ONLY valid JSON: "
    '{"language": "<name>", "confidence": <0.0-1.0>}\n\nText: '
)

# Low-confidence fallback: detect script family
_DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")


def _script_detect(text: str) -> tuple[str, float] | None:
    """Return (language, confidence) if a non-Latin script is dominant."""
    total = len(text.replace(" ", "")) or 1
    for lang, (pattern, _) in _SCRIPT_RANGES.items():
        count = len(re.findall(pattern, text))
        ratio = count / total
        if ratio > 0.25:
            return lang, min(0.95, 0.60 + ratio * 0.35)
    return None


def _gemini_detect(text: str, client: genai.Client) -> tuple[str, float]:
    """Use Gemini to detect language for Latin-script or ambiguous text."""
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[_GEMINI_PROMPT + text[:500]],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.0,
            ),
        )
        parsed = json.loads(response.text.strip())
        lang  = parsed.get("language", "English")
        conf  = float(parsed.get("confidence", 0.5))
        return lang, min(conf, 0.95)
    except Exception:
        return "English", 0.40


def _fallback(text: str) -> str:
    """If confidence is low, pick Hindi (Devanagari present) else English."""
    return "Hindi" if _DEVANAGARI_RE.search(text) else "English"


class LanguageDetector:
    """
    Stateless detector. Safe to use as a singleton.
    Returns dict: { detected_language, confidence, method }
    """

    def __init__(self):
        self._client = genai.Client(api_key=GEMINI_API_KEY)

    def detect(self, text: str) -> dict:
        if not text or not text.strip():
            return {"detected_language": "English", "confidence": 0.0, "method": "default"}

        # Stage 1 — fast script check
        result = _script_detect(text)
        if result:
            lang, conf = result
            return {"detected_language": lang, "confidence": round(conf, 2), "method": "script"}

        # Stage 2 — Gemini for Latin-script text
        lang, conf = _gemini_detect(text, self._client)

        # Low-confidence fallback
        if conf < 0.45:
            lang = _fallback(text)
            conf = 0.50

        return {"detected_language": lang, "confidence": round(conf, 2), "method": "gemini"}
