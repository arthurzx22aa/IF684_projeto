import random
import pygame
from config import BLOCK_SIZE, LIGHT_GREEN, BLACK, LIGHT_YELLOW, ORANGE
from elements import draw_food, draw_tree, draw_stones, draw_mountain, draw_water

def generate_map(size, tile_weights=None):
    if tile_weights is None:
        tile_weights = {0: 1, 5: 1, 10: 1, -1: 1, 20: 1}  # default to equal weights

    def place_cluster(map_data, tile, cluster_size, frequency):
        # place a number of cluster of tiles on the map, according to the frequency
        for _ in range(frequency):
            # select a random spot on the map
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            # place the cluster around that spot
            for _ in range(cluster_size):
                # check for map bounds
                if 0 <= x < size and 0 <= y < size:
                    map_data[y][x] = tile
                    x += random.choice([-1, 0, 1])
                    y += random.choice([-1, 0, 1])

    # initialize map with blank tiles
    game_map = [[0 for _ in range(size)] for _ in range(size)]

    total_weight = sum(tile_weights.values())

    # place water clusters
    water_weight = tile_weights.get(20, 1)
    place_cluster(game_map, 20, cluster_size=random.randint(3, 7), frequency=int((size**2 * (water_weight / total_weight))/4))

    # place mountain clusters
    mountain_weight = tile_weights.get(-1, 1)
    place_cluster(game_map, -1, cluster_size=random.randint(3, 5), frequency=int((size**2 * (mountain_weight / total_weight))/4))

    # place tree clusters near water
    tree_weight = tile_weights.get(5, 1)
    for y in range(size):
        for x in range(size):
            # find water tiles
            if game_map[y][x] == 20 and random.random() < 0.5:
                # place trees around it
                place_cluster(game_map, 5, cluster_size=random.randint(1, 3), frequency=tree_weight)

    # fill remaining tiles with blanks, and spread stones
    stone_weight = tile_weights.get(10, 1)
    for y in range(size):
        for x in range(size):
            if game_map[y][x] == 0:
                if random.random() < (0.1 * stone_weight):  # chance to place a stone based on weight
                    game_map[y][x] = 10

    return game_map

def draw_map(surface, game_map):
    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            x, y = col_index * BLOCK_SIZE, row_index * BLOCK_SIZE
            if tile == 5:
                draw_tree(surface, x, y)
            elif tile == 10:
                draw_stones(surface, x, y)
            elif tile == -1:
                draw_mountain(surface, x, y)
            elif tile == 20:
                draw_water(surface, x, y)
            elif tile == 99:
                draw_food(surface, x, y)
            else:
                pygame.draw.rect(surface, LIGHT_GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))

def draw_highlight_overlay(surface, player_pos, rows, cols):
    overlay_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    overlay_surface.fill((255, 255, 204, 128))  # Light yellow with transparency
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            col_index = (player_pos[0] // BLOCK_SIZE) + dx
            row_index = (player_pos[1] // BLOCK_SIZE) + dy
            if 0 <= col_index < cols and 0 <= row_index < rows:
                x = col_index * BLOCK_SIZE
                y = row_index * BLOCK_SIZE
                surface.blit(overlay_surface, (x, y))
                pygame.draw.rect(surface, ORANGE, (x, y, BLOCK_SIZE, BLOCK_SIZE), 3)
