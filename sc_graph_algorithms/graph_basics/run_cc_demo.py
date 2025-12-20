"""
run_cc_demo.py

End-to-end demo:
toy kNN graph -> BFS -> connected components.
"""

from toy_graph import graph
from connected_components import connected_components


def main():
    componets = connected_components(graph)
    print("Connected components (clusters):")
    for i, comp in enumerate(componets):
        print(f"Cluster {i}: {sorted(comp)}")


if __name__ == "__main__":
    main()
