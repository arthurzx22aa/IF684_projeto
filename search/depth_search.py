from search.search import Search

class DFS(Search):

    def search(self, game_map, start, goal):
        stack = [start]
        came_from = {}
        came_from[start] = None
        visited_nodes = []
        path = []

        while stack:
            current = stack.pop()
            visited_nodes.append(current)

            neighbors = self.get_neighbors(current)

            if current == goal:
                while current:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path, visited_nodes

            for next in neighbors:
                if next not in came_from:
                    stack.append(next)
                    came_from[next] = current

        return path, visited_nodes
