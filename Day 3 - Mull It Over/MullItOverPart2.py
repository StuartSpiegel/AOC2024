import re

def extract_and_sum_conditional_multiplications(filename):
    try:
        # Read the file content
        with open(filename, 'r') as file:
            memory = file.read()
        
        # Define patterns for valid instructions
        mul_pattern = r"mul\((\d+),(\d+)\)"
        control_pattern = r"(do\(\)|don't\(\))"
        
        # Split memory into instructions based on patterns
        instructions = re.findall(f"{mul_pattern}|{control_pattern}", memory)
        
        # Initialize state
        enabled = True
        total = 0
        
        # Process each instruction
        for inst in instructions:
            if inst[2] == "do()":
                enabled = True
            elif inst[2] == "don't()":
                enabled = False
            elif enabled and inst[0] and inst[1]:  # Valid mul instruction
                x, y = int(inst[0]), int(inst[1])
                total += x * y
        
        return total
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

# Specify the input file
input_file = "input.txt"

# Calculate and print the result
result = extract_and_sum_conditional_multiplications(input_file)
if result is not None:
    print("Sum of valid enabled multiplications:", result)
