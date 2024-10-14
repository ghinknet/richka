import richka

import logging

__VERSION = ("Alpha", 0, 0, 1)
USER_AGENT = f"Richka{__VERSION[0]}/{__VERSION[1]}.{__VERSION[2]}.{__VERSION[3]}"
HEADERS = {"user-agent": USER_AGENT}
COROUTINE_LIMIT = 10
SLICE_THRESHOLD = 10 # MiB

logger = logging.getLogger("Richka Engine")

def set_user_agent(user_agent: str) -> None:
    """
    Set Public User Agent for HTTP Requests
    :param user_agent: String
    :return:
    """
    richka.USER_AGENT = user_agent
    richka.HEADERS["user-agent"] = user_agent

def set_headers(headers: dict) -> None:
    """
    Set Public Headers for HTTP Requests
    :param headers: Dictionary
    :return:
    """
    for key, value in headers.items():
        richka.HEADERS[key.lower()] = value

def set_coroutine_limit(coroutine_limit: int) -> None:
    """
    Set Coroutine Limit for HTTP Requests
    :param coroutine_limit: Integer
    :return:
    """
    richka.COROUTINE_LIMIT = coroutine_limit

def set_slice_threshold(slice_threshold: int) -> None:
    """
    Set Slice Threshold for HTTP Requests
    :param slice_threshold: Integer
    :return:
    """
    richka.SLICE_THRESHOLD = slice_threshold
