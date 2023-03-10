import random
import json

from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format

game = Game(map_name='chasers.map')


print(game.get_all_possible_orders())
