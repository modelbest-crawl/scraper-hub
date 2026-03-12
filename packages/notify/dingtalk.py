import base64
import hashlib
import hmac
import os
import time
from urllib.parse import urlencode

import httpx
from dotenv import load_dotenv

load_dotenv()


class DingTalkNotifier:
    def __init__(self, webhook: str | None = None, secret: str | None = None) -> None:
        self.webhook = webhook or os.getenv("DINGTALK_WEBHOOK", "")
        self.secret = secret or os.getenv("DINGTALK_SECRET", "")

    def _sign(self) -> str:
        if not self.secret:
            return ""
        timestamp = str(round(time.time() * 1000))
        string_to_sign = f"{timestamp}\n{self.secret}"
        sign = base64.b64encode(
            hmac.new(
                self.secret.encode("utf-8"),
                string_to_sign.encode("utf-8"),
                digestmod=hashlib.sha256,
            ).digest()
        ).decode("utf-8")
        return urlencode({"timestamp": timestamp, "sign": sign})

    def send(self, message: str) -> None:
        if not self.webhook:
            return
        url = self.webhook
        if self.secret:
            sep = "?" if "?" not in url else "&"
            url = f"{url}{sep}{self._sign()}"
        payload = {"msgtype": "text", "text": {"content": message}}
        httpx.post(url, json=payload)
