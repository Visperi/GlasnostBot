from .types.user import User as UserPayload


class User:

    __slots__ = (
        "id",
        "is_bot",
        "first_name",
        "last_name",
        "username",
        "language_code",
        "is_premium",
        "added_to_attachment_menu",
        "can_join_groups",
        "can_read_all_group_messages",
        "supports_inline_queries"
    )

    def __init__(self, payload: UserPayload) -> None:
        self.__update(payload)

    def __update(self, payload: UserPayload) -> None:
        self.id = payload["id"]
        self.is_bot = payload["is_bot"]
        self.first_name = payload["first_name"]
        self.last_name = payload.get("last_name")
        self.username = payload.get("username")
        self.language_code = payload.get("language_code")
        self.is_premium = payload.get("is_premium", False)
        self.added_to_attachment_menu = payload.get("added_to_attachment_menu", False)
        self.can_join_groups = payload.get("can_join_groups", False)
        self.can_read_all_group_messages = payload.get("can_read_all_group_messages", False)
        self.supports_inline_queries = payload.get("supports_inline_queries", False)
