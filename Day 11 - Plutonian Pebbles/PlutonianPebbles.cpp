#include <iostream>
#include <fstream>
#include <queue>
#include <string>
#include <algorithm>

using namespace std;

// Helper function to split a number into two halves without leading zeros
pair<int, int> splitNumber(int number) {
    string numStr = to_string(number);
    size_t len = numStr.length();
    size_t mid = len / 2;

    string leftStr = numStr.substr(0, mid);
    string rightStr = numStr.substr(mid);

    // Remove leading zeros
    leftStr.erase(0, leftStr.find_first_not_of('0'));
    rightStr.erase(0, rightStr.find_first_not_of('0'));

    // Handle empty strings after trimming leading zeros
    int left = leftStr.empty() ? 0 : stoi(leftStr);
    int right = rightStr.empty() ? 0 : stoi(rightStr);

    return {left, right};
}

// Function to perform a single blink
void blink(queue<int> &stones) {
    size_t currentSize = stones.size();
    for (size_t i = 0; i < currentSize; ++i) {
        int stone = stones.front();
        stones.pop();

        if (stone == 0) {
            stones.push(1);
        } else {
            string stoneStr = to_string(stone);
            if (stoneStr.length() % 2 == 0) {
                auto [left, right] = splitNumber(stone);
                stones.push(left);
                stones.push(right);
            } else {
                stones.push(stone * 2024);
            }
        }
    }
}

// Helper function to trim whitespace from a string
string trim(const string &str) {
    size_t first = str.find_first_not_of(" \t\n\r");
    size_t last = str.find_last_not_of(" \t\n\r");
    return (first == string::npos || last == string::npos) ? "" : str.substr(first, last - first + 1);
}

int main() {
    // Read initial arrangement of stones from input.txt
    ifstream inputFile("input.txt");
    if (!inputFile) {
        cerr << "Error: Could not open input.txt" << endl;
        return 1;
    }

    queue<int> stones;
    string line;
    int lineNumber = 0;

    while (getline(inputFile, line)) {
        lineNumber++;
        try {
            line = trim(line); // Trim leading and trailing whitespace

            if (!line.empty()) {
                stones.push(stoi(line));
            } else {
                cerr << "Warning: Skipping empty or whitespace-only line at line " << lineNumber << "." << endl;
            }
        } catch (const invalid_argument &e) {
            cerr << "Error: Invalid number at line " << lineNumber << ": '" << line << "'" << endl;
            return 1;
        } catch (const out_of_range &e) {
            cerr << "Error: Number out of range at line " << lineNumber << ": '" << line << "'" << endl;
            return 1;
        }
    }
    inputFile.close();

    if (stones.empty()) {
        cerr << "Error: No valid numbers found in input file." << endl;
        return 1;
    }

    int totalBlinks = 25; // Number of blinks to simulate

    for (int i = 0; i < totalBlinks; ++i) {
        blink(stones);
    }

    cout << "Number of stones after " << totalBlinks << " blinks: " << stones.size() << endl;

    return 0;
}
