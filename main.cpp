#include <iostream>
#include <vector>
#include <queue>
#include <random>
#include <chrono>
#include <cmath>
#include <string>
#include <memory_resource>
#include <array>

struct Point { 
    int x, y; 
    
    bool operator==(const Point& other) const { 
        return x == other.x && y == other.y; 
    } 
    
    bool operator<(const Point& other) const {
        if (x != other.x) return x < other.x;
        return y < other.y;
    }
};

class PathfindingEngine {
private:
    int size;
    
   
    std::vector<int> grid;

    bool isValid(int x, int y) {
        return (x >= 0 && x < size && y >= 0 && y < size && grid[x * size + y] == 0);
    }

    int dx[4] = {-1, 1, 0, 0};
    int dy[4] = {0, 0, -1, 1};

public:
    PathfindingEngine(int s, double density) : size(s) {
        grid.assign(size * size, 0);
        std::random_device rd; 
        std::mt19937 gen(rd());
        std::uniform_real_distribution<> dis(0.0, 1.0);
        
        for(int r = 0; r < size; ++r) {
            for(int c = 0; c < size; ++c) {
                if(dis(gen) < density) grid[r * size + c] = 1;
            }
        }
        grid[0] = 0; 
        grid[(size-1) * size + (size-1)] = 0;
    }

    void runBFS() {
        int nodes_expanded = 0;
        int path_length = -1;
        
        std::vector<bool> visited(size * size, false);
        
        std::queue<std::pair<Point, int>> q; 
        
        auto start = std::chrono::high_resolution_clock::now();
        
        q.push({{0, 0}, 0});
        visited[0] = true; 

        while(!q.empty()) {
            auto [p, dist] = q.front();
            q.pop();
            nodes_expanded++;

            if(p.x == size-1 && p.y == size-1) { 
                path_length = dist; 
                break; 
            }

            for(int i = 0; i < 4; i++) {
                int nx = p.x + dx[i];
                int ny = p.y + dy[i];
        
                if(isValid(nx, ny) && !visited[nx * size + ny]) {
                    visited[nx * size + ny] = true;
                    q.push({{nx, ny}, dist + 1});
                }
      
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto dur = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
        
        std::cout << "BFS," << size << "," << path_length << "," << nodes_expanded << "," << dur << std::endl;
    }

    void runAStar() {
        int nodes_expanded = 0;
        int path_length = -1;
        
        auto heuristic = [&](int x, int y) { 
            return std::abs(x - (size-1)) + std::abs(y - (size-1)); 
        };

        using Element = std::pair<int, std::pair<Point, int>>;
        
    
        std::array<std::byte, 1024 * 1024> buffer; 
        
        std::pmr::monotonic_buffer_resource memory_pool(buffer.data(), buffer.size());

        std::priority_queue<
            Element, 
            std::pmr::vector<Element>, 
            std::greater<Element>
        > pq(&memory_pool);
        
        std::pmr::vector<int> g_score(size * size, 1e9, &memory_pool);

        auto start = std::chrono::high_resolution_clock::now();

        pq.push({heuristic(0, 0), {{0, 0}, 0}});
        g_score[0] = 0;

        while(!pq.empty()) {
            auto [f, data] = pq.top();
            auto [p, current_g] = data;
            pq.pop();
            nodes_expanded++;

            if(p.x == size-1 && p.y == size-1) { 
                path_length = current_g; 
                break; 
            }

            if(current_g > g_score[p.x * size + p.y]) continue;

            for(int i = 0; i < 4; i++) {
                int nx = p.x + dx[i];
                int ny = p.y + dy[i];
                
                if(isValid(nx, ny)) {
                    int tentative_g = current_g + 1;
                    if(tentative_g < g_score[nx * size + ny]) {
                        g_score[nx * size + ny] = tentative_g;
                        int f_score = tentative_g + heuristic(nx, ny);
                        pq.push({f_score, {{nx, ny}, tentative_g}});
                    }
                }
            }
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto dur = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
        
        std::cout << "A*," << size << "," << path_length << "," << nodes_expanded << "," << dur << std::endl;
    }
};

int main(int argc, char* argv[]) {
    int size = (argc > 1) ? std::stoi(argv[1]) : 50;
    PathfindingEngine engine(size, 0.15);
    engine.runBFS();
    engine.runAStar();
    return 0;
