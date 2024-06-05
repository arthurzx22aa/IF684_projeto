from collections import deque as queue


def bfs_search(map, start_point, goal):
    size = len(map)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queu = queue()
    x, y = start_point
    start = (x,y)
    queu.append((start, [start]))
    explored = set()


    def bounds(x, y):
        return 0 <= x < size and 0 <= y < size
   
    while queu:
        current_pos, path = queu.popleft()
        if current_pos in explored:
            continue
        explored.add(current_pos)

        if current_pos == goal:
            print(queu)
            return path
            
        x, y = current_pos
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if bounds(nx, ny) and (nx, ny) not in explored:
                queu.append(((nx, ny), path + [(nx, ny)]))

 
