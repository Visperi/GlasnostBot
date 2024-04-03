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

from typing import Optional, List, Union

from .types.api_response import (
    ApiResponse as ApiResponsePayload,
    FileQueryResult as FileQueryResultPayload
)
from .api_helpers import API_BASE_URL
from .update import Update
from .utils import replace_dictionary_keys


class FileQueryResult:

    def __init__(self, payload: FileQueryResultPayload):
        self.file_id = payload["file_id"]
        self.file_unique_id = payload["file_unique_id"]
        self.file_size = payload["file_size"]
        self.file_path = payload["file_path"]

    def build_download_url(self, bot_token: str) -> str:
        """
        Build download url for the queried file.

        :param bot_token: Bot token without the 'bot' prefix. Needed to access the API.
        :return: Complete url to download the file.
        """
        return f"{API_BASE_URL}/file/bot{bot_token}/{self.file_path}"


class ApiResponse:
    """
    A class that represents Telegram API responses in a high level. This class wraps either error details
    for unsuccessful API requests, or list of Update objects for successful API requests, and may not
    necessarily really be that interesting for receiving clients by itself. Mostly for internal use.
    """

    __slots__ = (
        "_ok",
        "_result",
        "_error_code",
        "_description"
    )

    def __init__(self, payload: ApiResponsePayload):
        """
        Initialize a nwe instance of ApiResponse.

        :param payload: Payload from the Telegram API. This object is automatically fetched into more useful
        properties for later usage.
        """
        self._ok = payload["ok"]
        self._result = payload.get("result")
        self._error_code = payload.get("error_code", -1)
        self._description = payload.get("description")

        if self._result:
            self.fetch_result()

    def fetch_result(self):
        # TODO: What other types of results are there to support?
        if isinstance(self._result, list):
            # Replace possible keys reserved in python for keywords with placeholder values
            self._result = [Update(replace_dictionary_keys(update)) for update in self._result]
        else:
            self._result = FileQueryResult(self._result)  # noqa

    @property
    def ok(self) -> bool:
        """
        True if the API request is successful and contains valid results.
        """
        return self._ok

    @property
    def result(self) -> Optional[Union[List[Update], FileQueryResult]]:
        """
        List of Update objects if the API request was successful.
        """
        return self._result

    @property
    def error_code(self) -> int:
        """
        Error code when the request was not successful. Has value of -1 for successful requests.
        """
        return self._error_code

    @property
    def description(self) -> Optional[str]:
        """
        Error description when the request is not successful. Has value of None for successful requests.
        """
        return self._description
