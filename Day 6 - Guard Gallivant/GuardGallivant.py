# read input
with open("input.txt", "r") as file:
    area = {(x, y): c for y, line in enumerate(file.readlines())
                    for x, c in enumerate(line.strip())}

# find start
start_pos = next((xy for xy, c in area.items() if c == '^'), None)
if not start_pos:
    raise ValueError("Starting position (^) not found in input.")

start_direction = (0, -1)

def do_walk(area, in_simulation=False):
    obstacle_placements = set()
    visits = dict()
    position = start_pos
    direction = start_direction
    while True:
        if direction in visits.get(position, []):
            raise OverflowError("Infinite loop detected")

        visits[position] = visits.get(position, []) + [direction]

        x, y = position
        dx, dy = direction
        next_pos = (x + dx, y + dy)
        next_field = area.get(next_pos, "")

        if next_field in ['.', '^']:
            if not in_simulation and next_pos not in obstacle_placements:
                try:
                    do_walk({**area, **{next_pos: '#'}}, True)
                except OverflowError:
                    obstacle_placements.add(next_pos)

            position = next_pos
        elif next_field == '#':
            direction = (-dy, dx)
        else:
            return visits, obstacle_placements


# Run the simulation
(visits, obstacle_placements) = do_walk(area)

# Print results
print("1:", len(visits)) 
print("2:", len(obstacle_placements))
