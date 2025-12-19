"""
toy_graph.py

Toy kNN graph for single-cell graph algorithms.
"""

# Each node is a cell
# Each edge represents kNN similarity
graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1],
    3: [4, 5],
    4: [3, 5]
    5: [3, 4]
}

if __name__ == '__main__':
    for node. neighbors in graph.items():
        print(f'Cell {node} -> Neighbors {neighbors}')
