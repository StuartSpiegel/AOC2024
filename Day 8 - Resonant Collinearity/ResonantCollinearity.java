import java.util.*;
import java.io.*;

public class ResonantCollinearity {

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

    // Method to calculate antinodes
    public static Set<Point> calculateAntinodes(List<Antenna> antennas, int width, int height) {
        Set<Point> antinodes = new HashSet<>();

        for (int i = 0; i < antennas.size(); i++) {
            for (int j = i + 1; j < antennas.size(); j++) {
                Antenna a1 = antennas.get(i);
                Antenna a2 = antennas.get(j);

                // Only consider antennas of the same frequency
                if (a1.frequency == a2.frequency) {
                    int dx = a2.x - a1.x;
                    int dy = a2.y - a1.y;

                    // Check for valid antinodes on either side of the antennas
                    int ax = a1.x - dx;
                    int ay = a1.y - dy;
                    int bx = a2.x + dx;
                    int by = a2.y + dy;

                    if (isValid(ax, ay, width, height)) {
                        antinodes.add(new Point(ax, ay));
                    }
                    if (isValid(bx, by, width, height)) {
                        antinodes.add(new Point(bx, by));
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

        // Calculate unique antinodes
        Set<Point> antinodes = calculateAntinodes(antennas, width, height);

        // Output the result
        System.out.println("Total unique antinode locations: " + antinodes.size());
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
