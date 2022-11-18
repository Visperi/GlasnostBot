"""
MIT License

Copyright (c) 2022 Niko Mätäsaho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


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
