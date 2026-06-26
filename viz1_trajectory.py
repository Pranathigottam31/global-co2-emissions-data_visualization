"""
VIZ 1 — Global CO2 trajectory, 1850-2024
Shows the overall arc of the story: emissions were near-zero, then exploded
with industrialization, accelerated after WWII, and have only recently
begun to plateau.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#444444",
    "axes.labelcolor": "#222222",
    "text.color": "#222222",
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

world = pd.read_csv("data/co2_world_clean.csv")
world = world[(world["year"] >= 1850) & (world["year"] <= 2024)]

fig, ax = plt.subplots(figsize=(11, 6), dpi=200)

ax.plot(world["year"], world["co2"], color="#c0392b", linewidth=2.5)
ax.fill_between(world["year"], world["co2"], color="#c0392b", alpha=0.12)

# Era annotations
events = [
    (1950, "Post-WWII\nindustrial boom"),
    (1990, "Globalization &\nChina's rise"),
    (2020, "COVID-19\ndip"),
]
for yr, label in events:
    val = world.loc[world["year"] == yr, "co2"]
    if not val.empty:
        y = val.values[0]
        ax.annotate(label, xy=(yr, y), xytext=(yr, y + 7000),
                    ha="center", fontsize=9, color="#444444",
                    arrowprops=dict(arrowstyle="-", color="#888888", lw=0.8))

ax.set_title("The Great Acceleration: Global CO\u2082 Emissions, 1850\u20132024",
             fontsize=15, fontweight="bold", pad=15, loc="left")

ax.set_xlabel("Year")
ax.set_ylabel("CO\u2082 emissions (million tonnes)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
ax.set_facecolor("white")
# ax.text(1855, world["co2"].max()*0.95,
#         "Source: Our World in Data \u2014 Global Carbon Project",
#         fontsize=8, color="#888888", style="italic")

fig.tight_layout()
fig.savefig("output/01_global_co2_trajectory.png", bbox_inches="tight")
print("saved 01_global_co2_trajectory.png")
