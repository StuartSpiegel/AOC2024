const fs = require('fs');

////////////////////////////////////////////////////////////////////////////////
// Step 1: Read Input
////////////////////////////////////////////////////////////////////////////////
const input = fs.readFileSync('input.txt', 'utf8').trimEnd();
const lines = input.split('\n');

// Separate map lines from move lines
let mapLines = [];
let movesLines = [];
let parsingMap = true;
for (let line of lines) {
  if (line.match(/[<>\^v]/)) {
    parsingMap = false;
  }
  
  if (parsingMap) {
    mapLines.push(line);
  } else {
    movesLines.push(line);
  }
}

const movesInput = movesLines.join('').replace(/\n/g, '');

// Scale rules for Part 2
function scaleLine(line) {
  let result = '';
  for (let ch of line) {
    if (ch === '#') {
      result += '##';
    } else if (ch === 'O') {
      result += '[]';
    } else if (ch === '.') {
      result += '..';
    } else if (ch === '@') {
      // Robot cell: '@.'
      result += '@.';
    } else {
      // Unexpected chars just duplicated
      result += ch + ch; 
    }
  }
  return result;
}

let scaledMapLines = mapLines.map(scaleLine);
let numRows = scaledMapLines.length;
let numCols = scaledMapLines[0].length;

////////////////////////////////////////////////////////////////////////////////
// Step 2: Represent the Warehouse in a Typed Array
////////////////////////////////////////////////////////////////////////////////

// Encoding scheme for cells:
// '.' = 0
// '#' = 1
// '[' = 2
// ']' = 3
// '@' = 4

function encodeCell(ch) {
  switch (ch) {
    case '.': return 0;
    case '#': return 1;
    case '[': return 2;
    case ']': return 3;
    case '@': return 4;
    default: return 0;
  }
}

function decodeCell(val) {
  switch (val) {
    case 0: return '.';
    case 1: return '#';
    case 2: return '[';
    case 3: return ']';
    case 4: return '@';
    default: return '.';
  }
}

let warehouse = new Uint8Array(numRows * numCols);
for (let r = 0; r < numRows; r++) {
  for (let c = 0; c < numCols; c++) {
    warehouse[r * numCols + c] = encodeCell(scaledMapLines[r][c]);
  }
}

////////////////////////////////////////////////////////////////////////////////
// Step 3: Find Robot Position
////////////////////////////////////////////////////////////////////////////////
let robotRow = -1;
let robotCol = -1;
for (let r = 0; r < numRows && robotRow === -1; r++) {
  for (let c = 0; c < numCols; c++) {
    if (warehouse[r * numCols + c] === 4) { // '@'
      robotRow = r;
      robotCol = c;
      break;
    }
  }
}

const moves = movesInput.split('');
const directions = {
  '^': [-1, 0],
  'v': [1, 0],
  '<': [0, -1],
  '>': [0, 1]
};

////////////////////////////////////////////////////////////////////////////////
// Step 4: Helper Functions
////////////////////////////////////////////////////////////////////////////////

function cell(r, c) {
  return warehouse[r * numCols + c];
}

function setCell(r, c, val) {
  warehouse[r * numCols + c] = val;
}

// Identify a box starting at position (r,c)
function identifyBox(r, c) {
  let val = cell(r, c);
  if (val === 2) { // '['
    // next cell should be ']'
    if (c+1 < numCols && cell(r, c+1) === 3) {
      return [[r, c], [r, c+1]];
    }
  } else if (val === 3) { // ']'
    // previous cell should be '['
    if (c-1 >= 0 && cell(r, c-1) === 2) {
      return [[r, c-1], [r, c]];
    }
  }
  return null;
}

function attemptMove(dR, dC) {
  const nextR = robotRow + dR;
  const nextC = robotCol + dC;
  const nextVal = cell(nextR, nextC);

  if (nextVal === 1) { // '#'
    // Wall
    return;
  }

  if (nextVal === 0) { // '.'
    // Just move robot
    setCell(robotRow, robotCol, 0);
    setCell(nextR, nextC, 4);
    robotRow = nextR;
    robotCol = nextC;
    return;
  }

  // If nextVal is '['=2 or ']'=3, we have a box
  if (nextVal === 2 || nextVal === 3) {
    let boxes = [];
    let firstBox = identifyBox(nextR, nextC);
    if (!firstBox) return; 
    boxes.push(firstBox);

    // Find chain of boxes and empty space
    while (true) {
      let lastBox = boxes[boxes.length - 1];
      let boxR = lastBox[0][0];
      let boxC = lastBox[0][1]; // '[' cell of last box
      let aheadR = boxR + dR;
      let aheadC = boxC + dC;

      if (aheadR < 0 || aheadR >= numRows || aheadC < 0 || aheadC + 1 >= numCols) {
        // out of bounds
        return;
      }

      let cellAhead1 = cell(aheadR, aheadC);
      let cellAhead2 = cell(aheadR, aheadC + 1);

      if (cellAhead1 === 1 || cellAhead2 === 1) {
        // Wall ahead
        return;
      }

      if (cellAhead1 === 0 && cellAhead2 === 0) {
        // Empty space found
        break; // we can push now
      }

      // Another box?
      if ((cellAhead1 === 2 || cellAhead1 === 3) && cellAhead2 === 3) {
        let candidateBox = identifyBox(aheadR, aheadC);
        if (candidateBox) {
          boxes.push(candidateBox);
          continue;
        }
      }

      // No suitable space or next box
      return;
    }

    // Found empty space to push into
    let oldPositions = boxes.map(b => b.map(x => [x[0], x[1]]));

    // Pushing sequence:
    // 1. Free the robot cell
    setCell(robotRow, robotCol, 0);

    // 2. Place the last box into final empty cell
    {
      let lastBox = boxes[boxes.length - 1];
      let boxR = lastBox[0][0];
      let boxC = lastBox[0][1];
      let finalR = boxR + dR;
      let finalC = boxC + dC;
      setCell(finalR, finalC, 2);
      setCell(finalR, finalC + 1, 3);
    }

    // 3. Move each preceding box forward
    for (let i = boxes.length - 1; i > 0; i--) {
      let curBox = boxes[i];
      let prevBox = boxes[i - 1];
      let pR = prevBox[0][0];
      let pC = prevBox[0][1];

      setCell(pR + dR, pC + dC, 2);
      setCell(pR + dR, pC + dC + 1, 3);

      // Clear old curBox position
      let cR = curBox[0][0];
      let cC = curBox[0][1];
      setCell(cR, cC, 0);
      setCell(cR, cC + 1, 0);
    }

    // 4. Move the first box into robot's old position
    {
      let fbR = boxes[0][0][0];
      let fbC = boxes[0][0][1];
      setCell(robotRow + dR, robotCol + dC, 2);
      setCell(robotRow + dR, robotCol + dC + 1, 3);

      // Clear old position of first box
      setCell(fbR, fbC, 0);
      setCell(fbR, fbC + 1, 0);
    }

    // 5. Move robot into (nextR, nextC)
    setCell(nextR, nextC, 4);
    robotRow = nextR;
    robotCol = nextC;
  }
}

////////////////////////////////////////////////////////////////////////////////
// Step 5: Simulate Moves
////////////////////////////////////////////////////////////////////////////////
for (let m of moves) {
  const [dR, dC] = directions[m];
  attemptMove(dR, dC);
}

////////////////////////////////////////////////////////////////////////////////
// Step 6: Compute final score
////////////////////////////////////////////////////////////////////////////////
// For each box '[]', GPS = 100*r + c where (r,c) is the '[' cell.
let sumCoordinates = 0;
for (let r = 0; r < numRows; r++) {
  for (let c = 0; c < numCols - 1; c++) {
    if (cell(r, c) === 2 && cell(r, c+1) === 3) { // '[' ']' pair
      sumCoordinates += 100 * r + c;
    }
  }
}

console.log(sumCoordinates);
