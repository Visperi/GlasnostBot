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


from .message_properties import MessageEntity
from .user import User
from .types.checklist import (
    ChecklistTask as ChecklistTaskPayload,
    Checklist as ChecklistPayload
)


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