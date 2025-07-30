import itertools
import math

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import networkx as nx
import matplotlib.cm as cm


def draw_heatmap(correlation_matrix, sigma_value=None):
    """Draw a heatmap for the correlation matrix."""
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='flare', square=True, vmin=-1, vmax=1)
    plt.title('Correlation Heatmap')
    if sigma_value:
        plt.text(1.1, 1.1, f'Sigma: {sigma_value:.2f}', fontsize=12, ha='right', va='top',
                 transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))

    plt.show()


def draw_plot(correlation_matrix):
    """Create a line plot from the correlation matrix."""
    plt.figure(figsize=(14, 8))

    for i in range(len(correlation_matrix)):
        plt.plot(correlation_matrix.index, correlation_matrix.iloc[:, i], marker='o',
                 label=correlation_matrix.columns[i])

    plt.title('Correlation Plot', fontsize=20)
    plt.xlabel('Attributes', fontsize=14)
    plt.ylabel('Correlation Coefficient', fontsize=14)
    plt.axhline(0, color='grey', linewidth=0.8, linestyle='--')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Attributes', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid()
    plt.tight_layout()
    plt.show()


def draw_rectangular_nodes(ax, pos):
    """Draw rectangular nodes with custom colors from a colormap."""
    num_nodes = len(pos)
    cmap = cm.get_cmap('Pastel1', num_nodes)
    for i, (node, (x, y)) in enumerate(pos.items()):
        color = cmap(i)
        node_text = str(node)
        if " " in node_text or "_" in node_text:
            node_text = node_text.replace(" ", "\n").replace("_", "\n")
        ax.text(
            x, y, str(node_text),
            fontsize=10,
            color='black',
            fontfamily='sans-serif',
            ha='center',
            va='center',
            bbox=dict(facecolor=color, edgecolor='black', boxstyle='round,pad=0.3')
        )


def draw_edges(ax, pos, G):
    """Draw edges for the graph without calculating intersection points."""
    for edge in G.edges():
        x1, y1 = pos[edge[0]]
        x2, y2 = pos[edge[1]]

        weight = G[edge[0]][edge[1]]['weight']
        linestyle = 'dashed' if weight == 0 else 'solid'
        ax.plot([x1, x2], [y1, y2], color='black', alpha=0.7, zorder=1, linestyle=linestyle)


def draw_edge_labels(ax, pos, G):
    """Draw edge labels for the graph."""
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f"{v:.2f}" for k, v in edge_labels.items()}
    # Explicitly use the 'pos' for edge label placement
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color='black', label_pos=0.65, font_size=11,
        bbox=dict(facecolor="white", ec="white"), ax=ax
    )


def create_graph(correlation_matrix, sigma_value=None):
    """Create a graph based on correlation matrix, optionally filtering by sigma."""
    G = nx.Graph()
    for i in range(len(correlation_matrix)):
        for j in range(i + 1, len(correlation_matrix)):
            corr_value = correlation_matrix.iloc[i, j]
            if sigma_value is None or abs(corr_value) > sigma_value:
                G.add_edge(correlation_matrix.index[i], correlation_matrix.columns[j], weight=corr_value)
    return G


def find_all_subgraphs(G):
    """Find all possible complete subgraphs (cliques) of size >= 3."""
    nodes = list(G.nodes())
    subgraphs = []

    for size in range(3, 7):
        for subset in itertools.combinations(nodes, size):
            subgraph = G.subgraph(subset)
            if subgraph.number_of_edges() == size * (size - 1) / 2:
                subgraphs.append(subgraph)
    return subgraphs


def is_encoded_node(node):
    return "_vec_" in str(node) or str(node).endswith("_LE") or str(node).endswith("_HS")

def is_encoded_subgraph(subgraph):
    return any(is_encoded_node(node) for node in subgraph.nodes())

def group_subgraphs_by_size(subgraphs):
    grouped = {}
    for sub in subgraphs:
        grouped.setdefault(len(sub.nodes()), []).append(sub)
    return grouped

def draw_encoded_attribute_subgraphs(subgraphs, dataset_name, correlation_method, encoding_method):
    """Draw all encoded subgraphs, separated by subgraph size."""
    encoded_subgraphs = [
        sg for sg in subgraphs
        if any(is_encoded_node(node) for node in sg.nodes())
    ]

    if not encoded_subgraphs:
        print("No subgraphs with encoded attributes found.")
        return

    print(f"Drawing {len(encoded_subgraphs)} subgraphs with encoded attributes")

    subgraph_groups = {}
    for sg in encoded_subgraphs:
        size = len(sg.nodes())
        if size not in subgraph_groups:
            subgraph_groups[size] = []
        subgraph_groups[size].append(sg)

    max_cols = 3
    max_graphs_per_fig = max_cols * max_cols

    for size, group in subgraph_groups.items():
        print(f"Drawing {len(group)} encoded subgraphs of size {size}")
        for batch_idx in range(0, len(group), max_graphs_per_fig):
            batch = group[batch_idx:batch_idx + max_graphs_per_fig]
            batch_size = len(batch)
            cols = min(max_cols, batch_size)
            rows = math.ceil(batch_size / cols)

            fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3), facecolor='white')
            axes = axes.flatten() if batch_size > 1 else [axes]

            for i, subgraph in enumerate(batch):
                pos = nx.circular_layout(subgraph)
                draw_rectangular_nodes(axes[i], pos)
                draw_edges(axes[i], pos, subgraph)
                draw_edge_labels(axes[i], pos, subgraph)
                axes[i].axis('off')

            for j in range(batch_size, len(axes)):
                fig.delaxes(axes[j])

            filename = f"EncodedSubgraphs_Size{size}_{dataset_name}_{correlation_method}_{encoding_method}_part{batch_idx // max_graphs_per_fig + 1}.png"
            plt.tight_layout()
            plt.savefig(filename, dpi=1200)
            print(f"Saved: {filename}")
            plt.show()



def plot_subgraph_batch(batch, dataset_name, correlation_method, encoding_method, size, batch_idx, avg_correlation_values):
    max_cols, max_graphs_per_fig = 3, 9
    batch_size = len(batch)
    cols = min(max_cols, batch_size)
    rows = math.ceil(batch_size / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3), facecolor='white')
    axes = axes.flatten() if batch_size > 1 else [axes]

    for i, subgraph in enumerate(batch):
        if is_encoded_subgraph(subgraph):
            edge_weights = [abs(subgraph[u][v]['weight']) for u, v in subgraph.edges() if 'weight' in subgraph[u][v]]
            if edge_weights:
                avg_correlation_values.append(np.mean(edge_weights))
        pos = nx.circular_layout(subgraph)
        draw_rectangular_nodes(axes[i], pos)
        draw_edges(axes[i], pos, subgraph)
        draw_edge_labels(axes[i], pos, subgraph)
        axes[i].axis('off')

    for j in range(batch_size, len(axes)):
        fig.delaxes(axes[j])

    filename = f"{size}ptychs_{dataset_name}_{correlation_method}_{encoding_method}_part{batch_idx + 1}.png"
    plt.tight_layout()
    plt.savefig(filename, dpi=1200)
    print(f"Saved: {filename}")
    plt.show()

def draw_graph(correlation_matrix, sigma_value=None, correlation_method=None, encoding_method=None, dataset_name=None):
    G = create_graph(correlation_matrix)
    print("Drawing main graph")
    print(f"Nodes in G: {G.nodes()}")
    print(f"Edges in G: {G.edges()}")

    fig, axes = plt.subplots(2, 1, figsize=(12, 14), facecolor='white', )
    draw_rectangular_nodes(axes[0], (pos := nx.circular_layout(G)))
    draw_edges(axes[0], pos, G)
    draw_edge_labels(axes[0], pos, G)
    axes[0].set_title('Main graph')
    axes[0].axis('off')

    if not sigma_value:
        return

    G_filtered = create_graph(correlation_matrix, sigma_value)
    print("Drawing filtered graph")
    print(f"Nodes in G_filtered: {G_filtered.nodes()}")
    print(f"Edges in G_filtered: {G_filtered.edges()}")

    draw_rectangular_nodes(axes[1], (pos_f := nx.circular_layout(G_filtered)))
    draw_edges(axes[1], pos_f, G_filtered)
    draw_edge_labels(axes[1], pos_f, G_filtered)
    axes[1].set_title('Main graph filtered by sigma value')
    axes[1].axis('off')

    filename = f"Base_graph_{dataset_name}_{correlation_method}_{encoding_method}.png"
    plt.savefig(filename, dpi=1200, bbox_inches='tight')
    print(f"Saved: {filename}")
    plt.tight_layout()
    plt.show()

    subgraphs = find_all_subgraphs(G_filtered)
    print(f"Found {len(subgraphs)} complete subgraphs")
    draw_encoded_attribute_subgraphs(subgraphs, dataset_name, correlation_method, encoding_method)


    encoded_count = sum(1 for sg in subgraphs if is_encoded_subgraph(sg))
    print(f"Number of complete subgraphs containing linguistic attribute: {encoded_count}")

    grouped_subgraphs = group_subgraphs_by_size(subgraphs)
    avg_correlation_values = []

    for size, group in grouped_subgraphs.items():
        print(f"Total number of {size}-ptychs: {len(group)}")
        for batch_idx in range(0, len(group), 9):
            batch = group[batch_idx:batch_idx + 9]
            plot_subgraph_batch(batch, dataset_name, correlation_method, encoding_method, size, batch_idx // 9, avg_correlation_values)

    if avg_correlation_values:
        print(f"Overall average correlation: {np.mean(avg_correlation_values):.4f}")
    else:
        print("No subgraphs with weighted edges found.")










