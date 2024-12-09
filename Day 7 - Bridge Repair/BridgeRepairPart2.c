#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

#define MAX_NUMBERS 10000

// Concatenation function: combines two numbers into one by concatenating their digits
long long concatenate(long long a, long long b) {
    long long factor = 1;
    while (factor <= b) {
        factor *= 10;
    }
    return a * factor + b;
}

// Function to evaluate the equation recursively with +, *, and ||
bool evaluate(long long numbers[], int n, long long target, int index, long long current_value) {
    if (index == n) {
        return current_value == target;
    }

    // Try addition
    if (evaluate(numbers, n, target, index + 1, current_value + numbers[index])) {
        return true;
    }

    // Try multiplication
    if (evaluate(numbers, n, target, index + 1, current_value * numbers[index])) {
        return true;
    }

    // Try concatenation
    if (evaluate(numbers, n, target, index + 1, concatenate(current_value, numbers[index]))) {
        return true;
    }

    return false;
}

// Function to parse a single line of input
int parse_line(char *line, long long numbers[], long long *target) {
    char *token = strtok(line, ":");
    *target = atoll(token); // Parse target

    int count = 0;
    token = strtok(NULL, " ");
    while (token != NULL && count < MAX_NUMBERS) {
        numbers[count++] = atoll(token); // Parse numbers
        token = strtok(NULL, " ");
    }

    return count;
}

int main() {
    const char *filename = "input.txt";
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Error opening input file");
        return 1;
    }

    char line[256];
    long long total_calibration = 0;

    while (fgets(line, sizeof(line), file)) {
        long long numbers[MAX_NUMBERS];
        long long target;

        int n = parse_line(line, numbers, &target);
        if (n > 0 && evaluate(numbers, n, target, 1, numbers[0])) {
            total_calibration += target;
        }
    }

    fclose(file);

    printf("Total Calibration Result (Part 2): %lld\n", total_calibration);
    return 0;
}
