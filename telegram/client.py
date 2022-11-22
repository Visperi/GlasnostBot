"""
MIT License

Copyright (c) 2022 Niko Mätäsaho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import aiohttp
import asyncio
import logging
from .update import Update
from .utils import replace_builtin_keywords

_logger = logging.getLogger(__name__)


class TgMethod:
    """ Methods supported by Telegram API """

    getUpdates = "/getUpdates"


class Client:

    API_BASE_URL = "https://api.telegram.org/"

    def __init__(self, secret: str, client_session: aiohttp.ClientSession = None) -> None:
        self.__secret: str = secret
        self.__client_session: aiohttp.ClientSession = client_session
        self.loop = asyncio.new_event_loop()
        self.updates_offset = -1
        asyncio.set_event_loop(self.loop)

        if not self.__client_session:
            self.loop.run_until_complete(self.__init_session())

    async def __init_session(self) -> None:
        self.__client_session = aiohttp.ClientSession()

    def __build_url(self, method_path: str) -> str:
        return self.API_BASE_URL + f"bot{self.__secret}" + method_path

    async def __request(
            self,
            http_method: str,
            method_path: str,
            request_timeout: float = 10,
            params: dict = None,
            headers: dict = None
    ) -> dict:
        url = self.API_BASE_URL + f"bot{self.__secret}" + method_path
        async with self.__client_session.request(
                http_method,
                url,
                timeout=request_timeout,
                params=params,
                headers=headers
        ) as resp:
            content = await resp.json(encoding="utf-8")

            try:
                resp.raise_for_status()

            except aiohttp.ClientResponseError:
                error_code = content["error_code"]
                description = content["description"]
                _logger.exception(f"Error {error_code}: {description}")

            else:
                return content

    async def __get(
            self,
            method_path: str,
            request_timeout: int = 10,
            params: dict = None,
            headers: dict = None
    ) -> dict:
        return await self.__request("GET", method_path, request_timeout, params, headers)

    async def __post(
            self,
            method_path: str,
            request_timeout: int = 10,
            params: dict = None,
            headers: dict = None
    ) -> dict:
        return await self.__request("POST", method_path, request_timeout, params, headers)

    async def __get_updates_loop(self) -> None:
        _logger.info("Now long polling messages")

        while True:
            params = {"timeout": 200, "offset": self.updates_offset}
            resp = await self.__get(TgMethod.getUpdates, request_timeout=200, params=params)
            # TODO: Try-catch here in case of not-OK status
            results = replace_builtin_keywords(resp["result"])

            updates = [Update(u) for u in results]
            if updates:
                self.updates_offset = updates[-1].update_id + 1

            await asyncio.sleep(1)

    def start(self) -> None:
        if not self.__secret:
            raise ValueError("Secret is needed to connect to Telegram API.")

        try:
            self.loop.create_task(self.__get_updates_loop())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
