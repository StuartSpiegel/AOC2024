# Initialize variables similar to Part 1.
index = 0
block_type = 1
num_char = 0
arr = []

# Read and process the input file.
with open('input.txt', 'r') as input:
    for line in input.readlines():
        for item in line.strip().replace('\n', ''):
            if block_type == 1:  # File block
                for i in range(0, int(item)):
                    arr.append(index)
                    num_char += 1
                block_type = 0
                index += 1
            elif block_type == 0:  # Free space block
                for i in range(0, int(item)):
                    arr.append('.')
                block_type = 1

# Group the array into segments of files and free spaces, keeping track of their start positions and lengths.
last_item = arr[0]
item_count = 0
start_pos = 0
new_arr = []
for item in arr:
    if last_item == '' or item == last_item:  # Continue counting if the block type remains the same.
        item_count += 1
    if item != last_item:  # If the block type changes, finalize the previous group.
        new_arr.append([last_item, item_count, start_pos])  # [Type, Count, Start Position]
        start_pos += item_count  # Update the start position.
        item_count = 1
    last_item = item
new_arr.append([last_item, item_count, start_pos])  # Append the final group.

# Attempt to move whole files to the largest leftmost free space.
empty_arr = []  # Keep track of free space segments.
for j in range(len(new_arr) - 1, 0, -1):  # Iterate files from right to left.
    for i in range(0, len(new_arr)):  # Check against all earlier segments.
        if (j > i and
            new_arr[j][2] > new_arr[i][2] and
            new_arr[j][0] != '.' and
            new_arr[j][1] <= new_arr[i][1] and
            new_arr[i][0] == '.'):  # Conditions to move the file:
            empty_arr.append(['.', new_arr[j][1], new_arr[j][2]])  # Mark old position as free space.
            new_arr[j][2] = new_arr[i][2]  # Update the file's start position.
            new_arr[i][1] = new_arr[i][1] - new_arr[j][1]  # Update the free space count.
            new_arr[i][2] = new_arr[i][2] + new_arr[j][1]  # Update the free space position.

# Rebuild the array in sorted order based on start positions.
new_arr.extend(empty_arr)
new_arr = sorted(new_arr, key=lambda x: x[2])

# Construct the final array from the grouped representation.
result = []
index = 0
for item in new_arr:
    if item[2] == index and item[1] > 0:
        for i in range(0, item[1]):
            result.append(item[0])
            index += 1

# Calculate the checksum as in Part 1.
index = 0
sum = 0
for i in result:
    if i != '.':
        sum += index * i
    index += 1

print(sum)  # Output the checksum.
