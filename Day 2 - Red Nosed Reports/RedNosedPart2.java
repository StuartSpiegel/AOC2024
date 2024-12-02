import java.io.*;
import java.util.*;

public class RedNosedReportsPartTwo {

    public static void main(String[] args) {
        String inputFile = "input.txt";

        try {
            // Read reports from the input file
            List<List<Integer>> reports = readReports(inputFile);

            // Count the number of safe reports (with Problem Dampener)
            int safeReportCount = countSafeReports(reports);

            // Print the result
            System.out.println("Number of Safe Reports: " + safeReportCount);

        } catch (IOException e) {
            System.err.println("Error reading the input file: " + e.getMessage());
        }
    }

    /**
     * Reads the input file and parses each report as a list of integers.
     * @param fileName The input file containing the reports.
     * @return A list of reports, where each report is a list of integers.
     * @throws IOException If an error occurs while reading the file.
     */
    private static List<List<Integer>> readReports(String fileName) throws IOException {
        List<List<Integer>> reports = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String line;
            while ((line = br.readLine()) != null) {
                List<Integer> report = new ArrayList<>();
                for (String num : line.trim().split("\\s+")) {
                    report.add(Integer.parseInt(num));
                }
                reports.add(report);
            }
        }

        return reports;
    }

    /**
     * Counts the number of safe reports, allowing one level to be removed for unsafe reports.
     * @param reports The list of reports.
     * @return The number of safe reports.
     */
    private static int countSafeReports(List<List<Integer>> reports) {
        int safeCount = 0;

        for (List<Integer> report : reports) {
            if (isSafe(report) || canBeSafeWithOneRemoval(report)) {
                safeCount++;
            }
        }

        return safeCount;
    }

    /**
     * Determines if a report is safe based on the given rules.
     * @param report The report to check.
     * @return True if the report is safe, otherwise false.
     */
    private static boolean isSafe(List<Integer> report) {
        if (report.size() < 2) {
            return false; // A single-level report cannot be increasing or decreasing
        }

        boolean increasing = report.get(1) > report.get(0);
        boolean decreasing = report.get(1) < report.get(0);

        for (int i = 1; i < report.size(); i++) {
            int diff = report.get(i) - report.get(i - 1);

            // Check if the difference is within the valid range
            if (Math.abs(diff) < 1 || Math.abs(diff) > 3) {
                return false;
            }

            // Check if the trend (increasing or decreasing) is consistent
            if ((increasing && diff <= 0) || (decreasing && diff >= 0)) {
                return false;
            }
        }

        return true;
    }

    /**
     * Determines if a report can be made safe by removing one level.
     * @param report The report to check.
     * @return True if the report can be safe after removing one level, otherwise false.
     */
    private static boolean canBeSafeWithOneRemoval(List<Integer> report) {
        if (report.size() < 3) {
            return false; // Cannot remove one level and still have a valid report
        }

        for (int i = 0; i < report.size(); i++) {
            // Create a new report excluding the i-th level
            List<Integer> modifiedReport = new ArrayList<>(report);
            modifiedReport.remove(i);

            // Check if the modified report is safe
            if (isSafe(modifiedReport)) {
                return true;
            }
        }

        return false;
    }
}
