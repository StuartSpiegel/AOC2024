import java.io.*;
import java.util.*;

public class ReindeerMazePart2 {
    static class State implements Comparable<State> {
        int r, c, d;
        int cost;
        State(int r, int c, int d, int cost) {
            this.r = r; this.c = c; this.d = d; this.cost = cost;
        }
        public int compareTo(State o) {
            return Integer.compare(this.cost, o.cost);
        }
    }
    
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader("input.txt"));
        List<String> lines = new ArrayList<>();
        String line;
        while ((line = br.readLine()) != null) {
            lines.add(line);
        }
        br.close();
        
        int R = lines.size();
        int C = lines.get(0).length();
        char[][] maze = new char[R][C];
        
        int startR = -1, startC = -1;
        int endR = -1, endC = -1;
        
        for (int i = 0; i < R; i++) {
            maze[i] = lines.get(i).toCharArray();
            for (int j = 0; j < C; j++) {
                if (maze[i][j] == 'S') {
                    startR = i; startC = j;
                }
                if (maze[i][j] == 'E') {
                    endR = i; endC = j;
                }
            }
        }

        // Directions: 0=East,1=South,2=West,3=North
        int[] dr = {0, 1, 0, -1};
        int[] dc = {1, 0, -1, 0};

        int[][][] dist = new int[R][C][4];
        for (int i = 0; i < R; i++) {
            for (int j = 0; j < C; j++) {
                Arrays.fill(dist[i][j], Integer.MAX_VALUE);
            }
        }

        // Start facing East
        dist[startR][startC][0] = 0;
        PriorityQueue<State> pq = new PriorityQueue<>();
        pq.add(new State(startR, startC, 0, 0));

        // Dijkstra to find minimal cost paths
        while (!pq.isEmpty()) {
            State cur = pq.poll();
            if (cur.cost > dist[cur.r][cur.c][cur.d]) continue;

            if (cur.r == endR && cur.c == endC) {
                // We found a minimal route to E. Not returning immediately,
                // because we need full dist array for part 2. But this is a hint.
            }

            int r = cur.r;
            int c = cur.c;
            int d = cur.d;
            int cost = cur.cost;

            // Move forward
            int nr = r + dr[d];
            int nc = c + dc[d];
            if (nr >= 0 && nr < R && nc >= 0 && nc < C && maze[nr][nc] != '#') {
                int newCost = cost + 1;
                if (newCost < dist[nr][nc][d]) {
                    dist[nr][nc][d] = newCost;
                    pq.add(new State(nr, nc, d, newCost));
                }
            }

            // Turn right
            int rd = (d + 1) % 4;
            int costR = cost + 1000;
            if (costR < dist[r][c][rd]) {
                dist[r][c][rd] = costR;
                pq.add(new State(r, c, rd, costR));
            }

            // Turn left
            int ld = (d + 3) % 4;
            int costL = cost + 1000;
            if (costL < dist[r][c][ld]) {
                dist[r][c][ld] = costL;
                pq.add(new State(r, c, ld, costL));
            }
        }

        // Find best cost at the end tile over all directions
        int bestCost = Integer.MAX_VALUE;
        for (int d = 0; d < 4; d++) {
            if (dist[endR][endC][d] < bestCost) {
                bestCost = dist[endR][endC][d];
            }
        }

        if (bestCost == Integer.MAX_VALUE) {
            System.out.println("No path found");
            return;
        }

        // bestCost is known. Now we find which tiles are on a best path.
        // We'll do a backward search from the end tile.
        boolean[][][] onBestPath = new boolean[R][C][4];
        Queue<int[]> queue = new LinkedList<>();

        // Start from all directions at (endR,endC) that achieve bestCost
        for (int d = 0; d < 4; d++) {
            if (dist[endR][endC][d] == bestCost) {
                onBestPath[endR][endC][d] = true;
                queue.add(new int[]{endR, endC, d});
            }
        }

        // Backward moves:
        // From (r,c,d):
        // 1) Forward step reversed: came from (r - dr[d], c - dc[d], d) with dist +1
        // 2) Turn right reversed: came from (r,c,(d+3)%4) with dist +1000
        // 3) Turn left reversed: came from (r,c,(d+1)%4) with dist +1000
        while (!queue.isEmpty()) {
            int[] cur = queue.poll();
            int r = cur[0], c = cur[1], d = cur[2];
            int curDist = dist[r][c][d];

            // Check forward predecessor
            int pr = r - dr[d];
            int pc = c - dc[d];
            if (pr >= 0 && pr < R && pc >= 0 && pc < C && maze[pr][pc] != '#') {
                // If we moved forward to get (r,c,d) from (pr,pc,d),
                // dist[pr][pc][d] = dist[r][c][d]-1
                if (curDist - 1 >= 0 && dist[pr][pc][d] == curDist - 1) {
                    if (!onBestPath[pr][pc][d]) {
                        onBestPath[pr][pc][d] = true;
                        queue.add(new int[]{pr, pc, d});
                    }
                }
            }

            // Check turn right predecessor
            // If we turned right to get direction d, we came from (r,c,(d+3)%4)
            // dist[r][c][(d+3)%4] = dist[r][c][d]-1000
            int leftD = (d + 3) % 4;
            if (curDist - 1000 >= 0 && dist[r][c][leftD] == curDist - 1000) {
                if (!onBestPath[r][c][leftD]) {
                    onBestPath[r][c][leftD] = true;
                    queue.add(new int[]{r, c, leftD});
                }
            }

            // Check turn left predecessor
            // If we turned left to get direction d, we came from (r,c,(d+1)%4)
            int rightD = (d + 1) % 4;
            if (curDist - 1000 >= 0 && dist[r][c][rightD] == curDist - 1000) {
                if (!onBestPath[r][c][rightD]) {
                    onBestPath[r][c][rightD] = true;
                    queue.add(new int[]{r, c, rightD});
                }
            }
        }

        // Now onBestPath[r][c][d] is true if that state is on a best path.
        // A tile is on a best path if any direction at that tile is on a best path.
        boolean[][] tileOnBest = new boolean[R][C];
        for (int r = 0; r < R; r++) {
            for (int c = 0; c < C; c++) {
                for (int d = 0; d < 4; d++) {
                    if (onBestPath[r][c][d]) {
                        tileOnBest[r][c] = true;
                        break;
                    }
                }
            }
        }

        // Count how many are on best path, and mark them
        int count = 0;
        for (int r = 0; r < R; r++) {
            for (int c = 0; c < C; c++) {
                if (tileOnBest[r][c] && maze[r][c] != '#') {
                    count++;
                }
            }
        }

        // Output results
        System.out.println("Minimal cost: " + bestCost);
        System.out.println("Tiles on at least one best path: " + count);

        // Create a copy of the maze to mark 'O'
        char[][] result = new char[R][C];
        for (int i = 0; i < R; i++) {
            System.arraycopy(maze[i], 0, result[i], 0, C);
        }

        for (int r = 0; r < R; r++) {
            for (int c = 0; c < C; c++) {
                if (tileOnBest[r][c] && (maze[r][c] == '.' || maze[r][c] == 'S' || maze[r][c] == 'E')) {
                    result[r][c] = 'O';
                }
            }
        }

        // Print the maze with O markings
        for (int i = 0; i < R; i++) {
            System.out.println(new String(result[i]));
        }
    }
}
