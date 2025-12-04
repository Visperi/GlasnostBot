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

from discord.ext import commands
from bots.discord_bot import DiscordBot


_logger = logging.getLogger(__name__)


class ErrorHandlerCog(commands.Cog):

    def __init__(self):
        pass

    @staticmethod
    def fetch_extension_handling_error(ctx: commands.Context, error: commands.CommandInvokeError) -> str:
        if isinstance(error.original, commands.ExtensionAlreadyLoaded):
            message = "Extension {} is already loaded."
        elif isinstance(error.original, commands.ExtensionNotFound):
            message = "Extension {} not found."
        elif isinstance(error.original, commands.ExtensionNotLoaded):
            message = "Extension {} is not loaded."
        elif isinstance(error.original, commands.ExtensionFailed):
            message = "Failed to load extension {}."
        else:
            message = f"Unexpected cog related error: {error}"

        cog_name = ctx.args[-1]
        return message.format(f"`{cog_name}`")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandInvokeError) -> None:
        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.NotOwner):
            await ctx.send("Only the bot owner can execute this command.")
        elif isinstance(error, commands.CheckFailure) and ctx.guild:
            # dm_only_commands is True and the command was executed in a channel
            await ctx.author.send(f"Hello {ctx.author.name}. My commands can be executed only in DMs.")
        else:
            await ctx.send(self.fetch_extension_handling_error(ctx, error))


async def setup(bot: DiscordBot):
    await bot.add_cog(ErrorHandlerCog())
