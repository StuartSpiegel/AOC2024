import java.io.*;
import java.util.*;

public class ReindeerMaze {
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
        // Read input from input.txt
        BufferedReader br = new BufferedReader(new FileReader("input.txt"));
        List<String> lines = new ArrayList<>();
        String line;
        while ((line = br.readLine()) != null) {
            lines.add(line);
        }
        br.close();
        
        // Convert to char array
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
        // dx,dy for directions: east=(0,1), south=(1,0), west=(0,-1), north=(-1,0)
        int[] dr = {0, 1, 0, -1};
        int[] dc = {1, 0, -1, 0};

        // dist array: dist[r][c][d]
        int[][][] dist = new int[R][C][4];
        for (int i = 0; i < R; i++) {
            for (int j = 0; j < C; j++) {
                Arrays.fill(dist[i][j], Integer.MAX_VALUE);
            }
        }

        // Start facing East (d=0)
        dist[startR][startC][0] = 0;
        PriorityQueue<State> pq = new PriorityQueue<>();
        pq.add(new State(startR, startC, 0, 0));

        while (!pq.isEmpty()) {
            State cur = pq.poll();
            if (cur.cost > dist[cur.r][cur.c][cur.d]) continue;

            // If we reached E, we can output and break
            if (cur.r == endR && cur.c == endC) {
                System.out.println(cur.cost);
                return;
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

            // Turn right: (d+1)%4
            int rd = (d + 1) % 4;
            int costR = cost + 1000;
            if (costR < dist[r][c][rd]) {
                dist[r][c][rd] = costR;
                pq.add(new State(r, c, rd, costR));
            }

            // Turn left: (d+3)%4 same as (d-1)%4
            int ld = (d + 3) % 4;
            int costL = cost + 1000;
            if (costL < dist[r][c][ld]) {
                dist[r][c][ld] = costL;
                pq.add(new State(r, c, ld, costL));
            }
        }

        // If we somehow never reach E, print something
        System.out.println("No path found");
    }
}
