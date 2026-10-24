import asyncio
import json
import urllib.request
from backend import config


def _sync_openrouter_call(model: str, prompt: str) -> dict | None:
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Tutor",
        },
    )
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        raw_text = data["choices"][0]["message"]["content"]
        return json.loads(raw_text)


async def call_openrouter(prompt: str, required_key: str | None = "steps") -> dict | None:
    """Call OpenRouter API with fallback across free-tier models."""
    if not config.OPENROUTER_API_KEY:
        return None

    for model in config.OPENROUTER_MODELS:
        try:
            result = await asyncio.to_thread(_sync_openrouter_call, model, prompt)
            if result and isinstance(result, dict):
                if required_key is None or required_key in result:
                    return result
        except Exception as e:
            print(f"OpenRouter model '{model}' failed: {e}")
            continue
    return None
