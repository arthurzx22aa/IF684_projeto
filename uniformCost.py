import heapq

def uniform_cost_search(game_map, start, goal):
    size = len(game_map)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def in_bounds(x, y):
        return 0 <= x < size and 0 <= y < size
    
    priority_queue = [(0, start, [start])]
    visited = set()
    
    while priority_queue:
        current_cost, current_pos, path = heapq.heappop(priority_queue)
        if current_pos in visited:
            continue
        visited.add(current_pos)
        
        if current_pos == goal:
            return path, current_cost
        
        x, y = current_pos
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and (nx, ny) not in visited:
                next_tile = game_map[ny][nx]
                if next_tile.cost >= 0:
                    heapq.heappush(priority_queue, (current_cost + next_tile.cost, (nx, ny), path + [(nx, ny)]))
    
    return [], float('inf')
