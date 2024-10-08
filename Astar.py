import pygame
import sys
import heapq
import time
import tracemalloc

pygame.init()

track_move_ghost = []
track_move_pacman = []
track_time_ghost = []
track_time_pacman = []
track_current_memory_ghost = []
track_peak_memory_ghost = []
track_current_memory_pacman = []
track_peak_memory_pacman = []

WIDTH, HEIGHT = 700, 750
CELL_SIZE = 25
BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR = (0, 0, 255)
PACMAN_COLOR = (255, 255, 0)
COIN_COLOR = (255, 128, 13)
GHOST_COLOR = (255, 255, 255)

game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 2, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Map")

def draw_map():
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 1:
                pygame.draw.rect(screen, WALL_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif game_map[row][col] == 0:
                pygame.draw.rect(screen, BACKGROUND_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif game_map[row][col] == 2:
                pygame.draw.circle(screen, COIN_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 5)

def heuristic(point, goal):
    # Manhattan distance heuristic
    return abs(point[0] - goal[0]) + abs(point[1] - goal[1])

def heuristic_pacman(point, goal, ghost_positions):
    h = abs(point[0] - goal[0]) + abs(point[1] - goal[1])
    ghost_penalty = 0
    for ghost in ghost_positions:
        dist_to_ghost = abs(point[0] - ghost[0]) + abs(point[1] - ghost[1])
        if dist_to_ghost < 5:
            ghost_penalty += (5 - dist_to_ghost) * 10
    return h + ghost_penalty

def ghost_astar(start, goal):
    start_time = time.time()
    tracemalloc.start()
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            end_time = time.time()
            track_time_ghost.append(end_time-start_time)
            current_a, peak_a = tracemalloc.get_traced_memory()
            track_current_memory_ghost.append(current_a)
            track_peak_memory_ghost.append(peak_a)
            tracemalloc.stop()
            return path

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = current[0] + dx, current[1] + dy
            neighbor = (x, y)

            # Assuming uniform cost for each step
            tentative_g = g_score[current] + 1

            if 0 <= x < len(game_map) and 0 <= y < len(game_map[0]) and (game_map[x][y] == 0 or game_map[x][y] == 2):
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current

    return None  # No path found

def pacman_astar(start, goal, ghost_positions):
    start_time = time.time()
    tracemalloc.start()
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic_pacman(start, goal, ghost_positions)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            end_time = time.time()
            track_time_pacman.append(end_time-start_time)
            current_a, peak_a = tracemalloc.get_traced_memory()
            track_current_memory_pacman.append(current_a)
            track_peak_memory_pacman.append(peak_a)
            current_a, peak_a = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(game_map) and 0 <= neighbor[1] < len(game_map[0]) and game_map[neighbor[0]][neighbor[1]] != 1:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic_pacman(neighbor, goal, ghost_positions)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def find_nearest_coin(pacman_pos, ghost_positions):
    nearest_coin = None
    shortest_path = None
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 2:
                path = pacman_astar(pacman_pos, (row, col), ghost_positions)
                if path and (shortest_path is None or len(path) < len(shortest_path)):
                    shortest_path = path
                    nearest_coin = (row, col)
    # if shortest_path:
        # print("Pacman Path: ", shortest_path)
    return shortest_path

def main():
    pacman_x, pacman_y = None, None
    ghost_x, ghost_y = 1, 1
    ghost_move_counter = 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and pacman_x is None and pacman_y is None:
                mouse_x, mouse_y = event.pos
                pacman_x = mouse_x // CELL_SIZE
                pacman_y = mouse_y // CELL_SIZE
                if game_map[pacman_y][pacman_x] == 1:
                    pacman_x, pacman_y = None, None

        coin = []
        for row in range(len(game_map)):
            for col in range(len(game_map[row])):
                if game_map[row][col] == 2:
                    coin.append((row, col))
                    
        if pacman_x is not None and pacman_y is not None:
            ghost_positions = [(ghost_y, ghost_x)]
            path = find_nearest_coin((pacman_y, pacman_x), ghost_positions)
            if path:
                next_move = path[0]
                pacman_y, pacman_x = next_move
                track_move_pacman.append((pacman_y, pacman_x))
                if game_map[pacman_y][pacman_x] == 2:
                    game_map[pacman_y][pacman_x] = 0

            if ghost_move_counter == 2: 
                path = ghost_astar((ghost_y, ghost_x), (pacman_y, pacman_x))
                if path and len(path) > 1:
                    track_move_ghost.append((ghost_y, ghost_x))
                    ghost_y, ghost_x = path[1]
                ghost_move_counter = 0 
            else: 
                ghost_move_counter +=1

        if ghost_x == pacman_x and ghost_y == pacman_y:
            print("Game Over! The ghost caught Pac-Man!")
            print("Pacman Path: ", track_move_pacman)
            print("Pacman Cost Path: ", len(track_move_pacman))
            print("Pacman Time Average: ", sum(track_time_pacman)/len(track_time_pacman))
            print("Pacman Time Memory: ", sum(track_current_memory_pacman)/len(track_current_memory_pacman))
            print("Pacman Time Peak Memory Average: ", sum(track_peak_memory_pacman)/len(track_peak_memory_pacman))
            print("Ghost Path: ", track_move_ghost)
            print("Ghost Cost Path: ", len(track_move_ghost))
            print("Ghost Time Average: ", sum(track_time_ghost)/len(track_time_ghost))
            print("Ghost Time Memory: ", sum(track_current_memory_ghost)/len(track_current_memory_ghost))
            print("Ghost Time Peak Memory Average: ", sum(track_peak_memory_ghost)/len(track_peak_memory_ghost))
            pygame.quit()
            sys.exit()
        if len(coin) == 0:
            print("You won!")
            print("Pacman Path: ", track_move_pacman)
            print("Pacman Cost Path: ", len(track_move_pacman))
            print("Pacman Time Average: ", sum(track_time_pacman)/len(track_time_pacman))
            print("Pacman Time Memory: ", sum(track_current_memory_pacman)/len(track_current_memory_pacman))
            print("Pacman Time Peak Memory Average: ", sum(track_peak_memory_pacman)/len(track_peak_memory_pacman))
            print("Ghost Path: ", track_move_ghost)
            print("Ghost Cost Path: ", len(track_move_ghost))
            print("Ghost Time Average: ", sum(track_time_ghost)/len(track_time_ghost))
            print("Ghost Time Memory: ", sum(track_current_memory_ghost)/len(track_current_memory_ghost))
            print("Ghost Time Peak Memory Average: ", sum(track_peak_memory_ghost)/len(track_peak_memory_ghost))
            pygame.quit()
            sys.exit()
        screen.fill(BACKGROUND_COLOR)
        draw_map()
        
        if pacman_x is not None and pacman_y is not None:
            pygame.draw.circle(screen, PACMAN_COLOR, (pacman_x * CELL_SIZE + CELL_SIZE // 2, pacman_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
        
        pygame.draw.circle(screen, GHOST_COLOR, (ghost_x * CELL_SIZE + CELL_SIZE // 2, ghost_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()