import httpx
from typing import Optional


class SlackNotifier:
    def __init__(
        self,
        webhook_url: str,
        default_channel: Optional[str] = None,
        default_username: Optional[str] = None,
    ):
        self.webhook_url = webhook_url
        self.default_channel = default_channel
        self.default_username = default_username

    async def send_message(
        self,
        text: str,
        channel: Optional[str] = None,
        username: Optional[str] = None,
    ):
        payload = {"text": text}

        if channel or self.default_channel:
            payload["channel"] = channel or self.default_channel

        if username or self.default_username:
            payload["username"] = username or self.default_username

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.webhook_url, json=payload)
                response.raise_for_status()
        except Exception as e:
            print(f"[SlackNotifier] Errore durante l'invio del messaggio: {e}")
