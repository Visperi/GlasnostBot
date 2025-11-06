from .types.reaction import (
    ReactionType as ReactionTypePayload,
    ReactionTypeEmoji as ReactionTypeEmojiPayload,
    ReactionTypeCustomEmoji as ReactionTypeCustomEmojiPayload,
    ReactionTypePaid as ReactionTypePaidPayload,
    ReactionCount as ReactionCountPayload
)


class ReactionType:

    __slots__ = (
        "type"
    )

    def __init__(self, payload: ReactionTypePayload):
        self.type = payload["type"]


class ReactionTypeEmoji(ReactionType):

    __slots__ = (
        "emoji"
    )

    def __init__(self, payload: ReactionTypeEmojiPayload):
        super().__init__(payload)
        self.emoji = payload["emoji"]


class ReactionTypeCustomEmoji(ReactionType):

    __slots__ = (
        "custom_emoji_id"
    )

    def __init__(self, payload: ReactionTypeCustomEmojiPayload):
        super().__init__(payload)
        self.custom_emoji_id = payload["custom_emoji_id"]


class ReactionTypePaid(ReactionType):

    def __init__(self, payload: ReactionTypePaidPayload):
        super().__init__(payload)


class ReactionCount:

    __slots__ = (
        "type",
        "total_count"
    )

    def __init__(self, payload: ReactionCountPayload):
        self.type = ReactionType(payload["type"])
        self.total_count = payload["total_count"]
