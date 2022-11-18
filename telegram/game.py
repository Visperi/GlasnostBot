from typing_extensions import TYPE_CHECKING
from .document import PhotoSize
from .types.game import (
    Game as GamePayload,
    Dice as DicePayload
)


if TYPE_CHECKING:
    from message import MessageEntity


class Game:

    __slots__ = (
        "title",
        "description",
        "photo",
        "text",
        "text_entities",
        "animation"
    )

    def __init__(self, payload: GamePayload):
        self.__update(payload)

    def __update(self, payload: GamePayload):
        self.title = payload["title"]
        self.description = payload["title"]
        self.photo = [PhotoSize(p) for p in payload["photo"]]
        self.text = payload.get("text")
        self.animation = payload["animation"]

        try:
            self.text_entities = [MessageEntity(t) for t in payload["text_entities"]]
        except KeyError:
            self.text_entities = []


class Dice:

    __slots__ = (
        "emoji",
        "value"
    )

    def __init__(self, payload: DicePayload):
        self.__update(payload)

    def __update(self, payload: DicePayload):
        self.emoji = payload["emoji"]
        self.value = payload["value"]
