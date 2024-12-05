def count_x_mas_in_file(filename):
    try:
        # Read the grid from the input file
        with open(filename, 'r') as file:
            grid = [list(line.strip()) for line in file.readlines()]
        
        rows = len(grid)
        cols = len(grid[0])
        count = 0

        # Function to check if a valid X-MAS exists at center (x, y)
        def is_x_mas(x, y):
            # Define two valid patterns for X-MAS
            forward_pattern = [
                (-1, -1, 'M'), (1, 1, 'M'),  # Diagonal 'M'
                (-1, 1, 'S'), (1, -1, 'S')   # Diagonal 'S'
            ]
            backward_pattern = [
                (-1, -1, 'S'), (1, 1, 'S'),  # Diagonal 'S'
                (-1, 1, 'M'), (1, -1, 'M')   # Diagonal 'M'
            ]

            # Check each pattern
            for pattern in [forward_pattern, backward_pattern]:
                for dx, dy, char in pattern:
                    nx, ny = x + dx, y + dy
                    # Ensure positions are within bounds and characters match
                    if nx < 0 or ny < 0 or nx >= rows or ny >= cols or grid[nx][ny] != char:
                        break
                else:  # If all positions match, it's a valid X-MAS
                    return True
            return False

        # Iterate through each cell in the grid
        for x in range(1, rows - 1):  # Skip edges where patterns can't fit
            for y in range(1, cols - 1):  # Skip edges
                if grid[x][y] == 'A':  # Check only if the center is 'A'
                    if is_x_mas(x, y):
                        count += 1

        return count
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

# Specify the input file
input_file = "input.txt"

# Calculate and print the result
result = count_x_mas_in_file(input_file)
if result is not None:
    print("Total occurrences of X-MAS:", result)
