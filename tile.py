import pygame
from config import BLOCK_SIZE, BROWN, GREEN, GREY, BLACK, LIGHT_GREEN, LIGHT_GREY, LIGHT_BROWN, LIGHT_BLUE, BLUE, ORANGE

class Tile:
    def __init__(self, id, cost):
        self.tile_id = id
        self.cost = cost

    def draw(self, surface, x, y):
        pass

class BlankTile(Tile):
    def __init__(self):
        super().__init__(id=0, cost=0)

    def draw(self, surface, x, y):
        pygame.draw.rect(surface, LIGHT_GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))

class TreeTile(Tile):
    def __init__(self):
        super().__init__(id=5, cost=5)

    def draw(self, surface, x, y):
        pygame.draw.rect(surface, LIGHT_GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        trunk_rect = pygame.Rect(x + BLOCK_SIZE // 2 - 5, y + BLOCK_SIZE // 2, 10, BLOCK_SIZE // 2)
        pygame.draw.rect(surface, BROWN, trunk_rect)
        points = [(x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 4), (x + BLOCK_SIZE // 4, y + BLOCK_SIZE // 2),
                  (x + 3 * BLOCK_SIZE // 4, y + BLOCK_SIZE // 2)]
        pygame.draw.polygon(surface, GREEN, points)

class StoneTile(Tile):
    def __init__(self):
        super().__init__(id=10, cost=10)

    def draw(self, surface, x, y):
        pygame.draw.rect(surface, LIGHT_GREY, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        small_stone = pygame.Rect(x + BLOCK_SIZE // 4, y + 3 * BLOCK_SIZE // 4, 10, 10)
        large_stone = pygame.Rect(x + BLOCK_SIZE // 2, y + 3 * BLOCK_SIZE // 4 - 5, 15, 15)
        pygame.draw.rect(surface, GREY, small_stone)
        pygame.draw.rect(surface, GREY, large_stone)

class MountainTile(Tile):
    def __init__(self):
        super().__init__(id=30, cost=-1)

    def draw(self, surface, x, y):
        pygame.draw.rect(surface, LIGHT_BROWN, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        points = [(x + BLOCK_SIZE // 2, y), (x, y + BLOCK_SIZE), (x + BLOCK_SIZE, y + BLOCK_SIZE)]
        pygame.draw.polygon(surface, BROWN, points)

class WaterTile(Tile):
    def __init__(self):
        super().__init__(id=20, cost=20)

    def draw(self, surface, x, y):
        pygame.draw.rect(surface, LIGHT_BLUE, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.polygon(surface, BLUE, [(x + BLOCK_SIZE // 4, y + BLOCK_SIZE // 2), (x + BLOCK_SIZE // 8, y + BLOCK_SIZE // 4), (x + 3 * BLOCK_SIZE // 8, y + BLOCK_SIZE // 2)])
        pygame.draw.polygon(surface, BLUE, [(x + 3 * BLOCK_SIZE // 4, y + BLOCK_SIZE // 2), (x + 5 * BLOCK_SIZE // 8, y + BLOCK_SIZE // 4), (x + 7 * BLOCK_SIZE // 8, y + BLOCK_SIZE // 2)])

class FoodTile(Tile):
    def __init__(self):
        super().__init__(id=99, cost=0)

    def draw(self, surface, x, y):
        pygame.draw.rect(surface, LIGHT_GREY, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.circle(surface, BLACK, (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2), BLOCK_SIZE // 4)
        pygame.draw.circle(surface, ORANGE, (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2), BLOCK_SIZE // 4, 2)
        pygame.draw.rect(surface, ORANGE, (x, y, BLOCK_SIZE, BLOCK_SIZE), 6)

# tile definitions
BLANK_TILE = BlankTile()
TREE_TILE = TreeTile()
STONE_TILE = StoneTile()
MOUNTAIN_TILE = MountainTile()
WATER_TILE = WaterTile()
FOOD_TILE = FoodTile()

# tile weights
TILE_WEIGHTS = {
    BLANK_TILE: 2,   # blank
    TREE_TILE: 1,    # trees
    STONE_TILE: 1,   # stones
    MOUNTAIN_TILE: 1, # mountains
    WATER_TILE: 1    # water
}
