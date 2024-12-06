#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define MAX_ROWS 1000
#define MAX_COLS 1000

// Directions: UP, RIGHT, DOWN, LEFT
int dRow[] = {-1, 0, 1, 0};
int dCol[] = {0, 1, 0, -1};

// Function to check if the next position is within bounds and not a wall
bool isValid(int row, int col, int rows, int cols, char **map) {
    return row >= 0 && row < rows && col >= 0 && col < cols && map[row][col] != '#';
}

// Function to print the current map state with markers
void printMap(char **map, bool **visited, int rows, int cols, int guardRow, int guardCol) {
    printf("Current Map State:\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (i == guardRow && j == guardCol) {
                printf("G"); // Guard's current position
            } else if (visited[i][j]) {
                printf("X"); // Visited position
            } else {
                printf("%c", map[i][j]);
            }
        }
        printf("\n");
    }
    printf("\n");
}

int main() {
    char **map = NULL;
    int rows = 0, cols = 0, maxCols = 0;
    size_t lineSize = 0;
    char *line = NULL;

    // Open the input file
    FILE *file = fopen("input.txt", "r");
    if (!file) {
        printf("Error: Could not open input.txt\n");
        return 1;
    }

    // Read the map dynamically
    while (getline(&line, &lineSize, file) != -1) {
        if (rows == 0) {
            maxCols = strlen(line);
        }
        map = realloc(map, sizeof(char *) * (rows + 1));
        map[rows] = malloc(maxCols + 1);
        strncpy(map[rows], line, maxCols);
        map[rows][strcspn(map[rows], "\n")] = '\0'; // Remove newline character
        rows++;
    }
    fclose(file);
    free(line);

    printf("[INFO] Finished reading input. Map size: %d rows x %d columns.\n", rows, maxCols);

    int guardRow = -1, guardCol = -1, direction = 0;

    // Find the initial position of the guard and facing direction
    printf("[INFO] Searching for the guard's starting position...\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < maxCols; j++) {
            if (map[i][j] == '^') {
                guardRow = i;
                guardCol = j;
                direction = 0; // Facing UP
                printf("[INFO] Guard found at (%d, %d) facing UP.\n", guardRow, guardCol);
                break;
            } else if (map[i][j] == '>') {
                guardRow = i;
                guardCol = j;
                direction = 1; // Facing RIGHT
                printf("[INFO] Guard found at (%d, %d) facing RIGHT.\n", guardRow, guardCol);
                break;
            } else if (map[i][j] == 'v') {
                guardRow = i;
                guardCol = j;
                direction = 2; // Facing DOWN
                printf("[INFO] Guard found at (%d, %d) facing DOWN.\n", guardRow, guardCol);
                break;
            } else if (map[i][j] == '<') {
                guardRow = i;
                guardCol = j;
                direction = 3; // Facing LEFT
                printf("[INFO] Guard found at (%d, %d) facing LEFT.\n", guardRow, guardCol);
                break;
            }
        }
    }

    if (guardRow == -1 || guardCol == -1) {
        printf("Error: Guard's starting position not found in the map.\n");
        return 1;
    }

    // Allocate visited matrix
    bool **visited = malloc(rows * sizeof(bool *));
    for (int i = 0; i < rows; i++) {
        visited[i] = calloc(maxCols, sizeof(bool));
    }

    int distinctPositions = 0;

    // Simulate the guard's movement
    printf("[INFO] Starting simulation of guard's movement...\n");
    while (true) {
        // Mark the current position as visited
        if (!visited[guardRow][guardCol]) {
            visited[guardRow][guardCol] = true;
            distinctPositions++;
            printf("[TRACE] Guard visited (%d, %d). Distinct positions: %d\n", guardRow, guardCol, distinctPositions);
        }

        // Print the map state
        printMap(map, visited, rows, maxCols, guardRow, guardCol);

        // Calculate the next position
        int nextRow = guardRow + dRow[direction];
        int nextCol = guardCol + dCol[direction];

        if (isValid(nextRow, nextCol, rows, maxCols, map)) {
            // Move forward
            guardRow = nextRow;
            guardCol = nextCol;
            printf("[TRACE] Guard moved to (%d, %d).\n", guardRow, guardCol);
        } else {
            // Turn right (90 degrees)
            direction = (direction + 1) % 4;
            printf("[TRACE] Guard turned. New direction: %d\n", direction);
        }

        // Check if the guard leaves the map
        if (guardRow < 0 || guardRow >= rows || guardCol < 0 || guardCol >= maxCols) {
            printf("[INFO] Guard left the map at (%d, %d).\n", guardRow, guardCol);
            break;
        }
    }

    // Free memory
    for (int i = 0; i < rows; i++) {
        free(map[i]);
        free(visited[i]);
    }
    free(map);
    free(visited);

    // Print the result
    printf("[INFO] Simulation complete. Guard visited %d distinct positions.\n", distinctPositions);

    return 0;
}

