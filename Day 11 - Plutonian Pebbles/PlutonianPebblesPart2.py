from collections import Counter

def count_digits(number):
    """Helper to count digits in a number."""
    return len(str(number))

def update_stone_counts(stone_counts):
    """Update the counts of stones for the next iteration."""
    next_counts = Counter()

    for stone, count in stone_counts.items():
        if stone == 0:
            next_counts[1] += count  # Rule 1: 0 becomes 1
        else:
            num_digits = count_digits(stone)
            if num_digits % 2 == 0:
                # Rule 2: Even digits, split into two stones
                half = num_digits // 2
                left = int(str(stone)[:half].lstrip('0') or '0')
                right = int(str(stone)[half:].lstrip('0') or '0')
                next_counts[left] += count
                next_counts[right] += count
            else:
                # Rule 3: Odd digits, multiply by 2024
                next_counts[stone * 2024] += count

    return next_counts

def compute_stone_count(initial_stones, iterations):
    """Compute the total number of stones after a given number of iterations."""
    # Initialize stone counts
    stone_counts = Counter(initial_stones)

    # Perform iterations
    for _ in range(iterations):
        stone_counts = update_stone_counts(stone_counts)

    # Total number of stones is the sum of all counts
    return sum(stone_counts.values())

def main():
    try:
        with open("input.txt", "r") as file:
            lines = file.readlines()

        # Read initial stones
        initial_stones = []
        for line in lines:
            line = line.strip()
            if line:
                initial_stones.append(int(line))

        # Compute the total number of stones after 75 iterations
        iterations = 75
        total_stones = compute_stone_count(initial_stones, iterations)
        print(f"Total number of stones after {iterations} blinks: {total_stones}")

    except FileNotFoundError:
        print("Error: input.txt not found.")
    except ValueError as e:
        print(f"Error: Invalid input in input.txt. {e}")

if __name__ == "__main__":
    main()
