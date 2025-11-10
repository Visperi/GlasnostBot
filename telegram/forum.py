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


from .types.forum import (
    ForumTopicCreated as ForumTopicCreatedPayload,
    ForumTopicEdited as ForumTopicEditedPayload,
    ForumTopicClosed as ForumTopicClosedPayload,
    ForumTopicReopened as ForumTopicReopenedPayload,
    GeneralForumTopicHidden as GeneralForumTopicHiddenPayload,
    GeneralForumTopicUnhidden as GeneralForumTopicUnhiddenPayload
)


class ForumTopicCreated:

    __slots__ = (
        "name",
        "icon_color",
        "icon_custom_emoji_id"
    )

    def __init__(self, payload: ForumTopicCreatedPayload):
        self.name = payload["name"]
        self.icon_color = payload["icon_color"]
        self.icon_custom_emoji_id = payload.get("icon_custom_emoji_id")


class ForumTopicEdited:
    __slots__ = (
        "name",
        "icon_custom_emoji_id"
    )

    def __init__(self, payload: ForumTopicEditedPayload):
        self.name = payload.get("name")
        self.icon_custom_emoji_id = payload.get("icon_custom_emoji_id")


class ForumTopicClosed:

    def __init__(self, payload: ForumTopicClosedPayload):
        pass


class ForumTopicReopened:

    def __init__(self, payload: ForumTopicReopenedPayload):
        pass


class GeneralForumTopicHidden:

    def __init__(self, payload: GeneralForumTopicHiddenPayload):
        pass


class GeneralForumTopicUnhidden:

    def __init__(self, payload: GeneralForumTopicUnhiddenPayload):
        pass
