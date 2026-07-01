import base64
from google import genai
from google.genai import types

from src.core.config              import GEMINI_API_KEY
from src.agents.voice.audio_utils import audio_to_base64

_STT_PROMPT = (
    "Transcribe the spoken audio exactly as heard. "
    "Output ONLY the transcribed text — no labels, no explanations, no punctuation corrections. "
    "If the audio is silent or inaudible, output exactly: [INAUDIBLE]"
)


class SpeechToText:
    """
    Transcribes audio using Gemini's multimodal capability.
    Stateless — safe to use as a singleton.
    """

    def __init__(self):
        self._client = genai.Client(api_key=GEMINI_API_KEY)

    def transcribe(self, audio_bytes: bytes, mime_type: str) -> str:
        """
        Transcribe audio bytes to text.

        Parameters
        ----------
        audio_bytes : raw audio data
        mime_type   : validated Gemini mime type (e.g. 'audio/webm')

        Returns
        -------
        str — transcript, or raises ValueError/RuntimeError
        """
        b64 = audio_to_base64(audio_bytes)

        response = self._client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                types.Part.from_bytes(data=base64.b64decode(b64), mime_type=mime_type),
                _STT_PROMPT,
            ],
        )

        transcript = response.text.strip()

        if not transcript or transcript == "[INAUDIBLE]":
            raise ValueError("Could not transcribe audio — please speak clearly and try again.")

        return transcript
