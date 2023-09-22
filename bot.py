import logging

import discord
from discord import Intents
from discord.ext.commands import Bot

from config import token

logging.basicConfig(format='[%(asctime)s] [%(levelname)s - %(name)s] %(message)s')


MESSAGE_ROLES = [
    (
        1069855245468971029,
        '**Welcome To The Server {user}! 🍸**',
        'https://media.tenor.com/4Nc9Ax9G864AAAAC/cheers-party.gif'
    ),
    (
        952658283271950357,
        '**Welcome to the VIP area 5+ holder {user}! 🍸**',
        'https://media.tenor.com/n3KTuj4eEjcAAAAd/thanos-infinity-war.gif'
    ),
    (
        1021091023490924574,
        '**Welcome to the VIP area 10+ holder {user}! 🍸**',
        'https://media.tenor.com/6etWehZn0lIAAAAC/impressed-agree.gif'
    )
]

MESSAGES_CHANNEL_ID = 1052444079172108330


class CustomBot(Bot):
    def __init__(self):
        intents = Intents.default()
        intents.members = True
        super().__init__('!', intents=intents, case_insensitive=True)
        self.remove_command('help')


bot = CustomBot()


@bot.event
async def on_ready():
    print('-------------------- Bot is ready! --------------------')


@bot.listen('on_member_update')
async def detect_role_added(before: discord.Member, after: discord.Member):
    """Detects when one of the roles was added and sends the welcome message embed."""

    for role_id, text, gif_url in MESSAGE_ROLES:
        if before.get_role(role_id) is not None or after.get_role(role_id) is None:
            continue

        channel = after.guild.get_channel(MESSAGES_CHANNEL_ID)
        if channel is None:
            print(f'Error: Channel with id {MESSAGES_CHANNEL_ID} not found!')
            return

        embed = discord.Embed(
            description=text.replace('{user}', after.mention),
            color=discord.Color.random()
        )
        embed.set_thumbnail(url=after.avatar.url)
        embed.set_image(url=gif_url)
        embed.set_author(name=after.name, icon_url=after.avatar.url)

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            print(f'Error: No permissions to send a message in the channel with id {MESSAGES_CHANNEL_ID}')
            return


bot.run(token)
