from .chat import Chat
from .user import User
from .contact import Contact
from .poll import Poll
from .game import Game, Dice
from .location import Location, Venue
from .document import (
    PhotoSize,
    Animation,
    Audio,
    Document,
    Video,
    Sticker,
    VideoNote,
    Voice
)
from .types.message import (
    Message as MessagePayload,
    MessageEntity as MessageEntityPayload,
    MessageAutoDeleteTimerChanged as MessageAutoDeleteTimerChangedPayload
)


class MessageEntity:

    __slots__ = (
        "type",
        "offset",
        "length",
        "url",
        "user",
        "language",
        "custom_emoji_id"
    )

    def __init__(self, payload: MessageEntityPayload):
        self.__update(payload)

    def __update(self, payload: MessageEntityPayload):
        self.type = payload["type"]
        self.offset = payload["offset"]
        self.length = payload["length"]
        self.url = payload.get("url")
        self.user = payload.get("user")
        self.language = payload.get("language")
        self.custom_emoji_id = payload.get("custom_emoji_id")


class MessageAutoDeleteTimerChanged:

    __slots__ = "message_auto_delete_time"

    def __init__(self, payload: MessageAutoDeleteTimerChangedPayload):
        self.message_auto_delete_time = payload["message_auto_delete_time"]


class Message:

    __slots__ = (
        "message_id",
        "from_",
        "sender_chat",
        "date",
        "chat",
        "forward_from",
        "forward_from_chat",
        "forward_from_message_id",
        "forward_signature",
        "forward_sender_name",
        "forward_date",
        "is_automatic_forward",
        "reply_to_message",
        "via_bot",
        "edit_date",
        "has_protected_content",
        "media_group_id",
        "author_signature",
        "text",
        "entities",
        "animation",
        "audio",
        "document",
        "photo",
        "sticker",
        "video",
        "video_note",
        "voice",
        "caption",
        "caption_entities",
        "contact",
        "dice",
        "game",
        "poll",
        "venue",
        "location",
        "new_chat_members",
        "left_chat_member",
        "new_chat_title",
        "new_chat_photo",
        "delete_chat_photo",
        "group_chat_created",
        "supergroup_chat_created",
        "channel_chat_created",
        "message_auto_delete_timer_changed",
        "migrate_to_chat_id",
        "pinned_message"
    )

    def __init__(self, payload: MessagePayload) -> None:
        self.__update(payload)

    # TODO: Figure out how to read variable 'from' to 'from_' from payload!
    def __update(self, payload: MessagePayload) -> None:
        self.message_id = payload["message_id"]
        self.date = payload["date"]
        self.chat = Chat(payload["chat"])
        self.from_ = payload.get("from_")
        self.sender_chat = payload.get("sender_chat")
        self.forward_from = payload.get("forward_from")
        self.forward_from_chat = payload.get("forward_from_chat")
        self.forward_from_message_id = payload.get("forward_from_message_id", -1)
        self.forward_signature = payload.get("forward_signature")
        self.forward_sender_name = payload.get("forward_sender_name")
        self.forward_date = payload.get("forward_date", -1)
        self.is_automatic_forward = payload.get("is_automatic_forward", False)
        self.reply_to_message = payload.get("reply_to_message")
        self.via_bot = payload.get("via_bot")
        self.edit_date = payload.get("edit_date", -1)
        self.has_protected_content = payload.get("has_protected_content", False)
        self.media_group_id = payload.get("media_group_id")
        self.author_signature = payload.get("author_signature")
        self.text = payload.get("text")
        self.entities = payload.get("entities", [])
        self.animation = payload.get("animation")
        self.audio = payload.get("audio")
        self.document = payload.get("document")
        self.photo = payload.get("photo", [])
        self.sticker = payload.get("sticker")
        self.video = payload.get("video")
        self.video_note = payload.get("video_note")
        self.voice = payload.get("voice")
        self.caption = payload.get("caption")
        self.caption_entities = payload.get("caption_entities", [])
        self.contact = payload.get("contact")
        self.dice = payload.get("dice")
        self.game = payload.get("game")
        self.poll = payload.get("poll")
        self.venue = payload.get("venue")
        self.location = payload.get("location")
        self.new_chat_members = payload.get("new_chat_members", [])
        self.left_chat_member = payload.get("left_chat_member")
        self.new_chat_title = payload.get("new_chat_title")
        self.new_chat_photo = payload.get("new_chat_photo", [])
        self.delete_chat_photo = payload.get("delete_chat_photo", False)
        self.group_chat_created = payload.get("group_chat_created", False)
        self.supergroup_chat_created = payload.get("supergroup_chat_created", False)
        self.channel_chat_created = payload.get("channel_chat_created", False)
        self.message_auto_delete_timer_changed = payload.get("message_auto_delete_timer_changed")
        self.migrate_to_chat_id = payload.get("migrate_to_chat_id", -1)
        self.pinned_message = payload.get("pinned_message")

        for slot in (
                "from_",
                "sender_chat",
                "forward_from",
                "forward_from_chat",
                "reply_to_message",
                "via_bot",
                "entities",
                "animation",
                "audio",
                "document",
                "photo",
                "sticker",
                "video",
                "video_note",
                "voice",
                "caption_entities",
                "contact",
                "dice",
                "game",
                "poll",
                "venue",
                "location",
                "new_chat_members",
                "left_chat_member",
                "new_chat_photo",
                "message_auto_delete_timer_changed",
                "pinned_message"
        ):
            try:
                getattr(self, f"__handle_{slot}")(payload[slot])  # type: ignore
            except KeyError:
                continue

    def __handle_from_(self, value):
        self.from_ = User(value)

    def __handle_sender_chat(self, value):
        self.sender_chat = Chat(value)

    def __handle_forward_from(self, value):
        self.forward_from = User(value)

    def __handle_forward_from_chat(self, value):
        self.forward_from_chat = Chat(value)

    def __handle_reply_to_message(self, value):
        self.reply_to_message = Message(value)

    def __handle_via_bot(self, value):
        self.via_bot = User(value)

    def __handle_entities(self, value):
        self.entities = [MessageEntity(e) for e in value]

    def __handle_animation(self, value):
        self.animation = Animation(value)

    def __handle_audio(self, value):
        self.audio = Audio(value)

    def __handle_document(self, value):
        self.document = Document(value)

    def __handle_photo(self, value):
        self.photo = [PhotoSize(p) for p in value]

    def __handle_sticker(self, value):
        self.sticker = Sticker(value)

    def __handle_video(self, value):
        self.video = Video(value)

    def __handle_video_note(self, value):
        self.video_note = VideoNote(value)

    def __handle_voice(self, value):
        self.voice = Voice(value)

    def __handle_caption_entities(self, value):
        self.caption_entities = [MessageEntity(e) for e in value]

    def __handle_contact(self, value):
        self.contact = Contact(value)

    def __handle_dice(self, value):
        self.dice = Dice(value)

    def __handle_game(self, value):
        self.game = Game(value)

    def __handle_poll(self, value):
        self.poll = Poll(value)

    def __handle_venue(self, value):
        self.venue = Venue(value)

    def __handle_location(self, value):
        self.location = Location(value)

    def __handle_new_chat_members(self, value):
        self.new_chat_members = [User(u) for u in value]

    def __handle_left_chat_member(self, value):
        self.left_chat_member = User(value)

    def __handle_new_chat_photo(self, value):
        self.new_chat_photo = [PhotoSize(p) for p in value]

    def __handle_message_auto_delete_timer_changed(self, value):
        self.message_auto_delete_timer_changed = MessageAutoDeleteTimerChanged(value)

    def __handle_pinned_message(self, value):
        self.pinned_message = Message(value)
