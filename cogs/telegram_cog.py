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


import json
import aiohttp
import discord
import telegram
import logging
from typing import Tuple, List, Optional
from discord.ext import commands
from discord_bot import DiscordBot
from database_handler import DatabaseHandler


_logger = logging.getLogger(__name__)


class TelegramCog(commands.Cog):
    """
    A cog listening defined Telegram channels and forwarding the messages to given Discord channels.
    """

    def __init__(self, bot: DiscordBot):
        self.credentials_path = "credentials.json"
        self.database_name = "glasnost.db"
        ids = self._read_channel_ids(self.credentials_path)

        self.tg_channel_id: int = ids[0]
        self.discord_channel_ids = ids[1]
        self.tg_bot = telegram.Client(aiohttp.ClientSession(), loop=bot.loop)
        self.bot = bot
        self.message_cache = DatabaseHandler(self.database_name)

    async def cog_load(self) -> None:
        _logger.debug(f"Starting Telegram polling before loading {__name__}")

        with open(self.credentials_path, "r") as credentials_file:
            credentials = json.load(credentials_file)

        tg_token = credentials["tokens"]["telegram"]

        try:
            self.tg_bot.start(tg_token)
        except ValueError:
            _logger.error("Cannot start Telegram polling. Already polling.")

        self.tg_bot.add_listener(self.on_update)
        if not self.message_cache.connection:
            _logger.debug(f"Connecting to dabatase '{self.database_name}'")
            self.message_cache.connect(self.database_name)

    async def cog_unload(self) -> None:
        _logger.debug(f"Stopping Telegram polling before unloading {__name__}.")
        self.tg_bot.stop()
        self.message_cache.close()

    @staticmethod
    def _read_channel_ids(filepath: str) -> Tuple[int, List[int]]:
        with open(filepath, "r") as credentials_file:
            credentials = json.load(credentials_file)

        tg_channel_ids = credentials["ids"]["telegram"]
        discord_channel_ids = [id_ for id_ in credentials["ids"]["discord"]]

        return tg_channel_ids, discord_channel_ids

    @staticmethod
    def fetch_forwarded_from(channel_post: telegram.Message, prefer_username: bool = False) -> Optional[str]:
        if not channel_post.forward_from and not channel_post.forward_from_chat:
            return None

        # TODO: This can be done inside User object
        if channel_post.forward_from:
            original_poster = channel_post.forward_from
            first_name = original_poster.first_name
            last_name = original_poster.last_name
            username = original_poster.username

            if username and prefer_username:
                return username
            elif last_name:
                return f"{first_name} {last_name}"
            else:
                return first_name

        else:
            original_poster = channel_post.forward_from_chat
            title = original_poster.title
            username = original_poster.username

            if title:
                return title
            else:
                return username

    async def on_update(self, update: telegram.Update) -> None:
        # TODO: Simplify when the library is updated
        if update.channel_post:
            channel_post = update.channel_post
            is_edit = False
            forwarded_from = self.fetch_forwarded_from(channel_post)
        elif update.edited_channel_post:
            channel_post = update.edited_channel_post
            is_edit = True
            forwarded_from = None  # Forwarded Telegram messages cannot be edited
        else:
            return

        text = channel_post.text
        tg_channel_id = channel_post.sender_chat.id
        if tg_channel_id == self.tg_channel_id:
            await self.forward_channel_post(text, channel_post.message_id, is_edit, forwarded_from)

    async def forward_channel_post(
            self,
            text: str,
            tg_message_id: int,
            is_edit: bool,
            forwarder_from: str = None
    ) -> None:
        """
        Send a channel post to all listening Discord channels.
        """
        # TODO: Do something for longer than 2000 char messages
        if forwarder_from is not None:
            text = f"**Forwarded from {forwarder_from}**\n\n{text}"
        if len(text) > 2000:
            _logger.warning(f"Got message of length {len(text)} characters. Skipping.")
            return

        # TODO: Simplify when library is updated
        if is_edit:
            await self.edit_discord_message(text, tg_message_id)
        else:
            for channel_id in self.discord_channel_ids:
                channel = self.bot.get_channel(channel_id)
                if not channel:
                    _logger.error(f"Attempted to forward Telegram message to unknown channel with ID {channel_id}.")
                    continue

                discord_message = await channel.send(text)
                if not forwarder_from:
                    self.message_cache.add(tg_message_id, discord_message)

    async def edit_discord_message(self, new_text: str, tg_message_id: int):
        discord_messages = await self.get_discord_messages(tg_message_id)
        if not discord_messages:
            _logger.warning(f"Cannot edit Discord message with Telegram message ID {tg_message_id}. "
                            f"No messages exist in cache with such ID.")
            return

        for discord_message in discord_messages:
            await discord_message.edit(content=new_text, attachments=discord_message.attachments)

    async def get_discord_messages(self, tg_message_id: int) -> List[discord.Message]:
        messages = []
        message_ids = self.message_cache.get(tg_message_id)

        for message_id, channel_id in message_ids:
            channel = self.bot.get_channel(channel_id)
            messages.append(await channel.fetch_message(message_id))

        return messages

    @commands.is_owner()
    @commands.dm_only()
    @commands.command("reload", description="Reload Telegram and Discord IDs from credentials file.")
    async def reload_ids(self, ctx: commands.Context):
        """
        Reload Telegram channel IDs to read and Discord channel IDs to post messages to.
        """

        credentials = self._read_channel_ids(self.credentials_path)
        self.tg_channel_id = credentials[0]
        self.discord_channel_ids = credentials[1]

        await ctx.send(f"IDs reloaded! There are now \n{len(self.discord_channel_ids)} Discord channel listeners for "
                       f"Telegram channel {self.tg_channel_id}.")


async def setup(bot: DiscordBot):
    await bot.add_cog(TelegramCog(bot))
