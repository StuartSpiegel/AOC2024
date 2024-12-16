# import re

# def read_input(filename):
#     button_pattern = re.compile(r'Button [AB]: X\+(\d+), Y\+(\d+)')
#     prize_pattern = re.compile(r'Prize: X=(\d+), Y=(\d+)')
#     data = []
#     with open(filename, 'r') as f:
#         lines = [line.strip() for line in f if line.strip()]
#     for i in range(0, len(lines), 3):
#         line_a = lines[i]
#         line_b = lines[i+1]
#         line_p = lines[i+2]

#         match_a = button_pattern.match(line_a)
#         if not match_a:
#             raise ValueError(f"Line does not match Button A format: {line_a}")
#         Ax, Ay = map(int, match_a.groups())

#         match_b = button_pattern.match(line_b)
#         if not match_b:
#             raise ValueError(f"Line does not match Button B format: {line_b}")
#         Bx, By = map(int, match_b.groups())

#         match_p = prize_pattern.match(line_p)
#         if not match_p:
#             raise ValueError(f"Line does not match Prize format: {line_p}")
#         Px_orig, Py_orig = map(int, match_p.groups())

#         data.append((Ax, Ay, Bx, By, Px_orig, Py_orig))
#     return data

# def find_min_tokens(Ax, Ay, Bx, By, Px_orig, Py_orig):
#     OFFSET = 10_000_000_000_000
#     Px = Px_orig + OFFSET
#     Py = Py_orig + OFFSET

#     det = Ax * By - Ay * Bx
#     if det == 0:
#         return None

#     # Check if divides evenly for i
#     numerator_i = Px * By - Py * Bx
#     if numerator_i % det != 0:
#         return None
#     i = numerator_i // det

#     # Check if divides evenly for j
#     numerator_j = Ax * Py - Ay * Px
#     if numerator_j % det != 0:
#         return None
#     j = numerator_j // det

#     if i < 0 or j < 0:
#         return None

#     return i + j

# def main():
#     data = read_input("input.txt")

#     # According to the puzzle: "it is only possible to win a prize on the second and fourth claw machines."
#     # This might mean we only sum the results from machines indexed 1 and 3 (0-based indexing).
#     # If your data corresponds to the same order mentioned in the puzzle, we can:
#     #  - Identify which machines are the second and fourth, or
#     #  - If we must consider all machines that yield a solution, sum them all.
#     #
#     # Let's assume we must consider only the second and fourth machines for demonstration.
#     # If the puzzle's known final answer corresponds to only these, filter them out:
#     # machine 1 -> index 0-based is 1
#     # machine 2 -> index 0-based is 3
#     # We'll attempt that approach. Adjust as needed.
    
#     possible_indices = [1, 3]  # The puzzle statement hint
#     min_tokens_per_machine = []
#     for idx in possible_indices:
#         if idx < len(data):
#             Ax, Ay, Bx, By, Px_orig, Py_orig = data[idx]
#             tokens = find_min_tokens(Ax, Ay, Bx, By, Px_orig, Py_orig)
#             if tokens is not None:
#                 min_tokens_per_machine.append(tokens)

#     if min_tokens_per_machine:
#         print(sum(min_tokens_per_machine))
#     else:
#         print("No possible prizes can be won.")

# if __name__ == "__main__":
#     main()
def main():
    with open("input.txt", "r") as f:
        data = [line.strip() for line in f if line.strip()]

    # Each machine is separated by a blank line in the input.
    # After stripping and filtering empty lines, we need to regroup the lines
    # in sets of three (A, B, Prize) lines.
    # The provided code snippet expects that machines are separated by double newlines.
    # We'll reconstruct them accordingly.

    # We know each machine description has exactly 3 lines.
    # So we can chunk the data every 3 lines.
    machines = [data[i:i+3] for i in range(0, len(data), 3)]

    total_coins = 0

    for machine in machines:
        btn_a_line, btn_b_line, prize_line = machine

        # Parse button A increments
        # Format: "Button A: X+94, Y+34"
        # After splitting by ": ", we'll get ["Button A", "X+94, Y+34"]
        # Then split by ", " to separate X and Y increments.
        btn_a = btn_a_line.split(": ")[1].split(", ")
        Ax = int(btn_a[0][2:])  # remove 'X+' or 'X-' -> int
        Ay = int(btn_a[1][2:])  # remove 'Y+' or 'Y-'

        # Parse button B increments
        btn_b = btn_b_line.split(": ")[1].split(", ")
        Bx = int(btn_b[0][2:])
        By = int(btn_b[1][2:])

        # Parse prize coordinates
        # Format: "Prize: X=8400, Y=5400"
        prize = prize_line.split(": ")[1].split(", ")
        Px = int(prize[0][2:]) + 10000000000000  # Add the large offset for part 2
        Py = int(prize[1][2:]) + 10000000000000

        # Solve the system of equations:
        # Ax*times_a + Bx*times_b = Px
        # Ay*times_a + By*times_b = Py
        denom = (By * Ax - Bx * Ay)
        if denom == 0:
            # No unique solution
            continue

        times_b = (Py * Ax - Px * Ay) / denom
        if Ax == 0:
            # If Ax is zero, then times_a must be solved differently
            # But given problem constraints, it's unlikely. If Ax=0 means A doesn't move X at all,
            # we'd handle similarly. Let's just skip if Ax=0 to avoid division by zero.
            continue
        times_a = (Px - Bx * times_b) / Ax

        # Check for integral and non-negative solution
        if times_a.is_integer() and times_b.is_integer():
            times_a = int(times_a)
            times_b = int(times_b)
            if times_a >= 0 and times_b >= 0:
                # Calculate cost
                cost = 3 * times_a + times_b
                total_coins += cost

    print(total_coins)


if __name__ == "__main__":
    main()
