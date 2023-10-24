import numpy as np
import time
import heapq

start = time.time()

# Create the initial state
# Create an array with the numbers 0-8
initial_numbers = np.arange(9)

# Shuffle the numbers into random order
np.random.shuffle(initial_numbers)

# Reshape the array into 3x3
initial_state = initial_numbers.reshape((3, 3))
print("Initial State:\n", initial_state)

# Define the goal state
# Create an array
numbers = [[1,2,3], [8,0,4], [7,6,5]]
numbers2 = np.array(numbers)

# Reshape the array into 3x3
goal_state = numbers2.reshape((3,3))
print("Goal State:\n ", goal_state)

# Define possible actions (Right, Down, Left, Up)
actions = [(0,1), (1,0), (0,-1), (-1,0)]

# Applies the specified action to the current state of the puzzle
# Returns child state
def apply_action(current_state, action):
    # Find the position of the empty space (0)
    empty_row, empty_col = None, None
    for row in range(3):
        for col in range(3):
            if current_state[row][col] == 0:
                empty_row, empty_col = row, col
                break

    # Calculate the new position after the action
    new_row = empty_row + action[0]
    new_col = empty_col + action[1]

    # Check if the new position is within bounds
    if 0 <= new_row < 3 and 0 <= new_col < 3:
        # Create a copy of the current state
        new_state = current_state.copy()

        # Create temporary variables to hold the values of the empty space and the adjacent tile
        temp_empty = new_state[empty_row][empty_col]
        temp_tile = new_state[new_row][new_col] 

        # Swap the empty space with the adjacent tile
        new_state[empty_row][empty_col] = temp_tile
        new_state[new_row][new_col] = temp_empty

        return new_state
    else:
        #Invalid action
        return None
   
def calculate_costs(current_state, goal_state):
    # Calculate the Manhattan distance
    distance = 0
    for number in range(1, 9): 
        x1, y1 = np.where(current_state == number)
        x2, y2 = np.where(goal_state == number)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance.item()


def a_star():
    print("**********A* SEARCH**********")
    goal_found = False
    
    open = []
    closed = []
    children = []
    visited = []
    # Unique counter for each state
    unique_counter = 0 
    # Put initial state onto heap
    heapq.heappush(open, (calculate_costs(initial_state, goal_state), unique_counter, initial_state, 0))

    while open and not goal_found:
        _, _, current, g_value = heapq.heappop(open)
        current_state = np.array(current)
        closed.append(current_state)
        print("Visited State: \n", current_state)

        # Check if the current state is equivalent to the goal state
        if np.all(current_state == goal_state):
            print("Goal State Found!\n")
            print("number of nodes visited: ", len(visited))
            print("run time: ", time.time() - start)
            goal_found = True
            break

        # Apply actions
        # Apply action - Right
        child_state = apply_action(current_state, (0,1))
        children.append(child_state)

        # Apply action - Down
        child_state = apply_action(current_state, (1,0))
        children.append(child_state)

        # Apply action - Left
        child_state = apply_action(current_state, (0,-1))
        children.append(child_state)

        # Apply action - Up
        child_state = apply_action(current_state, (-1,0))
        children.append(child_state)

        # Loop through children
        for child in children:
            # Check if the child state has already been visited
            if child is not None and not any(np.all(child == state) for state in visited):
                if not any(np.all(child == state) for state in closed):
                    unique_counter += 1
                    # Calculate the cost of the child state
                    g = g_value + 1
                    f = g + calculate_costs(child, goal_state)
                    child_state = child.tolist()
                    heapq.heappush(open, (f, unique_counter, child_state, g))
                    visited.append(child_state)

        children.clear()

a_star()