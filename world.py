import random

def generate_map(size, tile_weights=None):
    if tile_weights is None:
        tile_weights = {0: 1, 5: 1, 10: 1, -1: 1, 20: 1}  # default to equal weights

    tiles = [tile for tile, weight in tile_weights.items() for _ in range(weight)]
    game_map = [[random.choice(tiles) for _ in range(size)] for _ in range(size)]
    return game_map
