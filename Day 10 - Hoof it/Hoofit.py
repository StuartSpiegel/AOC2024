from collections import deque

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

def bfs_count_reachable_nines(topographic_map, start):
    """
    Perform a BFS from a given trailhead (start position) to count the number of reachable 9s.
    """
    rows, cols = len(topographic_map), len(topographic_map[0])
    visited = set()
    queue = deque([start])
    reachable_nines = set()

    while queue:
        x, y = queue.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))
        current_height = topographic_map[x][y]

        # Check if this is a reachable 9
        if current_height == 9:
            reachable_nines.add((x, y))
            continue

        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                neighbor_height = topographic_map[nx][ny]

                if neighbor_height == current_height + 1:
                    queue.append((nx, ny))

    return len(reachable_nines)

def calculate_total_trailhead_scores(file_path):
    """
    Calculate the sum of the scores of all trailheads on the topographic map.
    """
    topographic_map = parse_map(file_path)
    trailheads = find_trailheads(topographic_map)
    total_score = 0

    for trailhead in trailheads:
        total_score += bfs_count_reachable_nines(topographic_map, trailhead)

    return total_score

if __name__ == "__main__":
    # Path to the input file
    input_file = "input.txt"
    
    # Calculate and print the total score
    total_score = calculate_total_trailhead_scores(input_file)
    print(f"Total Score: {total_score}")
