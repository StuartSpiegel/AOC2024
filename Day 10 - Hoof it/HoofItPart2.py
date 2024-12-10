from collections import defaultdict

def parse_map(file_path):
    """
    Parse the input map from a file into a 2D list of integers.
    """
    with open(file_path, 'r') as file:
        return [list(map(int, line.strip())) for line in file.readlines()]

def find_trailheads(topographic_map):
    """
    Find all positions in the map with height 0.
    """
    trailheads = []
    for r in range(len(topographic_map)):
        for c in range(len(topographic_map[0])):
            if topographic_map[r][c] == 0:
                trailheads.append((r, c))
    return trailheads

def dfs_count_distinct_trails(topographic_map, x, y, visited):
    """
    Perform a DFS to count the number of distinct hiking trails starting at (x, y).
    """
    rows, cols = len(topographic_map), len(topographic_map[0])

    # Use a cache to store the number of distinct trails from a given position
    cache = defaultdict(int)

    def dfs(x, y, current_height):
        # If we reach height 9, this is a valid trail
        if current_height == 9:
            return 1

        if (x, y) in cache:
            return cache[(x, y)]

        trails = 0

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if topographic_map[nx][ny] == current_height + 1:
                    trails += dfs(nx, ny, topographic_map[nx][ny])

        cache[(x, y)] = trails
        return trails

    return dfs(x, y, topographic_map[x][y])

def calculate_total_trailhead_ratings(file_path):
    """
    Calculate the sum of the ratings of all trailheads on the topographic map.
    """
    topographic_map = parse_map(file_path)
    trailheads = find_trailheads(topographic_map)
    total_rating = 0

    for trailhead in trailheads:
        total_rating += dfs_count_distinct_trails(topographic_map, trailhead[0], trailhead[1], set())

    return total_rating

if __name__ == "__main__":
    # Path to the input file
    input_file = "input.txt"
    
    # Calculate and print the total trailhead ratings
    total_rating = calculate_total_trailhead_ratings(input_file)
    print(f"Total Rating: {total_rating}")
