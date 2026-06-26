"""
VIZ 7 — Network Graph: Countries Linked by Similar Emissions Profiles
Nodes = top 30 emitting countries (2022). Each country gets a 4-D "fuel
fingerprint" = share of CO2 from coal / oil / gas / cement.
An edge is drawn between two countries if their fingerprints are highly
similar (cosine similarity >= threshold) -- i.e. they rely on fossil
fuels in a similar way. Node size = total CO2 emitted. Node color =
CO2 per capita (darker = higher).
"""
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from itertools import combinations

df = pd.read_csv("data/co2_countries_clean.csv")
d = df[df["year"] == 2022].copy()
d = d.dropna(subset=["co2", "coal_co2", "oil_co2", "gas_co2", "cement_co2", "co2_per_capita"])
d = d[d["population"] > 1_000_000]

top = d.nlargest(30, "co2").copy()

# Build fuel-mix "fingerprint" (shares sum to 1 across the 4 sources we track)
fuel_cols = ["coal_co2", "oil_co2", "gas_co2", "cement_co2"]
fingerprint = top[fuel_cols].div(top[fuel_cols].sum(axis=1), axis=0).fillna(0)
fingerprint.index = top["country"].values

def cosine_sim(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0
    return np.dot(a, b) / (na * nb)

G = nx.Graph()
for _, row in top.iterrows():
    G.add_node(row["country"], size=row["co2"], pc=row["co2_per_capita"])

THRESHOLD = 0.985
for c1, c2 in combinations(fingerprint.index, 2):
    sim = cosine_sim(fingerprint.loc[c1].values, fingerprint.loc[c2].values)
    if sim >= THRESHOLD:
        G.add_edge(c1, c2, weight=sim)

# Drop isolated nodes with no strong similarity link for a cleaner graph
G.remove_nodes_from(list(nx.isolates(G)))

pos = nx.spring_layout(G, k=0.9, seed=42, weight="weight")

sizes = np.array([G.nodes[n]["size"] for n in G.nodes()])
node_sizes = 300 + 2200 * (sizes / sizes.max())
pcs = np.array([G.nodes[n]["pc"] for n in G.nodes()])
norm = Normalize(vmin=pcs.min(), vmax=pcs.max())
node_colors = cm.YlOrRd(norm(pcs))

fig, ax = plt.subplots(figsize=(12, 9), dpi=200)

nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#bbbbbb", width=1.2, alpha=0.7)
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=node_sizes,
                        node_color=node_colors, linewidths=0)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_weight="bold",
                         font_color="#222222")

ax.set_title("Countries Linked by Similar Fossil-Fuel Emissions Profiles (2022)",
              fontsize=15, fontweight="bold", pad=12)
ax.text(0.5, -0.04,
        "Node size = total CO\u2082 emitted   |   Node color = CO\u2082 per capita (darker = higher)\n"
        "An edge connects two countries whose coal/oil/gas/cement emissions mix is highly similar (cosine similarity \u2265 0.985)",
        transform=ax.transAxes, ha="center", fontsize=9.5, color="#555555")
# ax.text(0.0, -0.10, "Source: Our World in Data — Global Carbon Project. Top 30 emitters, population > 1M.",
#         transform=ax.transAxes, fontsize=8, color="#888888", style="italic")
ax.set_axis_off()

sm = cm.ScalarMappable(cmap="YlOrRd", norm=norm)
cbar = fig.colorbar(sm, ax=ax, fraction=0.035, pad=0.02)
cbar.set_label("Tonnes CO\u2082 per capita", fontsize=9)

fig.tight_layout()
fig.savefig("output/07_network_emissions_profile.png", bbox_inches="tight")
print("saved 07_network_emissions_profile.png | nodes:", G.number_of_nodes(), "edges:", G.number_of_edges())
