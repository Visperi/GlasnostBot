from typing_extensions import TypedDict, NotRequired


class Contact(TypedDict):
    phone_number: str
    first_name: str
    last_name: NotRequired[str]
    user_id: NotRequired[int]
    vcard: NotRequired[str]
