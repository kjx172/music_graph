import pandas as pd
import numpy as np
import umap
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import networkx as nx

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
