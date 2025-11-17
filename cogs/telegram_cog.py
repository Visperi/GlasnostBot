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

from typing import List, Optional
from datetime import datetime, UTC, timedelta
from pathlib import Path
import logging

import toml
import discord
import filetype
from discord.ext import commands, tasks
from discord_bot import DiscordBot

import telegram
from config import Config
from utils import Missing
from database_handler import DatabaseHandler


_logger = logging.getLogger(__name__)


def get_current_timestamp() -> int:
    """
    Get the current UTC time as POSIX timestamp.

    :return: POSIX timestamp.
    """
    return int(datetime.now(UTC).timestamp())


class TelegramCog(commands.Cog):
    """
    A cog listening defined Telegram channels and forwarding the messages to given Discord channels.
    """

    def __init__(self, bot: DiscordBot):
        self.config = Config("config.toml")

        self.database_name: str = Missing
        self.tg_channel_id: int = Missing
        self.discord_channel_ids: List[int] = Missing
        self.ignored_tg_users: List[int] = Missing
        self.listened_tg_users: List[int] = Missing
        self.prefer_telegram_usernames: bool = Missing
        self.send_orphans_as_new_message: bool = Missing
        self.update_age_threshold: int = Missing
        self.message_cleanup_threshold: int = Missing
        self.load_configuration()

        self.telegram_bot = telegram.Client(loop=bot.loop)
        self.discord_bot = bot
        self.database_handler = DatabaseHandler(self.database_name)

    def load_configuration(self):
        self.config.load()

        self.tg_channel_id = self.config.channel_ids.telegram
        self.discord_channel_ids = self.config.channel_ids.discord

        self.ignored_tg_users = self.config.users.ignored_users
        self.listened_tg_users = self.config.users.listened_users

        self.prefer_telegram_usernames = self.config.preferences.prefer_telegram_usernames
        self.send_orphans_as_new_message = self.config.preferences.send_orphans_as_new_message
        self.update_age_threshold = self.config.preferences.update_age_threshold
        self.message_cleanup_threshold = self.config.preferences.message_cleanup_threshold
        self.database_name = self.config.preferences.database_path

    def add_hooks(self):
        self.telegram_bot.add_listener(self.on_message)
        self.telegram_bot.add_listener(self.on_message_edit)
        self.telegram_bot.add_check(self.has_correct_chat)
        self.telegram_bot.add_check(self.is_new_enough)

    async def cog_load(self) -> None:
        _logger.debug(f"Starting Telegram polling before loading {__name__}")
        self.add_hooks()

        if not self.database_handler.connection:
            _logger.debug(f"Connecting to database '{self.database_name}'")
            self.database_handler.connect(self.database_name)

        self.database_cleanup_loop.start()

        try:
            self.telegram_bot.start(self.config.credentials.telegram)
        except ValueError:
            _logger.error("Cannot start Telegram polling. Already polling.")

    async def cog_unload(self) -> None:
        _logger.debug(f"Stopping Telegram polling before unloading {__name__}.")
        self.telegram_bot.stop()
        self.database_cleanup_loop.cancel()
        self.database_handler.disconnect()

    @tasks.loop(hours=6)
    async def database_cleanup_loop(self) -> None:
        """
        A background task deleting Discord message references from the database at least X days old defined in the
        configuration file.
        """
        threshold = self.message_cleanup_threshold
        _logger.debug(f"Running database auto cleanup task with timestamp threshold of {threshold} days.")
        upper_threshold_limit = datetime.now(UTC) - timedelta(days=threshold)
        self.database_handler.delete_by_age(upper_threshold_limit)

    async def has_correct_chat(self, update: telegram.Update) -> bool:
        message = update.effective_message
        if not message or message.chat.id != self.tg_channel_id:
            return False

        message_sender = message.from_
        if not message_sender:
            # The message is a channel post and has no user as sender
            return True

        user_id = message_sender.id
        # Discard ignored user messages. If listened users list exists, allow only their messages.
        if user_id in self.ignored_tg_users:
            return False
        if self.listened_tg_users and user_id not in self.listened_tg_users:
            return False

        return True

    async def is_new_enough(self, update: telegram.Update) -> bool:
        if update.is_edited_message:
            # Allow edits to always go through
            return True

        message = update.effective_message
        return message and get_current_timestamp() - message.date < self.update_age_threshold

    def create_discord_embed(self, message: telegram.Message) -> Optional[discord.Embed]:
        """
        Create a ``discord.Embed`` object from a Telegram message. If the Telegram does not have text content, and it
        is not a forwarded message, an embed cannot be made.

        :param message: A Telegram message object.
        :return: A Discord Embed object, or None if not relevant.
        """
        if not message.text_content and not message.forward_origin:
            return None

        embed = discord.Embed(description=message.markdownify(make_urls_to_hyperlink=False))
        forwarded_from = message.original_sender

        if forwarded_from is not None:
            if isinstance(forwarded_from, telegram.User):
                if self.prefer_telegram_usernames and forwarded_from.username:
                    sender_name = forwarded_from.username
                else:
                    sender_name = forwarded_from.full_name
            elif isinstance(forwarded_from, telegram.Chat):
                sender_name = forwarded_from.title
            else:
                sender_name = forwarded_from.sender_user_name  # type: ignore

            forward_notification = f"Forwarded from {sender_name}"
            if len(forward_notification) < 256:
                embed.title = f"Forwarded from {sender_name}"
            else:
                embed.description = f"**{forward_notification}\n\n{embed.description}**"

        if embed.description and len(embed.description) > 4096:
            raise ValueError(f"Too long message for Discord embed. "
                             f"Got message of length {len(embed.description)} characters.")

        return embed

    async def fetch_message_files(self, message: telegram.Message) -> Optional[List[discord.File]]:
        """
        Fetch all files present on a Telegram message.

        :param message: The telegram message.
        :return: A list of files in the message as ``discord.File`` object.
        """
        discord_files = []
        telegram_files = message.get_all_media()

        for file in telegram_files:
            file_bytes, filename = await self.telegram_bot.download_file(file)
            with file_bytes:
                if not Path(filename).suffix:
                    # Guess the file extensions if missing to render file properly in Discord
                    extension_guess = filetype.guess_extension(file_bytes)
                    if extension_guess:
                        filename = f"{filename}.{extension_guess}"

                discord_file = discord.File(file_bytes, filename=filename, spoiler=message.has_media_spoiler)
            discord_files.append(discord_file)

        return discord_files or None

    async def on_message(self, message: telegram.Message) -> None:
        """
        A listener method responsible for handling new messages from the Telegram client and forwarding them to Discord.

        :param message: A ``telegram.Message`` object.
        """
        await self.discord_bot.wait_until_ready()
        embed = self.create_discord_embed(message)
        files = await self.fetch_message_files(message)

        if message.reply_to_message:
            # TODO: Properly handle messages that do not come from the same chat and are ExternalReplyInfo
            await self.reply_discord_messages(message.message_id, message.reply_to_message.message_id, embed, files=files)
        else:
            await self.send_discord_messages(message.message_id, embed, files=files)

    async def on_message_edit(self, message: telegram.Message):
        """
        A listener method responsible for handling edited Telegram messages and applying changes to Discord.

        :param message: The edited Telegram message.
        """
        await self.discord_bot.wait_until_ready()

        embed = self.create_discord_embed(message)
        files = await self.fetch_message_files(message)
        message_id = message.message_id

        discord_messages = await self.get_discord_messages(message_id)
        if not discord_messages:
            _logger.warning(f"Cannot edit Discord message with Telegram message ID {message_id}. "
                            f"No messages exist in cache with such ID. Handling as orphans.")
            await self._handle_orphan_messages(message_id, embed, files=files)
            return

        for discord_message in discord_messages:
            if not files:
                files = discord_message.attachments
            await discord_message.edit(embed=embed, attachments=files)
            self.database_handler.update_ts(message_id, get_current_timestamp())

    def serialize_discord_message(self, tg_message_id: int, discord_message: discord.Message) -> None:
        """
        Serialize a Discord message to database so that it can be later retrieved and deserialized based on Telegram
        message ID.

        :param tg_message_id: The Telegram message ID.
        :param discord_message: A Discord message corresponding the Telegram message.
        """
        self.database_handler.add(tg_message_id, discord_message, get_current_timestamp())

    async def send_discord_messages(
            self,
            tg_message_id: int,
            embed: discord.Embed = None,
            text: str = None,
            files: List[discord.File] = None
    ) -> None:
        """
        Send Discord message to all configured Discord channels.

        :param tg_message_id: Telegram message ID from which the content is retrieved from. Needed for Discord message
                              serialization to the database.
        :param embed: A ``discord.Embed`` object to send to the Discord channels.
        :param text: Text content to send in addition to the Discord embed.
        :param files: A list of ``discord.File`` objects to send with the message.
        """

        for channel_id in self.discord_channel_ids:
            channel = self.discord_bot.get_channel(channel_id)
            if not channel:
                _logger.error(f"Attempted to forward Telegram message to unknown channel with ID {channel_id}.")
                continue

            discord_message = await channel.send(content=text, embed=embed, files=files)  # noqa
            self.serialize_discord_message(tg_message_id, discord_message)

    async def _handle_orphan_messages(
            self,
            tg_message_id: int,
            embed: discord.Embed = None,
            text: str = None,
            files: discord.File = None
    ) -> None:
        """
        Handle orphan messages not having matching references in the database. Sends a new message if
        ``send_orphans_as_new_messages`` is True, otherwise does nothing.

        :param tg_message_id: Telegram ID of the orphan message. Needed for handling references in the database.
        :param embed: A ``discord.Embed`` object to send to the Discord channels.
        :param text: Text content to send in addition to the Discord embed.
        :param files: A list of ``discord.File`` objects to send with the message.
        """
        if self.send_orphans_as_new_message:
            # TODO: Handle messages separately if they all are not missing references
            await self.send_discord_messages(tg_message_id, embed, text, files)

    async def reply_discord_messages(
            self,
            tg_message_id: int,
            replied_tg_message_id: int,
            embed: discord.Embed = None,
            text: str = None,
            files: List[discord.file] = None
    ) -> None:
        """
        Reply to a Discord message with a new message in all configured Discord channels. If no Discord message
        references are found from the database, sends a new message or does nothing, based on the configuration.

        :param tg_message_id: The new Telegram message ID. Needed for handling messages in the database.
        :param replied_tg_message_id: ID of the replied Telegram message. Needed for finding message references from the
                                      database.
        :param embed: ``discord.Embed`` object to send with the reply.
        :param text: Text content to send in addition to the Discord embed.
        :param files: A list of ``discord.File`` objects to send with the reply.
        """
        discord_messages = await self.get_discord_messages(replied_tg_message_id)
        if not discord_messages:
            _logger.warning(f"Cannot reply to Discord message with Telegram message ID {replied_tg_message_id}. "
                            f"No messages exist in database with such ID. Handling as orphans.")
            await self._handle_orphan_messages(tg_message_id, embed, text, files)
            return

        for discord_message in discord_messages:
            new_discord_message = await discord_message.reply(content=text, embed=embed, mention_author=False, files=files)  # noqa
            self.serialize_discord_message(tg_message_id, new_discord_message)
            self.database_handler.update_ts(replied_tg_message_id, get_current_timestamp())

    async def get_discord_messages(self, tg_message_id: int) -> List[discord.Message]:
        """
        Get all Discord message references from database based on Telegram message ID.

        :param tg_message_id: Telegram message ID to use to search for Discord messages.
        :return: List of Message objects, or an empty list of none found from database.
        """
        messages = []
        message_ids = self.database_handler.get(tg_message_id)

        for message_id, channel_id in message_ids:
            channel = self.discord_bot.get_channel(channel_id)
            if not channel:
                _logger.error(f"Discord channel with ID {channel_id} not found. Cannot fetch message reference. "
                              f"Skipping.")
                continue

            try:
                messages.append(await channel.fetch_message(message_id))
            except discord.NotFound:
                _logger.error(f"Discord message with ID {message_id} not found. Cannot fetch message reference. "
                              f"Skipping.")
                continue

        return messages

    @commands.is_owner()
    @commands.command("reload", description="Reload channel IDs and preferences in runtime.")
    async def reload_configuration(self, ctx: commands.Context):
        """
        Reload Telegram and Discord channel IDs and preferences from the configuration files.
        """
        old_config = self.config.as_dict()
        try:
            self.load_configuration()
        except toml.decoder.TomlDecodeError:
            await ctx.send("Invalid configuration file syntax. Cannot reload.")
            return

        updated_sections = {}
        for section, section_dict in self.config.as_dict().items():
            for variable, value in section_dict.items():
                if old_config[section][variable] != value:
                    updated_sections[variable] = value

        if "activity_status" in updated_sections:
            await self.discord_bot.update_activity_status(self.config.bot_settings.activity_status)
        if "dm_only_commands" in updated_sections:
            self.discord_bot.set_dm_only_check(self.config.bot_settings.dm_only_commands)
        if "command_prefix" in updated_sections:
            self.discord_bot.set_command_prefix(self.config.bot_settings.command_prefix)

        if not updated_sections:
            await ctx.send("Configuration reloaded with no updates.")
        else:
            current_config = f"```toml\n{self.config}```"
            updated = f"Following variables were updated:\n```toml\n{toml.dumps(updated_sections)}```"
            await ctx.send(f"Configuration reloaded. Configuration is now as follows:\n{current_config}\n{updated}")


async def setup(bot: DiscordBot):
    await bot.add_cog(TelegramCog(bot))
