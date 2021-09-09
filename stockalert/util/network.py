import logging

import requests

logger = logging.getLogger(__name__)


def get_public_ip():
    return requests.get('https://api.ipify.org', timeout=1).text


def log_public_ip():
    try:
        ip = get_public_ip()
        logger.info(f"public_ip={ip}")
    except:
        logger.info("failed to get public ip")
