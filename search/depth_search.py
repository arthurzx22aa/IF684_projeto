from search.search import Search

class DFS(Search):

    def search(self, start, goal):
        stack = [start]
        came_from = {}
        came_from[start] = None
        visited_nodes = []
        path = []
        frontier_nodes = []

        while stack:
            current = stack.pop()
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
                    stack.append(next)
                    came_from[next] = current

        return path, visited_nodes, frontier_nodes
