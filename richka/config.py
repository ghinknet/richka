import richka

__VERSION = ("Alpha", 0, 0, 1)
USER_AGENT = f"Richka{__VERSION[0]}/{__VERSION[1]}.{__VERSION[2]}.{__VERSION[3]}"
HEADERS = {"user-agent": USER_AGENT}

def set_user_agent(user_agent: str) -> None:
    richka.USER_AGENT = user_agent
    richka.HEADERS["user-agent"] = user_agent

def set_headers(headers: dict) -> None:
    for key, value in headers.items():
        richka.HEADERS[key.lower()] = value