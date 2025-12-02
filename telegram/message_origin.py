from typing import Union
from .chat import Chat
from .user import User
from .types.message_origin import (
    MessageOrigin as MessageOriginPayload,
    MessageOriginUser as MessageOriginUserPayload,
    MessageOriginHiddenUser as MessageOriginHiddenUserPayload,
    MessageOriginChat as MessageOriginChatPayload,
    MessageOriginChannel as MessageOriginChannelPayload
)


class MessageOrigin:

    __slots__ = (
        "type",
        "date"
    )

    def __init__(self, payload: MessageOriginPayload):
        self.type = payload["type"]
        self.date = payload["date"]

    @property
    def sender(self) -> Union[User, str, Chat]:
        """
        :return: Original sender for the message. The origin type is ``telegram.User`` for messages originally sent by a
                 known users, or ``Chat`` for messages in channel chats and messages sent behalf of chat into groups.
                 For unknown users the origin is their Telegram username as a string.
        :raises ValueError: If the origin type is unknown and correct origin attribute cannot be fetched.
        """
        if isinstance(self, MessageOriginUser):
            return self.sender_user
        elif isinstance(self, MessageOriginHiddenUser):
            return self.sender_user_name
        elif isinstance(self, MessageOriginChat):
            return self.sender_chat
        elif isinstance(self, MessageOriginChannel):
            return self.chat
        else:
            raise ValueError(f"Unknown MessageOrigin instance type: {type(self)}")


class MessageOriginUser(MessageOrigin):

    __slots__ = (
        "sender_user"
    )

    def __init__(self, payload: MessageOriginUserPayload):
        super().__init__(payload)
        self.sender_user = User(payload["sender_user"])


class MessageOriginHiddenUser(MessageOrigin):

    __slots__ = (
        "sender_user_name"
    )

    def __init__(self, payload: MessageOriginHiddenUserPayload):
        super().__init__(payload)
        self.sender_user_name = payload["sender_user_name"]


class MessageOriginChat(MessageOrigin):

    __slots__ = (
        "sender_chat",
        "author_signature"
    )

    def __init__(self, payload: MessageOriginChatPayload):
        super().__init__(payload)
        self.sender_chat = Chat(payload["sender_chat"])
        self.author_signature = payload.get("author_signature")


class MessageOriginChannel(MessageOrigin):

    __slots__ = (
        "chat",
        "message_id",
        "author_signature"
    )

    def __init__(self, payload: MessageOriginChannelPayload):
        super().__init__(payload)
        self.chat = Chat(payload["chat"])
        self.message_id = payload["message_id"]
        self.author_signature = payload.get("author_signature")
