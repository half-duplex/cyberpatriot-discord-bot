import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class CoreCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def chatinfo(self, context: commands.Context):
        response = ""
        if context.guild:
            response += "\nGuild ID: `{}`".format(context.guild.id)
        response += "\nChat ID: `{}`".format(context.channel.id)
        await context.send(response)

    # Cog management
    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, context: commands.Context, *, extension: str = None):
        await self._manage_ext(self._bot.load_extension, context, extension)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, context: commands.Context, *, extension: str = None):
        await self._manage_ext(self._bot.unload_extension, context, extension)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, context: commands.Context, *, extension: str = None):
        await self._manage_ext(self._bot.reload_extension, context, extension)

    async def _manage_ext(
        self, func: callable, context: commands.Context, extension: str = None
    ):
        if extension is None:
            await context.send("Usage: {context.command} some_cog")
            return
        return func("cogs." + extension)


def setup(bot: commands.Bot):
    logger.info("Loaded Core cog")
    bot.add_cog(CoreCog(bot))
