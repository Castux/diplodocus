import random
import json
import sys
import discord
from discord.ext import commands

sys.path.append('diplomacy')

from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format

# game = Game(map_name='chasers.map')
# game.process()
#
# # print(game.map.convoy_paths[10])
#
# game.set_units('EMPIRE', ['F ANA', 'F TIT'])
#
# game.set_orders("EMPIRE", [
#     'F ANA - RIV',
#     'F TIT C F ANA - RIV'
# ])
#
# for err in game.error:
#     print(err)
#
# print(game.get_orders())
# game.process()
# print(game.get_order_status())


#to_saved_game_format(game, output_path='game.json')

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)

def start_bot(config):

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged on as {bot.user}: {bot.user.id}!')

    @bot.command()
    async def ping(ctx, content):
        await ctx.send("Pong! " + content or "")

    @bot.group()
    async def cool(ctx):
        """Says if a user is cool.
        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

    bot.run(config["token"])


config = load_config("config.json")
start_bot(config)
