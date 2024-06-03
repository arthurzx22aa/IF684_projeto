import pygame
from config import BLOCK_SIZE, BROWN, GREEN, GREY, BLACK, LIGHT_GREEN, LIGHT_GREY, LIGHT_BROWN, LIGHT_BLUE, BLUE, ORANGE

def draw_tree(surface, x, y):
    pygame.draw.rect(surface, LIGHT_GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))
    trunk_rect = pygame.Rect(x + BLOCK_SIZE // 2 - 5, y + BLOCK_SIZE // 2, 10, BLOCK_SIZE // 2)
    pygame.draw.rect(surface, BROWN, trunk_rect)
    points = [(x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 4), (x + BLOCK_SIZE // 4, y + BLOCK_SIZE // 2),
              (x + 3 * BLOCK_SIZE // 4, y + BLOCK_SIZE // 2)]
    pygame.draw.polygon(surface, GREEN, points)

def draw_stones(surface, x, y):
    pygame.draw.rect(surface, LIGHT_GREY, (x, y, BLOCK_SIZE, BLOCK_SIZE))
    small_stone = pygame.Rect(x + BLOCK_SIZE // 4, y + 3 * BLOCK_SIZE // 4, 10, 10)
    large_stone = pygame.Rect(x + BLOCK_SIZE // 2, y + 3 * BLOCK_SIZE // 4 - 5, 15, 15)
    pygame.draw.rect(surface, GREY, small_stone)
    pygame.draw.rect(surface, GREY, large_stone)

def draw_mountain(surface, x, y):
    pygame.draw.rect(surface, LIGHT_BROWN, (x, y, BLOCK_SIZE, BLOCK_SIZE))
    points = [(x + BLOCK_SIZE // 2, y), (x, y + BLOCK_SIZE), (x + BLOCK_SIZE, y + BLOCK_SIZE)]
    pygame.draw.polygon(surface, BROWN, points)

def draw_water(surface, x, y):
    pygame.draw.rect(surface, LIGHT_BLUE, (x, y, BLOCK_SIZE, BLOCK_SIZE))

def draw_overlay(surface, game_map):
    font = pygame.font.Font(None, 36)
    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            number = tile
            x, y = col_index * BLOCK_SIZE, row_index * BLOCK_SIZE
            text = font.render(str(number), True, BLACK)
            text_rect = text.get_rect(center=(x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 4))
            surface.blit(text, text_rect)

def draw_player(surface, position):
    player_rect = pygame.Rect(position[0], position[1], BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(surface, GREEN, player_rect)

def draw_food(surface, x, y):
    pygame.draw.rect(surface, ORANGE, (x, y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.circle(surface, BLACK, (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2), BLOCK_SIZE // 3)