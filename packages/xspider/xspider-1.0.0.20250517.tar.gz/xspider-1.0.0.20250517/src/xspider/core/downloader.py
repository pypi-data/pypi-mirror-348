import time
import random
import asyncio
import requests
from xspider.http.request import Request


class Downloader(object):
    def __init__(self):
        pass

    async def download(self, request: Request):
        return await self._download(request)

    async def _download(self, request: Request):
        # response = requests.get(request.url)
        # return response

        await asyncio.sleep(random.uniform(0, 1))
        return "<Response [200]>"
