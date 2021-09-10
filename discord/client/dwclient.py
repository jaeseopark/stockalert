import requests


class DiscordWebhookClient:
    def publish(self, url, message):
        assert isinstance(message, str)
        payload = {"content": message}
        requests.post(url, json=payload)
