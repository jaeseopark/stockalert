import requests


class DiscordWebhookClient:
    def publish(self, url, message):
        assert isinstance(message, str)
        payload = {"content": message.strip()}
        requests.post(url, json=payload)
