import heapq
import math
import matplotlib.pyplot as plt


# This file is just to get all the data into one file for generating the plots

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
    expanded_nodes = 0

    while frontier:
        node = heapq.heappop(frontier)
        expanded_nodes += 1
        if problem.goal_test(node.state):
            return get_solution(node), expanded_nodes, max_queue_size
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
    return None, expanded_nodes, max_queue_size


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
    initial_states = [
        (1, 2, 3, 4, 5, 6, 7, 8, 0),  # Trivial
        (1, 2, 3, 4, 5, 6, 7, 0, 8),  # Very Easy
        (1, 2, 0, 4, 5, 3, 7, 8, 6),  # Easy
        (0, 1, 2, 4, 5, 3, 7, 8, 6),  # Doable
        (8, 7, 1, 6, 0, 2, 5, 4, 3),  # Oh Boy
        (1, 2, 3, 4, 5, 6, 8, 7, 0)   # Impossible
    ]
    heuristics = ['uniform_cost', 'misplaced_tile', 'euclidean_distance']

    results = {heuristic: {'expanded_nodes': [], 'max_queue_size': []} for heuristic in heuristics}

    for heuristic in heuristics:
        print(f"\nTesting heuristic: {heuristic}\n")
        for initial_state in initial_states:
            problem = Problem(initial_state, (1, 2, 3, 4, 5, 6, 7, 8, 0))
            _, expanded_nodes, max_queue_size = a_star_search(problem, heuristic=heuristic)
            results[heuristic]['expanded_nodes'].append(expanded_nodes)
            results[heuristic]['max_queue_size'].append(max_queue_size)

    # Output results to file
    save_results_to_file(results, initial_states, heuristics)


def save_results_to_file(results, initial_states, heuristics):
    difficulties = ['Trivial', 'VeryEasy', 'Easy', 'Doable', 'OhBoy', 'Impossible']
    with open("results.txt", "w") as f:
        # Save maximum queue size
        f.write("Maximum Queue Size\n")
        f.write("{:<15} {:<25} {:<25} {:<25}\n".format("Difficulty", *heuristics))
        for i, difficulty in enumerate(difficulties):
            row = [difficulty]
            for heuristic in heuristics:
                row.append(str(results[heuristic]['max_queue_size'][i]))
            f.write("{:<15} {:<25} {:<25} {:<25}\n".format(*row))

        # Save number of nodes expanded
        f.write("\nNumber of Nodes Expanded\n")
        f.write("{:<15} {:<25} {:<25} {:<25}\n".format("Difficulty", *heuristics))
        for i, difficulty in enumerate(difficulties):
            row = [difficulty]
            for heuristic in heuristics:
                row.append(str(results[heuristic]['expanded_nodes'][i]))
            f.write("{:<15} {:<25} {:<25} {:<25}\n".format(*row))


if __name__ == "__main__":
    main()
