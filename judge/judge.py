import random
import json
import sys
import discord
from discord.ext import commands

sys.path.append('diplomacy')

from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format

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

################################################################################

with open("config.json", "r") as f:
	config = json.load(f)

with open(config["database"], "r") as f:
	database = json.load(f)

def save_database():
	with open(config["database"], "w") as f:
		f.write(json.dumps(database))

################################################################################

if "game" in database:
	game = from_saved_game_format(database["game"])
else:
	game = Game(map_name=config["variant"])

def save_game():
	database["game"] = to_saved_game_format(game)

################################################################################

save_game()
save_database()

################################################################################

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready():
	print(f"Connected as {bot.user}")

@bot.command()
async def ping(ctx, *, content):
	await ctx.send("Pong! " + content or "")

bot.run(config["token"])
