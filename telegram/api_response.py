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
