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


from .chat import Chat
from .user import User
from .types.reaction import (
    ReactionType as ReactionTypePayload,
    ReactionTypeEmoji as ReactionTypeEmojiPayload,
    ReactionTypeCustomEmoji as ReactionTypeCustomEmojiPayload,
    ReactionTypePaid as ReactionTypePaidPayload,
    ReactionCount as ReactionCountPayload,
    MessageReactionUpdated as MessageReactionUpdatedPayload,
    MessageReactionCountUpdated as MessageReactionCountUpdatedPayload
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


class MessageReactionUpdated:

    __slots__ = (
        "chat",
        "message_id",
        "user",
        "actor_chat",
        "date",
        "old_reaction",
        "new_reaction"
    )

    def __init__(self, payload: MessageReactionUpdatedPayload):
        self.chat = Chat(payload["chat"])
        self.message_id = payload["message_id"]
        self.date = payload["date"]
        self.old_reaction = [ReactionType(r) for r in payload["old_reaction"]]
        self.new_reaction = [ReactionType(r) for r in payload["new_reaction"]]

        try:
            self.user = User(payload["user"])
        except KeyError:
            self.user = None

        try:
            self.actor_chat = Chat(payload["actor_chat"])
        except KeyError:
            self.actor_chat = None


class MessageReactionCountUpdated:

    __slots__ = (
        "chat",
        "message_id",
        "date",
        "reactions"
    )

    def __init__(self, payload: MessageReactionCountUpdatedPayload):
        self.chat = Chat(payload["chat"])
        self.message_id = payload["message_id"]
        self.date = payload["date"]
        self.reactions = [ReactionCount(r) for r in payload["reactions"]]
