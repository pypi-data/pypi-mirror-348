from asyncio import create_task

from xspider.spider import Spider
from xspider.http.request import Request
from xspider.core.scheduler import Scheduler
from xspider.core.downloader import Downloader
from xspider.utils.project import transform
from xspider.types import Iterator, Callable, iscoroutine


class Engine(object):
    def __init__(self):
        self.scheduler: Scheduler | None = None
        self.downloader: Downloader | None = None
        self.spider: Spider | None = None

        self.start_requests: Iterator[str] | None = None

    async def start_spider(self, spider: Spider):
        self.scheduler = Scheduler()
        if hasattr(self.scheduler, "open"):
            self.scheduler.open()
        self.downloader = Downloader()
        self.spider = spider

        self.start_requests = iter(spider.start_requests())

        await self._open_spider()

    async def _open_spider(self):
        crawling = create_task(self.crawl())
        await crawling

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
        # todo: 处理去重
        await self.scheduler.enqueue_request(request)

    async def _get_dequeue_request(self):
        return await self.scheduler.dequeue_request()

    async def _crawl(self, request):
        # todo: 处理并发
        outputs = await self._fetch(request)
        if outputs:
            async for output in outputs:
                print(output)

    async def _fetch(self, request: Request):
        async def success(response):
            callback: Callable = request.callback or self.spider.parse

            # type(callback(response))
            # <class 'generator'>
            # <class 'async_generator'>
            # <class 'NoneType'>

            if outputs := callback(response):
                if iscoroutine(outputs):
                    await outputs
                else:
                    return transform(outputs)

        resp = await self.downloader.download(request)
        outs = await success(resp)
        return outs
