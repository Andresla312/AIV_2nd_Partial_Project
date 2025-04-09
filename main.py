from environment import Environment

def dijkstra(start_index, end_index, edges, num_nodes):
    import heapq

    graph = {i: [] for i in range(num_nodes)}
    for a, b, w in edges:
        graph[a].append((b, w))
        graph[b].append((a, w))

    distances = [float('inf')] * num_nodes
    previous = [None] * num_nodes
    distances[start_index] = 0

    queue = [(0, start_index)]

    while queue:
        current_dist, current_node = heapq.heappop(queue)

        if current_dist > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Reconstruir el camino
    path = []
    node = end_index
    while node is not None:
        path.insert(0, node)
        node = previous[node]

    return path, distances[end_index]

# -------- MAIN LOOP -------------
if __name__ == "__main__":
    env = Environment()
    env.run_editor()

    nodes, edges, labels = env.get_graph_data()

    print("\nNODOS DISPONIBLES:")
    for i, label in enumerate(labels):
        print(f"{label} ({i}) - Posición: {nodes[i]}")

    # Elegir nodos de inicio y fin
    start_letter = input("Letra del nodo de inicio: ").upper()
    end_letter = input("Letra del nodo de destino: ").upper()

    if start_letter not in labels or end_letter not in labels:
        print("Nodos inválidos.")
        exit()

    start_index = labels.index(start_letter)
    end_index = labels.index(end_letter)

    path, total_cost = dijkstra(start_index, end_index, edges, len(nodes))

    if path:
        label_path = [labels[i] for i in path]
        print(f"\nCamino más corto: {', '.join(label_path)}")
        print(f"Costo total: {total_cost}")
        env.highlight_path(path)
    else:
        print("No hay camino entre los nodos seleccionados.")

