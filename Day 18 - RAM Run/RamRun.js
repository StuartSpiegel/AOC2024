function readInputLines() {
    // Implement this function to return lines of input coordinates as an array of strings
    const fs = require('fs');
    return fs.readFileSync('input.txt', 'utf-8').trim().split('\n');
    
    // For demonstration, this returns an empty array. Replace with your actual input.
    // return [];
}

function main() {
    const lines = readInputLines();
    // Our memory space is 71x71 (coordinates 0 to 70)
    const size = 71;
    // Create a grid and initialize to false (not corrupted)
    const grid = Array.from({length: size}, () => Array(size).fill(false));

    // Process the first 1024 bytes (or fewer if input is shorter)
    const limit = Math.min(lines.length, 1024);
    for (let i = 0; i < limit; i++) {
        const line = lines[i].trim();
        if (!line) continue;
        const [xStr, yStr] = line.split(',').map(s => parseInt(s, 10));
        const x = xStr, y = yStr;
        if (x >= 0 && x < size && y >= 0 && y < size) {
            grid[y][x] = true; // Mark corrupted
        }
    }

    // We need to find the shortest path from (0,0) to (70,70).
    // BFS on the grid:
    // Moves: up, down, left, right
    const directions = [
        [1,0], [-1,0], [0,1], [0,-1]
    ];

    function isValid(nx, ny) {
        return nx >= 0 && nx < size && ny >= 0 && ny < size && !grid[ny][nx];
    }

    // If start or end is corrupted, no path
    if (grid[0][0] || grid[size-1][size-1]) {
        console.log("No path available");
        return;
    }

    const visited = Array.from({length: size}, () => Array(size).fill(false));
    const queue = [];
    // We'll store [x, y, steps]
    queue.push([0, 0, 0]);
    visited[0][0] = true;

    let shortest = -1;

    while (queue.length > 0) {
        const [x, y, steps] = queue.shift();
        // Check if reached the exit
        if (x === size - 1 && y === size - 1) {
            shortest = steps;
            break;
        }

        for (const [dx, dy] of directions) {
            const nx = x + dx;
            const ny = y + dy;
            if (isValid(nx, ny) && !visited[ny][nx]) {
                visited[ny][nx] = true;
                queue.push([nx, ny, steps + 1]);
            }
        }
    }

    if (shortest >= 0) {
        console.log(shortest);
    } else {
        console.log("No path available");
    }
}

// Run the main function
main();
