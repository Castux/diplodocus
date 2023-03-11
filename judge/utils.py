def gamestate_to_text(game):
	lines = []
	lines.append("**" + game.phase + "**\n")

	for name, power in game.powers.items():
		lines.append("__" + name + "__ (SCs: " + " ".join(power.centers) + ")" )
		lines.append("\n".join(power.units))

	return '\n'.join(lines)
