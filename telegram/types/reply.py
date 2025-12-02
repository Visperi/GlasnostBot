"""
MIT License

Copyright (c) 2025 Niko Mätäsaho

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


from typing import TypedDict, NotRequired, List

from .message_entity import MessageEntity
from .message_origin import MessageOrigin
from .link_preview_options import LinkPreviewOptions
from .chat import Chat, Story
from .checklist import Checklist
from .contact import Contact
from .games import Dice, Game
from .giveaway import Giveaway, GiveawayWinners
from .payments import Invoice
from .location import Location, Venue
from .poll import Poll
from .media import (
    Animation,
    Audio,
    Document,
    PaidMediaInfo,
    PhotoSize,
    Sticker,
    Video,
    VideoNote,
    Voice
)


class ExternalReplyInfo(TypedDict):
    origin: MessageOrigin
    chat: NotRequired[Chat]
    message_id: NotRequired[int]
    link_preview_options: NotRequired[LinkPreviewOptions]
    animation: NotRequired[Animation]
    audio: NotRequired[Audio]
    document: NotRequired[Document]
    paid_media: NotRequired[PaidMediaInfo]
    photo: NotRequired[List[PhotoSize]]
    sticker: NotRequired[Sticker]
    story: NotRequired[Story]
    video: NotRequired[Video]
    video_note: NotRequired[VideoNote]
    voice: NotRequired[Voice]
    has_media_spoiler: NotRequired[bool]
    checklist: NotRequired[Checklist]
    contact: NotRequired[Contact]
    dice: NotRequired[Dice]
    game: NotRequired[Game]
    giveaway: NotRequired[Giveaway]
    giveaway_winners: NotRequired[GiveawayWinners]
    invoice: NotRequired[Invoice]
    location: NotRequired[Location]
    poll: NotRequired[Poll]
    venue: NotRequired[Venue]


class TextQuote(TypedDict):
    text: str
    entities: NotRequired[List[MessageEntity]]
    position: int
    is_manual: NotRequired[bool]
