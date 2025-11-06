from typing_extensions import TypedDict


class ReactionType(TypedDict):
    type: str


class ReactionTypeEmoji(ReactionType):
    emoji: str


class ReactionTypeCustomEmoji(ReactionType):
    custom_emoji_id: str


class ReactionTypePaid(ReactionType):
    pass


class ReactionCount(TypedDict):
    type: ReactionType
    total_count: int
