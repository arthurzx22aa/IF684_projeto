from queue import PriorityQueue
from typing import Literal
from search.search import Search


class PrioritySearch(Search):

    def search(
        self, start, goal, type: Literal["greedy", "a_star", "uniform"] = "greedy"
    ):

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
            neighbors = self.get_neighbors(current)
            frontier_nodes.append(neighbors)

            if current == goal:
                while current:
                    path.append(current)
                    current = came_from[current]
                path.reverse()

                return path, visited_nodes, frontier_nodes            

            for next in neighbors:
                if type == "greedy":
                    if next not in came_from:
                        priority = self.get_heuristic(next, goal)  # f(n) = h(n)
                        frontier.put((priority, next))
                        came_from[next] = current
                else:
                    new_cost = (
                        cost_so_far[current] + self.game_map[next[1]][next[0]].cost
                    )
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        g_n = cost_so_far[next]  # g(n)
                        h_n = self.get_heuristic(next, goal)  # h(n)
                        # para uniforme, f(n) = g(n), para a*, f(n) = g(n) + h(n)
                        priority = g_n if type == "uniform" else g_n + h_n
                        frontier.put((priority, next))
                        came_from[next] = current

        return path, visited_nodes, frontier_nodes
