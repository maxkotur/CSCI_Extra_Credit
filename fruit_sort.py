import heapq
import random

# Define the initial state
fruits = [['apple'+str(i) for i in range(1,11)], ['banana'+str(i) for i in range(1,11)], ['orange'+str(i) for i in range(1,11)]]
random.shuffle(fruits[0])
random.shuffle(fruits[1])
random.shuffle(fruits[2])
initial_state = fruits

# Define the goal state
goal_state = [['apple'+str(i) for i in range(1,11)], ['banana'+str(i) for i in range(1,11)], ['orange'+str(i) for i in range(1,11)]]

# Define the heuristic function
def heuristic(state):
    h = 0
    for i in range(3):
        for j in range(10):
            fruit = state[i][j]
            goal_pos = [(k, l) for k in range(3) for l in range(10) if goal_state[k][l] == fruit][0]
            h += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
    return h

# Define the function to generate successors
def generate_successors(state):
    successors = []
    for i in range(3):
        for j in range(9):
            # Swap horizontally
            new_state = [row[:] for row in state]
            new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
            successors.append(new_state)
        for j in range(10):
            # Swap vertically
            if i < 2:
                new_state = [row[:] for row in state]
                new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
                successors.append(new_state)
    return successors

# Define the A* algorithm
def astar(initial_state, goal_state, heuristic):
    open_list = [(heuristic(initial_state), initial_state)]
    closed_list = set()
    g_score = {str(initial_state): 0}
    f_score = {str(initial_state): heuristic(initial_state)}

    while open_list:
        current = heapq.heappop(open_list)[1]
        if current == goal_state:
            return g_score[str(current)], current

        closed_list.add(str(current))
        for successor in generate_successors(current):
            if str(successor) in closed_list:
                continue

            tentative_g_score = g_score[str(current)] + 1
            if str(successor) not in g_score or tentative_g_score < g_score[str(successor)]:
                g_score[str(successor)] = tentative_g_score
                f_score[str(successor)] = tentative_g_score + heuristic(successor)
                heapq.heappush(open_list, (f_score[str(successor)], successor))

    return float('inf')

# Test the algorithm with a random initial state
print('Initial state:')
for row in initial_state:
    print(row)

# Getting solution
num_moves, current = astar(initial_state, goal_state, heuristic)
print(f'Number of moves: {num_moves}')

for row in current:
    print(row)