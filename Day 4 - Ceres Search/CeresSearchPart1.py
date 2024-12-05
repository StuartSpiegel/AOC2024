def count_xmas_in_file(filename, word="XMAS"):
    try:
        # Read the grid from the input file
        with open(filename, 'r') as file:
            grid = [list(line.strip()) for line in file.readlines()]
        
        rows = len(grid)
        cols = len(grid[0])
        word_length = len(word)
        count = 0

        # Helper function to check if a word exists in a given direction
        def check_direction(x, y, dx, dy):
            for i in range(word_length):
                nx, ny = x + i * dx, y + i * dy
                if nx < 0 or nx >= rows or ny < 0 or ny >= cols or grid[nx][ny] != word[i]:
                    return False
            return True

        # Iterate through each cell in the grid
        for x in range(rows):
            for y in range(cols):
                # Check all 8 possible directions
                directions = [
                    (0, 1),   # Right
                    (1, 0),   # Down
                    (0, -1),  # Left
                    (-1, 0),  # Up
                    (1, 1),   # Down-Right
                    (-1, -1), # Up-Left
                    (1, -1),  # Down-Left
                    (-1, 1)   # Up-Right
                ]
                for dx, dy in directions:
                    if check_direction(x, y, dx, dy):
                        count += 1

        return count
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

# Specify the input file
input_file = "input.txt"

# Calculate and print the result
result = count_xmas_in_file(input_file)
if result is not None:
    print("Total occurrences of XMAS:", result)
