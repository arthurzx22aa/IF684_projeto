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


def path_manhattan(start, end):
    path = []
    x1, y1 = start
    x2, y2 = end

    while x1 != x2:
        path.append((x1, y1))
        x1 += 1 if x1 < x2 else -1

    while y1 != y2:
        path.append((x1, y1))
        y1 += 1 if y1 < y2 else -1

    path.append((x2, y2))

    return path
