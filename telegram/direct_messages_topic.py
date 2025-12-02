from .user import User
from .types.direct_messages_topic import DirectMessagesTopic as DirectMessagesTopicPayload


class DirectMessagesTopic:

    __slots__ = (
        "topic_id",
        "user"
    )

    def __init__(self, payload: DirectMessagesTopicPayload):
        self.topic_id = payload["topic_id"]

        try:
            self.user = User(payload["user"])
        except KeyError:
            self.user = None
