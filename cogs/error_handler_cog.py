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


from discord.ext import commands
from discord_bot import DiscordBot


class ErrorHandlerCog(commands.Cog):

    def __init__(self):
        pass

    @staticmethod
    async def _send_dm_help(ctx: commands.Context):
        await ctx.author.send(f"Hello {ctx.author.name}! My commands can be executed only in DMs.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandInvokeError) -> None:
        if isinstance(error, commands.CheckFailure):
            if not ctx.guild:
                await ctx.send("Only the bot owner can execute this command.")
            else:
                await self._send_dm_help(ctx)


async def setup(bot: DiscordBot):
    await bot.add_cog(ErrorHandlerCog())
