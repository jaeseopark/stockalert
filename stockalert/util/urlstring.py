from urllib.parse import urlparse, parse_qs


def get_query_param(url: str, key: str) -> str:
    parsed_url = urlparse(url)
    qs = parse_qs(parsed_url.query).get(key)

    if qs is None:
        return None

    return qs[0]
