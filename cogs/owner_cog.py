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
from discord_bot import DiscordBot


_logger = logging.getLogger(__name__)


class OwnerCog(commands.Cog, name="OwnerOnly",
               description="Various bot owner only commands for managing the bot through Discord chat."):

    def __init__(self, bot: DiscordBot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.group(name="extension")
    async def manage_extensions(self, ctx: commands.Context) -> None:
        """
        Load, reload or unload an extension. Give extension names as their import names, e.g. cogs.my_cog.
        """
        if ctx.invoked_subcommand is None:
            subcommand = ctx.subcommand_passed
            if subcommand is None:
                await ctx.send("This command required extension management command `load`, `unload` or `reload` to "
                               "manage cogs.")
            else:
                await ctx.send(f"Invalid extension management command: `{ctx.subcommand_passed}`. "
                               f"See `help extension` command for available options.")


    @manage_extensions.command(name="load")
    async def load_cog(self, ctx: commands.Context, extension_name: str) -> None:
        """
        Load an extension atomically.

        :param ctx:
        :param extension_name: Extension name to load.
        """
        await self.bot.load_extension(extension_name)
        await ctx.send(f"Successfully loaded extension `{extension_name}`.")
        _logger.info(f"Loaded a discord.py cog {extension_name}.")

    @manage_extensions.command(name="unload")
    async def unload_cog(self, ctx: commands.Context, extension_name: str) -> None:
        """
        Unload an extension atomically.

        :param ctx:
        :param extension_name: Extension name to unload.
        """
        await self.bot.unload_extension(extension_name)
        await ctx.send(f"Successfully unloaded extension `{extension_name}`.")
        _logger.info(f"Unloaded a discord.py cog {extension_name}.")

    @manage_extensions.command(name="reload")
    async def reload_cog(self, ctx: commands.Context, extension_name: str) -> None:
        """
        Reload an extension atomically.

        :param ctx:
        :param extension_name: Extension name to reload.
        """
        await self.bot.reload_extension(extension_name)
        await ctx.send(f"Successfully reloaded extension `{extension_name}`")
        _logger.info(f"Reloaded a discord.py cog {extension_name}.")

    @commands.command(name="sync")
    async def sync_commands(self, ctx: commands.Context, guild_id: int = None) -> None:
        """
        Synchronize slash commands to Discord API for the bot.
        :param ctx:
        :param guild_id: Guild ID to sync the commands for. If not provided, sync for all guilds.
        """
        await self.bot.tree.sync(guild=guild_id)
        await ctx.send("Commands synced!")


async def setup(bot: DiscordBot):
    await bot.add_cog(OwnerCog(bot))