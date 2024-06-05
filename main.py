import sys
import pygame
from config import BLOCK_SIZE, WHITE
from elements import draw_player
from search.greedy_search import priority_search
from world import draw_highlight_overlay, draw_map, draw_overlay, draw_path, draw_steps, generate_map
from tile import MOUNTAIN_TILE, TILE_WEIGHTS, FOOD_TILE

# initialize pygame
pygame.init()

# generate map
map_size = 32  # size of the map
game_map = generate_map(map_size, TILE_WEIGHTS)

# screen dimensions based on game_map
SCREEN_WIDTH = len(game_map[0]) * BLOCK_SIZE
SCREEN_HEIGHT = len(game_map) * BLOCK_SIZE

# initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vizualizing Algorithms")

# initial agent position
agent_pos = [0, 0]

# main loop
running = True
overlay = False
highlight_overlay = False
food_position = None
path = []
current_step = 0
next_move_time = 0
move_delay = 100  # ms
original_tile = None

# create path surface
path_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
# path_surface.fill((0, 0, 0, 128)) # black

# create visited steps surface
visited_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
# visited_surface.fill((255, 255, 0, 128)) # yellow

# create marked nodes surface
marked_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
# marked_surface.fill((255, 0, 0, 255))  # red

finished_steps = False

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                agent_pos[0] = max(agent_pos[0] - 1, 0)
            elif event.key == pygame.K_RIGHT:
                agent_pos[0] = min(agent_pos[0] + 1, SCREEN_WIDTH - 1)
            elif event.key == pygame.K_UP:
                agent_pos[1] = max(agent_pos[1] - 1, 0)
            elif event.key == pygame.K_DOWN:
                agent_pos[1] = min(agent_pos[1] + 1, SCREEN_HEIGHT - 1)
            elif event.key == pygame.K_F1:
                overlay = not overlay
            elif event.key == pygame.K_F2:
                highlight_overlay = not highlight_overlay
        elif event.type == pygame.MOUSEBUTTONDOWN: # add food on mouse click
            if event.button == 1:  # left mouse button
                # get the position of the mouse click
                x, y = event.pos
                food_position = (x // BLOCK_SIZE, y // BLOCK_SIZE)

                # reset path variables
                current_step = 0 
                path = None
                current_step = 0
                finished_steps = False

                # set game map info with new food
                original_tile = game_map[food_position[1]][food_position[0]]
                game_map[food_position[1]][food_position[0]] = FOOD_TILE

                # call pathfinding algorithm
                path, visited_nodes, frontier_nodes = priority_search(game_map, tuple(agent_pos), food_position, "greedy")

                next_move_time = current_time + move_delay

    # path update logic
    if path is not None:
        # draw visited nodes
        if not finished_steps and food_position and current_step < len(visited_nodes):
            if current_time >= next_move_time:
                current_step += 1
                next_move_time = current_time + 10
            # all steps finished
            if current_step == len(visited_nodes):
                finished_steps = True
                current_step = 0
        # draw final path
        elif finished_steps and food_position and current_step < len(path):
            if current_time >= next_move_time:
                agent_pos = path[current_step]
                current_step += 1
                # update next move time
                # based on the cost of the current tile
                next_move_time = current_time + (move_delay * game_map[agent_pos[1]][agent_pos[0]].cost)
            # reset path variables
            if current_step == len(path): 
                game_map[food_position[1]][food_position[0]] = original_tile
                agent_pos = list(agent_pos)

    # draw map and player
    screen.fill(WHITE)
    draw_map(screen, game_map)
    draw_player(screen, agent_pos)
    if food_position:
        if not finished_steps:
            draw_steps(screen, visited_surface, marked_surface, visited_nodes, frontier_nodes, current_step)
        else: 
            draw_steps(screen, visited_surface, marked_surface, visited_nodes, frontier_nodes, len(visited_nodes))
            draw_path(screen, path_surface, path, current_step)

    # draw overlay if toggled
    if overlay:
        draw_overlay(screen, game_map, 20)
        
    # draw highlight overlay if toggled
    if highlight_overlay:
        draw_highlight_overlay(screen, agent_pos, len(game_map), len(game_map[0]))

    pygame.display.flip()

# quit pygame
pygame.quit()
sys.exit()
