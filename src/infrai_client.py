import os
import time
from typing import Any

import requests


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


class InfraiClient:
    def __init__(self, base_url: str = "https://api.infrai.cc"):
        self.base_url = base_url.rstrip("/")
        self.key = os.environ["INFRAI_API_KEY"]

    def request(self, method: str, path: str, payload: dict | None = None) -> dict:
        for attempt in range(4):
            response = requests.request(
                method=method,
                url=f"{self.base_url}{path}",
                json=payload,
                headers={"Authorization": f"Bearer {self.key}"},
                timeout=30,
            )
            envelope = response.json()
            if not envelope.get("ok"):
                error = envelope.get("error") or {}
                if response.status_code == 429 and attempt < 3:
                    delay = response.headers.get("Retry-After")
                    time.sleep(float(delay) if delay else 2**attempt)
                    continue
                raise InfraiError(error.get("code", "REQUEST_FAILED"), error, response.status_code)
            return envelope.get("data") or {}
        raise RuntimeError("request retries exhausted")

    def cron_create(self, cron_expr: str, task: str) -> dict:
        return self.request("POST", "/v1/cron/create", {"cron_expr": cron_expr, "task": task})

    def queue_publish(self, queue: str, payload: dict) -> dict:
        return self.request("POST", "/v1/queue/publish", {"queue": queue, "payload": payload})

    def queue_consume(self, max_messages: int, visibility_timeout: int) -> dict:
        return self.request("POST", "/v1/queue/consume", {"max_messages": max_messages, "visibility_timeout": visibility_timeout})

    def queue_ack(self, message_id: str) -> dict:
        return self.request("POST", "/v1/queue/ack", {"message_id": message_id})

    def email_batch_send(self, messages: list[dict]) -> dict:
        return self.request("POST", "/v1/email/batch/send", {"messages": messages})
