from queue import PriorityQueue
from typing import Literal


def priority_search(
    game_map, start, goal, type: Literal["greedy", "a_star", "uniform"] = "greedy"
):

    def get_neighbors(pos):
        neighbors = []
        x, y = pos
        if x > 0 and game_map[y][x - 1].cost != -1:
            neighbors.append((x - 1, y))
        if x < len(game_map[0]) - 1 and game_map[y][x + 1].cost != -1:
            neighbors.append((x + 1, y))
        if y > 0 and game_map[y - 1][x].cost != -1:
            neighbors.append((x, y - 1))
        if y < len(game_map) - 1 and game_map[y + 1][x].cost != -1:
            neighbors.append((x, y + 1))
        return neighbors

    def manhattan_distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    visited_nodes = []
    frontier_nodes = []
    path = []

    while not frontier.empty():
        _, current = frontier.get()
        visited_nodes.append(current)

        if current == goal:
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()

            # remove visited nodes from frontier
            visited_nodes_set = set(visited_nodes)
            filtered_frontier = [
                [item for item in sublist if item not in visited_nodes_set]
                for sublist in frontier_nodes
            ]

            return path, visited_nodes, filtered_frontier

        neighbors = get_neighbors(current)
        frontier_nodes.append(neighbors)

        for next in neighbors:
            if type == "greedy":
                if next not in came_from:
                    priority = manhattan_distance(next, goal) # f(n) = h(n)
                    frontier.put((priority, next))
                    came_from[next] = current
            else:
                new_cost = cost_so_far[current] + game_map[next[1]][next[0]].cost
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    g_n = cost_so_far[next] # g(n)
                    h_n = manhattan_distance(next, goal) # h(n)
                    # para uniforme, f(n) = g(n), para a*, f(n) = g(n) + h(n)
                    priority = g_n if type == "uniform" else g_n + h_n 
                    frontier.put((priority, next))
                    came_from[next] = current

    return path, visited_nodes, frontier_nodes
