from typing import List

from typing_extensions import NotRequired, TypedDict

from .message import Message, MessageEntity
from .user import User


class ChecklistTask(TypedDict):
    id: int
    text: str
    text_entities: NotRequired[List[MessageEntity]]
    completed_by_user: NotRequired[User]
    completion_date: NotRequired[int]


class Checklist(TypedDict):
    title: str
    title_entities: NotRequired[List[MessageEntity]]
    tasks: List[ChecklistTask]
    others_can_add_tasks: NotRequired[bool]
    others_can_mark_tasks_as_done: NotRequired[bool]


class ChecklistTasksDone(TypedDict):
    checklist_message: NotRequired[Message]
    marked_as_done_task_ids: NotRequired[List[int]]
    marked_as_not_done_task_ids: NotRequired[List[int]]


class ChecklistTasksAdded(TypedDict):
    checklist_message: NotRequired[Message]
    tasks: List[ChecklistTask]
