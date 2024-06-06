import pygame
from config import BLACK, BLOCK_SIZE, GREEN, RED, WHITE

def draw_player(surface, position):
    player_rect = pygame.Rect(position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(surface, BLACK, player_rect)
    pygame.draw.rect(surface, WHITE, player_rect, 4)