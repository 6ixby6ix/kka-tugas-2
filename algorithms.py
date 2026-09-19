import heapq
import time
from romania_data import ROMANIA_MAP, get_heuristic

def greedy_bfs(start_city: str, goal_city: str):
    start_time = time.perf_counter()

    counter = 0
    h_start = get_heuristic(start_city, goal_city)
    pq = [(h_start, counter, start_city, [start_city], 0)]
    
    explored = set()
    steps = []
    step_num = 0
    
    result_path = []
    result_cost = 0
    found = False

    while pq:
        f, _, current, path, g = heapq.heappop(pq)

        if current in explored:
            continue

        explored.add(current)
        step_num += 1

        steps.append({
            'step': step_num,
            'city': current,
            'g': g,
            'h': f,
            'f': f,
            'path_so_far': " -> ".join(path),
            'action': f"Ekspansi kota {current} (h = {f})"
        })

        if current == goal_city:
            result_path = path
            result_cost = g
            found = True
            break

        for neighbor, edge_cost in sorted(ROMANIA_MAP[current].items()):
            if neighbor not in explored:
                counter += 1
                h_val = get_heuristic(neighbor, goal_city)
                new_g = g + edge_cost
                new_path = path + [neighbor]
                heapq.heappush(pq, (h_val, counter, neighbor, new_path, new_g))

    exec_time_ms = (time.perf_counter() - start_time) * 1000

    return {
        'algorithm': 'Greedy Best-First Search',
        'found': found,
        'path': result_path,
        'total_cost': result_cost,
        'nodes_expanded': len(explored),
        'steps': steps,
        'exec_time_ms': round(exec_time_ms, 3)
    }

def a_star_search(start_city: str, goal_city: str):
    start_time = time.perf_counter()

    counter = 0
    h_start = get_heuristic(start_city, goal_city)
    f_start = 0 + h_start
    pq = [(f_start, counter, start_city, [start_city], 0)]

    best_g = {start_city: 0}
    explored = set()
    steps = []
    step_num = 0

    result_path = []
    result_cost = 0
    found = False

    while pq:
        f, _, current, path, g = heapq.heappop(pq)

        if current in explored:
            continue

        explored.add(current)
        step_num += 1
        h_val = get_heuristic(current, goal_city)

        steps.append({
            'step': step_num,
            'city': current,
            'g': g,
            'h': h_val,
            'f': f,
            'path_so_far': " -> ".join(path),
            'action': f"Ekspansi kota {current} (g={g}, h={h_val}, f={f})"
        })

        if current == goal_city:
            result_path = path
            result_cost = g
            found = True
            break

        for neighbor, edge_cost in sorted(ROMANIA_MAP[current].items()):
            new_g = g + edge_cost
            if neighbor not in best_g or new_g < best_g[neighbor]:
                best_g[neighbor] = new_g
                counter += 1
                new_h = get_heuristic(neighbor, goal_city)
                new_f = new_g + new_h
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_f, counter, neighbor, new_path, new_g))

    exec_time_ms = (time.perf_counter() - start_time) * 1000

    return {
        'algorithm': 'A* Search',
        'found': found,
        'path': result_path,
        'total_cost': result_cost,
        'nodes_expanded': len(explored),
        'steps': steps,
        'exec_time_ms': round(exec_time_ms, 3)
    }
