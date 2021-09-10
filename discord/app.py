import base64
import json
import os
from typing import Dict, Tuple

import boto3

from client.dwclient import DiscordWebhookClient

KMS_KEY = os.getenv("KMS_KEY")
CHANNEL_MAP = dict()

kmsclient = boto3.client('kms')
dwclient = DiscordWebhookClient()


def read_discord_channel_map() -> Dict[str, str]:
    with open("webhookmap.json") as fp:
        return json.load(fp)


def parse(org_message: str) -> Tuple[str, str]:
    channel, *rest = org_message.split(",")
    if channel not in CHANNEL_MAP:
        channel = "#debug"
    return channel, ",".join(rest).strip()


def decrypt_webhook_url(ciphertext: str) -> str:
    decoded_ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
    response = kmsclient.decrypt(
        CiphertextBlob=decoded_ciphertext,
        KeyId=KMS_KEY
    )
    return response["Plaintext"]


def lambda_handler(event, context=None):
    messages = [r["Sns"]["Message"] for r in event["Records"]]
    CHANNEL_MAP.update(read_discord_channel_map())

    for message in messages:
        channel_name, parsed_message = parse(message)
        url_plaintext = decrypt_webhook_url(CHANNEL_MAP.get(channel_name))
        dwclient.publish(url_plaintext, parsed_message)
