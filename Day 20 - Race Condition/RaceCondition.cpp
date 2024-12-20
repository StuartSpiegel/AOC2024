#include <bits/stdc++.h>
using namespace std;

struct Cell {
    int r, c;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    // Read the input map from input.txt
    // We assume the input is a rectangular grid of characters
    // We'll store it in a vector<vector<char>>
    freopen("input.txt", "r", stdin);

    vector<string> grid;
    {
        string line;
        while (getline(cin, line)) {
            if(!line.empty())
                grid.push_back(line);
        }
    }

    int R = (int)grid.size();
    int C = (int)(R > 0 ? grid[0].size() : 0);

    // Find S and E
    int start_r = -1, start_c = -1;
    int end_r = -1, end_c = -1;

    for (int r = 0; r < R; r++) {
        for (int c = 0; c < C; c++) {
            if (grid[r][c] == 'S') {
                start_r = r; start_c = c;
            }
            if (grid[r][c] == 'E') {
                end_r = r; end_c = c;
            }
        }
    }

    // Directions for movement
    int dr[4] = {1, -1, 0, 0};
    int dc[4] = {0, 0, 1, -1};

    auto inBounds = [&](int rr, int cc){
        return rr >= 0 && rr < R && cc >= 0 && cc < C;
    };

    auto isTrack = [&](int rr, int cc) {
        // Track includes '.' 'S' 'E' (any that is not '#')
        return grid[rr][cc] != '#';
    };

    // BFS from start to get distFromStart
    vector<vector<int>> distFromStart(R, vector<int>(C, -1));
    {
        queue<Cell>q;
        distFromStart[start_r][start_c] = 0;
        q.push({start_r, start_c});
        while(!q.empty()){
            auto [r,c] = q.front(); q.pop();
            for (int i=0; i<4; i++){
                int nr = r+dr[i], nc = c+dc[i];
                if(inBounds(nr,nc) && isTrack(nr,nc) && distFromStart[nr][nc] == -1){
                    distFromStart[nr][nc] = distFromStart[r][c]+1;
                    q.push({nr,nc});
                }
            }
        }
    }

    // BFS from end to get distToEnd
    vector<vector<int>> distToEnd(R, vector<int>(C, -1));
    {
        queue<Cell>q;
        distToEnd[end_r][end_c] = 0;
        q.push({end_r,end_c});
        while(!q.empty()){
            auto [r,c] = q.front(); q.pop();
            for (int i=0; i<4; i++){
                int nr = r+dr[i], nc = c+dc[i];
                if(inBounds(nr,nc) && isTrack(nr,nc) && distToEnd[nr][nc] == -1){
                    distToEnd[nr][nc] = distToEnd[r][c]+1;
                    q.push({nr,nc});
                }
            }
        }
    }

    // Normal shortest path from S to E:
    int normalDist = distFromStart[end_r][end_c];
    if (normalDist == -1) {
        // No path at all; no cheats matter. Just print 0.
        cout << 0 << "\n";
        return 0;
    }

    // Now we consider all possible cheats.
    // A cheat: choose a cell c_start (must be track and reachable from start),
    // then move through up to 2 cells ignoring walls, ending at c_end (must be track and reachable to end).
    // The cost of the cheat route is distFromStart[c_start] + 2 (the cheat steps) + distToEnd[c_end].
    // The saving = normalDist - that cost.

    // We must consider all pairs (c_start, c_end) that can be connected by exactly 2 steps
    // going through walls if needed. Both c_start and c_end must be on track.

    // We'll store cheats in a set to avoid duplicates if needed.
    // But the problem states each cheat is uniquely identified by start and end position
    // (the "start position" is where cheat is activated and "end position" is after the cheat moves).
    // We'll just count them directly.

    long long countAtLeast100 = 0;

    for (int r = 0; r < R; r++) {
        for (int c = 0; c < C; c++) {
            // c_start cell
            if (distFromStart[r][c] == -1) continue; // not reachable from start
            if (!isTrack(r,c)) continue; // must be track

            // From (r,c) try 2 steps in any combination of 4 directions:
            // We have to consider all sequences of two moves: (r,c) -> (r1,c1) -> (r2,c2)
            // (r1,c1) can be through a wall, (r2,c2) can also be through a wall,
            // but final (r2,c2) must be track and distToEnd[r2][c2] != -1.

            for (int i1 = 0; i1 < 4; i1++) {
                int r1 = r+dr[i1], c1 = c+dc[i1];
                if (!inBounds(r1,c1)) continue; 
                // first step can go through wall or track, no restriction
                for (int i2 = 0; i2 < 4; i2++) {
                    int r2 = r1+dr[i2], c2 = c1+dc[i2];
                    if (!inBounds(r2,c2)) continue;

                    // Check end cell of cheat
                    if (!isTrack(r2,c2)) continue; // must end on track
                    if (distToEnd[r2][c2] == -1) continue; // must reach end from there

                    // Compute the saving
                    int distWithCheat = distFromStart[r][c] + 2 + distToEnd[r2][c2];
                    int saving = normalDist - distWithCheat;
                    if (saving >= 100) {
                        countAtLeast100++;
                    }
                }
            }
        }
    }

    cout << countAtLeast100 << "\n";

    return 0;
}
