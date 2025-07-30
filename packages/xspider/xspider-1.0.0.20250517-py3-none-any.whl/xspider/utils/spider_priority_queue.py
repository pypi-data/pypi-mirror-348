from asyncio import PriorityQueue, wait_for, TimeoutError

from xspider.types import Any


class SpiderPriorityQueue(PriorityQueue):
    def __init__(self, maxsize: int = 0):
        super(SpiderPriorityQueue, self).__init__(maxsize=maxsize)

    async def get(self) -> Any | None:
        fut = super().get()
        try:
            return await wait_for(fut, timeout=0.1)
        except TimeoutError:
            return None
