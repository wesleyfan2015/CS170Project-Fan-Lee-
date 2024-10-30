import heapq
import math


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, heuristic_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost
        self.total_cost = path_cost + heuristic_cost

    def __lt__(self, other):
        return self.total_cost < other.total_cost


class Problem:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def actions(self, state):
        actions = []
        zero_index = state.index(0)
        row, col = zero_index // 3, zero_index % 3
        if row > 0: actions.append('UP')
        if row < 2: actions.append('DOWN')
        if col > 0: actions.append('LEFT')
        if col < 2: actions.append('RIGHT')
        return actions

    def result(self, state, action):
        new_state = list(state)
        zero_index = state.index(0)
        row, col = zero_index // 3, zero_index % 3
        if action == 'UP':
            new_state[zero_index], new_state[zero_index - 3] = new_state[zero_index - 3], new_state[zero_index]
        elif action == 'DOWN':
            new_state[zero_index], new_state[zero_index + 3] = new_state[zero_index + 3], new_state[zero_index]
        elif action == 'LEFT':
            new_state[zero_index], new_state[zero_index - 1] = new_state[zero_index - 1], new_state[zero_index]
        elif action == 'RIGHT':
            new_state[zero_index], new_state[zero_index + 1] = new_state[zero_index + 1], new_state[zero_index]
        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal_state

    def step_cost(self, current_state, action):
        return 1

    def misplaced_tile_heuristic(self, state):
        return sum([1 if state[i] != self.goal_state[i] and state[i] != 0 else 0 for i in range(9)])

    def euclidean_distance_heuristic(self, state):
        distance = 0
        for i, value in enumerate(state):
            if value != 0:
                goal_index = self.goal_state.index(value)
                current_row, current_col = i // 3, i % 3
                goal_row, goal_col = goal_index // 3, goal_index % 3
                distance += math.sqrt((current_row - goal_row) ** 2 + (current_col - goal_col) ** 2)
        return distance


def a_star_search(problem, heuristic='misplaced_tile'):
    frontier = []
    initial_node = Node(problem.initial_state, path_cost=0,
                        heuristic_cost=get_heuristic_cost(problem, heuristic, problem.initial_state))
    heapq.heappush(frontier, initial_node)
    explored = set()
    max_queue_size = 1

    while frontier:
        node = heapq.heappop(frontier)
        print(f"Expanding state\n{format_state(node.state)}\n")
        print(f"g(n) = {node.path_cost}, h(n) = {node.heuristic_cost}, f(n) = {node.total_cost}\n")
        if problem.goal_test(node.state):
            print("Goal!!!")
            print(f"To solve this problem the search algorithm expanded a total of {len(explored)} nodes.")
            print(f"The maximum number of nodes in the queue at any one time: {max_queue_size}.")
            print(f"The depth of the goal node was {node.path_cost}.")
            return get_solution(node)
        explored.add(node.state)
        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            path_cost = node.path_cost + problem.step_cost(node.state, action)
            heuristic_cost = get_heuristic_cost(problem, heuristic, child_state)
            child_node = Node(child_state, parent=node, action=action, path_cost=path_cost,
                              heuristic_cost=heuristic_cost)
            if child_state not in explored and all(child_state != n.state for n in frontier):
                heapq.heappush(frontier, child_node)
        max_queue_size = max(max_queue_size, len(frontier))
    return None


def get_heuristic_cost(problem, heuristic, state):
    if heuristic == 'misplaced_tile':
        return problem.misplaced_tile_heuristic(state)
    elif heuristic == 'euclidean_distance':
        return problem.euclidean_distance_heuristic(state)
    elif heuristic == 'uniform_cost':
        return 0
    return 0


def get_solution(node):
    solution = []
    while node.parent is not None:
        solution.append(node.action)
        node = node.parent
    solution.reverse()
    return solution


def format_state(state):
    return f"{state[0]} {state[1]} {state[2]}\n{state[3]} {state[4]} {state[5]}\n{state[6]} {state[7]} {state[8]}"


def main():
    print("Welcome to (862276559) 8 puzzle solver.")
    choice = input("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle: ")
    if choice == "1":
        initial_state = (1, 2, 3, 4, 8, 0, 7, 6, 5)
    else:
        print("Enter your puzzle, use a zero to represent the blank")
        row1 = input("Enter the first row, use space or tabs between numbers: ").split()
        row2 = input("Enter the second row, use space or tabs between numbers: ").split()
        row3 = input("Enter the third row, use space or tabs between numbers: ").split()
        initial_state = tuple(map(int, row1 + row2 + row3))

    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    problem = Problem(initial_state, goal_state)

    print("\nEnter your choice of algorithm")
    print("1. Uniform Cost Search")
    print("2. A* with the Misplaced Tile heuristic.")
    print("3. A* with the Euclidean distance heuristic.")
    algorithm_choice = input("\n")

    if algorithm_choice == "1":
        heuristic = 'uniform_cost'
    elif algorithm_choice == "2":
        heuristic = 'misplaced_tile'
    elif algorithm_choice == "3":
        heuristic = 'euclidean_distance'
    else:
        print("Invalid choice. Exiting.")
        return

    solution = a_star_search(problem, heuristic=heuristic)
    if solution:
        print("Solution:", solution)
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
