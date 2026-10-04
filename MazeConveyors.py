from collections import deque


def maze_solver_with_conveyors(maze: list[list[str]]) -> dict:
    if not maze or not maze[0]:
        return {"distance": -1, "path": []}

    rows = len(maze)
    cols = len(maze[0])

    start = None
    end = None
    for r in range(rows):
        if len(maze[r]) != cols:
            return {"distance": -1, "path": []}
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)

    if start is not None and end is None:
        return {"distance": 0, "path": [[start[0], start[1]]]}
    if start is None or end is None:
        return {"distance": -1, "path": []}
    if start == end:
        return {"distance": 0, "path": [[start[0], start[1]]]}

    conveyor_dirs = {
        '>': (0, 1),
        '<': (0, -1),
        '^': (-1, 0),
        'v': (1, 0)
    }
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def inside(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def follow_conveyor(r, c):
        cells = []
        seen = set()
        while maze[r][c] in conveyor_dirs:
            if (r, c) in seen:
                return None
            seen.add((r, c))
            cells.append((r, c))
            dr, dc = conveyor_dirs[maze[r][c]]
            nr, nc = r + dr, c + dc
            if not inside(nr, nc) or maze[nr][nc] == '#':
                return None
            r, c = nr, nc
        return (r, c), cells

    
    distance = [[-1] * cols for _ in range(rows)]
    previous = [[None] * cols for _ in range(rows)]
    edge_path = [[None] * cols for _ in range(rows)]

    sr, sc = start
    er, ec = end
    distance[sr][sc] = 0
    queue = deque([start])

    while queue:
        r, c = queue.popleft()
        if (r, c) == end:
            break

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not inside(nr, nc) or maze[nr][nc] == '#':
                continue

            if maze[nr][nc] in conveyor_dirs:
                result = follow_conveyor(nr, nc)
                if result is None:
                    continue
                final_cell, conveyor_cells = result
                fr, fc = final_cell
                if distance[fr][fc] != -1:
                    continue
                distance[fr][fc] = distance[r][c] + 1
                previous[fr][fc] = (r, c)
                edge_path[fr][fc] = conveyor_cells + [final_cell]
                queue.append(final_cell)
            else:
                if distance[nr][nc] != -1:
                    continue
                distance[nr][nc] = distance[r][c] + 1
                previous[nr][nc] = (r, c)
                edge_path[nr][nc] = [(nr, nc)]
                queue.append((nr, nc))

    if distance[er][ec] == -1:
        return {"distance": -1, "path": []}

    chunks = []
    current = end
    while current != start:
        r, c = current
        if previous[r][c] is None:
            return {"distance": -1, "path": []}
        chunks.append(edge_path[r][c])
        current = previous[r][c]

    path = [[sr, sc]]
    for chunk in reversed(chunks):
        path.extend([[r, c] for r, c in chunk])

    return {"distance": distance[er][ec], "path": path}


if __name__ == "__main__":
    maze = [
        ['S', '.', '>', '>', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 2, 'path': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]}

    maze = [
        ['S', '.', '>', '#', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {"distance": -1, "path": []}


    maze = [
        ['S', '.', 'v', '.', 'E'],
        ['#', '#', 'v', '.', '#'],
        ['.', '.', 'v', '.', '.'],
        ['#', '#', '.', '.', '#'],
        ['.', '.', '.', '.', '.']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 7, 'path': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [3, 3], [2, 3], [1, 3], [0, 3], [0, 4]]}
