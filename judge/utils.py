def gamestate_to_text(game):
	lines = []
	lines.append("**" + game.phase + "**\n")

	for name, power in game.powers.items():
		lines.append("__" + name + "__ (SCs: " + " ".join(power.centers) + ")" )
		lines.append("\n".join(power.units))

	return '\n'.join(lines)


def get_ready_players_count(database):
	count = len(database["orders"])

	if count == 0:
		return "No player has"
	elif count == 1:
		return "One player has"
	else:
		return (count + " players have")

def save_orders(config, database, username, orders):
	if not "orders" in database:
		database["orders"] = {}

	database["orders"][username] = orders
