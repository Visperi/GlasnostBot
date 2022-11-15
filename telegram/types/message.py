from __future__ import annotations
from typing import List
from typing_extensions import TypedDict, NotRequired, TYPE_CHECKING
from .user import User
from .location import Location, Venue
from .contact import Contact
from .document import (
    Animation,
    Audio,
    Document,
    PhotoSize,
    Video,
    VideoNote,
    Voice,
    Sticker
)


if TYPE_CHECKING:
    from .chat import Chat
    from .game import Game, Dice
    from .poll import Poll


class MessageEntity(TypedDict):
    type: str
    offset: int
    length: int
    url: NotRequired[str]
    user: NotRequired[User]
    language: NotRequired[str]
    custom_emoji_id: NotRequired[str]


class MessageAutoDeleteTimerChanged(TypedDict):
    message_auto_delete_time: int


class Message(TypedDict):
    message_id: int
    from_: NotRequired[User]
    sender_chat: NotRequired[Chat]
    date: int
    chat: Chat
    forward_from: NotRequired[User]
    forward_from_chat: NotRequired[Chat]
    forward_from_message_id: NotRequired[int]
    forward_signature: NotRequired[str]
    forward_sender_name: NotRequired[str]
    forward_date: NotRequired[int]
    is_automatic_forward: NotRequired[bool]
    reply_to_message: NotRequired[Message]
    via_bot: NotRequired[User]
    edit_date: NotRequired[int]
    has_protected_content: NotRequired[bool]
    media_group_id: NotRequired[str]
    author_signature: NotRequired[str]
    text: NotRequired[str]
    entities: NotRequired[List[MessageEntity]]
    animation: NotRequired[Animation]
    audio: NotRequired[Audio]
    document: NotRequired[Document]
    photo: NotRequired[List[PhotoSize]]
    sticker: NotRequired[Sticker]
    video: NotRequired[Video]
    video_note: NotRequired[VideoNote]
    voice: NotRequired[Voice]
    caption: NotRequired[str]
    caption_entities: NotRequired[List[MessageEntity]]
    contact: NotRequired[Contact]
    dice: NotRequired[Dice]
    game: NotRequired[Game]
    poll: NotRequired[Poll]
    venue: NotRequired[Venue]
    location: NotRequired[Location]
    new_chat_members: NotRequired[List[User]]
    left_chat_member: NotRequired[User]
    new_chat_title: NotRequired[str]
    new_chat_photo: NotRequired[List[PhotoSize]]
    delete_chat_photo: NotRequired[bool]
    group_chat_created: NotRequired[bool]
    supergroup_chat_created: NotRequired[bool]
    channel_chat_created: NotRequired[bool]
    message_auto_delete_timer_changed: NotRequired[MessageAutoDeleteTimerChanged]
    migrate_to_chat_id: NotRequired[int]
    pinned_message: NotRequired[Message]
