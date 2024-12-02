
### Explanation:
- `3` appears 3 times in the `rightList`: `3 * 3 = 9`
- `4` appears 1 time in the `rightList`: `4 * 1 = 4`
- `2` appears 0 times in the `rightList`: `2 * 0 = 0`
- `1` appears 0 times in the `rightList`: `1 * 0 = 0`
- `3` appears 3 times in the `rightList`: `3 * 3 = 9`
- `3` appears 3 times in the `rightList`: `3 * 3 = 9`

**Total Similarity Score**: `9 + 4 + 0 + 0 + 9 + 9 = 31`

---

## Solution Overview

### Code Structure

The solution is implemented in a single Java file: `HistorianHysteriaPartTwo.java`.

#### Key Functions:
1. **`readInputFile(String fileName)`**:
   - Reads and parses the input file to extract the two lists of integers (`leftList` and `rightList`).
   - Returns the two lists as integer arrays.

2. **`calculateSimilarityScore(int[] leftList, int[] rightList)`**:
   - Creates a frequency map for the `rightList` to count occurrences of each integer.
   - Iterates through the `leftList` to calculate the similarity score using the frequency map.

---

### Data Structures

#### 1. **Frequency Map (HashMap)**
- **Purpose**: To store the frequency of each integer in the `rightList`.
- **Key**: The integer value from the `rightList`.
- **Value**: The count of occurrences of the integer.
- **Reason for Use**: HashMap provides `O(1)` average-time complexity for insertions and lookups, making it ideal for counting occurrences efficiently.

#### 2. **Arrays**
- **Purpose**: To store the numbers from the `leftList` and `rightList` for processing.
- **Reason for Use**: Arrays are simple, efficient, and allow direct indexing for fast traversal.

---

## Algorithm

### Steps:
1. **Read Input**:
   - Parse the `input.txt` file line by line.
   - Split each line into two integers and add them to `leftList` and `rightList`.

2. **Build Frequency Map**:
   - Traverse the `rightList` and count the occurrences of each number using a `HashMap`.

3. **Compute Similarity Score**:
   - Traverse the `leftList`.
   - For each number, retrieve its frequency from the frequency map.
   - Multiply the number by its frequency and add it to the total similarity score.

4. **Output Result**:
   - Print the total similarity score.

---

## How to Run

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd historian-hysteria
