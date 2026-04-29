import httpx

from app.core.config import settings


class DeepSeekClient:
    async def chat(self, prompt: str) -> str:
        if not settings.deepseek_api_key:
            return "DeepSeek API Key 尚未配置。请在 backend/.env 中填写 DEEPSEEK_API_KEY 后重试。"

        payload = {
            "model": settings.deepseek_model,
            "messages": [
                {"role": "system", "content": "你是高校本科《冰冻圈科学概论》课程的虚拟助教。"},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        headers = {
            "Authorization": f"Bearer {settings.deepseek_api_key}",
            "Content-Type": "application/json",
        }
        url = f"{settings.deepseek_base_url.rstrip('/')}/chat/completions"

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
