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
