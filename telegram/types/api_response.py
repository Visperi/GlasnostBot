from typing_extensions import TypedDict, NotRequired
from typing import List
from .update import Update


class ApiResponse(TypedDict):

    ok: bool
    result: NotRequired[List[Update]]
    error_code: NotRequired[int]
    description: NotRequired[str]
