import random
import json
import sys

sys.path.append('diplomacy')

from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format

game = Game(map_name='chasers.map')

#print(game.map.convoy_paths[10])

game.set_units('EMPIRE', ['A ANA', 'F IMP', 'F CHA'])
game.process()
#
# orders =  game.get_all_possible_orders()
# for x in orders:
#     print(x, orders[x])

game.set_orders("EMPIRE", [
    'A ANA - HOW',
    'F IMP C A ANA - HOW'
])

game.process()
print(game.get_state())

#to_saved_game_format(game, output_path='game.json')
