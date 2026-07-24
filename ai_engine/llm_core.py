import requests
import json
from core.settings import LLM_API_URL, LLM_API_KEY, LLM_MODEL


def call_llm(prompt: str, system_prompt: str = "", max_tokens: int = 1000) -> str:
    """
    统一大模型调度层，支持DeepSeek/通义千问/火山等
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLM_API_KEY}"
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.8
    }

    try:
        resp = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[LLM Error] {e}")
        return ""
