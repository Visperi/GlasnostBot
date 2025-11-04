from typing import TypedDict, List, NotRequired


class PassportFile(TypedDict):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


class EncryptedPassportElement(TypedDict):
    type: str
    data: NotRequired[str]
    phone_number: NotRequired[str]
    email: NotRequired[str]
    files: NotRequired[List[PassportFile]]
    front_side: NotRequired[PassportFile]
    reverse_side: NotRequired[PassportFile]
    selfie: NotRequired[PassportFile]
    translation: NotRequired[List[PassportFile]]
    hash: str


class EncryptedCredentials(TypedDict):
    data: str
    hash: str
    secret: str


class PassportData(TypedDict):
    data: List[EncryptedPassportElement]
    credentials: EncryptedCredentials
