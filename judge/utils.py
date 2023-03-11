from diplomacy.utils.export import to_saved_game_format, from_saved_game_format

def gamestate_to_text(game):
	lines = []
	lines.append("**" + game.phase + "**\n")

	for name, power in game.powers.items():
		lines.append(name + " (SCs: " + " ".join(power.centers) + ")" )
		lines.append("\n".join(power.units))
		lines.append("")

	return '\n'.join(lines)


def get_ready_players_count(database):
	count = len(database["orders"])

	if count == 0:
		return "No player has"
	elif count == 1:
		return "One player has"
	else:
		return (count + " players have")

def get_player_power(config, ctx):
	player = ctx.author.name
	if (not "players" in config) or (not player in config["players"]):
		return None, None, f"Player {player}'s power missing from config"

	return player, config["players"][player], None

def check_orders(database, power, orders):
	game = from_saved_game_format(database["game"])
	orders = orders.split('\n')

	try:
		game.set_orders(power, orders)
		errors = game.error
		valid_orders = game.get_orders(power)
		return valid_orders, errors
	except:
		return [], ["Error while reading orders"]

def save_orders(config, database, username, orders):
	if not "orders" in database:
		database["orders"] = {}

	database["orders"][username] = orders

def orders_to_text(player, power, database):

	lines = ["Orders for " + player + ":"]
	lines.append(power)
	for o in database["orders"][player]:
		lines.append("\t" + o)

	return "\n".join(lines)

def get_hint_for_province(game, prov):
	hints = game.get_all_possible_orders()

	if prov == None:
		text = "Missing province name"
	else:
		prov = prov.upper()
		if prov in hints:
			if len(hints[prov]) > 0:
				text = "\n".join(hints[prov])
			else:
				text = "No orders possible for " + prov
		else:
			text = "Unknown province: " + prov

	return text

def simulate(database, orders):

	game = from_saved_game_format(database["game"])
	power = None

	for line in orders.split("\n"):
		if line in game.powers.keys():
			power = line
		elif power != None and line != "":
			game.set_orders(power, line)

	if len(game.error) > 0:
		return "\n".join(map(str, game.error))

	lines = []
	for power, porders in game.get_orders().items():
		lines.append(power)
		for o in porders:
			lines.append("\t" + o)
		lines.append("")

	game.process()
	statuses = game.get_order_status()
	lines += ["\n", gamestate_to_text(game)]

	return "\n".join(lines)
