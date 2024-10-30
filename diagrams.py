import matplotlib.pyplot as plt

# Generate plots from the results file

def plot_results_from_file(filename):
    difficulties = ['Trivial', 'VeryEasy', 'Easy', 'Doable', 'OhBoy', 'Impossible']
    heuristics = ['Uniform Cost Search', 'Misplaced Tile Heuristic', 'Manhattan Distance Heuristic']
    results = {'expanded_nodes': {heuristic: [None] * len(difficulties) for heuristic in heuristics},
               'max_queue_size': {heuristic: [None] * len(difficulties) for heuristic in heuristics}}

    with open(filename, 'r') as file:
        lines = file.readlines()
        max_queue_section = False
        expanded_nodes_section = False
        for line in lines:
            line = line.strip()
            if 'Maximum Queue Size' in line:
                max_queue_section = True
                expanded_nodes_section = False
                continue
            elif 'Number of Nodes Expanded' in line:
                expanded_nodes_section = True
                max_queue_section = False
                continue

            if max_queue_section or expanded_nodes_section:
                if line.startswith('Difficulty'):
                    continue  # Skip headers
                parts = line.split()
                if len(parts) < len(heuristics) + 1:
                    continue  # Skip lines that do not contain enough data

                # 合并前两个部分作为难度名称，确保与 difficulties 匹配
                difficulty = ' '.join(parts[:2]).strip() if parts[0] in ['Very', 'Oh'] else parts[0]
                try:
                    difficulty_index = difficulties.index(difficulty)
                    values = [int(parts[i]) for i in range(1 if difficulty in difficulties else 2, len(parts))]
                except (ValueError, IndexError) as e:
                    print(f"Skipping line due to error: {line}, Error: {e}")
                    continue  # Skip lines with invalid data

                if max_queue_section:
                    for i, heuristic in enumerate(heuristics):
                        results['max_queue_size'][heuristic][difficulty_index] = values[i]
                elif expanded_nodes_section:
                    for i, heuristic in enumerate(heuristics):
                        results['expanded_nodes'][heuristic][difficulty_index] = values[i]

    # Fill missing data points with 0 for consistent plotting and log the results for verification
    for heuristic in heuristics:
        print(f"Data for {heuristic} - Nodes Expanded: {results['expanded_nodes'][heuristic]}")
        print(f"Data for {heuristic} - Max Queue Size: {results['max_queue_size'][heuristic]}")
        results['expanded_nodes'][heuristic] = [0 if value is None else value for value in
                                                results['expanded_nodes'][heuristic]]
        results['max_queue_size'][heuristic] = [0 if value is None else value for value in
                                                results['max_queue_size'][heuristic]]

    # Plot Number of Nodes Expanded - Line Chart
    plt.figure(figsize=(10, 5))
    for heuristic in heuristics:
        plt.plot(difficulties, results['expanded_nodes'][heuristic], marker='o', label=heuristic)
    plt.yscale('log')
    plt.xlabel('Puzzle (Difficulty)')
    plt.ylabel('Number of Nodes Expanded')
    plt.title('Number of Nodes Expanded Per Puzzle')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Maximum Queue Size - Line Chart
    plt.figure(figsize=(10, 5))
    for heuristic in heuristics:
        plt.plot(difficulties, results['max_queue_size'][heuristic], marker='o', label=heuristic)
    plt.yscale('log')
    plt.xlabel('Puzzle (Difficulty)')
    plt.ylabel('Maximum Queue Size')
    plt.title('Maximum Queue Size Per Puzzle')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Number of Nodes Expanded - Bar Chart
    plt.figure(figsize=(10, 5))
    width = 0.25
    x = range(len(difficulties))
    for i, heuristic in enumerate(heuristics):
        plt.bar([p + i * width for p in x], results['expanded_nodes'][heuristic], width=width, label=heuristic)
    plt.xticks([p + 1.5 * width for p in x], difficulties)
    plt.yscale('log')
    plt.xlabel('Puzzle (Difficulty)')
    plt.ylabel('Number of Nodes Expanded')
    plt.title('Number of Nodes Expanded Per Puzzle - Bar Chart')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    # choose data
    plot_results_from_file('results.txt')
