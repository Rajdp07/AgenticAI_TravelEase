import os
import httpx


class NotifierService:
    def __init__(self):
        self.default_webhook = os.getenv("DEFAULT_NOTIFY_WEBHOOK_URL")

    def notify(self, message: str, webhook_url: str | None = None) -> None:
        url = webhook_url or self.default_webhook
        if url:
            try:
                httpx.post(url, json={"text": message}, timeout=5.0)
            except Exception:
                # Best-effort delivery; in production add retries and logging
                pass
        # Always print to console for observability
        print(f"[NOTIFY] {message}")

