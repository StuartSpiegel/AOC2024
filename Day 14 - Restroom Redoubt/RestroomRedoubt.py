def read_robots_from_file(filename):
    robots = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Each line looks like: p=x,y v=dx,dy
            # We'll parse out the coordinates.
            # Example: "p=0,4 v=3,-3"
            parts = line.split()
            # parts[0] = p=x,y
            # parts[1] = v=dx,dy

            # Parse position
            p_part = parts[0]
            # remove leading 'p='
            p_part = p_part[2:]
            x_str, y_str = p_part.split(',')
            x, y = int(x_str), int(y_str)

            # Parse velocity
            v_part = parts[1]
            # remove leading 'v='
            v_part = v_part[2:]
            dx_str, dy_str = v_part.split(',')
            dx, dy = int(dx_str), int(dy_str)

            robots.append((x, y, dx, dy))
    return robots

def main():
    width = 101
    height = 103
    # Middle column = x=50, middle row = y=51

    robots = read_robots_from_file('input.txt')
    time_elapsed = 100

    # Compute new positions after 100 seconds
    new_positions = []
    for (x, y, dx, dy) in robots:
        new_x = (x + dx * time_elapsed) % width
        new_y = (y + dy * time_elapsed) % height
        new_positions.append((new_x, new_y))

    # Count quadrants
    q1 = 0  # top-left: x < 50, y < 51
    q2 = 0  # top-right: x > 50, y < 51
    q3 = 0  # bottom-left: x < 50, y > 51
    q4 = 0  # bottom-right: x > 50, y > 51

    for (x, y) in new_positions:
        if x == 50 or y == 51:
            # On the middle line, does not count towards any quadrant
            continue
        if x < 50 and y < 51:
            q1 += 1
        elif x > 50 and y < 51:
            q2 += 1
        elif x < 50 and y > 51:
            q3 += 1
        elif x > 50 and y > 51:
            q4 += 1

    # Calculate safety factor
    safety_factor = q1 * q2 * q3 * q4

    print(safety_factor)

if __name__ == "__main__":
    main()
