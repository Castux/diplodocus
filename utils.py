from diplomacy.utils.export import to_saved_game_format, from_saved_game_format

def orders_to_text(player, power, database):

	lines = ["Orders for " + player + ":"]
	lines.append(power)
	for o in database["orders"][player]:
		lines.append(o)

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

def order_to_unit(order):
	return " ".join(order.split()[0:2])

def sanitize_result(r):
	r = str(r)
	if r == "":
		r = "OK"
	return r

def format_order_results(game):

	phase = game.get_phase_history()[-1]
#
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

def simulate(database, orders):

	game = from_saved_game_format(database["game"])
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
	return format_order_results(game)

def adjudicate(database, config, game):

	for player, orders in database["orders"].items():
		power = config["players"][player]
		game.set_orders(power, orders)

	if len(game.error) > 0:
		return "\n".join(map(str, game.error))

	game.process()
	database["orders"] = {}

	return format_order_results(game)
