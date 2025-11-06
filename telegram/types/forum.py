from typing_extensions import TypedDict, NotRequired


class ForumTopicCreated(TypedDict):
    name: str
    icon_color: int
    icon_custom_emoji_id: NotRequired[str]


class ForumTopicEdited(TypedDict):
    name: NotRequired[str]
    icon_custom_emoji_id: NotRequired[str]


# TODO: How to represent the 4 below empty classes properly?
class ForumTopicClosed(TypedDict):
    pass


class ForumTopicReopened(TypedDict):
    pass


class GeneralForumTopicHidden(TypedDict):
    pass


class GeneralForumTopicUnhidden(TypedDict):
    pass