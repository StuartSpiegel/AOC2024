const fs = require('fs');

// Read the entire input file
const input = fs.readFileSync('input.txt', 'utf8').trimEnd();
const lines = input.split('\n');

// Separate map lines from move lines
// We know the map is typically surrounded by walls (#).
// Once we find a line that clearly no longer matches the map pattern (or we reach a line that contains movement symbols), 
// we will assume that we've reached the moves.

// A heuristic: The map lines contain '#', '@', 'O', '.' but no '^', 'v', '<', '>'.
// We'll read lines until we encounter one that includes a movement character or until all lines are processed.

let mapLines = [];
let movesLines = [];

let parsingMap = true;
for (let line of lines) {
  // Check if line might be a moves line
  if (line.match(/[<>\^v]/)) {
    // Once we detect a moves character, we assume the rest are moves.
    parsingMap = false;
  }

  if (parsingMap) {
    mapLines.push(line);
  } else {
    movesLines.push(line);
  }
}

// Combine all moves lines into a single string, removing newlines
const movesInput = movesLines.join('');

// Now we have mapLines for the warehouse, and movesInput for the moves.
// The rest of the code is similar to the previous solution.

let warehouse = mapLines.map(line => line.split(''));
let numRows = warehouse.length;
let numCols = warehouse[0].length;

let robotRow = -1;
let robotCol = -1;

// Find the robot's initial position
for (let r = 0; r < numRows; r++) {
  for (let c = 0; c < numCols; c++) {
    if (warehouse[r][c] === '@') {
      robotRow = r;
      robotCol = c;
      break;
    }
  }
  if (robotRow !== -1) break;
}

const moves = movesInput.replace(/\n/g, '').split(''); // Just to be sure if there are any stray newlines.

// Direction mapping
const directions = {
  '^': [-1, 0],
  'v': [1, 0],
  '<': [0, -1],
  '>': [0, 1]
};

function attemptMove(dRow, dCol) {
  const nextR = robotRow + dRow;
  const nextC = robotCol + dCol;
  
  const nextCell = warehouse[nextR][nextC];
  
  if (nextCell === '#') {
    return; // Can't move into a wall
  }

  if (nextCell === '.') {
    // Move robot
    warehouse[robotRow][robotCol] = '.';
    warehouse[nextR][nextC] = '@';
    robotRow = nextR;
    robotCol = nextC;
    return;
  }

  if (nextCell === 'O') {
    // Push boxes if possible
    let boxes = [];
    let cr = nextR;
    let cc = nextC;
    
    while (warehouse[cr][cc] === 'O') {
      boxes.push([cr, cc]);
      cr += dRow;
      cc += dCol;
    }

    // After collecting boxes, check the next cell
    if (warehouse[cr][cc] !== '.') {
      // Can't push
      return;
    }

    // Move boxes forward
    warehouse[cr][cc] = 'O';

    for (let i = boxes.length - 1; i > 0; i--) {
      const [boxR, boxC] = boxes[i];
      const [prevR, prevC] = boxes[i - 1];
      warehouse[boxR][boxC] = 'O';
      warehouse[prevR][prevC] = '.';
    }

    // The first box vacates its spot
    const [firstBoxR, firstBoxC] = boxes[0];
    warehouse[firstBoxR][firstBoxC] = '.';

    // Move robot into the place of the first box
    warehouse[robotRow][robotCol] = '.';
    warehouse[robotRow + dRow][robotCol + dCol] = '@';
    
    robotRow += dRow;
    robotCol += dCol;
  }
}

// Simulate all moves
for (let m of moves) {
  const [dR, dC] = directions[m];
  attemptMove(dR, dC);
}

// Compute final GPS coordinate sum
let sumCoordinates = 0;
for (let r = 0; r < numRows; r++) {
  for (let c = 0; c < numCols; c++) {
    if (warehouse[r][c] === 'O') {
      sumCoordinates += 100 * r + c;
    }
  }
}

console.log(sumCoordinates);
