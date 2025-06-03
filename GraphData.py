import pandas as pd
import numpy as np
import umap
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import networkx as nx

CSV_PATH = r"modeloutput\song_embeddings.csv"

# 1) ─── Load embeddings ────────────────────────────────────────────
df = pd.read_csv(CSV_PATH)

song_names = df["song_name"].tolist()
embed_cols = [c for c in df.columns if c.startswith("d")]
X = df[embed_cols].to_numpy(dtype=np.float32)      # shape (N, 1280)

# 2) ─── 2-D projection with UMAP ───────────────────────────────────
umap_model = umap.UMAP(
    n_components=2,
    metric="cosine",          # use cosine in high-dim space
    n_neighbors = min(15, X.shape[0] - 1),
    random_state=42,
)
coords = umap_model.fit_transform(X)              # (N,2)

# 3) ─── Scatter plot ───────────────────────────────────────────────
plt.figure(figsize=(10, 8))
plt.scatter(coords[:, 0], coords[:, 1], s=18, alpha=0.8)

# OPTIONAL: annotate a few points
for i, name in enumerate(song_names):
    plt.text(coords[i, 0], coords[i, 1], name, fontsize=7)

plt.title("UMAP projection of song embeddings")
plt.xlabel("UMAP-1"); plt.ylabel("UMAP-2")
plt.tight_layout()

# Save to a Windows-visible location
out_png = r"modeloutput\song_plot.png"
plt.savefig(out_png, dpi=300)
print("✅ scatter saved to", out_png)


# 4) ─── Build k-NN graph (OPTIONAL) ────────────────────────────────
#     Useful if you want an actual network plot in Gephi, Cytoscape, etc.
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
graph_path = "modeloutput\song_knn.graphml"
nx.write_graphml(G, graph_path)
print("✅ k-NN graph written to", graph_path)
