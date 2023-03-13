from diplomacy.utils.export import to_saved_game_format, from_saved_game_format


def adjudicate(database, config, game):

	for player, orders in database["orders"].items():
		power = config["players"][player]
		game.set_orders(power, orders)

	if len(game.error) > 0:
		return "\n".join(map(str, game.error))

	game.process()
	database["orders"] = {}

	return format_order_results(game)
