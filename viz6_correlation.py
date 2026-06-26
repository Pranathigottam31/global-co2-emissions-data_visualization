"""
VIZ 6 — Correlation heatmap: what factors move together with emissions?
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/co2_countries_clean.csv")
d = df[df["year"] == 2022].copy()
d["gdp_per_capita"] = d["gdp"] / d["population"]

cols = {
    "co2_per_capita": "CO\u2082 / capita",
    "gdp_per_capita": "GDP / capita",
    "energy_per_capita": "Energy use / capita",
    "population": "Population",
    "methane": "Methane",
    "nitrous_oxide": "Nitrous oxide",
    "temperature_change_from_ghg": "Temp. change (GHG)",
}
sub = d[list(cols.keys())].rename(columns=cols).dropna()
corr = sub.corr(method="spearman")

fig, ax = plt.subplots(figsize=(8, 6.5), dpi=200)
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
            vmin=-1, vmax=1, square=True, linewidths=0.5,
            cbar_kws={"label": "Spearman correlation"}, ax=ax)
ax.set_title("What Moves Together With Emissions? (2022, country-level)",
              fontsize=13, fontweight="bold", pad=15)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

# fig.text(0.02, -0.02, "Source: Our World in Data — Global Carbon Project. Spearman rank correlation across countries.",
#          fontsize=8, color="#888888", style="italic")

fig.tight_layout()
fig.savefig("output/06_correlation_heatmap.png", bbox_inches="tight")
print("saved 06_correlation_heatmap.png")
