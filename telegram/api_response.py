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


from .types.api_response import ApiResponse as ApiResponsePayload
from .update import Update
from .utils import replace_dictionary_keys
from typing import Optional, List


class ApiResponse:

    __slots__ = (
        "_ok",
        "_result",
        "_error_code",
        "_description"
    )

    def __init__(self, payload: ApiResponsePayload):
        self._ok = payload["ok"]
        self._result = payload.get("result")
        self._error_code = payload.get("error_code", -1)
        self._description = payload.get("description")

        if self._result:
            self._result = [Update(replace_dictionary_keys(u)) for u in self._result]

    @property
    def ok(self) -> bool:
        return self._ok

    @property
    def result(self) -> Optional[List[Update]]:
        return self._result

    @property
    def error_code(self) -> int:
        return self._error_code

    @property
    def description(self) -> Optional[str]:
        return self._description
