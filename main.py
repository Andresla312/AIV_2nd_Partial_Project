from environment import Environment

'''
Implementation of Dijkstra's algorithm to find the shortest path between nodes.
    Args:
        start_index: Index of starting node
        end_index: Index of target node
        edges: List of edges as tuples (start, end, weight)
        num_nodes: Total number of nodes in graph
    Returns:
        Tuple of (path as list of node indices, total path cost)
'''
def dijkstra(start_index, end_index, edges, num_nodes):
    import heapq

    # Create a graph from edges
    graph = {i: [] for i in range(num_nodes)}
    for a, b, w in edges:
        graph[a].append((b, w))

    # Initialize distances and previous nodes arrays
    distances = [float('inf')] * num_nodes
    previous = [None] * num_nodes
    distances[start_index] = 0

    #Priority queue using min-heap
    queue = [(0, start_index)]

    while queue:
        current_dist, current_node = heapq.heappop(queue)

        # Skip if we have already found a better path
        if current_dist > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Rebuild the path
    path = []
    node = end_index
    while node is not None:
        path.insert(0, node)
        node = previous[node]

    return path, distances[end_index]

# ---------- MAIN LOOP ----------
if __name__ == "__main__":
    # Initialize the environment and run the editor
    env = Environment()
    env.run_editor()

    # Get graph data from the environment
    nodes, edges, labels = env.get_graph_data()

    print("\nAvailable Nodes:")
    for i, label in enumerate(labels):
        print(label)

    # Get user input for start and end nodes
    start_letter = input("Start Node Letter: ").upper()
    end_letter = input("Target Node Letter: ").upper()

    if start_letter not in labels or end_letter not in labels:
        print("Invalid Nodes.")
        exit()

    start_index = labels.index(start_letter)
    end_index = labels.index(end_letter)

    # Run Dijkstra's algorithm
    path, total_cost = dijkstra(start_index, end_index, edges, len(nodes))

    # Display results
    if path:
        label_path = [labels[i] for i in path]
        print(f"\nShortest Distance: {', '.join(label_path)}")
        print(f"Total Cost: {total_cost}")
        env.highlight_path(path)
    else:
        print("There is no path between the selected nodes.")