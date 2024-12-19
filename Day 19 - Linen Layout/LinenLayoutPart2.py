def count_ways_to_form_design(design, patterns):
    # dp[i] = number of ways to form design[:i]
    dp = [0] * (len(design) + 1)
    dp[0] = 1  # one way to form empty prefix
    
    for i in range(len(design)):
        if dp[i] == 0:
            continue
        for p in patterns:
            # If pattern p matches starting at index i
            if design.startswith(p, i):
                dp[i + len(p)] += dp[i]
    return dp[len(design)]

def main():
    with open('input.txt', 'r') as f:
        lines = [line.strip() for line in f]
    
    # First line: comma-separated patterns
    patterns_line = lines[0]
    patterns = [p.strip() for p in patterns_line.split(',')]
    
    # Find blank line index
    blank_line_index = 1
    while blank_line_index < len(lines) and lines[blank_line_index] != '':
        blank_line_index += 1
    
    designs = lines[blank_line_index+1:]
    
    total_ways = 0
    for design in designs:
        total_ways += count_ways_to_form_design(design, patterns)
    
    print(total_ways)

if __name__ == "__main__":
    main()
