import base64
import json
import os

import boto3

from client.dwclient import DiscordWebhookClient

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
KMS_KEY = os.getenv("KMS_KEY")

kmsclient = boto3.client('kms')

dwclient = DiscordWebhookClient()


def decrypt_webhook_url():
    ciphertext = base64.b64decode(DISCORD_WEBHOOK_URL.encode('utf-8'))
    response = kmsclient.decrypt(
        CiphertextBlob=ciphertext,
        KeyId=KMS_KEY
    )
    return response["Plaintext"]


def to_messages(event):
    return [json.loads(r["body"])["Message"] for r in event["Records"]]


def lambda_handler(event, context=None):
    messages = to_messages(event)

    url = decrypt_webhook_url()

    for message in messages:
        dwclient.publish(url, message)
