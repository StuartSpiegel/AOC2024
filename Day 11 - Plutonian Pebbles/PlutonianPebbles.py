from collections import deque

def split_number(number):
    """Split a number into two halves without leading zeros."""
    num_str = str(number)
    mid = len(num_str) // 2
    left_str = num_str[:mid].lstrip('0')
    right_str = num_str[mid:].lstrip('0')
    
    # Convert to integers (empty strings become 0)
    left = int(left_str) if left_str else 0
    right = int(right_str) if right_str else 0
    
    return left, right

def blink(stones):
    """Perform a single blink transformation."""
    new_stones = deque()
    
    while stones:
        stone = stones.popleft()
        if stone == 0:
            new_stones.append(1)
        else:
            stone_str = str(stone)
            if len(stone_str) % 2 == 0:
                left, right = split_number(stone)
                new_stones.append(left)
                new_stones.append(right)
            else:
                new_stones.append(stone * 2024)
    
    return new_stones

def main():
    try:
        with open("input.txt", "r") as file:
            lines = file.readlines()
        
        # Read initial stones from input.txt
        stones = deque()
        for line in lines:
            line = line.strip()
            if line:
                stones.append(int(line))
        
        # Simulate 25 blinks
        # Part 2: Just change # of iterations to 75 lolz. JK thats O(2^N) good luck
        total_blinks = 75
        for _ in range(total_blinks):
            stones = blink(stones)
        
        print(f"Number of stones after {total_blinks} blinks: {len(stones)}")
    
    except FileNotFoundError:
        print("Error: input.txt not found.")
    except ValueError as e:
        print(f"Error: Invalid input in input.txt. {e}")

if __name__ == "__main__":
    main()
