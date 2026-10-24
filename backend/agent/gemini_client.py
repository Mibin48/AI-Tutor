import asyncio
import json
import urllib.request
from backend import config


def _sync_gemini_call(model: str, prompt: str) -> dict | None:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={config.GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(raw_text)


async def call_gemini(prompt: str, required_key: str | None = "steps") -> dict | None:
    """Call Google Gemini API with fallback across configured models."""
    if not config.GEMINI_API_KEY:
        return None

    for model in config.GEMINI_MODELS:
        try:
            result = await asyncio.to_thread(_sync_gemini_call, model, prompt)
            if result and isinstance(result, dict):
                if required_key is None or required_key in result:
                    return result
        except Exception as e:
            print(f"Gemini model '{model}' failed: {e}")
            continue
    return None
