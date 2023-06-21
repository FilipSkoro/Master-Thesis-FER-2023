import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk


############################################## MAX-PLUS FUNCTIONS ##############################################

def draw_max_plus_graph(weights, text, squares=None):
    """
    Draw a max-plus graph with weights displayed as two connection lines.

    Args:
        weights (dict): A dictionary where keys are tuples representing edges (node1, node2),
                        and values are tuples (weight1, weight2) representing the weights of the edges.
        squares (list): A list of nodes for which black squares will be drawn on the blue lines.

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
    edges2 = [(v, u) for u, v, w in graph.edges(data='weight2') if w != float("-inf")]

    # Calculate the optimal layout using the spring layout algorithm
    pos = nx.circular_layout(graph)

    # Draw the graph
    nx.draw_networkx_nodes(graph, pos)
    # Make subscript
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    nx.draw_networkx_labels(graph, pos, labels={node: f'x{node[1:]}'.translate(SUB) for node in graph.nodes()}, font_size=12)
    nx.draw_networkx_edges(graph, pos, edgelist=edges1, edge_color='blue', width=2, arrows=True, connectionstyle="arc3,rad=0.0")
    nx.draw_networkx_edges(graph, pos, edgelist=edges2, edge_color='red', width=2, arrows=True, connectionstyle="arc3,rad=0.3")

    # Add weight labels
    for edge, weight in weights.items():
        node1, node2 = edge
        weight1, weight2 = weight
        x1, y1 = pos[node1]
        x2, y2 = pos[node2]

        if weight1 != float("-inf"):
            plt.text(x1 + 0.5 * (x2 - x1), y1 + 0.5 * (y2 - y1) + 0.1, str(weight1), ha='center', va='center', color='blue')
            if squares and node1 in squares:
                # 0.2 for circular layout
                plt.plot([x1 + 0.2 * (x2 - x1)], [y1 + 0.2 * (y2 - y1)], marker='s', markersize=6, color='black')

        if weight2 != float("-inf"):
            plt.text(x1 + 0.5 * (x2 - x1), y1 + 0.5 * (y2 - y1) - 0.1, str(weight2), ha='center', va='center', color='red')

    # Print equations
    node_equations = {}

    # display equation
    text.insert(tk.INSERT, "\n===================================\n")
    text.insert(tk.INSERT, "             Equations\n")
    text.insert(tk.INSERT, "===================================\n")
    text.insert(tk.INSERT, "\n")

    for node in graph.nodes():
        equations = []
        for predecessor in graph.predecessors(node):
            weight1 = graph[predecessor][node]['weight1']
            if weight1 != float("-inf"):
                if f'x{predecessor[1:]}' in squares:
                    equations.append(f'{weight1}*x{predecessor[1:]}(k - 1)')
                else:
                    equations.append(f'{weight1}*x{predecessor[1:]}(k)')

        for successor in graph.successors(node):
            weight2 = graph[node][successor]['weight2']
            if weight2 != float("-inf"):
                equations.append(f'{weight2}*x{successor[1:]}(k)')

        equation_str = ' ⊕ '.join(equations)
        node_equations[f'x{node[1:]}'] = equation_str
    
        # display equaton
        text.insert(tk.INSERT, f'x{node[1:]}(k) = {equation_str}\n')
    
    text.insert(tk.INSERT, "\n")


    # Print matrices
    matrix_len = len(node_equations.keys())
    A0 = np.full((matrix_len, matrix_len), "ε", dtype=object)
    A1 = np.full((matrix_len, matrix_len), "ε", dtype=object)

    for key in node_equations.keys():
        # get matrix row
        matrix_row = int(key[1])-1 if len(key) == 2 else int(key[1:])-1
        # get equation factors
        factors = node_equations.get(key).split(" ⊕ ")

        for factor in factors:
            # get value
            value = int(factor.split("*")[0]) if factor.split("*")[0] != "e" else factor.split("*")[0]

            # fill matrix A0
            if "(k)" in factor:
                # get matrix column
                matrix_column = int(factor.split("*")[1].replace("x", "").replace("(k)", ""))-1
                # fill matrix
                A0[matrix_row][matrix_column] = value

            # fill matrix A1
            elif "(k - 1)" in factor:
                # get matrix column
                matrix_column = int(factor.split("*")[1].replace("x", "").replace("(k - 1)", ""))-1
                # fill matrix
                A1[matrix_row][matrix_column] = value

    # display matrices
    text.insert(tk.INSERT, "===================================\n")
    text.insert(tk.INSERT, "         Matrices A0 & A1\n")
    text.insert(tk.INSERT, "===================================\n")
    # display matrix A0
    text.insert(tk.INSERT, "\nA0 = \n")
    text.insert(tk.INSERT, "\n")
    text.insert(tk.INSERT, A0)
    # display matrix A1
    text.insert(tk.INSERT, "\n")
    text.insert(tk.INSERT, "\nA1 = \n")
    text.insert(tk.INSERT, "\n")
    text.insert(tk.INSERT, A1)
    text.insert(tk.INSERT, "\n")
    text.insert(tk.INSERT, "\n")

    # Display the graph
    plt.axis('off')
    plt.show()


def get_weights(state_dict, trains_list):
    weights = {}
    squares = []

    x_first = None
    x = None
    i = 0

    for train in trains_list:
        for state in state_dict.keys():
            if train.train_name in state_dict.get(state):
                if x == None:
                    x_first = state
                    x = state
                else:
                    if i % 2 == 0:
                        value = train.stops[i//2].text
                        weight = "e" if value == "" else int(value)

                        weights[(x, state)] = (weight, "e")

                        if i // 2 == 0:
                            squares.append(state)

                        x = state
                        i+=1

                    else:
                        value = train.rails[i//2].text
                        weight = "e" if value == "" else int(value)

                        weights[(x, state)] = (weight, float("-inf"))

                        x = state
                        i+=1

        value = train.rails[len(train.rails)-1].text
        weight = weight = "e" if value == "" else int(value)
        weights[(x_first, x)] = (float("-inf"), weight)

        x_first = None
        x = None
        i = 0


    for train in trains_list:
        for stop in train.stops:
            for train2 in trains_list:
                if train2 != train:
                    if stop in train2.stops:

                        index = train.stops.index(stop)-1 if train.stops.index(stop) != 0 else len(train.stops)-1
                        train_stop_pred = train.stops[index]
                        index = train2.stops.index(stop)-1 if train2.stops.index(stop) != 0 else len(train2.stops)-1
                        train2_stop_pred = train2.stops[index]

                        for state in state_dict.keys():
                            if train.train_name in state_dict.get(state) and stop.stop_name in state_dict.get(state) and " leaves " in state_dict.get(state):
                                value = train.rails[train.stops.index(stop)].text if len(train.rails) >=2 else train.rails[0].text
                                weight = int(value) if value != "" else "e"
                                train_leaves = (state, weight)

                            if train2.train_name in state_dict.get(state) and stop.stop_name in state_dict.get(state) and " leaves " in state_dict.get(state):
                                value = train2.rails[train2.stops.index(stop)].text if len(train2.rails) >= 2 else train2.rails[0].text
                                weight = int(value) if value != "" else "e"
                                train2_leaves = (state, weight)

                            if train.train_name in state_dict.get(state) and train_stop_pred.stop_name in state_dict.get(state) and " leaves " in state_dict.get(state):
                                train_predcessor = (state, float("-inf"))

                            if train2.train_name in state_dict.get(state) and train2_stop_pred.stop_name in state_dict.get(state) and " leaves " in state_dict.get(state):
                                train2_predcessor = (state, float("-inf"))


                        if train_leaves[0] < train2_predcessor[0]:
                            weights[(train_leaves[0], train2_predcessor[0])] = (train_leaves[1], train2_predcessor[1])
                        else:
                            weights[(train2_predcessor[0], train_leaves[0])] = (train2_predcessor[1], train_leaves[1])

                        if train2_leaves[0] < train_predcessor[0]:
                            weights[(train2_leaves[0], train_predcessor[0])] = (train2_leaves[1], train_predcessor[1])
                        else:
                            weights[(train_predcessor[0], train2_leaves[0])] = (train_predcessor[1], train2_leaves[1])

                    else:
                        continue

    return [weights, squares]

################################################################################################################
