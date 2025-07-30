from xspider.types import Literal, Callable, Any


class Request(object):
    def __init__(
            self,
            url: str,
            /,
            *,
            callback: Callable[..., Any] | None = None,
            method: Literal["GET", "POST", "PUT", "DELETE"] = "GET",
            headers: dict[str, str] | None = None,
            body: bytes | str | None = None,
            cookies: dict[str, str] | None = None,
            priority: int = 0,
            proxy: dict[str, str] | None = None
    ):
        self.url = url
        self.callback = callback
        self.method = method
        self.headers = headers
        self.body = body
        self.cookies = cookies
        self.priority = priority
        self.proxy = proxy


__all__ = [
    "Request"
]
