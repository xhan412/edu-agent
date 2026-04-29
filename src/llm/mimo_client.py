from typing import Dict, List
import requests
from src.config import settings
from .base import BaseLLMClient


class MimoClient(BaseLLMClient):
    """
    Mimo API 适配层。

    注意：
    这里保留为通用 OpenAI-compatible 风格示例。
    等拿到 Mimo 正式 API 文档后，只需要修改 endpoint、headers、payload 字段即可。
    """

    def chat(self, system: str, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        if not settings.mimo_api_key or not settings.mimo_base_url:
            raise RuntimeError("MIMO_API_KEY or MIMO_BASE_URL is missing.")

        url = settings.mimo_base_url.rstrip("/") + "/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.mimo_api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": settings.mimo_model,
            "temperature": temperature,
            "messages": [{"role": "system", "content": system}] + messages,
        }

        response = requests.post(url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]
