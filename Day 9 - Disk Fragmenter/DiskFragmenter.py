# Initialize variables to keep track of the block index, block type (file or free space), and array to hold disk representation.
index = 0
block_type = 1  # 1 indicates file, 0 indicates free space
num_char = 0
arr = []

# Read the input file containing the disk map and convert it into an array representation.
with open('input.txt', 'r') as input:
    for line in input.readlines():
        for item in line.strip().replace('\n', ''):
            if block_type == 1:  # File block
                for i in range(0, int(item)):  # Add `item` number of file blocks with the current index as ID.
                    arr.append(index)
                    num_char += 1
                block_type = 0  # Switch to free space
                index += 1
            elif block_type == 0:  # Free space block
                for i in range(0, int(item)):  # Add `item` number of free space blocks.
                    arr.append('.')
                block_type = 1  # Switch to file

# Rearrange file blocks to fill gaps, moving each file block one at a time to the leftmost free space.
last = len(arr) - 1  # Start from the last position of the array.
for i in range(0, num_char):  # Iterate through the file blocks.
    for j in range(last, 0, -1):  # Move from the end of the array backward.
        if arr[i] == '.' and arr[j] != '.':  # If a free space and a file block are found:
            arr[i] = arr[j]  # Move the file block to the free space.
            arr[j] = '.'  # Mark the previous position as free space.
            last = j  # Update the last filled position.
            break

# Calculate the checksum based on the rearranged array.
index = 0
sum = 0
for i in arr:
    if i != '.':  # Only consider file blocks for the checksum.
        sum += index * i
    index += 1

print(sum)  # Output the checksum.
