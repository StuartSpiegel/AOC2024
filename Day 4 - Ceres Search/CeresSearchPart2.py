# def count_x_mas_in_file(filename):
#     try:
#         # Read the grid from the input file
#         with open(filename, 'r') as file:
#             grid = [list(line.strip()) for line in file.readlines()]
        
#         rows = len(grid)
#         cols = len(grid[0])
#         count = 0

#         # Helper function to check if a pattern matches one of the valid "X-MAS" shapes
#         def check_x_mas(x, y):
#             # Valid patterns to form an X-MAS
#             patterns = [
#                 [(-1, -1), (1, 1), (-1, 1), (1, -1)],  # Pattern 1: MMSS
#                 [(-1, -1), (1, -1), (-1, 1), (1, 1)],  # Pattern 2: MSSM
#                 [(-1, 1), (1, 1), (-1, -1), (1, -1)],  # Pattern 3: SSMM
#                 [(-1, 1), (1, -1), (-1, -1), (1, 1)]   # Pattern 4: SMMS
#             ]
#             expected_chars = [
#                 ['M', 'M', 'S', 'S'],
#                 ['M', 'S', 'S', 'M'],
#                 ['S', 'S', 'M', 'M'],
#                 ['S', 'M', 'M', 'S']
#             ]

#             # Check all patterns
#             for pattern, chars in zip(patterns, expected_chars):
#                 if all(0 <= x + dx < rows and 0 <= y + dy < cols and grid[x + dx][y + dy] == char for (dx, dy), char in zip(pattern, chars)):
#                     return True
#             return False

#         # Iterate through each cell in the grid
#         for x in range(1, rows - 1):
#             for y in range(1, cols - 1):
#                 # Check if the center is 'A' and if the "X-MAS" shape exists centered at (x, y)
#                 if grid[x][y] == 'A' and check_x_mas(x, y):
#                     count += 1

#         return count
#     except FileNotFoundError:
#         print(f"Error: File '{filename}' not found.")
#         return None

# # Specify the input file
# input_file = "input.txt"

# # Calculate and print the result
# result = count_x_mas_in_file(input_file)
# if result is not None:
#     print("Total occurrences of X-MAS:", result)
def part2():
    # Read input from the file
    with open("input.txt", "r") as file:
        rows = file.read().strip().split('\n')

    m = len(rows)
    n = len(rows[0])

    def check(r, c):
        if rows[r][c] != 'A':
            return False
        ul = rows[r-1][c-1]
        ur = rows[r-1][c+1]
        dl = rows[r+1][c-1]
        dr = rows[r+1][c+1]
        return sorted([ul, ur, dl, dr]) == ['M', 'M', 'S', 'S'] and ul != dr

    return sum(check(r, c) for r in range(1, m-1) for c in range(1, n-1))

# Run the function and print the result
if __name__ == "__main__":
    result = part2()
    print(result)
