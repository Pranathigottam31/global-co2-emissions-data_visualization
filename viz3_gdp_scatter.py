"""
VIZ 3 — Wealth, Energy Use, and Emissions (2022)
A true 4-variable bubble chart (stateless/OO matplotlib interface):
  x      = GDP per capita (log scale)
  y      = CO2 emissions per capita
  size   = population
  color  = energy use per capita  <-- a genuinely different variable from
                                       the axes, so the colorbar adds new
                                       information instead of repeating
                                       what's already on the y-axis.
Points are semi-transparent with NO outlines, since this dataset has many
overlapping bubbles -- outlines would create visual clutter and make
overlap regions look artificially darker/heavier than they are.

Label collisions: with ~150 overlapping bubbles, simply placing a text
label next to each highlighted country causes labels to overlap each
other and get hidden behind nearby bubbles. We fix this with adjustText,
which automatically repels labels away from each other and from the
data points, then draws a thin leader line back to the true bubble
location so the label is never ambiguous about which country it names.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text

df = pd.read_csv("data/co2_countries_clean.csv")
d = df[df["year"] == 2022].copy()
d["gdp_per_capita"] = d["gdp"] / d["population"]
d = d.dropna(subset=["gdp_per_capita", "co2_per_capita", "population", "energy_per_capita"])
d = d[(d["population"] > 1_000_000) & (d["gdp_per_capita"] > 0)]

fig, ax = plt.subplots(figsize=(12, 7.5), dpi=200)
ax.set_facecolor("white")
fig.patch.set_facecolor("white")

sizes = (d["population"] / d["population"].max()) * 3000 + 20
sc = ax.scatter(
    d["gdp_per_capita"], d["co2_per_capita"],
    s=sizes, alpha=0.55,
    c=d["energy_per_capita"], cmap="viridis",
    edgecolors="none",            # <- no outlines on points
)

ax.set_xscale("log")
ax.set_xlabel("GDP per capita (current US$, log scale)")
ax.set_ylabel("CO\u2082 emissions per capita (tonnes)")
ax.set_title("GDP per Capita vs. CO\u2082 Emissions per Capita (2022)",
             fontsize=15, fontweight="bold", loc="left", pad=15)

# Label a handful of countries that anchor the story.
# Each gets a small black dot marking its TRUE location, since the text
# label itself will be pushed away from that point by adjust_text below.
highlight = ["United States", "China", "India", "Qatar", "Germany",
             "Norway", "Nigeria", "Brazil", "France", "Sweden"]
hl = d[d["country"].isin(highlight)]

ax.scatter(hl["gdp_per_capita"], hl["co2_per_capita"],
           s=18, color="#222222", zorder=5)

texts = [
    ax.text(row["gdp_per_capita"], row["co2_per_capita"], row["country"],
             fontsize=9.5, color="#222222", fontweight="bold", zorder=6)
    for _, row in hl.iterrows()
]

# Push labels apart from each other and away from bubbles/markers;
# draw a thin gray leader line from each label back to its true point.
adjust_text(
    texts, ax=ax,
    x=d["gdp_per_capita"].values, y=d["co2_per_capita"].values,  # repel from ALL bubbles, not just highlighted ones
    expand=(1.4, 1.6),
    force_text=(0.6, 0.8),
    arrowprops=dict(arrowstyle="-", color="#888888", lw=0.8, shrinkA=2, shrinkB=2),
)

# Clean look: no top/right spines, no gridlines, white background
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

# Colorbar acts as the "legend" here -- a real 4th variable, clearly labeled
cbar = fig.colorbar(sc, ax=ax, pad=0.015)
cbar.set_label("Energy use per capita (kWh)", fontsize=10)
cbar.outline.set_visible(False)

# A small separate legend explaining bubble size, since size isn't on a colorbar
for pop_m, label in [(50, "50M"), (300, "300M"), (1000, "1B")]:
    ax.scatter([], [], s=(pop_m * 1e6 / d["population"].max()) * 3000 + 20,
               color="#999999", alpha=0.5, edgecolors="none", label=label)
leg = ax.legend(title="Population", loc="upper left", frameon=False,
                 labelspacing=1.4, borderpad=1, fontsize=9, title_fontsize=10)

# ax.text(0.0, -0.13,
#         "Source: Our World in Data — Global Carbon Project. Countries with population < 1M excluded.",
#         transform=ax.transAxes, fontsize=8, color="#888888", style="italic")

fig.tight_layout()
fig.savefig("output/03_gdp_vs_co2_bubble.png", bbox_inches="tight")
print("saved 03_gdp_vs_co2_bubble.png")