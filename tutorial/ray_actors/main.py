import ray, time, statistics, sys, os
import numpy as np
import os

# for library helper functions
sys.path.append(".") 

# import utils from game_of_life.py
from game_of_life import Game, State, ConwaysRules

# import utils from actor_util
from actor_util import new_game_of_life_graph, new_game_of_life_grid, run_games, run_ray_games, show_cmap

# main body
steps = 100
game_size = 100
plot_size = 800
max_cell_age = 10
use_fixed_cell_sizes = True

# Color maps from Bokeh: 
cmap = 'RdYlBu' # others: 'Turbo' 'YlOrBr'
bgcolor = '#C0CfC8' # a greenish color, but not great for forms of red-green color blindness, where 'white' is better.

# A custom color map created at https://projects.susielu.com/viz-palette. Works best with white or dark grey background
#cmap=['#ffd700', '#ffb14e', '#fa8775', '#ea5f94', '#cd34b5', '#9d02d7', '#0000ff']
#bgcolor = 'darkgrey' # 'white'

def new_game(game_size):
    initial_state = State(size = game_size)
    rules = ConwaysRules()
    game  = Game(initial_state=initial_state, rules=rules)
    return game

game = new_game(10)
print(game.states[0])

_, graphs = new_game_of_life_grid(game_size, plot_size, x_grid=1, y_grid=1, shrink_factor=1.0,
                                  bgcolor=bgcolor, cmap=cmap,
                                  use_fixed_cell_sizes=use_fixed_cell_sizes, max_cell_age=max_cell_age)
graphs[0]

def do_trial(graphs, num_games=1, steps=steps, batch_size=1, game_size_for_each=game_size, pause_between_batches=0.0):
    games = [new_game(game_size_for_each) for _ in range(num_games)]
    return run_games(games, graphs, steps, batch_size, pause_between_batches)

# num_games, steps, batch_size, duration = do_trial(graphs, steps=steps, pause_between_batches=0.1)
# num_games, steps, batch_size, duration