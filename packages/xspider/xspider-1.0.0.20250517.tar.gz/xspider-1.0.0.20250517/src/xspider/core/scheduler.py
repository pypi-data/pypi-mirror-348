from xspider.utils.spider_priority_queue import SpiderPriorityQueue


class Scheduler(object):
    def __init__(self):
        self.request_queue: SpiderPriorityQueue | None = None

    def open(self):
        self.request_queue = SpiderPriorityQueue()

    async def enqueue_request(self, request):
        await self.request_queue.put(request)

    async def dequeue_request(self):
        return await self.request_queue.get()
