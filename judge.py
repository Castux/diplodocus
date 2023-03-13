import random
import json
import sys
import os
import discord
from datetime import datetime
from discord.ext import commands
import typing

sys.path.append('diplomacy')

import diplomacy
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format

import utils

class Diplodocus():

	def __init__(self):

		with open("config.json", "r") as f:
			self.config = json.load(f)

		with open(self.config["database"], "r") as f:
			self.database = json.load(f)

		if not "orders" in self.database:
			self.database["orders"] = {}

		if "game" in self.database:
			self.game = from_saved_game_format(self.database["game"])
		else:
			self.game = diplomacy.Game(map_name=self.config["variant"])

		if len(self.game.error) > 0:
			for err in self.game.error:
				print(err)
			sys.exit(1)

		self.save_game()
		self.save_database()
		self.setup_bot()

	def save_game(self):
		self.database["game"] = to_saved_game_format(self.game)

	def save_database(self):
		old_name = self.config["database"]
		new_name = self.config["database"] + "." + datetime.now().isoformat() + ".json"
		os.rename(old_name, new_name)

		with open(self.config["database"], "w") as f:
			f.write(json.dumps(self.database))

	def setup_bot(self):
		intents = discord.Intents.default()
		intents.message_content = True
		bot = commands.Bot(command_prefix=self.config["prefix"], intents=intents)
		self.bot = bot

		@bot.event
		async def on_ready():
			print(f"Connected as {bot.user}")

		@bot.command()
		async def ping(ctx, *, message):
			"""Ping-pong, baby!

			Parameters
			----------
			message
				A message I'll send back to you
			"""

			await ctx.send("Pong! " + message or "")

		@bot.command()
		async def gamestate(ctx):
			"""Show the game state"""

			text = utils.gamestate_to_text(self.game)
			await ctx.send(text)

		@bot.command()
		async def status(ctx):
			"""Show the current phase

			Including how many players have submitted orders for it
			"""

			text = f"Current phase is **{self.game.phase}**. {utils.get_ready_players_count(self.database)} sent their orders."
			await ctx.send(text)

		@bot.command()
		async def send(ctx, *, orders):
			"""Send your orders for the phase

			They will replace any previously submitted set of orders. Expected format:
			A LON H	(hold),
			F IRI - MAO (move),
			A WAL S F LON (support a non moving unit),
			A WAL S F MAO - IRI (support a moving unit),
			F NWG C A NWY - EDI (convoy),
			A IRO R MAO (retreat),
			A IRO D (disband),
			A LON B (build)

			Parameters
			----------
			orders
				Your orders, exactly one per line. Only sets of valid orders are accepted.
			"""

			player, power, err = utils.get_player_power(self.config, ctx)
			if err:
				await ctx.send(err)
				return

			valid, errors = utils.check_orders(self.database, power, orders)

			if len(errors) > 0:
				text = "\n".join(map(str, errors))
			else:
				utils.save_orders(self.config, self.database, player, valid)
				self.save_database()
				text = utils.orders_to_text(player, power, self.database)

			await ctx.send(text)

		@bot.command()
		async def check(ctx):
			"""Check your orders for this phase"""

			player, power, err = utils.get_player_power(self.config, ctx)
			if err:
				await ctx.send(err)
				return

			if not player in self.database["orders"]:
				text = f"No orders sent for {player}"
			else:
				text = utils.orders_to_text(player, power, self.database)

			await ctx.send(text)

		@bot.command()
		async def remove(ctx):
			"""Remove your orders for this phase"""

			player = ctx.author.name
			if not player in self.database["orders"]:
				text = f"No orders sent for {player}"
			else:
				self.database["orders"].pop(player)
				self.save_database()
				text = f"Removed orders for {player}"

			await ctx.send(text)

		@bot.command()
		async def hint(ctx, prov: typing.Optional[str]):
			"""See all possible valid orders for a province

			Parameters
			----------
			prov
				The abbreviation for the province
			"""

			await ctx.send(utils.get_hint_for_province(self.game, prov))

		@bot.command()
		async def simulate(ctx, *, orders):
			"""Simulate a set of orders for the current phase

			Each order on a single line. Orders from a power grouped together and preceded
			by the power's name.

			Parameters
			----------
			orders
				The orders to simulate
			"""

			result = utils.simulate(self.database, orders)
			await ctx.send(result)

		@bot.command()
		async def adjudicate(ctx):
			"""Adjudicate the current phase

			All currently submitted orders are resolved, their results displayed, along
			with the next game state. The phase progresses to the next.

			This can only be used on a public channel.
			"""

			if ctx.channel.type == discord.ChannelType.private:
				await ctx.send("Cannot adjudicate in a private channel")
			else:
				result = utils.adjudicate(self.database, self.config, self.game)
				self.save_game()
				self.save_database()
				await ctx.send(result)

	def run_bot(self):
		self.bot.run(self.config["token"])

################################################################################

diplodocus = Diplodocus()
diplodocus.run_bot()
