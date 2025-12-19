def connected_components(graph):
    visited = set()
    components = []

    for node in graph:
        if node not in visited:
            comp = bfs(graph, node)
            components.append(comp)
            visited |= comp
    return components
