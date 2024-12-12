import java.util.*;
import java.io.*;

public class GardenGroups {

    // Method to calculate the total price of fencing all regions
    public static int calculateTotalFenceCost(char[][] map) {
        int rows = map.length;
        int cols = map[0].length;
        boolean[][] visited = new boolean[rows][cols];
        int totalCost = 0;

        // Iterate through each cell in the map
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                // If the cell is not visited, process the region
                if (!visited[r][c]) {
                    char plantType = map[r][c];
                    int[] areaAndPerimeter = calculateRegion(map, visited, r, c, plantType);
                    int area = areaAndPerimeter[0];
                    int perimeter = areaAndPerimeter[1];
                    totalCost += area * perimeter;
                }
            }
        }

        return totalCost;
    }

    // Method to calculate the area and perimeter of a region using BFS
    private static int[] calculateRegion(char[][] map, boolean[][] visited, int startRow, int startCol, char plantType) {
        int rows = map.length;
        int cols = map[0].length;
        int area = 0;
        int perimeter = 0;

        // Directions for moving up, down, left, and right
        int[][] directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        Queue<int[]> queue = new LinkedList<>();
        queue.add(new int[]{startRow, startCol});
        visited[startRow][startCol] = true;

        while (!queue.isEmpty()) {
            int[] cell = queue.poll();
            int row = cell[0];
            int col = cell[1];
            area++;

            // Check all four neighbors
            for (int[] dir : directions) {
                int newRow = row + dir[0];
                int newCol = col + dir[1];

                if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols) {
                    if (map[newRow][newCol] == plantType && !visited[newRow][newCol]) {
                        visited[newRow][newCol] = true;
                        queue.add(new int[]{newRow, newCol});
                    } else if (map[newRow][newCol] != plantType) {
                        // Neighbor is not part of the region, count as perimeter
                        perimeter++;
                    }
                } else {
                    // Out of bounds, count as perimeter
                    perimeter++;
                }
            }
        }

        return new int[]{area, perimeter};
    }

    public static void main(String[] args) {
        try {
            // Read the input from the file
            List<String> lines = new ArrayList<>();
            BufferedReader br = new BufferedReader(new FileReader("input.txt"));
            String line;
            while ((line = br.readLine()) != null) {
                lines.add(line);
            }
            br.close();

            // Convert the input into a 2D char array
            int rows = lines.size();
            int cols = lines.get(0).length();
            char[][] map = new char[rows][cols];
            for (int i = 0; i < rows; i++) {
                map[i] = lines.get(i).toCharArray();
            }

            // Calculate and print the total cost
            int totalCost = calculateTotalFenceCost(map);
            System.out.println("Total Cost: " + totalCost);
        } catch (IOException e) {
            System.err.println("Error reading input file: " + e.getMessage());
        }
    }
}
