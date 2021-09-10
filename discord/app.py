import base64
import json
import os
from typing import Dict

import boto3

from client.dwclient import DiscordWebhookClient

KMS_KEY = os.getenv("KMS_KEY")

kmsclient = boto3.client('kms')

dwclient = DiscordWebhookClient()


def read_discord_channel_map() -> Dict[str, str]:
    with open("webhookmap.json") as fp:
        return json.load(fp)


def decrypt_webhook_url(ciphertext: str) -> str:
    decoded_ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
    response = kmsclient.decrypt(
        CiphertextBlob=decoded_ciphertext,
        KeyId=KMS_KEY
    )
    return response["Plaintext"]


def lambda_handler(event, context=None):
    messages = [r["Sns"]["Message"] for r in event["Records"]]
    channel_map = read_discord_channel_map()

    for message in messages:
        channel, *rest = message.split(",")
        if channel not in channel_map:
            channel = "#debug"
        ciphertext = channel_map.get(channel)

        url = decrypt_webhook_url(ciphertext)
        dwclient.publish(url, ",".join(rest))
