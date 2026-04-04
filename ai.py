"""OpenAI integration for converting free text into a music mood payload."""

import json
import os

from openai import OpenAI

from config import get_openai_model


EMOTION_FIELDS = ("emotion", "mood", "keywords", "energy")


class AIError(Exception):
    """Raised when the emotion extraction step fails."""


def _require_non_empty_string(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise AIError(f"Emotion payload field '{field_name}' must be a non-empty string.")
    return value.strip()


def _validate_emotion_payload(payload):
    if not isinstance(payload, dict):
        raise AIError("OpenAI returned invalid JSON.")

    missing_fields = [field for field in EMOTION_FIELDS if field not in payload]
    if missing_fields:
        joined_fields = ", ".join(missing_fields)
        raise AIError(f"Emotion payload missing required fields: {joined_fields}")

    keywords = payload["keywords"]
    if not isinstance(keywords, list) or not keywords:
        raise AIError("Emotion payload field 'keywords' must be a non-empty list of strings.")

    normalized_keywords = []
    for keyword in keywords:
        if not isinstance(keyword, str) or not keyword.strip():
            raise AIError("Emotion payload field 'keywords' must be a non-empty list of strings.")
        normalized_keywords.append(keyword.strip())

    return {
        "emotion": _require_non_empty_string(payload["emotion"], "emotion"),
        "mood": _require_non_empty_string(payload["mood"], "mood"),
        "keywords": normalized_keywords,
        "energy": _require_non_empty_string(payload["energy"], "energy"),
    }


def convert_to_emotion(user_input, client=None, model=None):
    """Convert user input into a validated emotion payload."""
    mood_text = user_input.strip()
    if not mood_text:
        raise AIError("Mood text cannot be empty.")

    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise AIError("Missing OPENAI_API_KEY.")
        client = OpenAI(api_key=api_key)

    prompt = """
You are a helpful assistant that converts user input into an emotion.
Return only valid JSON in the following format:
{
"emotion": "here emotion",
"mood": "here mood",
"keywords": ["music-ready", "keywords"],
"energy": "low/medium/high"
}
Give only the JSON object without markdown, explanation, or extra text.
"""

    try:
        response = client.chat.completions.create(
            model=model or get_openai_model(),
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": (
                        "Convert the following user input into an emotion payload: "
                        f"{mood_text}"
                    ),
                },
            ],
        )
    except Exception as error:
        raise AIError(f"OpenAI request failed: {error}") from error

    choices = getattr(response, "choices", [])
    if not choices:
        raise AIError("OpenAI returned an empty response.")

    message = getattr(choices[0], "message", None)
    content = getattr(message, "content", None)
    if not isinstance(content, str) or not content.strip():
        raise AIError("OpenAI returned an empty response.")

    try:
        payload = json.loads(content)
    except json.JSONDecodeError as error:
        raise AIError("OpenAI returned invalid JSON.") from error

    return _validate_emotion_payload(payload)
