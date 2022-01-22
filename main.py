#!/usr/bin/env python3

import logging
import os
from sys import stdout

from discord.ext import commands
from tomlkit.toml_file import TOMLFile

LOGGER = logging.getLogger()


class CyberBot:
    _config: dict

    def __init__(self):
        config_file = os.environ.get(
            "CONFIG", os.path.join(os.path.dirname(__file__), "config.toml")
        )
        toml = TOMLFile(config_file)
        self._config = toml.read()

        LOGGER.setLevel(self._config.get("loglevel", "INFO"))
        handler = logging.StreamHandler(stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
        )
        LOGGER.addHandler(handler)
        logging.getLogger("websockets").setLevel("INFO")
        logging.getLogger("discord").setLevel("INFO")

        self._bot = commands.Bot(command_prefix=self._config.get("command_prefix", "."))
        # If discord.py ever creates Bot.config, this will be a bad time
        # Until then, this is the least stupid way of passing config to cogs.
        self._bot.config = self._config

        for cog in self._config.get("cogs", []):
            LOGGER.info("Loading cog: %r", cog)
            self._bot.load_extension("cogs." + cog)

    def run(self):
        self._bot.run(self._config["discord_token"], bot=True, reconnect=True)


if __name__ == "__main__":
    client = CyberBot()
    client.run()
