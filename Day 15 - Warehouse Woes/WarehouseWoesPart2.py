class Solution:
    dirs = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }

    def get_robot_pos(self, grid):
        rows, cols = len(grid), len(grid[0])
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == "@":
                    return (i, j)

    def moving(self, grid, pos, moves, part):
        for move in moves:
            ny = pos[0] + self.dirs[move][0]
            nx = pos[1] + self.dirs[move][1]

            if grid[ny][nx] == ".":
                pos = (ny, nx)
            elif grid[ny][nx] == "#":
                continue
            else:
                edges, adjs = self.get_adjs_and_edges(grid, pos, move, part)
                blocked = 0
                dy, dx = self.dirs[move]
                for box in edges:
                    ny2, nx2 = (box[0] + dy, box[1] + dx)
                    if grid[ny2][nx2] == "#":
                        blocked += 1
                if blocked == 0:
                    grid = self.update_grid(grid, adjs, move)
                    pos = (pos[0] + dy, pos[1] + dx)
        return grid

    def get_adjs_and_edges(self, grid, pos, move, part=1):
        y, x = pos
        dy, dx = self.dirs[move]

        adjs = set()
        if part == 1 or move in "<>":
            # For part 1 or horizontal moves in part 2, just line pushing
            while True:
                ny, nx = y + dy, x + dx
                if grid[ny][nx] in ".#":
                    return [(ny - dy, nx - dx)], adjs
                y = ny
                x = nx
                adjs.add((y, x))
        else:
            # For vertical moves in part 2, we can have a stack of boxes
            edges = []
            queue = [(y, x)]
            while queue:
                cy, cx = queue.pop(0)
                if (cy, cx) in adjs:
                    continue
                adjs.add((cy, cx))
                ny, nx = cy + dy, cx + dx
                if grid[ny][nx] in ".#":
                    edges.append((cy, cx))
                elif grid[ny][nx] == "[":
                    queue.append((ny, nx))
                    queue.append((ny, nx + 1))
                elif grid[ny][nx] == "]":
                    queue.append((ny, nx))
                    queue.append((ny, nx - 1))

            return edges, adjs - {(pos[0], pos[1])}

    def update_grid(self, grid, adjs, move):
        # sort coords from the edge to the robot's position
        match move:
            case "^":
                sorted_coords = sorted(adjs, key=lambda x: x[0])
            case "v":
                sorted_coords = sorted(adjs, key=lambda x: x[0], reverse=True)
            case "<":
                sorted_coords = sorted(adjs, key=lambda x: x[1])
            case ">":
                sorted_coords = sorted(adjs, key=lambda x: x[1], reverse=True)

        dy, dx = self.dirs[move]
        for coord in sorted_coords:
            y, x = coord
            ny, nx = y + dy, x + dx
            grid[ny][nx] = grid[y][x]
            grid[y][x] = "."

        return grid

    def get_coords_sum(self, grid, part=1):
        box = "[" if part == 2 else "O"
        rows, cols = len(grid), len(grid[0])
        return sum(100 * y + x for y in range(rows) for x in range(cols) if grid[y][x] == box)

    def resize_grid(self, grid):
        _mappings = {
            "#": "##",
            "O": "[]",
            ".": "..",
            "@": "@.",
        }
        return [list("".join(_mappings[c] for c in line)) for line in grid]

    def part2(self, data):
        part = 2
        grid, moves = "\n".join(data).split("\n\n")
        grid = [list(row) for row in grid.split("\n")]
        moves = list("".join(moves.split("\n")))

        grid = self.resize_grid(grid)

        pos = self.get_robot_pos(grid)
        grid[pos[0]][pos[1]] = "."

        grid = self.moving(grid, pos, moves, part)
        _sum = self.get_coords_sum(grid, part)
        return _sum


if __name__ == "__main__":
    # Read input from input.txt
    with open("input.txt", "r") as f:
        data = f.read().splitlines()

    sol = Solution()
    result = sol.part2(data)
    print(result)
