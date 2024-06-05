from typing import Literal, Tuple


class Search:
    def __init__(self, game_map, heuristic: Literal["manhattan", "euclidean"] = "manhattan"):
        self.game_map = game_map
        self.heuristic = heuristic

    def search(self, start, goal):
        pass

    def get_neighbors(self, position: Tuple):
        neighbors = []
        x, y = position
        if x > 0 and self.game_map[y][x - 1].cost != -1:
            neighbors.append((x - 1, y))
        if x < len(self.game_map[0]) - 1 and self.game_map[y][x + 1].cost != -1:
            neighbors.append((x + 1, y))
        if y > 0 and self.game_map[y - 1][x].cost != -1:
            neighbors.append((x, y - 1))
        if y < len(self.game_map) - 1 and self.game_map[y + 1][x].cost != -1:
            neighbors.append((x, y + 1))
        return neighbors

    def get_heuristic(self, a, b):
        if self.heuristic == "manhattan":
            return self.manhattan_distance(a, b)
        elif self.heuristic == "euclidean":
            return self.euclidean_distance(a, b)
        
    def manhattan_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def euclidean_distance(self, a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
