"""
VIZ 4 — Global CO2 emissions by source (coal, oil, gas, cement), 1900-2023
Shows HOW the composition of emissions has shifted -- coal's dominance,
oil's mid-century rise, and gas's modern growth.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

world = pd.read_csv("data/co2_world_clean.csv")
w = world[(world["year"] >= 1900) & (world["year"] <= 2023)].copy()
w = w.fillna(0)

fig, ax = plt.subplots(figsize=(11, 6), dpi=200)

sources = ["coal_co2", "oil_co2", "gas_co2", "cement_co2"]
labels = ["Coal", "Oil", "Gas", "Cement"]
colors = ["#2c2c2c", "#8b4513", "#4a90d9", "#a0a0a0"]

ax.stackplot(w["year"], *[w[s] for s in sources], labels=labels, colors=colors, alpha=0.88)

ax.set_title("What's Driving Global Emissions? The Fuel Mix, 1900\u20132023",
              fontsize=15, fontweight="bold", loc="left", pad=15)
ax.set_xlabel("Year")
ax.set_ylabel("CO\u2082 emissions (million tonnes)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
ax.legend(loc="upper left", frameon=False, fontsize=10)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.set_facecolor("white")
# fig.text(0.12, 0.02, "Source: Our World in Data — Global Carbon Project",
#          fontsize=8, color="#888888", style="italic")

fig.tight_layout()
fig.savefig("output/04_emissions_by_source_stacked.png", bbox_inches="tight")
print("saved 04_emissions_by_source_stacked.png")
