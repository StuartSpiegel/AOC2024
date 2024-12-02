import java.io.*;
import java.util.*;

public class HistorianHysteriaFromFile {

    public static void main(String[] args) {
        String inputFile = "input.txt";
        
        try {
            // Read the input file and parse the two lists
            List<int[]> lists = readInputFile(inputFile);
            int[] leftList = lists.get(0);
            int[] rightList = lists.get(1);

            // Calculate the total distance
            int totalDistance = calculateTotalDistance(leftList, rightList);

            // Print the result
            System.out.println("Total Distance: " + totalDistance);

        } catch (IOException e) {
            System.err.println("Error reading the input file: " + e.getMessage());
        }
    }

    /**
     * Reads the input file and parses two lists of integers.
     * @param fileName The input file containing the two lists.
     * @return A list containing two integer arrays (left and right lists).
     * @throws IOException If an error occurs while reading the file.
     */
    private static List<int[]> readInputFile(String fileName) throws IOException {
        List<Integer> leftList = new ArrayList<>();
        List<Integer> rightList = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] numbers = line.trim().split("\\s+");
                if (numbers.length == 2) {
                    leftList.add(Integer.parseInt(numbers[0]));
                    rightList.add(Integer.parseInt(numbers[1]));
                }
            }
        }

        return Arrays.asList(
            leftList.stream().mapToInt(Integer::intValue).toArray(),
            rightList.stream().mapToInt(Integer::intValue).toArray()
        );
    }

    /**
     * Calculates the total distance between two sorted lists of integers.
     * @param leftList The first list of integers.
     * @param rightList The second list of integers.
     * @return The total distance.
     */
    private static int calculateTotalDistance(int[] leftList, int[] rightList) {
        // Sort both lists
        Arrays.sort(leftList);
        Arrays.sort(rightList);

        int totalDistance = 0;

        // Calculate the sum of distances between corresponding elements
        for (int i = 0; i < leftList.length; i++) {
            totalDistance += Math.abs(leftList[i] - rightList[i]);
        }

        return totalDistance;
    }
}
