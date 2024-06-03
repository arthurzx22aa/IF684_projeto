import pygame
import sys
from config import BLOCK_SIZE, WHITE, BLACK, GREEN
from elements import draw_map, draw_overlay, draw_player, draw_highlight_overlay
from world import generate_map

# initialize pygame
pygame.init()

# define tile weights
tile_weights = {
    0: 2,   # blank
    5: 1,   # trees
    10: 1,  # stones
    -1: 1,  # mountains
    20: 1   # water
}

# generate map
map_size = 32  # size of the map
game_map = generate_map(map_size, tile_weights)

# screen dimensions based on game_map
SCREEN_WIDTH = len(game_map[0]) * BLOCK_SIZE
SCREEN_HEIGHT = len(game_map) * BLOCK_SIZE

# initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid with Movable Block, Trees, Stones, Mountains, and Water")

# Initial position of the green block
agent_pos = [0, 0]

# main loop
running = True
overlay = False
highlight_overlay = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                agent_pos[0] = max(agent_pos[0] - BLOCK_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                agent_pos[0] = min(agent_pos[0] + BLOCK_SIZE, SCREEN_WIDTH - BLOCK_SIZE)
            elif event.key == pygame.K_UP:
                agent_pos[1] = max(agent_pos[1] - BLOCK_SIZE, 0)
            elif event.key == pygame.K_DOWN:
                agent_pos[1] = min(agent_pos[1] + BLOCK_SIZE, SCREEN_HEIGHT - BLOCK_SIZE)
            elif event.key == pygame.K_F1:
                overlay = not overlay
            elif event.key == pygame.K_F2:
                highlight_overlay = not highlight_overlay

    # clear screen
    screen.fill(WHITE)

    # draw the map
    draw_map(screen, game_map)

    # draw the agent
    draw_player(screen, agent_pos)

    # draw overlay if toggled
    if overlay:
        draw_overlay(screen, game_map)
        
    # draw highlight overlay if toggled
    if highlight_overlay:
        draw_highlight_overlay(screen, agent_pos, len(game_map), len(game_map[0]))

    # update the display
    pygame.display.flip()

# quit pygame
pygame.quit()
sys.exit()
