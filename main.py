import copy
from random import randint
import sys
import pygame
from config import BLACK, BLOCK_SIZE, WHITE
from elements import draw_player
from menu import draw_food_helper, draw_heuristic_menu, draw_info, draw_menu
from search.breadth_search import Breadth
from search.depth_search import DFS
from search.priority_search import PrioritySearch
from world import draw_highlight_overlay, draw_map, draw_overlay, draw_path, draw_steps, generate_map
from tile import MOUNTAIN_TILE, TILE_WEIGHTS, FOOD_TILE
import bfs


# initialize pygame
pygame.init()

# generate map
map_size = 32  # size of the map
game_map = generate_map(map_size, TILE_WEIGHTS)
original_map = copy.deepcopy(game_map)

# screen dimensions based on game_map
SCREEN_WIDTH = len(game_map[0]) * BLOCK_SIZE
SCREEN_HEIGHT = len(game_map) * BLOCK_SIZE

# initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vizualizing Algorithms")

# set initial agent position (can't be obstructed)
while True:
    agent_pos = [randint(0, map_size - 1), randint(0, map_size - 1)]
    if game_map[agent_pos[1]][agent_pos[0]].cost != -1:
        break

# set font
menu_font = pygame.font.Font(None, 36)

# main loop
running = True
algorithm_selected = None
heuristic_selected = None


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

finished_steps = True
can_walk = True # flag to allow player movement

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if can_walk and algorithm_selected and heuristic_selected:
                if (event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
                    # reset path variables on move
                    path = None
                    current_step = 0
                    finished_steps = False

                # move player
                if event.key == pygame.K_LEFT:
                    blocked = game_map[agent_pos[1]][agent_pos[0] - 1].cost == -1
                    agent_pos[0] = max(agent_pos[0] - 1, 0) if not blocked else agent_pos[0]
                elif event.key == pygame.K_RIGHT:
                    blocked = game_map[agent_pos[1]][agent_pos[0] + 1].cost == -1
                    agent_pos[0] = min(agent_pos[0] + 1, SCREEN_WIDTH - 1) if not blocked else agent_pos[0]
                elif event.key == pygame.K_UP:
                    blocked = game_map[agent_pos[1] - 1][agent_pos[0]].cost == -1
                    agent_pos[1] = max(agent_pos[1] - 1, 0) if not blocked else agent_pos[1]
                elif event.key == pygame.K_DOWN:
                    blocked = game_map[agent_pos[1] + 1][agent_pos[0]].cost == -1
                    agent_pos[1] = min(agent_pos[1] + 1, SCREEN_HEIGHT - 1) if not blocked else agent_pos[1]
                    
            # overlay keys
            if event.key == pygame.K_F1 and algorithm_selected and heuristic_selected:
                overlay = not overlay
            if event.key == pygame.K_F2 and algorithm_selected and heuristic_selected:
                highlight_overlay = not highlight_overlay

            # menu keys (algorithms)
            if event.key == pygame.K_b:
                algorithm_selected = "bfs"
                heuristic_selected = True
            elif event.key == pygame.K_d:
                algorithm_selected = "dfs"
                heuristic_selected = True
            elif event.key == pygame.K_a:
                algorithm_selected = "a_star"
            elif event.key == pygame.K_u:
                algorithm_selected = "uniform"
            elif event.key == pygame.K_g:
                algorithm_selected = "greedy"
            elif event.key == pygame.K_r:
                game_map = generate_map(map_size, TILE_WEIGHTS)
                # reset path variables
                path = None
                current_step = 0
                finished_steps = False
                can_walk = True
                # set initial agent position (can't be obstructed)
                while True:
                    agent_pos = [randint(0, map_size - 1), randint(0, map_size - 1)]
                    if game_map[agent_pos[1]][agent_pos[0]].cost != -1:
                        break

            # menu keys (heuristics)
            elif event.key == pygame.K_m and algorithm_selected:
                heuristic_selected = "manhattan"
            elif event.key == pygame.K_e and algorithm_selected:
                heuristic_selected = "euclidean"
            
            # esc to go back to menu
            elif event.key == pygame.K_ESCAPE:
                # if already in menu, close
                if algorithm_selected is None and heuristic_selected is None:
                    running = False
                # else, just clear the selections
                algorithm_selected = None
                heuristic_selected = None

            
        elif event.type == pygame.MOUSEBUTTONDOWN and algorithm_selected and heuristic_selected: 
            # add food on mouse click
            if event.button == 1:  # left mouse button
                # get the position of the mouse click
                x, y = event.pos

                # check if the tile is not obstructed
                if game_map[y // BLOCK_SIZE][x // BLOCK_SIZE].cost == -1:
                    continue

                food_position = (x // BLOCK_SIZE, y // BLOCK_SIZE)

                # reset path variables
                path = None
                current_step = 0
                finished_steps = False
                can_walk = False

                # set game map info with new food
                game_map[food_position[1]][food_position[0]] = FOOD_TILE

                # call pathfinding algorithm
                priority_search = PrioritySearch(game_map, heuristic_selected) # type: ignore
                depth_search = DFS(game_map)
                breadth_search = Breadth(game_map)

                match algorithm_selected:
                    case "a_star":
                        path, visited_nodes, frontier_nodes = priority_search.search(tuple(agent_pos), food_position, "a_star")
                    case "greedy":
                        path, visited_nodes, frontier_nodes = priority_search.search(tuple(agent_pos), food_position, "greedy")
                    case "bfs":
                        path, visited_nodes, frontier_nodes = breadth_search.search(tuple(agent_pos), food_position)
                    case "dfs":
                        path, visited_nodes, frontier_nodes = depth_search.search(tuple(agent_pos), food_position)
                    case "uniform":
                        path, visited_nodes, frontier_nodes = priority_search.search(tuple(agent_pos), food_position, "uniform")

                next_move_time = current_time + move_delay
            if event.button == 3 and can_walk: # right mouse button
                # teleport agent
                x, y = event.pos

                # check if the tile is not obstructed
                if game_map[y // BLOCK_SIZE][x // BLOCK_SIZE].cost == -1:
                    continue

                # place agent
                agent_pos = [x // BLOCK_SIZE, y // BLOCK_SIZE]

    if algorithm_selected is None and heuristic_selected is None:
        draw_menu(screen, menu_font, SCREEN_HEIGHT, SCREEN_WIDTH)
    elif heuristic_selected is None:
        draw_heuristic_menu(screen, menu_font, SCREEN_HEIGHT, SCREEN_WIDTH)
    
    else:
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
                    next_move_time = current_time + (move_delay * game_map[agent_pos[1]][agent_pos[0]].cost / 2)
                # reset path variables
                if current_step == len(path): 
                    agent_pos = list(agent_pos)
                    can_walk = True
        
        # eat food
        if game_map[agent_pos[1]][agent_pos[0]].tile_id == FOOD_TILE.tile_id:
            game_map[agent_pos[1]][agent_pos[0]] = original_map[agent_pos[1]][agent_pos[0]]

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

        # draw food helper text
        draw_food_helper(screen, menu_font)

        # draw info text
        draw_info(screen, menu_font, algorithm_selected, heuristic_selected, SCREEN_WIDTH)

    pygame.display.flip()

# quit pygame
pygame.quit()
sys.exit()
