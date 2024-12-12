import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.function.Function;
import java.util.function.Predicate;

public class Day12Part2 {

    private static String INPUT = "";

    record Point(int i, int j){}
    enum EdgeDirection {LEFT_VERTICAL, RIGHT_VERTICAL, ABOVE_HORIZONTAL, BELOW_HORIZONTAL }
    record PointOnEdge(Point p, EdgeDirection dir){}

    private static final int[][] DIFFS = new int[][]{{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

    public static void solve() {
        try {
            INPUT = Files.readString(Path.of("input.txt"));
        } catch (IOException e) {
            System.err.println("Error reading input file: " + e.getMessage());
            return;
        }

        List<String> lines = Arrays.stream(INPUT.split("\n")).toList();

        Set<Point> allVisited = new HashSet<>();
        int total2 = 0;

        for (int i = 0; i < lines.size(); i++) {
            for (int j = 0; j < lines.get(i).length(); j++) {
                Point pt = new Point(i, j);
                if (allVisited.contains(pt)) continue;
                char ch = get(lines, pt);

                Set<Point> visited = bfs(pt,
                        neighbor -> get(lines, neighbor) == ch,
                        cur -> Arrays.stream(DIFFS).map(d -> new Point(cur.i + d[0], cur.j + d[1])).toList());

                Set<PointOnEdge> allEdgePoints = new HashSet<>();
                for (Point p : visited) {
                    for (int[] d : DIFFS) {
                        Point n = new Point(p.i + d[0], p.j + d[1]);
                        if (!visited.contains(n)) {
                            if (d[0] == 0) { // Vertical edge
                                allEdgePoints.add(new PointOnEdge(p,
                                        d[1] == -1 ? EdgeDirection.LEFT_VERTICAL : EdgeDirection.RIGHT_VERTICAL));
                            }
                            if (d[1] == 0) { // Horizontal edge
                                allEdgePoints.add(new PointOnEdge(p,
                                        d[0] == -1 ? EdgeDirection.ABOVE_HORIZONTAL : EdgeDirection.BELOW_HORIZONTAL));
                            }
                        }
                    }
                }

                int edges = 0;
                while (!allEdgePoints.isEmpty()) {
                    PointOnEdge start = allEdgePoints.iterator().next();
                    Set<PointOnEdge> edgeVisited = bfs(start,
                            allEdgePoints::contains,
                            cur -> Arrays.stream(DIFFS)
                                    .map(d -> new PointOnEdge(new Point(cur.p.i + d[0], cur.p.j + d[1]), cur.dir))
                                    .toList());

                    allEdgePoints.removeAll(edgeVisited);
                    edges++;
                }

                allVisited.addAll(visited);
                total2 += visited.size() * edges;
            }
        }

        System.out.println("Part 2: " + total2);
    }

    private static <T> Set<T> bfs(T start, Predicate<T> additionalNeighborCheck,
                                  Function<T, List<T>> neighborCreator) {
        Set<T> visited = new HashSet<>();
        Queue<T> queue = new ArrayDeque<>();
        visited.add(start);
        queue.add(start);

        while (!queue.isEmpty()) {
            T cp = queue.remove();
            for (T neighbor : neighborCreator.apply(cp)) {
                if (additionalNeighborCheck.test(neighbor) && !visited.contains(neighbor)) {
                    queue.add(neighbor);
                    visited.add(neighbor);
                }
            }
        }
        return visited;
    }

    private static char get(List<String> lines, Point p) {
        try {
            return lines.get(p.i).charAt(p.j);
        } catch (Exception e) {
            return '\0';
        }
    }

    public static void main(String[] args) {
        solve();
    }
}
