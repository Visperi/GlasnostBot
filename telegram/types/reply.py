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
