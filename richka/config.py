import richka

import logging

__VERSION = ("Alpha", 0, 0, 2)
USER_AGENT = f"Richka{__VERSION[0]}/{__VERSION[1]}.{__VERSION[2]}.{__VERSION[3]}"
HEADERS = {"user-agent": USER_AGENT}
COROUTINE_LIMIT = 10
SLICE_THRESHOLD = 10 # MiB
TIMEOUT = 30
RETRY_TIMES = 5
CHUNK_SIZE = 102400

logger = logging.getLogger("Richka Engine")

def set_user_agent(user_agent: str) -> None:
    """
    Set Public User Agent for HTTP Requests
    :param user_agent: String User-Agent you want to set.
    :return:
    """
    richka.USER_AGENT = user_agent
    richka.HEADERS["user-agent"] = user_agent

def set_headers(headers: dict) -> None:
    """
    Set Public Headers for HTTP Requests
    :param headers: Dictionary Headers you want to set.
    :return:
    """
    for key, value in headers.items():
        richka.HEADERS[key.lower()] = value

def set_coroutine_limit(coroutine_limit: int) -> None:
    """
    Set Coroutine Limit for HTTP Requests
    :param coroutine_limit: Integer Coroutine number limit.
    :return:
    """
    richka.COROUTINE_LIMIT = coroutine_limit

def set_slice_threshold(slice_threshold: int) -> None:
    """
    Set Slice Threshold for HTTP Requests
    :param slice_threshold: Integer Slice threshold to enable coroutine download.
    :return:
    """
    richka.SLICE_THRESHOLD = slice_threshold

def set_timeout(timeout: int) -> None:
    """
    Set Timeout for HTTP Requests
    :param timeout: Integer Timeout time in seconds.
    :return:
    """
    richka.TIMEOUT = timeout

def set_retry_times(retry_times: int) -> None:
    """
    Set Retry Times for HTTP Requests
    :param retry_times: Integer Allowed retry times.
    :return:
    """
    richka.RETRY_TIMES = retry_times
