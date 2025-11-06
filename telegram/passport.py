from .types.passport import (
    PassportFile as PassportFilePayload,
    EncryptedPassportElement as EncryptedPassportElementPayload,
    EncryptedCredentials as EncryptedCredentialsPayload,
    PassportData as PassportDataPayload
)


class PassportFile:

    __slots__ = (
        "file_id",
        "file_unique_id",
        "file_size",
        "file_date"
    )

    def __init__(self, payload: PassportFilePayload):
        self.file_id = payload["file_id"]
        self.file_unique_id = payload["file_unique_id"]
        self.file_size = payload["file_size"]
        self.file_date = payload["file_date"]


class EncryptedPassportElement:

    __slots__ = (
        "type",
        "data",
        "phone_number",
        "email",
        "files",
        "front_side",
        "reverse_side",
        "selfie",
        "translation",
        "hash"
    )

    def __init__(self, payload: EncryptedPassportElementPayload):
        self.type = payload["type"]
        self.data = payload.get("data")
        self.phone_number = payload.get("phone_number")
        self.email = payload.get("email")
        self.files = [PassportFile(p) for p in payload.get("files", [])]
        self.translation = [PassportFile(p) for p in payload.get("translation", [])]
        self.hash = payload["hash"]

        try:
            self.front_side = PassportFile(payload["front_side"])
        except KeyError:
            self.front_side = None

        try:
            self.reverse_side = PassportFile(payload["reverse_side"])
        except KeyError:
            self.reverse_side = None

        try:
            self.selfie = PassportFile(payload["selfie"])
        except KeyError:
            self.selfie = None


class EncryptedCredentials:

    __slots__ = (
        "data",
        "hash",
        "secret"
    )

    def __init__(self, payload: EncryptedCredentialsPayload):
        self.data = payload["data"]
        self.hash = payload["hash"]
        self.secret = payload["secret"]


class PassportData:

    __slots__ = (
        "data",
        "credentials"
    )

    def __init__(self, payload: PassportDataPayload):
        self.data = [EncryptedPassportElement(e) for e in payload["data"]]
        self.credentials = EncryptedCredentials(payload["credentials"])
