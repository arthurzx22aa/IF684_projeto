from collections import deque
from search.search import Search


class Breadth(Search):

    def search(self, start, goal):
        frontier = deque([start])
        came_from = {}
        came_from[start] = None
        visited_nodes = []
        frontier_nodes = []
        path = []

        while frontier:
            current = frontier.popleft()
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
                if next not in came_from:
                    frontier.append(next)
                    came_from[next] = current
                    
        return path, visited_nodes, frontier_nodes