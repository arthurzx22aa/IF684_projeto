import pygame
from config import BLOCK_SIZE, GREEN

def draw_player(surface, position):
    player_rect = pygame.Rect(position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(surface, GREEN, player_rect)