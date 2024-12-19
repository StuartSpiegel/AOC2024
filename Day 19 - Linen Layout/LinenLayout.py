def can_form_design(design, patterns):
    # Dynamic Programming approach
    dp = [False] * (len(design) + 1)
    dp[0] = True  # Empty string can always be formed
    
    for i in range(len(design)):
        if not dp[i]:
            continue
        for p in patterns:
            if design.startswith(p, i):
                dp[i + len(p)] = True
                # Early exit if we already know we can form full design
                if dp[len(design)]:
                    return True
    return dp[len(design)]

def main():
    # Read input data from input.txt
    with open('input.txt', 'r') as f:
        lines = [line.strip() for line in f]
    
    # First line: comma-separated patterns
    patterns_line = lines[0]
    patterns = [p.strip() for p in patterns_line.split(',')]
    
    # Remaining lines after a blank line are the designs
    # Find blank line index
    blank_line_index = 1
    while blank_line_index < len(lines) and lines[blank_line_index] != '':
        blank_line_index += 1
    
    designs = lines[blank_line_index+1:]
    
    # Check each design
    count_possible = 0
    for design in designs:
        if can_form_design(design, patterns):
            count_possible += 1
    
    # Print the number of possible designs
    print(count_possible)

if __name__ == "__main__":
    main()
