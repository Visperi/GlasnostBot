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


import discord
import logging
import os
from discord.ext import commands
from typing import Iterable, Union, Optional


_logger = logging.getLogger(__name__)


class DiscordBot(commands.Bot):

    def __init__(
            self,
            command_prefix: Union[str, Iterable[str]],
            activity_status: Optional[str],
            dm_only_commands: bool = True
    ):
        """
        Initialize new Telegram listener Discord bot instance.

        :param command_prefix: Command prefix for the bot. Both strings and iterable of strings are valid.
        :param activity_status: Activity status for the bot to show in Discord. If None, no status is shown.
        :param dm_only_commands: Allow commands only through DMs to the bot.
        """
        self.dm_only_commands = dm_only_commands

        _intents = discord.Intents.default()
        _intents.message_content = True
        activity = None

        if activity_status:
            activity = discord.Game(activity_status)

        super().__init__(command_prefix=command_prefix, intents=_intents,
                         activity=activity)

    @staticmethod
    async def is_dm(ctx: commands.Context) -> bool:
        return ctx.guild is None

    async def setup_hook(self) -> None:
        cogs_path = f"{os.path.dirname(__file__)}/cogs"
        cogs = [f"cogs.{filename.rstrip('.py')}" for filename in os.listdir(cogs_path) if filename.endswith(".py")]

        for cog in cogs:
            try:
                await self.load_extension(cog)
            except Exception as e:
                _logger.error(f"Failed to load extension {cog}: ", exc_info=e)

        if self.dm_only_commands:
            self.add_check(self.is_dm)
