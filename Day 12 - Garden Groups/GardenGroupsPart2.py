from collections import deque

def calculate_total_fence_cost(grid):
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    total_cost = 0

    def bfs(start_row, start_col, plant_type):
        # Directions: Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue = deque([(start_row, start_col)])
        visited[start_row][start_col] = True
        area = 0
        boundaries = set()

        while queue:
            row, col = queue.popleft()
            area += 1

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                if (new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols or grid[new_row][new_col] != plant_type):
                    # Represent boundary as a sorted tuple to ensure uniqueness
                    boundary = tuple(sorted(((row, col), (row + dr, col + dc))))
                    boundaries.add(boundary)
                elif not visited[new_row][new_col]:
                    visited[new_row][new_col] = True
                    queue.append((new_row, new_col))

        # Return the area and the count of unique boundaries
        return area, len(boundaries)

    # Process each cell in the grid
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant_type = grid[r][c]
                area, sides = bfs(r, c, plant_type)
                region_cost = area * sides
                total_cost += region_cost

    return total_cost

# Read the input from a file
def main():
    with open("input.txt", "r") as file:
        grid = [list(line.strip()) for line in file.readlines()]

    total_cost = calculate_total_fence_cost(grid)
    print(f"Total Cost: {total_cost}")

if __name__ == "__main__":
    main()
