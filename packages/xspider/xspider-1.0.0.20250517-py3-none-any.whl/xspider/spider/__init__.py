from xspider.http.request import Request
from xspider.types import is_str, is_list_of


class Spider(object):
    start_url: str | None = None
    start_urls: list[str] | None = None

    def __init__(self):
        pass

    def start_requests(self):
        if is_str(url := self.start_url):
            yield Request(url)
        if is_list_of(urls := self.start_urls, str):
            for url in urls:
                yield Request(url)

    def parse(self, response):
        raise NotImplementedError("必须实现 parse 方法！")


__all__ = [
    "Spider"
]
