import java.io.*;
import java.util.*;

public class HistorianHysteriaPartTwo {

    public static void main(String[] args) {
        String inputFile = "input.txt";
        
        try {
            // Read the input file and parse the two lists
            List<int[]> lists = readInputFile(inputFile);
            int[] leftList = lists.get(0);
            int[] rightList = lists.get(1);

            // Calculate the similarity score
            int similarityScore = calculateSimilarityScore(leftList, rightList);

            // Print the result
            System.out.println("Similarity Score: " + similarityScore);

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
     * Calculates the similarity score between two lists.
     * @param leftList The first list of integers.
     * @param rightList The second list of integers.
     * @return The similarity score.
     */
    private static int calculateSimilarityScore(int[] leftList, int[] rightList) {
        // Create a frequency map for the right list
        Map<Integer, Integer> rightListFrequency = new HashMap<>();
        for (int num : rightList) {
            rightListFrequency.put(num, rightListFrequency.getOrDefault(num, 0) + 1);
        }

        int similarityScore = 0;

        // Calculate the similarity score for the left list
        for (int num : leftList) {
            int frequency = rightListFrequency.getOrDefault(num, 0);
            similarityScore += num * frequency;
        }

        return similarityScore;
    }
}
