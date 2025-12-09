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


import logging
from datetime import datetime, UTC

import telegram
from config import Config


_logger = logging.getLogger(__name__)


class TelegramBot(telegram.Client):

    def __init__(self, loop, config: Config):
        """
        A Telegram bot responsible for listening to Telegram messages and filtering them before they are
        forwarded to Discord.

        :param loop: An existing asyncio loop where to attach to.
        :param config: A ``Config`` object to load telegram configuration from.
        """
        super().__init__(loop)
        self.update_age_threshold = config.preferences.update_age_threshold
        self.telegram_channel_id = config.channel_ids.telegram
        self.ignored_users = config.users.ignored_users
        self.listened_users = config.users.listened_users

        self.add_check(self.is_new_enough_message)
        self.add_check(self.is_from_listened_origin)
        _logger.info("TelegramBot initialized and ready.")

    def load_config(self, config: Config):
        self.update_age_threshold = config.preferences.update_age_threshold
        self.telegram_channel_id = config.channel_ids.telegram
        self.ignored_users = config.users.ignored_users
        self.listened_users = config.users.listened_users

    async def is_new_enough_message(self, update: telegram.Update):
        if update.is_edited_message:
            # Allow edits always go through and let Telegram cog handle possible orphans
            return True

        message = update.effective_message
        return message and datetime.now(UTC).timestamp() - message.date < self.update_age_threshold

    async def is_from_listened_origin(self, update: telegram.Update):
        message = update.effective_message
        if not message or message.chat.id != self.telegram_channel_id:
            return False

        message_sender = message.from_
        if not message_sender:
            # The message is a channel post and has no user as sender
            return True

        user_id = message_sender.id
        # Discard ignored user messages. If listened user list exists, allow only their messages.
        if user_id in self.ignored_users:
            _logger.debug(f"Discarding message from ignored user {user_id}")
            return False
        if self.listened_users and user_id not in self.listened_users:
            return False

        return True
