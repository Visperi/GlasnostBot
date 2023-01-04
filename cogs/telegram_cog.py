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
import toml
import aiohttp
import discord
import telegram
import datetime
import logging
from typing import List, Optional, TypeVar, Any
from discord.ext import commands, tasks
from discord_bot import DiscordBot
from database_handler import DatabaseHandler


_logger = logging.getLogger(__name__)
Missing = TypeVar("Missing", Any, None)


class TelegramCog(commands.Cog):
    """
    A cog listening defined Telegram channels and forwarding the messages to given Discord channels.
    """

    def __init__(self, bot: DiscordBot):
        self.config_path: str = "config.toml"

        self.database_name: str = Missing
        self.tg_channel_id: int = Missing
        self.discord_channel_ids: List[int] = Missing
        self.prefer_telegram_usernames: bool = Missing
        self.send_orphans_as_new_message: bool = Missing
        self.update_age_threshold: int = Missing
        self.message_cleanup_threshold: int = Missing
        self.read_configuration()

        self.tg_bot = telegram.Client(aiohttp.ClientSession(), loop=bot.loop)
        self.bot = bot
        self.database_handler = DatabaseHandler(self.database_name)

    def read_configuration(self) -> dict:
        config = toml.load("config.toml")
        self.tg_channel_id = config["credentials"]["channel_ids"]["telegram"]
        self.discord_channel_ids = config["credentials"]["channel_ids"]["discord"]
        self.prefer_telegram_usernames = config["preferences"]["prefer_telegram_usernames"]
        self.send_orphans_as_new_message = config["preferences"]["send_orphans_as_new_message"]
        self.update_age_threshold = config["preferences"]["update_age_threshold"]
        self.message_cleanup_threshold = config["preferences"]["message_cleanup_threshold"]
        self.database_name = config["preferences"]["database_path"]

        return dict(
            channel_ids=config["credentials"]["channel_ids"],
            preferences=config["preferences"]
        )

    async def cog_load(self) -> None:
        _logger.debug(f"Starting Telegram polling before loading {__name__}")

        config = toml.load("config.toml")
        telegram_token = config["credentials"]["tokens"]["telegram"]
        try:
            self.tg_bot.start(telegram_token)
        except ValueError:
            _logger.error("Cannot start Telegram polling. Already polling.")

        self.tg_bot.add_listener(self.on_update)
        if not self.database_handler.connection:
            _logger.debug(f"Connecting to dabatase '{self.database_name}'")
            self.database_handler.connect(self.database_name)

        self.database_cleanup_loop.start()

    async def cog_unload(self) -> None:
        _logger.debug(f"Stopping Telegram polling before unloading {__name__}.")
        self.tg_bot.stop()
        self.database_cleanup_loop.cancel()
        self.database_handler.disconnect()

    @staticmethod
    def fetch_forwarded_from(channel_post: telegram.Message, prefer_username: bool = False) -> Optional[str]:
        """
        Fetch the original Telegram messages author name or username.

        :param channel_post: Message forwarded to the channel as a channel post.
        :param prefer_username: Prefer Telegram username over first name and last name for persons.
        :return: The Telegram name, or None if not valid user.
        """
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

    @tasks.loop(hours=6)
    async def database_cleanup_loop(self) -> None:
        """
        A background task deleting Discord message references from the database at least X days old defined in the
        configuration file.
        """
        youngest_to_delete = datetime.datetime.utcnow() - datetime.timedelta(days=self.message_cleanup_threshold)
        _logger.debug(f"Deleting message references younger than {youngest_to_delete}.")
        self.database_handler.delete_by_age(youngest_to_delete)

    async def on_update(self, update: telegram.Update) -> None:
        """
        Listener coroutine for the new Telegram Update objects received. Sends channel posts from determined Telegram
        channels to listening Discord channels.

        :param update: An update object from Telegram API.
        """
        await self.bot.wait_until_ready()
        # TODO: Simplify when the library is updated
        if update.channel_post:
            channel_post = update.channel_post
            is_edit = False
        elif update.edited_channel_post:
            channel_post = update.edited_channel_post
            is_edit = True
        else:
            return

        update_age = int(datetime.datetime.now().timestamp()) - channel_post.date
        if is_edit is False and update_age > self.update_age_threshold:
            _logger.warning(f"Got update older than configured threshold age of {self.update_age_threshold} seconds.")
            return

        tg_channel_id = channel_post.sender_chat.id
        if tg_channel_id == self.tg_channel_id:
            await self.forward_channel_post(channel_post, is_edit)

    def format_channel_post(self, message: telegram.Message) -> discord.Embed:
        """
        Format a channel post so that stylised text stays as is when sent to discord. Add forwarded messages original
        author name if it is forwarded message.

        :param message: Channel post to format.
        :return: Channel post text changed to Discord compatible format.
        """
        forwarded_from = self.fetch_forwarded_from(message, prefer_username=self.prefer_telegram_usernames)
        formatted_message = message.text_formatted
        embed = discord.Embed(description=formatted_message)

        if forwarded_from is not None:
            forward_notification = f"Forwarded from {forwarded_from}"
            if len(forward_notification) < 256:
                embed.title = f"Forwarded from {forwarded_from}"
            else:
                embed.description = f"**{forward_notification}\n\n{embed.description}**"

        if len(embed.description) > 4096:
            raise ValueError(f"Too long message for Discord embed. "
                             f"Got message of length {len(embed.description)} characters.")

        return embed

    async def forward_channel_post(
            self,
            channel_post: telegram.Message,
            is_edit: bool
    ) -> None:
        """
        Send a channel post content to all listening Discord channels specified in the configuration file.

        :param channel_post: Telegram channel post to forward to Discord.
        :param is_edit: Tells if the Telegram message was edited. If True, a Discord message reference is searched
        from the database and then edited with the new embed.
        """
        embed = self.format_channel_post(channel_post)
        content = None

        # TODO: Simplify when library is updated
        if is_edit:
            await self.edit_discord_messages(embed, channel_post.message_id, content=content)
        elif channel_post.reply_to_message:
            await self.reply_discord_messages(embed,
                                              channel_post.message_id,
                                              channel_post.reply_to_message.message_id,
                                              content=content)
        else:
            await self.send_discord_messages(embed, channel_post.message_id, content=content)

    def serialize_discord_message(self, tg_message_id: int, discord_message: discord.Message) -> None:
        """
        Serialize a Discord message to database so that it can be later retrieved and deserialized based on Telegram
        message ID.

        :param tg_message_id: The Telegram message ID.
        :param discord_message: A Discord message corresponding the Telegram message.
        """
        ts = int(datetime.datetime.utcnow().timestamp())
        self.database_handler.add(tg_message_id, discord_message, ts)

    async def send_discord_messages(
            self,
            embed: discord.Embed,
            tg_message_id: int,
            content: str = None
    ) -> None:
        """
        Send Discord message to all channels defined in the configuration file.

        :param embed: A discord.Embed object to send to the Discord channels.
        :param tg_message_id: Telegram message ID from which the content is retrieved from. Needed for database
        serialization.
        :param content: Text content to send in addition to the Discord embed.
        """
        for channel_id in self.discord_channel_ids:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                _logger.error(f"Attempted to forward Telegram message to unknown channel with ID {channel_id}.")
                continue

            discord_message = await channel.send(content=content, embed=embed)
            self.serialize_discord_message(tg_message_id, discord_message)

    async def _handle_orphan_messages(self, embed: discord.Embed, tg_message_id: int, content: str = None) -> None:
        """
        Handle orphan messages not having matching references in the database.
        Does nothing if send_orphans_as_new_message is set to False, otherwise sends new messages.

        :param embed: Content of the orphan message.
        :param tg_message_id: Telegram ID of the orphan message. Needed for adding a new reference to the database.
        :param content: Text content to send in addition to the Discord embed.
        """
        if self.send_orphans_as_new_message:
            await self.send_discord_messages(embed, tg_message_id, content=content)

    async def reply_discord_messages(
            self,
            reply_embed: discord.Embed,
            tg_message_id: int,
            replied_tg_message_id: int,
            content: str = None
    ) -> None:
        """
        Fetch old Discord message references from the database and reply to them with given text.
        If no messages are found in database, send new messages or do nothing based on the configuration.

        :param reply_embed: Embed to reply with to the old Discord message.
        :param tg_message_id: The new Telegram message ID. Needed for adding a new Discord message reference to
        the database.
        :param replied_tg_message_id: ID of the replied Telegram message. Needed for finding message reference from the
        database.
        :param content: Text content to send in addition to the Discord embed.
        """
        discord_messages = await self.get_discord_messages(replied_tg_message_id)
        if not discord_messages:
            _logger.warning(f"Cannot reply to Discord message with Telegram message ID {replied_tg_message_id}. "
                            f"No messages exist in cache with such ID. Sending new messages instead.")
            await self._handle_orphan_messages(reply_embed, tg_message_id, content)
            return

        for discord_message in discord_messages:
            new_discord_message = await discord_message.reply(content=content, embed=reply_embed, mention_author=False)
            self.serialize_discord_message(tg_message_id, new_discord_message)
            utc_timestamp = int(datetime.datetime.utcnow().timestamp())
            self.database_handler.update_ts(replied_tg_message_id, utc_timestamp)

    async def edit_discord_messages(
            self,
            new_embed: discord.Embed,
            tg_message_id: int,
            content: str = None
    ) -> None:
        """
        Edit a Discord messages based on a Telegram ID to match the content.
        If no messages are found in database, send new messages or do nothing based on the configuration.

        :param new_embed: New embed for the edited Discord message.
        :param tg_message_id: The Telegram message ID, which is used for finding the Discord message reference.
        :param content: Text content to send in addition to the Discord embed.
        """
        discord_messages = await self.get_discord_messages(tg_message_id)
        if not discord_messages:
            _logger.warning(f"Cannot edit Discord message with Telegram message ID {tg_message_id}. "
                            f"No messages exist in cache with such ID.")
            await self._handle_orphan_messages(new_embed, tg_message_id, content)
            return

        for discord_message in discord_messages:
            await discord_message.edit(content=content, embed=new_embed, attachments=discord_message.attachments)
            self.database_handler.update_ts(tg_message_id, int(datetime.datetime.utcnow().timestamp()))

    async def get_discord_messages(self, tg_message_id: int) -> List[discord.Message]:
        """
        Get all Discord message references from database based on Telegram message ID.

        :param tg_message_id: Telegram message ID to use to search for Discord messages.
        :return: List of Message objects, or an empty list of none found from database.
        """
        messages = []
        message_ids = self.database_handler.get(tg_message_id)

        for message_id, channel_id in message_ids:
            channel = self.bot.get_channel(channel_id)
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
    @commands.dm_only()
    @commands.command("reload", description="Reload channel IDs and preferences in runtime.")
    async def reload_configuration(self, ctx: commands.Context):
        """
        Reload Telegram and Discord channel IDs and preferences from the configuration files.
        """
        configuration = self.read_configuration()

        await ctx.send(f"Configuration reloaded! IDs and preferences are now as follows:\n "
                       f"```toml\n{toml.dumps(configuration)}```")


async def setup(bot: DiscordBot):
    await bot.add_cog(TelegramCog(bot))
