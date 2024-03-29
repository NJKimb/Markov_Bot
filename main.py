import asyncio
import os
import discord
import logging.handlers

from aiohttp import ClientSession
from discord.ext import commands

from markov_chain import MarkovChain

trigger_phrases = {
    "i'm", "im",
    "think",
    "imagine",
    "what's", "whats",
    "challenged"
}


class MarkovBot(commands.Bot):
    client: discord.Client
    chain: MarkovChain
    client = discord.Client

    def __init__(self, *args, web_client: ClientSession, **kwargs):
        self.chain = MarkovChain()
        super().__init__(*args, **kwargs)
        self.web_client = web_client

    async def on_ready(self) -> None:
        print(f'We have logged in as {self.user}!')

    async def on_message(self, message) -> None:
        if message.author == self.user:
            return

        for word in trigger_phrases:
            if word in message.content.lower().split():
                generated_message = self.chain.generate(word)
                await message.channel.send(generated_message)
                return


async def main():
    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,
        backupCount=5
    )
    discord.utils.setup_logging(handler=handler, root=False)

    async with ClientSession() as our_client:
        intents = discord.Intents.default()
        intents.message_content = True
        async with MarkovBot(
                commands.when_mentioned,
                intents=intents,
                web_client=our_client
        ) as bot:
            await bot.start(os.environ['TOKEN'])


asyncio.run(main())
