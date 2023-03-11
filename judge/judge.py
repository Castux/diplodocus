import random
import json
import sys
import os
import discord
from datetime import datetime
from discord.ext import commands

sys.path.append('diplomacy')

from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format

import utils

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

if not "orders" in database:
	database["orders"] = {}

def save_database():
	old_name = config["database"]
	new_name = config["database"] + "." + datetime.now().isoformat() + ".json"
	os.rename(old_name, new_name)

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

@bot.command()
async def gamestate(ctx):
	text = utils.gamestate_to_text(game)
	await ctx.send(text)

@bot.command()
async def status(ctx):
	text = f"Current phase is **{game.phase}**. {utils.get_ready_players_count(database)} sent their orders."
	await ctx.send(text)

@bot.command()
async def send(ctx, *, content):
	player =  ctx.author.name
	utils.save_orders(config, database, player, content)
	save_database()

	await ctx.send(f"Saved orders for {player}:\n{content}")

@bot.command()
async def check(ctx):
	player = ctx.author.name
	if not player in database["orders"]:
		text = f"No orders sent for {player}"
	else:
		text = f"Orders for {player}:\n{database['orders'][player]}"

	await ctx.send(text)

@bot.command()
async def remove(ctx):
	player = ctx.author.name
	if not player in database["orders"]:
		text = f"No orders sent for {player}"
	else:
		database["orders"].pop(player)
		save_database()
		text = f"Removed orders for {player}"

	await ctx.send(text)

bot.run(config["token"])
