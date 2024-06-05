import random
import pygame
from typing import List
from config import BLACK, BLOCK_SIZE, GREEN, LIGHT_YELLOW, ORANGE, OVERLAY_FONT_SIZE, RED, WHITE, YELLOW
from tile import Tile, BLANK_TILE, TREE_TILE, STONE_TILE, MOUNTAIN_TILE, WATER_TILE, TILE_WEIGHTS
from utils import interpolate_color

def generate_map(size, tile_weights=None):
    if tile_weights is None:
        tile_weights = TILE_WEIGHTS

    def place_cluster(map_data, tile, cluster_size, frequency):
        for _ in range(frequency):
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            for _ in range(cluster_size):
                if 0 <= x < size and 0 <= y < size:
                    map_data[y][x] = tile
                    x += random.choice([-1, 0, 1])
                    y += random.choice([-1, 0, 1])

    # initialize map with blank tiles
    game_map: List[List[Tile]] = [[BLANK_TILE for _ in range(size)] for _ in range(size)]

    total_weight = sum(tile_weights.values())

    # place water clusters
    water_weight = tile_weights.get(WATER_TILE, 1)
    place_cluster(game_map, WATER_TILE, cluster_size=random.randint(3, 7), frequency=int((size**2 * (water_weight / total_weight))/4))

    # place mountain clusters
    mountain_weight = tile_weights.get(MOUNTAIN_TILE, 1)
    place_cluster(game_map, MOUNTAIN_TILE, cluster_size=random.randint(3, 5), frequency=int((size**2 * (mountain_weight / total_weight))/4))

    # place tree clusters near water
    tree_weight = tile_weights.get(TREE_TILE, 1)
    for y in range(size):
        for x in range(size):
            if game_map[y][x].tile_id == WATER_TILE.tile_id and random.random() < 0.5:
                place_cluster(game_map, TREE_TILE, cluster_size=random.randint(1, 3), frequency=tree_weight)

    # spread stones
    stone_weight = tile_weights.get(STONE_TILE, 1)
    for y in range(size):
        for x in range(size):
            if game_map[y][x].tile_id == BLANK_TILE.tile_id:
                if random.random() < (0.1 * stone_weight):  # chance to place a stone based on weight
                    game_map[y][x] = STONE_TILE

    return game_map

def draw_map(surface, game_map):
    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            x, y = col_index * BLOCK_SIZE, row_index * BLOCK_SIZE
            tile.draw(surface, x, y)

def draw_highlight_overlay(surface, player_pos, rows, cols):
    overlay_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    overlay_surface.fill((255, 255, 204, 128))
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


def draw_overlay(surface, game_map, max_cost):
    font = pygame.font.Font(None, OVERLAY_FONT_SIZE)
    padding = 4  # padding around the text box

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            number = tile.cost
            x, y = col_index * BLOCK_SIZE, row_index * BLOCK_SIZE
            text_color, bg_color = interpolate_color(number, max_cost)
            text = font.render(str(number), True, text_color)
            text_rect = text.get_rect(center=(x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 4))

            # create the background box
            bg_rect = pygame.Rect(
                text_rect.left - padding,
                text_rect.top - padding,
                text_rect.width + 2 * padding,
                text_rect.height + 2 * padding
            )

            # draw background box
            bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill(bg_color)
            surface.blit(bg_surface, bg_rect.topleft)

            # draw the text
            surface.blit(text, text_rect)


def draw_path(screen, surface, path, current_step):
    for step in range(current_step):
        x, y = path[step]
        center_x = x * BLOCK_SIZE + BLOCK_SIZE // 2
        center_y = y * BLOCK_SIZE + BLOCK_SIZE // 2
        pygame.draw.circle(screen, BLACK, (center_x, center_y), BLOCK_SIZE // 4 + 2)
        pygame.draw.circle(screen, WHITE, (center_x, center_y), BLOCK_SIZE // 4)
        screen.blit(surface, (x * BLOCK_SIZE, y * BLOCK_SIZE))

def draw_steps(screen, surface_visited, surface_target, visited, frontiers, current_step):
    pygame.draw.rect(surface_target, RED + (180,), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 5)
    pygame.draw.rect(surface_visited, YELLOW + (180,), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 5)
    for step in range(current_step - 1):
        for node in range(len(frontiers[step])):
            x, y = frontiers[step][node]
            screen.blit(surface_target, (x * BLOCK_SIZE, y * BLOCK_SIZE))
    for step in range(current_step):
        position = visited[step]
        screen.blit(surface_visited, (position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE))