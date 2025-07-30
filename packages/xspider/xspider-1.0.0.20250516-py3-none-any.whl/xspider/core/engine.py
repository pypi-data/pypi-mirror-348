from xspider.spider import Spider
from xspider.core.scheduler import Scheduler
from xspider.core.downloader import Downloader
from xspider.types import Iterator


class Engine(object):
    def __init__(self):
        self.scheduler: Scheduler | None = None
        self.downloader: Downloader | None = None

        self.start_requests: Iterator[str] | None = None

    async def start_spider(self, spider: Spider):
        self.scheduler = Scheduler()
        if hasattr(self.scheduler, "open"):
            self.scheduler.open()
        self.downloader = Downloader()

        self.start_requests = iter(spider.start_requests())

        await self.crawl()

    async def crawl(self):
        while True:
            if (request := await self._get_dequeue_request()) is not None:
                await self._crawl(request)
            else:
                try:
                    start_request = next(self.start_requests)  # noqa
                except StopIteration:
                    self.start_requests = None
                except Exception as e:
                    break
                else:
                    await self.enqueue_request(start_request)

    async def enqueue_request(self, request):
        await self._schedule_request(request)

    async def _schedule_request(self, request):
        # todo: 去重
        await self.scheduler.enqueue_request(request)

    async def _get_dequeue_request(self):
        return await self.scheduler.dequeue_request()

    async def _crawl(self, request):
        await self.downloader.download(request)
