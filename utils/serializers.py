def serialize_httpurls(urls: str | list[str]) -> list[str] | str | None:
    """
    Serialize http urls to strings
    :param urls: urls to serialize (typically pydantic.HttpUrl)
    :return: list[str] | str
    """
    if isinstance(urls, list):
        return [str(url) for url in urls]
    return str(urls) if urls else None
