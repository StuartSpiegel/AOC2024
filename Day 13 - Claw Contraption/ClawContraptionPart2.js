const fs = require('fs');

// Function to compute the Greatest Common Divisor (GCD) and coefficients using the Extended Euclidean Algorithm
function extendedGCD(a, b) {
    if (b === 0) return { gcd: a, x: 1, y: 0 };
    const { gcd, x: x1, y: y1 } = extendedGCD(b, a % b);
    return { gcd, x: y1, y: x1 - Math.floor(a / b) * y1 };
}

// Function to adjust coefficients to ensure non-negative token costs
function adjustCoefficients(x, y, a, b, gcd, scale) {
    const modX = Math.abs(b / gcd);
    const modY = Math.abs(a / gcd);

    // Adjust x and y to be non-negative
    while (x < 0) {
        x += modX;
        y -= modY;
    }
    while (y < 0) {
        x -= modX;
        y += modY;
    }

    // Ensure both x and y are non-negative
    if (x < 0 || y < 0) {
        return null; // Invalid adjustment
    }
    return { x, y };
}


// Function to solve a single claw machine problem
function solveMachine(machine) {
    const { buttonA, buttonB, prize } = machine;
    const { x: ax, y: ay } = buttonA;
    const { x: bx, y: by } = buttonB;
    const { x: px, y: py } = prize;

    // Solve for X-axis
    const { gcd: gcdX, x: xCoeff, y: yCoeff } = extendedGCD(ax, bx);
    if (px % gcdX !== 0) return null;

    const scaleX = px / gcdX;
    let aX = xCoeff * scaleX;
    let bX = yCoeff * scaleX;

    // Solve for Y-axis
    const { gcd: gcdY, x: xCoeffY, y: yCoeffY } = extendedGCD(ay, by);
    if (py % gcdY !== 0) return null;

    const scaleY = py / gcdY;
    let aY = xCoeffY * scaleY;
    let bY = yCoeffY * scaleY;

    // Check alignment
    if (gcdX !== gcdY) return null;

    // Synchronize solutions for X and Y
    const factorX = Math.abs(by / gcdY);
    const factorY = Math.abs(bx / gcdX);

    aX *= factorX;
    bX *= factorX;
    aY *= factorY;
    bY *= factorY;

    const totalA = aX + aY;
    const totalB = bX + bY;

    // Ensure all values are valid and non-negative
    if (totalA < 0 || totalB < 0) return null;

    // Calculate token cost
    const cost = totalA * 3 + totalB;
    return { minTokens: cost, aPresses: totalA, bPresses: totalB };
}


// Main function to process input and calculate results
function main() {
    const input = fs.readFileSync('input.txt', 'utf-8');
    const machines = input.trim().split('\n\n').map(block => {
        const lines = block.split('\n');

        const buttonA = lines[0].match(/X\+(\d+), Y\+(\d+)/);
        const buttonB = lines[1].match(/X\+(\d+), Y\+(\d+)/);
        const prize = lines[2].match(/X=(\d+), Y=(\d+)/);

        return {
            buttonA: { x: parseInt(buttonA[1], 10), y: parseInt(buttonA[2], 10) },
            buttonB: { x: parseInt(buttonB[1], 10), y: parseInt(buttonB[2], 10) },
            prize: { x: parseInt(prize[1], 10) + 10000000000000, y: parseInt(prize[2], 10) + 10000000000000 } // Adjusted prize positions
        };
    });

    let totalTokens = 0;
    let prizesWon = 0;

    machines.forEach((machine, index) => {
        const result = solveMachine(machine);
        if (result) {
            console.log(`Machine ${index + 1}: Win with ${result.minTokens} tokens (A: ${result.aPresses}, B: ${result.bPresses})`);
            totalTokens += result.minTokens;
            prizesWon++;
        } else {
            console.log(`Machine ${index + 1}: No solution`);
        }
    });

    console.log(`\nTotal Prizes Won: ${prizesWon}`);
    console.log(`Total Tokens Used: ${totalTokens}`);
}

// Run the main function
main();
