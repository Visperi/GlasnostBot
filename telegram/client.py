"""
MIT License

Copyright (c) 2025 Niko Mätäsaho

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
from typing import (
    Coroutine,
    Any,
    Callable,
    Dict,
    List,
    TypeVar
)

_logger = logging.getLogger(__name__)
Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])


class _TgMethod:
    """ Methods supported by Telegram API """

    getUpdates = "/getUpdates"


class Client:
    """
    A class responsible for handling asynchronous connection to Telegram API.
    """

    API_BASE_URL = "https://api.telegram.org/"

    # noinspection PyTypeChecker
    def __init__(
            self,
            client_session: aiohttp.ClientSession = None,
            loop: asyncio.AbstractEventLoop = None
    ) -> None:
        """
        Initialize a new client for connection to the Telegram API. This client is then responsible for polling updates
        and invoking events based on the received data. Can either be attached to an existing client session and/or
        event loop, or initialized as is with new connections.

        :param client_session: An existing client session. If omitted, new one is automatically initialized.
        :param loop: An existing event loop where to attach to. If omitted, new one is automatically initialized.
        """
        self._secret: str = None
        self._client_session: aiohttp.ClientSession = client_session
        self.loop: asyncio.AbstractEventLoop = loop
        self.updates_offset: int = -1
        self.listeners: Dict[str, List[Coro]] = {}
        self.polling_task: asyncio.Task = None

        self._existing_loop = self.loop is not None
        if loop is None:
            _logger.debug("Creating new event loop")
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        if client_session is None:
            _logger.debug("Initializing new aiohttp.ClientSession")
            self.loop.run_until_complete(self._init_http_session())

    async def _init_http_session(self) -> None:
        """
        Initialize a new aiohttp.ClientSession used in connection for the API for the client.
        Automatically called if no session is given to the initializer.
        """
        self._client_session = aiohttp.ClientSession()

    async def _request(
            self,
            http_method: str,
            method_path: str,
            request_timeout: float = 10,
            params: dict = None,
            headers: dict = None
    ) -> ApiResponse:
        """
        Make an HTTP request to the Telegram API.

        :param http_method: HTTP method to send to the API.
        :param method_path: Path of the method in Telegram API.
        :param request_timeout: Timeout in seconds for the request itself.
        :param params: Params for the request.
        :param headers: Headers for the request.
        :return: The response object containing OK status and possible results, error codes etc.
        :exception ValueError: The HTTP method is not GET or POST and thus not supported by Telegram API.
        """
        if http_method != "GET" and http_method != "POST":
            raise ValueError("The Telegram API supports only GET and POST methods for HTTP requests.")

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
            request_timeout: float = 10,
            params: dict = None,
            headers: dict = None
    ) -> ApiResponse:
        """
        Shorthand method to make a GET request on Telegram API.

        :param method_path: Path of the API method.
        :param request_timeout: Timeout in seconds for the request itself.
        :param params: Params for the GET request.
        :param headers: Headers for the GET request.
        :return: The response object containing OK status and possible results, error codes etc.
        """
        return await self._request("GET", method_path, request_timeout, params, headers)

    async def _post(
            self,
            method_path: str,
            request_timeout: float = 10,
            params: dict = None,
            headers: dict = None
    ) -> ApiResponse:
        """
        Shorthand method to make a POST request on Telegram API.

        :param method_path: Path of the API method.
        :param request_timeout: Timeout in seconds for the request itself.
        :param params: Params for the POST request.
        :param headers: Headers for the POST request.
        :return: The response object containing OK status and possible results, error codes etc.
        """
        return await self._request("POST", method_path, request_timeout, params, headers)

    async def _get_updates_loop(self) -> None:
        """
        An infinite loop, using long polling to receive updates from the Telegram API. Handling the received
        data is then passed to on_update method.
        """
        _logger.info("Now long polling messages")

        while True:
            params = {"timeout": 200, "offset": self.updates_offset}
            resp = await self._get(_TgMethod.getUpdates, request_timeout=200, params=params)
            updates = resp.result

            if updates:
                await self.invoke_update_listeners(updates)
                latest = updates[-1]
                # Trigger all received messages read next time updates are received
                self.updates_offset = latest.update_id + 1

            await asyncio.sleep(1)

    async def invoke_update_listeners(self, updates: List[Update]) -> None:
        """
        Send updates to all registered event listeners.
        """
        listeners = self.listeners.get("on_update", [])
        _logger.debug(f"Invoking all {len(listeners)}+1 listeners for {len(updates)} updates.")
        for update in updates:
            await self.on_update(update)

            for listener in listeners:
                try:
                    await listener(update)
                except Exception as e:
                    _logger.error("Ignoring unexpected exception: ", exc_info=e)
                    break

    def add_listener(self, coroutine: Coro, event_name: str = None) -> Coro:
        """
        Add a listener to an event method. The amount of listeners per event is unlimited.

        :param coroutine: Coroutine function to call when the event occurs.
        :param event_name: Name of the event to listen. If omitted, the coroutine name is used and must match an event name.
        :return: The decorated function.
        :exception ValueError: The coroutine is not actually a coroutine function.
        """
        if not asyncio.iscoroutinefunction(coroutine):
            raise ValueError("Event listener must be a coroutine function.")
        if not event_name:
            event_name = coroutine.__name__

        try:
            self.listeners[event_name].append(coroutine)
        except KeyError:
            self.listeners[event_name] = []
            self.listeners[event_name].append(coroutine)

        _logger.debug(f"Registered listener for event '{event_name}'")
        return coroutine

    def event(self, coroutine: Coro) -> Coro:
        """
        Shorthand, decorator method for adding a listener to event listener.

        :param coroutine: Coroutine to add the listener for
        :return:
        """
        return self.add_listener(coroutine)

    async def on_update(self, update: Update) -> None:
        """
        Method called when an Update is received from Telegram API. When overridden, nothing is done to this data
        before or after this method is called.

        :param update: Update object received from the Telegram API
        """
        # TODO: Handle commands, messages, more granular objects etc. here by default
        pass

    def start(self, secret: str) -> None:
        """
        Connect to the Telegram API and start polling Telegram Updates and invoking related events.

        :param secret: Secret to the Telegram API.
        """
        if not secret:
            raise ValueError("Secret is needed to connect to Telegram API.")
        if self.polling_task is not None:
            raise ValueError("Already connected to Telegram API.")
        self._secret = secret

        try:
            self.polling_task = self.loop.create_task(self._get_updates_loop())
            if not self._existing_loop:
                _logger.debug("Starting the event listeners.")
                self.loop.run_forever()
        except KeyboardInterrupt:
            pass

    def stop(self):
        if self.polling_task is None:
            raise ValueError("There is no connection to Telegram api.")

        self.polling_task.cancel()
        self.polling_task = None
