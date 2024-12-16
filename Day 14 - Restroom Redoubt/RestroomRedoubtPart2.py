# def read_robots_from_file(filename):
#     robots = []
#     with open(filename, 'r') as f:
#         for line in f:
#             line = line.strip()
#             if not line:
#                 continue
#             # Expected format: p=x,y v=dx,dy
#             # Example: p=0,4 v=3,-3
#             parts = line.split()
#             p_part = parts[0][2:]  # remove 'p='
#             v_part = parts[1][2:]  # remove 'v='

#             x_str, y_str = p_part.split(',')
#             dx_str, dy_str = v_part.split(',')

#             x, y = int(x_str), int(y_str)
#             dx, dy = int(dx_str), int(dy_str)

#             robots.append((x, y, dx, dy))
#     return robots

# def bounding_box_area(positions):
#     xs = [p[0] for p in positions]
#     ys = [p[1] for p in positions]
#     width = max(xs) - min(xs)
#     height = max(ys) - min(ys)
#     return width * height

# def positions_at_time(robots, t):
#     return [(x + dx * t, y + dy * t) for (x, y, dx, dy) in robots]

# def main():
#     robots = read_robots_from_file('input.txt')

#     # We'll track the bounding box areas over time and look for a local minimum.
#     # A local minimum occurs when area[t-1] < area[t-2] and area[t-1] < area[t].
#     # We'll start from t=0 and go forward until we find a turning point.

#     prev_area = None
#     prev_prev_area = None
#     min_time = None

#     # Set a reasonable upper limit to avoid infinite loops if no pattern emerges.
#     # Adjust if needed.
#     max_time = 500000

#     for t in range(max_time):
#         pos = positions_at_time(robots, t)
#         area = bounding_box_area(pos)

#         # We can only detect a local minimum starting from t=2
#         if t >= 2:
#             # Check if area[t-1] was a local minimum
#             # That means prev_area < prev_prev_area and prev_area < area
#             if prev_area is not None and prev_prev_area is not None:
#                 if prev_area < prev_prev_area and prev_area < area:
#                     # local minimum found at time t-1
#                     min_time = t - 1
#                     break

#         prev_prev_area = prev_area
#         prev_area = area

#     # If we never broke out of the loop, it might mean that the area never formed a local minimum
#     # different from t=0, or that the pattern never emerges within max_time.
#     # In that case, min_time might still be None.

#     if min_time is None:
#         # If no local minimum was found, it might mean the minimal area was at the start (t=0)
#         # or at the end of our search range. Let's fall back to finding the absolute minimum over
#         # the entire range if needed.
#         # Re-run to find absolute min:
#         min_area = None
#         min_area_time = 0
#         for t in range(max_time):
#             pos = positions_at_time(robots, t)
#             area = bounding_box_area(pos)
#             if min_area is None or area < min_area:
#                 min_area = area
#                 min_area_time = t
#         min_time = min_area_time

#     print(min_time)

# if __name__ == "__main__":
#     main()

class Solution:
    def part1(self, data):
        robots = []
        for line in data:
            a, b = line.split(" ")
            x, y = map(int, a[2:].split(","))
            vx, vy = map(int, b[2:].split(","))
            robots.append(((x, y), (vx, vy)))

        width = 101
        height = 103

        # For the test input based on the problem description
        # (If you know the input set is the "small" example)
        if len(robots) == 12:
            width = 11
            height = 7

        quads = [0, 0, 0, 0]

        # Simulate exactly 100 seconds
        for i in range(len(robots)):
            (x, y), (vx, vy) = robots[i]
            # Apply velocities for 100 seconds, wrapping around as needed
            x = (x + 100 * (vx + width)) % width
            y = (y + 100 * (vy + height)) % height

            # If on the dividing line, do not count in quadrants
            if x == width // 2 or y == height // 2:
                continue

            # Determine which quadrant
            # top-left (0): x < mid_x, y < mid_y
            # top-right (1): x > mid_x, y < mid_y
            # bottom-left (2): x < mid_x, y > mid_y
            # bottom-right (3): x > mid_x, y > mid_y
            quad_idx = (int(x > width // 2)) + (int(y > height // 2) * 2)
            quads[quad_idx] += 1

        return quads[0] * quads[1] * quads[2] * quads[3]

    def part2(self, data):
        """
        This method checks each second to find when the robots form
        the special Easter egg pattern (a "Christmas tree").

        The logic:
        - Increment time t by 1 each iteration.
        - Move all robots according to their velocities (with wrapping).
        - Check if all robot positions are unique.
        - If unique, return t (the number of seconds).
        """
        robots = []
        for line in data:
            a, b = line.split(" ")
            x, y = map(int, a[2:].split(","))
            vx, vy = map(int, b[2:].split(","))
            robots.append(((x, y), (vx, vy)))

        width = 101
        height = 103

        t = 0
        while True:
            t += 1
            pos = set()
            valid = True

            for (x, y), (vx, vy) in robots:
                # Move robot for t seconds, wrapping around
                x = (x + t * (vx + width)) % width
                y = (y + t * (vy + height)) % height
                if (x, y) in pos:
                    # A collision occurred, not the pattern we want
                    valid = False
                    break
                pos.add((x, y))

            if valid:
                # All unique positions found at time t,
                # this indicates the Easter egg pattern.
                return t

def main():
    # Read input from input.txt
    with open('input.txt', 'r') as f:
        data = [line.strip() for line in f if line.strip()]

    solution = Solution()
    answer_part1 = solution.part1(data)
    answer_part2 = solution.part2(data)

    print("Part 1:", answer_part1)
    print("Part 2:", answer_part2)

if __name__ == "__main__":
    main()
