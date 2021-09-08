import logging

import requests

logger = logging.getLogger(__name__)

BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"


def get_public_ip():
    return requests.get('https://api.ipify.org', timeout=1).text


def log_public_ip():
    try:
        ip = get_public_ip()
        logger.info(f"public_ip={ip}")
    except:
        logger.info("failed to get public ip")
