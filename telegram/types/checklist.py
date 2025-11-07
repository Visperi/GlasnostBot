from typing import List

from typing_extensions import TypedDict, NotRequired

from .message_entity import MessageEntity
from .user import User


# TODO: Move
class ChecklistTask(TypedDict):
    id: int
    text: str
    text_entities: NotRequired[List[MessageEntity]]
    completed_by_user: NotRequired[User]
    completion_date: NotRequired[int]


# TODO: Move
class Checklist(TypedDict):
    title: str
    title_entities: NotRequired[List[MessageEntity]]
    tasks: List[ChecklistTask]
    others_can_add_tasks: NotRequired[bool]
    others_can_mark_tasks_as_done: NotRequired[bool]
