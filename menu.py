import pygame
from config import BLACK, RED, WHITE


def draw_menu(screen, font, SCREEN_HEIGHT, SCREEN_WIDTH):
    
    screen.fill(WHITE)
    wm1 = "Welcome to the algorithm visualizer!"
    wm2 = "Press one of the following keys to visualize an algorithm."
    wm1f = font.render(wm1, True, BLACK)
    wm2f = font.render(wm2, True, BLACK)
    options = [
        ("B", "for BFS"),
        ("D", "for DFS"),
        ("A", "for A*"),
        ("U", "for Uniform"),
        ("G", "for Greedy"),
        ("R", "to generate a new map"),
    ]
    info1 = "Press F1 to see tile weight information"
    info2 = "Click anywhere to create food"
    info3 = "Right click anywhere to teleport agent"
    
    screen.blit(wm1f, (SCREEN_WIDTH // 2 - wm1f.get_width() // 2, SCREEN_HEIGHT // 2 - 200))
    screen.blit(wm2f, (SCREEN_WIDTH // 2 - wm2f.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
    
    y_offset = SCREEN_HEIGHT // 2 - 50
    for key, desc in options:
        draw_key(screen, font, y_offset, key, desc, SCREEN_WIDTH)
        y_offset += 50
    
    info1_f = font.render(info1, True, BLACK)
    info2_f = font.render(info2, True, BLACK)
    info3_f = font.render(info3, True, BLACK)
    screen.blit(info1_f, (SCREEN_WIDTH // 2 - info1_f.get_width() // 2, SCREEN_HEIGHT - 150))
    screen.blit(info2_f, (SCREEN_WIDTH // 2 - info2_f.get_width() // 2, SCREEN_HEIGHT - 100))
    screen.blit(info3_f, (SCREEN_WIDTH // 2 - info3_f.get_width() // 2, SCREEN_HEIGHT - 50))

def draw_heuristic_menu(screen, font, SCREEN_HEIGHT, SCREEN_WIDTH):
    screen.fill(WHITE)
    message = "Select Heuristic"
    message_surf = font.render(message, True, BLACK)
    options = [
        ("M", "for Manhattan"),
        ("E", "for Euclidean"),
    ]
    
    screen.blit(message_surf, (SCREEN_WIDTH // 2 - message_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    
    y_offset = SCREEN_HEIGHT // 2 - 50
    for key, desc in options:
        draw_key(screen, font, y_offset, key, desc, SCREEN_WIDTH)
        y_offset += 50
    
def draw_key(screen, font, y_offset, key, desc, SCREEN_WIDTH):
    key_surf = font.render(key, True, RED)
    desc_surf = font.render(f" {desc}", True, BLACK)
    
    key_rect = key_surf.get_rect(topleft=(SCREEN_WIDTH // 2 - 100, y_offset))
    pygame.draw.rect(screen, BLACK, key_rect.inflate(10, 10), 2)
    
    screen.blit(key_surf, (SCREEN_WIDTH // 2 - 100, y_offset))
    screen.blit(desc_surf, (SCREEN_WIDTH // 2 - 50, y_offset))

def draw_food_helper(screen, font):
    message = "Click anywhere to create food"
    message_surf = font.render(message, True, BLACK)
    message_width = message_surf.get_width() + 20
    message_height = message_surf.get_height() + 20
    
    food_surface = pygame.Surface((message_width, message_height), pygame.SRCALPHA)
    food_surface.fill((255, 255, 255, 128))
    pygame.draw.rect(food_surface, BLACK, food_surface.get_rect(), 2)
    
    food_surface.blit(message_surf, (10, 10))
    screen.blit(food_surface, (0, 0))
    return food_surface

def draw_info(screen, font, algorithm, heuristic, SCREEN_WIDTH):
    algorithm_message = f"Algorithm: {algorithm}"
    heuristic_message = f"Heuristic: {heuristic if isinstance(heuristic, str) else 'N/A'}"
    
    algorithm_f = font.render(algorithm_message, True, BLACK)
    heuristic_f = font.render(heuristic_message, True, BLACK)
    
    # get text width to scale the window
    max_width = max(algorithm_f.get_width(), heuristic_f.get_width()) + 20
    total_height = algorithm_f.get_height() + heuristic_f.get_height() + 30
    
    info_surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
    info_surface.fill((255, 255, 255, 128))
    pygame.draw.rect(info_surface, BLACK, info_surface.get_rect(), 2)

    info_surface.blit(algorithm_f, (10, 10))
    info_surface.blit(heuristic_f, (10, algorithm_f.get_height() + 20))

    screen.blit(info_surface, (SCREEN_WIDTH - max_width - 10, 10))