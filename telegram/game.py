from .types.game import (
    Game as GamePayload,
    Dice as DicePayload
)


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
        self.photo = payload["photo"]
        self.text = payload.get("text")
        self.text_entities = payload.get("text_entities", [])
        self.animation = payload["animation"]


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
