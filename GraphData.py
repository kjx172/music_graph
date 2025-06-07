import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import networkx as nx
from tqdm import tqdm

def visualize_data():
    CSV_PATH = r"modeloutput\song_embeddings.csv"

    # 1) ─── Load embeddings ────────────────────────────────────────────
    df = pd.read_csv(CSV_PATH)

    song_names = df["song_name"].tolist()
    embed_cols = [c for c in df.columns if c.startswith("d")]
    X = df[embed_cols].to_numpy(dtype=np.float32)      # shape (N, 1280)

    # 2) ─── Build k-NN graph  ────────────────────────────────
    k = 6                          # edges per node
    sim = cosine_similarity(X)     # (N,N)
    np.fill_diagonal(sim, 0)

    G = nx.Graph()
    G.add_nodes_from(song_names)

    for i, src in enumerate(song_names):
        # pick top-k neighbours
        nbr_idx = np.argsort(sim[i])[::-1][:k]
        for j in nbr_idx:
            dst = song_names[j]
            G.add_edge(src, dst, weight=float(sim[i, j]))

    # Write to GraphML (Gephi-friendly) on Windows side
    graph_path = r"modeloutput\song_knn.graphml"
    nx.write_graphml(G, graph_path)
    print("✅ k-NN graph written to", graph_path)

def recluster_graph():
    while True:
        # Since I rename my files for storage sake
        file_name = input("Enter the csv file for the graph you would like to recluster (without extension): ")
        file_path = "CSV_GRAPHS\\" + file_name + ".csv"

        if not os.path.exists(file_path):
            print("Please enter a valid file name")
            continue
        
        # Load your data (must include cluster labels and embeddings)
        df = pd.read_csv(file_path, encoding='utf-8-sig')

        # Extract vectors and meta
        song_names = df["song_name"].values
        clusters = df["Modularity"].values
        vectors = df.drop(columns=["song_name", "Modularity"]).values

        # Compute full cosine similarity matrix
        sim_matrix = cosine_similarity(vectors)

        # Build edges ONLY if nodes are in different clusters and above similarity threshold
        threshold = 0.8
        edges = []

        for i in tqdm(range(len(song_names))):
            for j in range(i + 1, len(song_names)):
                if clusters[i] != clusters[j]:  # only inter-cluster
                    sim = sim_matrix[i][j]
                    if sim > threshold:
                        edges.append((song_names[i], song_names[j], sim))

        output_path = "CSV_GRAPHS\\" + file_name +  "output.csv"
        edge_df = pd.DataFrame(edges, columns=["Source", "Target", "Weight"])
        edge_df.to_csv(output_path, index=False)

        # Load edge list
        df = pd.read_csv(output_path)

        # Create an undirected graph
        G = nx.Graph()

        # Add edges with weights
        for _, row in df.iterrows():
            G.add_edge(row['Source'], row['Target'], weight=row['Weight'])

        # Save as GraphML
        output_path = "CSV_GRAPHS\\" + file_name +  "_modularity_reclustered.graphml"
        nx.write_graphml(G, output_path)

        break
