import random
import pygame
from config import BLOCK_SIZE, LIGHT_GREEN, BLACK, LIGHT_YELLOW, ORANGE
from elements import draw_food, draw_tree, draw_stones, draw_mountain, draw_water

def generate_map(size, tile_weights=None):
    if tile_weights is None:
        tile_weights = {0: 1, 5: 1, 10: 1, -1: 1, 20: 1}  # default to equal weights

    tiles = [tile for tile, weight in tile_weights.items() for _ in range(weight)]
    game_map = [[random.choice(tiles) for _ in range(size)] for _ in range(size)]
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
