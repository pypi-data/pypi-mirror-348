import time
import asyncio

import requests


class Downloader(object):
    def __init__(self):
        pass

    async def download(self, url: str):
        # response = requests.get(url)
        # print(response)

        await asyncio.sleep(0.1)
        print("<Response [200]>")
