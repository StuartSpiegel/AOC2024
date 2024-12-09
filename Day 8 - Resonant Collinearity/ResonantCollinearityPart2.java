import java.util.*;
import java.io.*;

public class ResonantCollinearityPart2 {

    // Method to parse the input map into a list of antennas
    public static List<Antenna> parseInput(List<String> map) {
        List<Antenna> antennas = new ArrayList<>();
        for (int y = 0; y < map.size(); y++) {
            String row = map.get(y);
            for (int x = 0; x < row.length(); x++) {
                char c = row.charAt(x);
                if (c != '.') {
                    antennas.add(new Antenna(x, y, c));
                }
            }
        }
        return antennas;
    }

    // Method to calculate antinodes based on Part Two rules
    public static Set<Point> calculateAntinodes(List<Antenna> antennas, int width, int height) {
        Set<Point> antinodes = new HashSet<>();

        // Group antennas by frequency
        Map<Character, List<Antenna>> frequencyGroups = new HashMap<>();
        for (Antenna antenna : antennas) {
            frequencyGroups
                .computeIfAbsent(antenna.frequency, k -> new ArrayList<>())
                .add(antenna);
        }

        // Process each frequency group
        for (Map.Entry<Character, List<Antenna>> entry : frequencyGroups.entrySet()) {
            List<Antenna> group = entry.getValue();

            // Add all antennas in the group as antinodes (if there are at least two antennas of this frequency)
            if (group.size() > 1) {
                for (Antenna antenna : group) {
                    antinodes.add(new Point(antenna.x, antenna.y));
                }
            }

            // Consider all pairs of antennas in the group
            for (int i = 0; i < group.size(); i++) {
                for (int j = i + 1; j < group.size(); j++) {
                    Antenna a1 = group.get(i);
                    Antenna a2 = group.get(j);

                    // Calculate the vector between the antennas
                    int dx = a2.x - a1.x;
                    int dy = a2.y - a1.y;
                    int gcd = gcd(Math.abs(dx), Math.abs(dy));

                    // Reduce dx and dy to their smallest steps
                    dx /= gcd;
                    dy /= gcd;

                    // Add all points along the line between the antennas
                    int x = a1.x, y = a1.y;
                    while (isValid(x, y, width, height)) {
                        antinodes.add(new Point(x, y));
                        x += dx;
                        y += dy;
                    }

                    // Include the other direction
                    x = a1.x - dx;
                    y = a1.y - dy;
                    while (isValid(x, y, width, height)) {
                        antinodes.add(new Point(x, y));
                        x -= dx;
                        y -= dy;
                    }
                }
            }
        }

        return antinodes;
    }

    // Helper method to check if a point is within bounds
    private static boolean isValid(int x, int y, int width, int height) {
        return x >= 0 && x < width && y >= 0 && y < height;
    }

    // Helper method to calculate the greatest common divisor
    private static int gcd(int a, int b) {
        return b == 0 ? a : gcd(b, a % b);
    }

    public static void main(String[] args) throws IOException {
        // Read input map from file
        List<String> map = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader("input.txt"))) {
            String line;
            while ((line = br.readLine()) != null) {
                map.add(line);
            }
        }

        int height = map.size();
        int width = map.get(0).length();

        // Parse antennas from the input map
        List<Antenna> antennas = parseInput(map);

        // Calculate unique antinodes based on Part Two rules
        Set<Point> antinodes = calculateAntinodes(antennas, width, height);

        // Output the result
        System.out.println("Total unique antinode locations (Part 2): " + antinodes.size());
    }
}

// Class to represent an antenna
class Antenna {
    int x, y;
    char frequency;

    public Antenna(int x, int y, char frequency) {
        this.x = x;
        this.y = y;
        this.frequency = frequency;
    }
}

// Class to represent a point on the map
class Point {
    int x, y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Point)) return false;
        Point other = (Point) obj;
        return this.x == other.x && this.y == other.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
}
