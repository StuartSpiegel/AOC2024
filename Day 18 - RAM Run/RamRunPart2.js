function readInputLines() {
    // Implement this function to return lines of input coordinates as an array of strings.
    const fs = require('fs');
    return fs.readFileSync('input.txt', 'utf-8').trim().split('\n');
    
    // For now, an empty placeholder:
    // return [];
}

function canReachExit(grid) {
    const size = 71;
    if (grid[0][0] || grid[size-1][size-1]) return false;

    const visited = Array.from({length: size}, () => Array(size).fill(false));
    const queue = [[0,0]];
    visited[0][0] = true;
    const directions = [[1,0],[-1,0],[0,1],[0,-1]];

    while (queue.length > 0) {
        const [x,y] = queue.shift();
        if (x === size-1 && y === size-1) return true;
        for (const [dx,dy] of directions) {
            const nx = x+dx;
            const ny = y+dy;
            if (nx>=0 && nx<size && ny>=0 && ny<size && !grid[ny][nx] && !visited[ny][nx]) {
                visited[ny][nx] = true;
                queue.push([nx,ny]);
            }
        }
    }

    return false;
}

function main() {
    const lines = readInputLines();
    const size = 71;
    const grid = Array.from({length: size}, () => Array(size).fill(false));

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;
        const [xStr, yStr] = line.split(',').map(s => parseInt(s,10));
        const x = xStr, y = yStr;

        // Place the byte
        if (x >=0 && x<size && y>=0 && y<size) {
            grid[y][x] = true;
        }

        // Check if path is still available
        if (!canReachExit(grid)) {
            // The path is no longer reachable!
            console.log(`${x},${y}`);
            return;
        }
    }

    // If we finish placing all given bytes and a path remains, print something indicating no cutoff was found
    // (The problem states to find the first that prevents exit, so if we never find one, we might print nothing.)
    console.log("No cutoff found");
}

main();
