"""
Undirected_Graph Class

This class represents an Undirected_Graph data structure and provides methods for adding and removing edges between vertices,
Also, it provides methods for checking edge existence, counting connected components, getting the size of the graph, and clearing the graph.
also it provides methods for checking if the graph is connected or not.


@ Author            Reda Ghanem
@ Version           1.0
@ Last update       11/11/2023
"""

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ********************  importing libraries and classes  ************************ #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #

# [1]- importing libraries
import numpy as np

# ⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️⤵️ #


# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #
# ┃----------------------- # Undirected_Graph Class # -------------------------┃ #
# ┃━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┃ #

class Undirected_Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.adj_matrix = np.zeros((vertices, vertices), dtype=bool)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def add_edge(self, source, destination):
        # Add an edge between source and destination if the edge doesn't already exist
        if not self.edge_exists(source, destination):
            self.adj_matrix[source][destination] = True
            self.adj_matrix[destination][source] = True

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def remove_edge(self, source, destination):
        # Remove the edge between source and destination if the edge already exist
        if self.edge_exists(source, destination):
            self.adj_matrix[source][destination] = False
            self.adj_matrix[destination][source] = False

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def edge_exists(self, source, destination):
        # Check if the edge exists
        return self.adj_matrix[source][destination]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def is_connected(self):
        """
        Checks if the graph is connected.

        Returns:
        - bool: True if the graph is connected, False otherwise.
        """
        if self.vertices == 0:
            return False

        visited = np.zeros(self.vertices, dtype=bool)
        queue = []

        # Start BFS from the first vertex
        queue.append(0)

        while queue:
            vertex = queue.pop(0)

            # Visit the vertex if it's not visited yet
            if not visited[vertex]:
                visited[vertex] = True

                # Visit all neighbors of the current vertex
                for neighbor in np.where(self.adj_matrix[vertex])[0]:
                    if not visited[neighbor]:
                        queue.append(neighbor)

        # If all vertices are visited, the graph is connected
        return all(visited)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def count_connected_components(self):
        visited = np.zeros(self.vertices, dtype=bool)   # Keep track of visited vertices
        count = 0                                       # Initialize the count of connected components
        # Iterate over all vertices
        for i in range(self.vertices):
            # If the current vertex is unvisited, perform DFS to explore the connected component
            if not visited[i]:
                self.DFS(i, visited)
                count += 1              # Increment the count of connected components
        # Return the final count of connected components
        return count

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def DFS(self, start, visited):
        # Depth First Search Algorithm
        visited[start] = True

        # Find neighbors of the current vertex
        neighbors = np.where(self.adj_matrix[start])[0]

        for neighbor in neighbors:
            if not visited[neighbor]:
                self.DFS(neighbor, visited)  # Recursive call for unvisited neighbors

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def get_size(self):
        # Return the number of vertices in the graph
        return self.vertices

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
    def clear(self):
        # Clear the adjacency matrix by resetting all values to False
        self.adj_matrix = np.zeros((self.vertices, self.vertices), dtype=bool)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Test code
def test_grapgh_count_connected_components():
    graph = Undirected_Graph(4)
    print("Initial number of Subgraphs:", graph.count_connected_components())

    graph.add_edge(0, 1)
    print("Number of Subgraphs after adding edge between 0 and 1:", graph.count_connected_components())

    graph.add_edge(0, 2)
    print("Number of Subgraphs after adding edge between 0 and 2:", graph.count_connected_components())

    graph.add_edge(1, 3)
    print("Number of Subgraphs after adding edge between 1 and 3:", graph.count_connected_components())

    graph.remove_edge(0, 1)
    print("Number of Subgraphs after removing edge between 0 and 1:", graph.count_connected_components())
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# Test code
def test_grapgh_is_connected():
    graph = Undirected_Graph(4)
    print("Initial number of Subgraphs:", graph.count_connected_components())
    graph.add_edge(0, 1)
    graph.add_edge(2, 1)
    graph.add_edge(2, 3)
    # test is_connected
    print("Is the graph connected?", graph.is_connected())
    # test after removing edge
    graph.remove_edge(0, 1)
    print("Is the graph connected after removing edge?", graph.is_connected())

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #


if __name__ == '__main__':
    test_grapgh_is_connected()
