import networkx as nx
import matplotlib.pyplot as plt

def draw_max_plus_graph(weights):
    """
    Draw a max-plus graph with weights displayed as two connection lines.

    Args:
        weights (dict): A dictionary where keys are tuples representing edges (node1, node2),
                        and values are tuples (weight1, weight2) representing the weights of the edges.

    Returns:
        None
    """
    graph = nx.DiGraph()

    # Add nodes and edges to the graph
    for edge, weight in weights.items():
        node1, node2 = edge
        weight1, weight2 = weight
        graph.add_edge(node1, node2, weight1=weight1, weight2=weight2)

    # Create two separate edge lists for drawing
    edges1 = [(u, v) for u, v, w in graph.edges(data='weight1') if w != float("-inf")]
    edges2 = [(u, v) for u, v, w in graph.edges(data='weight2') if w != float("-inf")]

    # Calculate the optimal layout using the spring layout algorithm
    pos = nx.circular_layout(graph)

    # Draw the graph
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_labels(graph, pos, labels={node: f'x{node[1:]}' for node in graph.nodes()})
    nx.draw_networkx_edges(graph, pos, edgelist=edges1, edge_color='blue', width=2, arrows=True, connectionstyle="arc3,rad=0.2")
    nx.draw_networkx_edges(graph, pos, edgelist=edges2, edge_color='red', width=2, arrows=True, connectionstyle="arc3,rad=-0.2")

    # Add weight labels
    for edge, weight in weights.items():
        node1, node2 = edge
        weight1, weight2 = weight
        x1, y1 = pos[node1]
        x2, y2 = pos[node2]

        if weight1 != float("-inf"):
            plt.text(x1 + 0.5 * (x2 - x1), y1 + 0.5 * (y2 - y1) + 0.1, str(weight1), ha='center', va='center', color='blue')
        if weight2 != float("-inf"):
            plt.text(x1 + 0.5 * (x2 - x1), y1 + 0.5 * (y2 - y1) - 0.1, str(weight2), ha='center', va='center', color='red')

    # Display the graph
    plt.axis('off')
    plt.show()