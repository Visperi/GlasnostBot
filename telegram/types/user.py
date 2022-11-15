from typing_extensions import TypedDict, NotRequired


class User(TypedDict):
    id: int
    is_bot: bool
    first_name: str
    last_name: NotRequired[str]
    username: NotRequired[str]
    language_code: NotRequired[str]
    is_premium: NotRequired[bool]
    added_to_attachment_menu: NotRequired[bool]
    can_join_groups: NotRequired[bool]
    can_read_all_group_messages: NotRequired[bool]
    supports_inline_queries: NotRequired[bool]
