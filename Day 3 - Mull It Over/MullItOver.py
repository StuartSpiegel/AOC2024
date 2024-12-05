import re

def extract_and_sum_multiplications(filename):
    try:
        # Read the file content
        with open(filename, 'r') as file:
            memory = file.read()
        
        # Define a regular expression to match valid mul(X,Y) instructions
        pattern = r"mul\((\d+),(\d+)\)"
        
        # Find all matches in the corrupted memory
        matches = re.findall(pattern, memory)
        
        # Calculate the sum of all valid multiplications
        total = 0
        for x, y in matches:
            total += int(x) * int(y)
        
        return total
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

# Specify the input file
input_file = "input.txt"

# Calculate and print the result
result = extract_and_sum_multiplications(input_file)
if result is not None:
    print("Sum of valid multiplications:", result)
