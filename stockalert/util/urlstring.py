from urllib.parse import urlparse, parse_qs


def get_query_param(url: str, key: str) -> str:
    """
    Extracts the query param.

    Example:
      get_query_param("https://apple.ca?mykey=myvalue", "mykey"), will return "myvalue"

    :param url: URL, including the query params
    :param key: Name of the param
    :return: Value of the param. Only the first will be returned if there are multiple values.
    """
    parsed_url = urlparse(url)
    qs = parse_qs(parsed_url.query).get(key)

    if qs is None:
        return None

    return qs[0]
