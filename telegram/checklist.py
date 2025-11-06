from .types.checklist import (
    ChecklistTask as ChecklistTaskPayload,
    Checklist as ChecklistPayload,
    ChecklistTasksDone as ChecklistTasksDonePayload,
    ChecklistTasksAdded as ChecklistTasksAddedPayload
)
from .message import Message, MessageEntity
from .user import User


class ChecklistTask:

    __slots__ = (
        "id",
        "text",
        "text_entities",
        "completed_by_user",
        "completion_date"
    )

    def __init__(self, payload: ChecklistTaskPayload):
        self.id = payload["id"]
        self.text = payload["text"]
        self.text_entities = [MessageEntity(e) for e in payload.get("text_entities", [])]
        self.completion_date = payload.get("completion_date", -1)

        try:
            self.completed_by_user = User(payload["completed_by_user"])
        except KeyError:
            self.completed_by_user = None


class Checklist:

    __slots__ = (
        "title",
        "title_entities",
        "tasks",
        "others_can_add_tasks",
        "others_can_mark_tasks_as_done"
    )

    def __init__(self, payload: ChecklistPayload):
        self.title = payload["title"]
        self.title_entities = [MessageEntity(e) for e in payload.get("title_entities", [])]
        self.tasks = [ChecklistTask(t) for t in payload["tasks"]]
        self.others_can_add_tasks = payload.get("others_can_add_tasks", False)
        self.others_can_mark_tasks_as_done = payload.get("others_can_mark_tasks_as_done", False)


class ChecklistTasksDone:

    __slots__ = (
        "checklist_message",
        "marked_as_done_task_ids",
        "marked_as_not_done_task_ids"
    )

    def __init__(self, payload: ChecklistTasksDonePayload):
        self.marked_as_done_task_ids = payload.get("marked_as_done_task_ids", [])
        self.marked_as_not_done_task_ids = payload.get("marked_as_not_done_task_ids", [])

        try:
            self.checklist_message = Message(payload["checklist_message"])
        except KeyError:
            self.checklist_message = None


class ChecklistTasksAdded:

    __slots__ = (
        "checklist_message",
        "tasks"
    )

    def __init__(self, payload: ChecklistTasksAddedPayload):
        self.tasks = [ChecklistTask(t) for t in payload["tasks"]]

        try:
            self.checklist_message = Message(payload["checklist_message"])
        except KeyError:
            self.checklist_message = None
