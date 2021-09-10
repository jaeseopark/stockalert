"""
Windows equiv:
  aws kms encrypt --profile {PROFILE} --key-id {ARN} --plaintext fileb://plaintext.txt --output text --query CiphertextBlob
"""

import base64

import boto3

KMS_KEY = "arn:aws:kms:.../..."
plaintext = '...'.encode('utf-8')

kmsclient = boto3.client('kms')

if __name__ == '__main__':
    response = kmsclient.encrypt(
        KeyId=KMS_KEY,
        Plaintext=plaintext
    )

    ciphertext = response['CiphertextBlob']
    ciphertext_b64_str = base64.b64encode(ciphertext).decode('utf-8')

    print(ciphertext_b64_str)
