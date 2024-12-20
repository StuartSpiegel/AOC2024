#include <bits/stdc++.h>
using namespace std;

struct Cell {
    int r, c;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    freopen("input.txt", "r", stdin);

    vector<string> grid;
    {
        string line;
        while (getline(cin, line)) {
            if (!line.empty())
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

    auto inBounds = [&](int rr, int cc) {
        return rr >= 0 && rr < R && cc >= 0 && cc < C;
    };

    auto isTrack = [&](int rr, int cc) {
        return grid[rr][cc] != '#';
    };

    // BFS from start
    vector<vector<int>> distFromStart(R, vector<int>(C, -1));
    {
        queue<Cell> q;
        distFromStart[start_r][start_c] = 0;
        q.push({start_r, start_c});
        int dr[4] = {1,-1,0,0};
        int dc[4] = {0,0,1,-1};
        while(!q.empty()){
            auto [r,c] = q.front(); q.pop();
            for (int i=0;i<4;i++){
                int nr = r+dr[i], nc = c+dc[i];
                if (inBounds(nr,nc) && isTrack(nr,nc) && distFromStart[nr][nc]==-1){
                    distFromStart[nr][nc]=distFromStart[r][c]+1;
                    q.push({nr,nc});
                }
            }
        }
    }

    // BFS from end
    vector<vector<int>> distToEnd(R, vector<int>(C, -1));
    {
        queue<Cell> q;
        distToEnd[end_r][end_c] = 0;
        q.push({end_r,end_c});
        int dr[4] = {1,-1,0,0};
        int dc[4] = {0,0,1,-1};
        while(!q.empty()){
            auto [r,c] = q.front(); q.pop();
            for (int i=0;i<4;i++){
                int nr = r+dr[i], nc = c+dc[i];
                if (inBounds(nr,nc) && isTrack(nr,nc) && distToEnd[nr][nc]==-1){
                    distToEnd[nr][nc]=distToEnd[r][c]+1;
                    q.push({nr,nc});
                }
            }
        }
    }

    int normalDist = distFromStart[end_r][end_c];
    if (normalDist == -1) {
        // No path at all
        cout << 0 << "\n";
        return 0;
    }

    // For identifying cheats uniquely by (start_pos, end_pos), we can store them in a map:
    // Key: (start_r, start_c, end_r, end_c), Value: best saving
    // Or use a map from pair of cells to best cost.
    // We'll use an unordered_map keyed by a tuple<int,int,int,int> for simplicity.

    struct Key {
        int sr, sc, er, ec;
        bool operator==(const Key &o) const {
            return sr==o.sr && sc==o.sc && er==o.er && ec==o.ec;
        }
    };
    struct KeyHash {
        std::size_t operator()(const Key &k) const {
            // a simple hash combine
            auto h1 = std::hash<int>()(k.sr);
            auto h2 = std::hash<int>()(k.sc);
            auto h3 = std::hash<int>()(k.er);
            auto h4 = std::hash<int>()(k.ec);
            // Combine them
            return ((h1 * 31 + h2)*31 + h3)*31 + h4;
        }
    };

    unordered_map<Key, int, KeyHash> bestCheatCost;

    int dr[4] = {1,-1,0,0};
    int dc[4] = {0,0,1,-1};

    // We'll iterate over all track cells c_start reachable from start
    // and run a BFS up to 20 steps ignoring walls.
    for (int sr=0; sr<R; sr++){
        for (int sc=0; sc<C; sc++){
            if (distFromStart[sr][sc] == -1) continue; // not reachable
            if (!isTrack(sr,sc)) continue; // must be track cell

            // BFS from (sr,sc) up to 20 steps, ignoring walls
            // We'll keep track of visited with step count to avoid reprocessing
            vector<vector<int>> stepsDist(R, vector<int>(C, -1));
            stepsDist[sr][sc] = 0;
            queue<Cell>q;
            q.push({sr,sc});
            while(!q.empty()){
                auto [r,c] = q.front(); q.pop();
                int d = stepsDist[r][c];
                if (d == 20) continue; // can't go further than 20 steps

                for (int i=0;i<4;i++){
                    int nr = r+dr[i], nc = c+dc[i];
                    if (!inBounds(nr,nc)) continue;
                    // We can move through walls here
                    if (stepsDist[nr][nc]==-1) {
                        stepsDist[nr][nc] = d+1;
                        q.push({nr,nc});
                        // If this is track and reachable to end
                        if (isTrack(nr,nc) && distToEnd[nr][nc]!=-1) {
                            int L = d+1; // cheat length
                            int distWithCheat = distFromStart[sr][sc] + L + distToEnd[nr][nc];
                            // record this cheat
                            Key k{sr,sc,nr,nc};
                            auto it = bestCheatCost.find(k);
                            if (it == bestCheatCost.end() || distWithCheat < it->second) {
                                bestCheatCost[k] = distWithCheat;
                            }
                        }
                    }
                }
            }
        }
    }

    // Now count how many have saving >= 100
    // saving = normalDist - distWithCheat
    // distWithCheat = distFromStart[c_start] + L + distToEnd[c_end]
    // We already have the best cheat costs in bestCheatCost.

    long long countAtLeast100 = 0;
    for (auto &entry : bestCheatCost) {
        int cost = entry.second;
        int saving = normalDist - cost;
        if (saving >= 100) {
            countAtLeast100++;
        }
    }

    cout << countAtLeast100 << "\n";

    return 0;
}
