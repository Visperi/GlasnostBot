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
from .api_response import ApiResponse
from .update import Update
from typing import Coroutine

_logger = logging.getLogger(__name__)


class _TgMethod:
    """ Methods supported by Telegram API """

    getUpdates = "/getUpdates"


class Client:

    API_BASE_URL = "https://api.telegram.org/"

    def __init__(self, secret: str, client_session: aiohttp.ClientSession = None) -> None:
        self._secret: str = secret
        self._client_session: aiohttp.ClientSession = client_session
        self.loop = asyncio.new_event_loop()
        self.updates_offset = -1
        self.listeners = {}
        asyncio.set_event_loop(self.loop)

        if not self._client_session:
            self.loop.run_until_complete(self._init_session())

    async def _init_session(self) -> None:
        self._client_session = aiohttp.ClientSession()

    def __build_url(self, method_path: str) -> str:
        return self.API_BASE_URL + f"bot{self._secret}" + method_path

    async def _request(
            self,
            http_method: str,
            method_path: str,
            request_timeout: float = 10,
            params: dict = None,
            headers: dict = None
    ) -> ApiResponse:
        url = self.API_BASE_URL + f"bot{self._secret}" + method_path
        async with self._client_session.request(
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

            return ApiResponse(content)

    async def _get(
            self,
            method_path: str,
            request_timeout: int = 10,
            params: dict = None,
            headers: dict = None
    ) -> ApiResponse:
        return await self._request("GET", method_path, request_timeout, params, headers)

    async def _post(
            self,
            method_path: str,
            request_timeout: int = 10,
            params: dict = None,
            headers: dict = None
    ) -> ApiResponse:
        return await self._request("POST", method_path, request_timeout, params, headers)

    async def _get_updates_loop(self) -> None:
        _logger.info("Now long polling messages")

        while True:
            params = {"timeout": 200, "offset": self.updates_offset}
            resp = await self._get(_TgMethod.getUpdates, request_timeout=200, params=params)
            # TODO: Do something here with non-OK response?

            if resp.result:
                latest = resp.result[-1]
                # Trigger all received messages read next time updates are received
                self.updates_offset = latest.update_id + 1

                for listener in self.listeners.get("on_update", []):
                    await listener(latest)

                await self.on_update(latest)

            await asyncio.sleep(1)

    def event(self, coroutine: Coroutine) -> Coroutine:
        if not asyncio.iscoroutinefunction(coroutine):
            raise ValueError("Event listener must be a coroutine function.")

        try:
            self.listeners[coroutine.__name__].append(coroutine)
        except KeyError:
            self.listeners[coroutine.__name__] = []
            self.listeners[coroutine.__name__].append(coroutine)

        _logger.debug(f"Registered listener for event '{coroutine.__name__}'")
        return coroutine

    async def on_update(self, update: Update):
        pass

    def start(self) -> None:
        if not self._secret:
            raise ValueError("Secret is needed to connect to Telegram API.")

        try:
            self.loop.create_task(self._get_updates_loop())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
