import httpx

from app.core.config import settings


class DeepSeekError(RuntimeError):
    pass


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
        timeout = httpx.Timeout(connect=10.0, read=180.0, write=30.0, pool=10.0)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except httpx.TimeoutException as exc:
            raise DeepSeekError("DeepSeek API 响应超时") from exc
        except httpx.HTTPStatusError as exc:
            raise DeepSeekError(f"DeepSeek API 返回异常状态：{exc.response.status_code}") from exc
        except (httpx.HTTPError, KeyError, IndexError, TypeError) as exc:
            raise DeepSeekError("DeepSeek API 调用失败") from exc
