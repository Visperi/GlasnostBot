from typing import List

from .message_entity import MessageEntity
from .types.reply import TextQuote as TextQuotePayload


class TextQuote:

    __slots__ = (
        "text",
        "entities",
        "position",
        "is_manual"
    )

    def __init__(self, payload: TextQuotePayload):
        """
        Represents a quoted part in a message that quotes and replies another message.

        :param payload: ``TextQuote`` dictionary received from Telegram API.
        """
        self.text: str = payload["text"]
        """
        Quoted part of the replied message.
        """
        self.entities: List[MessageEntity] = [MessageEntity(e) for e in payload.get("entities", [])]
        """
        List of message entities in the quote.
        """
        self.position = payload["position"]
        """
        Approximate position on the quote in the original message in UTF-16 code units.
        """
        self.is_manual = payload.get("is_manual", False)
        """
        True if the quote was manually selected by user. Otherwise the quote was added by Telegram servers.
        """

    # TODO: Relocate the markdown algorithm to common place where it can be called where applicable
    def markdown(self, make_urls_to_hyperlinks: bool = True) -> str:
        sorted_entities = sorted(self.entities, key=lambda e: e.offset)
        grouped_entities = {}
        for message_entity in sorted_entities:
            grouped_entities.setdefault(message_entity.offset, []).append(message_entity)

        utf16_bytes = bytearray(self.text, "utf-16-le")
        cumulative_offset = 0
        for offset_group in grouped_entities.values():
            entity = offset_group[0]
            entity_start = entity.offset * 2 + cumulative_offset
            entity_end = entity_start + entity.length * 2
            entity_text = utf16_bytes[entity_start:entity_end].decode("utf-16-le")
            markdown, offset = entity.nested_markdown(entity_text, offset_group[1:], make_urls_to_hyperlinks)
            utf16_bytes[entity_start:entity_end] = markdown.encode("utf-16-le")
            cumulative_offset += offset * 2

        return utf16_bytes.decode("utf-16-le")
