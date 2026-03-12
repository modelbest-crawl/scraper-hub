import os

import httpx
from dotenv import load_dotenv

load_dotenv()


class WeChatNotifier:
    def __init__(self, webhook: str | None = None) -> None:
        self.webhook = webhook or os.getenv("WECHAT_WEBHOOK", "")

    def send(self, message: str) -> None:
        if not self.webhook:
            return
        payload = {"msgtype": "text", "text": {"content": message}}
        httpx.post(self.webhook, json=payload)

    def send_markdown(self, title: str, content: str) -> None:
        if not self.webhook:
            return
        body = f"# {title}\n\n{content}"
        payload = {"msgtype": "markdown", "markdown": {"content": body}}
        httpx.post(self.webhook, json=payload)
