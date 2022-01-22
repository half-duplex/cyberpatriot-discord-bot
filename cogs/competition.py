from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from typing import Dict

from bs4 import BeautifulSoup
from discord.ext import commands, tasks
import requests

logger = logging.getLogger(__name__)


@dataclass
class ImageScore:
    name: str
    time: timedelta
    objectives_found: int
    objectives_remaining: int
    penalties: int
    score: int
    flags: str

    def __post_init__(self):
        if type(self.time) != timedelta:
            logger.critical("converting time")
            h, m = [int(x) for x in self.time.split(":")]
            self.time = timedelta(hours=h, minutes=m)
        self.objectives_found = int(self.objectives_found)
        self.objectives_remaining = int(self.objectives_remaining)
        self.penalties = int(self.penalties)
        self.score = int(self.score)

        logger.critical(self)


class CompetitionCog(commands.Cog):
    _bot: commands.Bot
    _scores: Dict[str, ImageScore]

    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._session = requests.Session()

        if "scoreboard" not in self._bot.config or "team_id" not in self._bot.config:
            logger.error(
                "Bot config is missing `user_agent`, `scoreboard`, or `team_id`."
            )
            # todo: unload cog

        self._session.headers = {"User-Agent": self._bot.config["user_agent"]}

    def cog_unload(self):
        self.check_score.cancel()

    @commands.command()
    @commands.is_owner()
    async def compete(self, context: commands.Context, start_time: str = None):
        if start_time is None:
            await context.send("You forgot to tell me the start time!")

        h, m = [int(x) for x in start_time.split(":")]
        # todo aoeu get TZ from conf
        start_time = datetime.now()
        start_time.replace(hour=h, minute=m)
        self.start_time = start_time

        await context.send(
            "Competition started at {}. Good luck, team!".format(start_time)
        )

    @tasks.loop(seconds=60)
    async def check_score(self):
        r = self._session.get(
            self._bot.config["team_scoreboard"].format(
                team_id=self._bot.config["team_id"]
            )
        )
        bs = BeautifulSoup(r.text, "lxml")
        print(bs)


def setup(bot: commands.Bot):
    bot.add_cog(CompetitionCog(bot))
