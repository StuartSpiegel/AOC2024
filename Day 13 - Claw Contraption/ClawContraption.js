const fs = require('fs');

// Function to solve a single claw machine problem
function solveMachine(machine) {
    const { buttonA, buttonB, prize } = machine;
    const { x: ax, y: ay } = buttonA;
    const { x: bx, y: by } = buttonB;
    const { x: px, y: py } = prize;

    let minTokens = Infinity;
    let aPresses = -1;
    let bPresses = -1;

    for (let a = 0; a <= 100; a++) {
        for (let b = 0; b <= 100; b++) {
            const totalX = a * ax + b * bx;
            const totalY = a * ay + b * by;

            if (totalX === px && totalY === py) {
                const cost = a * 3 + b;
                if (cost < minTokens) {
                    minTokens = cost;
                    aPresses = a;
                    bPresses = b;
                }
            }
        }
    }

    return minTokens === Infinity ? null : { minTokens, aPresses, bPresses };
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
            prize: { x: parseInt(prize[1], 10), y: parseInt(prize[2], 10) }
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
