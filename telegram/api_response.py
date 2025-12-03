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


from typing import Optional, Union, List

from .types.api_response import (
    ApiResponseBase as ApiResponseBasePayload
)
from .update import Update
from .media import File
from .utils import replace_dictionary_keys


class ApiResponseBase:
    """
    A generic base class for Telegram API responses. Contains an OK status for requests, and on error also the error
    code and error description. All child classes must implement method ``finalize`` to convert the result attribute
    to objects.
    """

    __slots__ = (
        "_ok",
        "_result",
        "_error_code",
        "_description"
    )

    def __init__(self, payload: ApiResponseBasePayload):
        self._ok = payload["ok"]
        self._result = payload.get("result")
        self._error_code = payload.get("error_code")
        self._description = payload.get("description")

        self.finalize()

    def finalize(self) -> None:
        """
        Finalize the result field into valid Telegram object(s).
        """
        raise NotImplementedError(f"Finalize method not implemented in API response class {self.__class__.__name__}")

    @property
    def ok(self) -> bool:
        """
        True if an API request was successful, False otherwise.
        """
        return self._ok

    @property
    def result(self) -> Union[List[Update], File]:
        """
        Data returned by the Telegram API on successful requests.
        """
        return self._result

    @property
    def error_code(self) -> Optional[int]:
        """
        Error code on unsuccessful API requests.
        """
        return self._error_code

    @property
    def description(self) -> Optional[str]:
        """
        Description of the error on unsuccessful requests.
        """
        return self._description


class ApiResponse(ApiResponseBase):
    """
    An API response for Telegram updates.
    """

    def finalize(self):
        if self._result is not None:
            self._result = [Update(replace_dictionary_keys(u)) for u in self._result]


class FileQueryResult(ApiResponseBase):
    """
    An API response for file queries.
    """

    def finalize(self):
        if self._result is not None:
            self._result = File(self._result)
