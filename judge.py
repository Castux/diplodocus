import random
import json
import sys
import os
import io
import discord
from datetime import datetime
from discord.ext import commands
import typing

sys.path.append('diplomacy')

import diplomacy
from diplomacy.utils.export import to_saved_game_format, from_saved_game_format

################################################################################

def order_to_unit(order):
	return " ".join(order.split()[0:2])

def sanitize_result(r):
	r = str(r)
	if r == "":
		r = "OK"
	return r

def gamestate_to_text(game):
	lines = []
	lines.append("**" + game.phase + "**\n")

	for name, power in game.powers.items():
		lines.append(name + " (SCs: " + " ".join(power.centers) + ")")
		lines.append("\n".join(power.units))
		if game.phase_type == 'A':
			count = len(power.centers) - len(power.units)
			lines.append("Adjustments: " + str(count))
			if count > 0:
				lines.append("Available build sites: " + ", ".join(game._build_sites(power)))
		lines.append("")

	return '\n'.join(lines)

def format_order_results(game):

	phase = game.get_phase_history()[-1]

	lines = ["**" + game.map.phase_long(phase.name) + "**", ""]
	for power, orders in phase.orders.items():
		lines.append(power)
		for order in orders:
			results = phase.results[order_to_unit(order)]
			results = map(str, results)
			results = ", ".join(results)
			if results != "":
				results = " (" + results + ")"
			lines.append(order + results)
		lines.append("")

	lines += [gamestate_to_text(game)]
	return "\n".join(lines)

################################################################################

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

	def get_player_power(self, player):
		if (not "players" in self.config) or (not player in self.config["players"]):
			return None, f"Player {player}'s power missing from config"
		else:
			return self.config["players"][player], None

	def check_orders(self, power, orders):
		game = from_saved_game_format(self.database["game"])
		orders = orders.split('\n')

		try:
			game.set_orders(power, orders)
			errors = game.error
			valid_orders = game.get_orders(power)
			return valid_orders, errors
		except:
			return [], ["Error while reading orders"]

	def orders_to_text(self, player, power):

		lines = ["Orders for " + player + ":"]
		lines.append(power)
		for o in self.database["orders"][player]:
			lines.append(o)

		return "\n".join(lines)

################################################################################

	def setup_bot(self):
		intents = discord.Intents.default()
		intents.message_content = True
		bot = commands.Bot(command_prefix=self.config["prefix"], intents=intents)
		self.bot = bot

		@bot.event
		async def on_ready():
			print(f"Connected as {bot.user}")

		@bot.event
		async def on_command_error(ctx, error):
			await ctx.send("Error: " + str(error))

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

			text = gamestate_to_text(self.game)
			await ctx.send(text)

		@bot.command()
		async def status(ctx):
			"""Show the current phase

			Including how many players have submitted orders for it
			"""

			count = len(self.database["orders"])
			if count == 0:
				count = "No player has"
			elif count == 1:
				count = "One player has"
			else:
				count = f"{count} players have"

			text = f"Current phase is **{self.game.phase}**. {count} sent their orders."
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

			player = ctx.author.name
			power, err = self.get_player_power(player)
			if err:
				await ctx.send(err)
				return

			valid, errors = self.check_orders(power, orders)

			if len(errors) > 0:
				text = "\n".join(map(str, errors))
			else:
				self.database["orders"][player] = valid
				self.save_database()
				text = self.orders_to_text(player, power)

			await ctx.send(text)

		@bot.command()
		async def check(ctx):
			"""Check your orders for this phase"""

			player = ctx.author.name
			power, err = self.get_player_power(player)
			if err:
				await ctx.send(err)
				return

			if not player in self.database["orders"]:
				text = f"No orders sent for {player}"
			else:
				text = self.orders_to_text(player, power)

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
		async def hint(ctx, province):
			"""See all possible valid orders for a province

			Parameters
			----------
			province
				The abbreviation for the province
			"""

			hints = self.game.get_all_possible_orders()
			province = province.upper()
			if province in hints:
				if len(hints[province]) > 0:
					text = "\n".join(hints[province])
				else:
					text = "No orders possible for " + province
			else:
				text = "Unknown province: " + province

			await ctx.send(text)

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

			game = from_saved_game_format(self.database["game"])
			power = None

			for line in orders.split("\n"):
				line = line.upper()
				if line in game.powers.keys():
					power = line
				elif power != None and line != "":
					game.set_orders(power, line)

			if len(game.error) > 0:
				return "\n".join(map(str, game.error))

			game.process()
			text = format_order_results(game)
			await ctx.send(text)

		@bot.command()
		async def adjudicate(ctx):
			"""Adjudicate the current phase

			All currently submitted orders are resolved, their results displayed, along
			with the next game state. The phase progresses to the next.

			This can only be used on a public channel.
			"""

			if ctx.channel.type == discord.ChannelType.private:
				await ctx.send("Cannot adjudicate in a private channel")
				return

			for player, orders in self.database["orders"].items():
				power = self.config["players"][player]
				self.game.set_orders(power, orders)

			if len(self.game.error) > 0:
				await ctx.send("\n".join(map(str, game.error)))
				return

			self.game.process()
			self.database["orders"] = {}
			result = format_order_results(self.game)

			self.save_game()
			self.save_database()
			await ctx.send(result)

		@bot.command()
		async def dump(ctx):
			"""Send a JSON file for the current game state and its history"""

			text = json.dumps(self.database["game"])
			stream = io.StringIO(text)

			await ctx.send(file=discord.File(stream, filename="game.json"))


	def run_bot(self):
		self.bot.run(self.config["token"])

################################################################################

diplodocus = Diplodocus()
diplodocus.run_bot()
