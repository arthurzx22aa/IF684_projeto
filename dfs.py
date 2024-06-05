class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # custo from start to current
        self.h = 0  # heuristic cost
        self.f = 0  # total cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f


def path_dfs(start, end, game_map):
    start_node = Node(start)
    end_node = Node(end)
    
    stack = [start_node]
    visited = set()

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # movimentos possíveis: esquerda, direita, cima, baixo

    while stack:
        current_node = stack.pop()
        current_position = current_node.position

        if current_position in visited:
            continue

        visited.add(current_position)

        if current_node == end_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # retorna o caminho reverso

        for direction in directions:
            neighbor_position = (current_position[0] + direction[0], current_position[1] + direction[1])
            if (0 <= neighbor_position[0] < len(game_map) and
                    0 <= neighbor_position[1] < len(game_map[0]) and
                    game_map[neighbor_position[1]][neighbor_position[0]].cost != -1):  # Verifica se não é obstáculo
                neighbor_node = Node(neighbor_position, current_node)
                stack.append(neighbor_node)

    return None  # se não encontrar um caminho
