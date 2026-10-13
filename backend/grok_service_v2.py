import os
import requests

from dotenv import load_dotenv

from prompts_v2 import DOCTYN_SYSTEM_PROMPT


load_dotenv()


XAI_API_URL = "https://api.x.ai/v1/chat/completions"


def ask_grok(
    user_message: str,
    verified_context: str,
    conversation_history=None
):
    api_key = os.getenv("XAI_API_KEY")
    model = os.getenv("XAI_MODEL")

    if not api_key:
        print("XAI_API_KEY is not configured.")
        return None

    if not model:
        print("XAI_MODEL is not configured.")
        return None

    if conversation_history is None:
        conversation_history = []

    messages = [
        {
            "role": "system",
            "content": (
                DOCTYN_SYSTEM_PROMPT
                + "\n\nVERIFIED DOCTYN CONTEXT:\n"
                + verified_context
            )
        }
    ]

    for item in conversation_history[-8:]:
        if (
            isinstance(item, dict)
            and item.get("role") in ["user", "assistant"]
            and item.get("content")
        ):
            messages.append(item)

    messages.append({
        "role": "user",
        "content": user_message
    })

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            XAI_API_URL,
            headers=headers,
            json=payload,
            timeout=45
        )

        if not response.ok:
            print(
                "Grok API error:",
                response.status_code,
                response.text
            )
            return None

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as exc:
        print("Grok request failed:", exc)
        return None
