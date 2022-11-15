from .types.contact import Contact as ContactPayload


class Contact:

    __slots__ = (
        "phone_number",
        "first_name",
        "last_name",
        "user_id",
        "vcard"
    )

    def __init__(self, payload: ContactPayload):
        self.__update(payload)

    def __update(self, payload: ContactPayload):
        self.phone_number = payload["phone_number"]
        self.first_name = payload["first_name"]
        self.last_name = payload.get("last_name")
        self.user_id = payload.get("user_id", -1)
        self.vcard = payload.get("vcard")
