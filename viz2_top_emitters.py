"""
VIZ 2 — Top 10 emitters by TOTAL CO2 vs TOP 10 by PER-CAPITA CO2 (2023)
This is the key tension in the climate narrative: the countries with the
biggest absolute footprint are not the same as those with the biggest
footprint per person.
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/co2_countries_clean.csv")
latest_year = 2023
d = df[df["year"] == latest_year].dropna(subset=["co2", "co2_per_capita"])
d = d[d["population"] > 1_000_000]  # exclude micro-states for fair per-capita comparison

top_total = d.nlargest(10, "co2")[["country", "co2"]].sort_values("co2")
top_pc = d.nlargest(10, "co2_per_capita")[["country", "co2_per_capita"]].sort_values("co2_per_capita")

fig, axes = plt.subplots(1, 2, figsize=(13, 6), dpi=200)

colors1 = plt.cm.Reds([0.4 + 0.5*i/len(top_total) for i in range(len(top_total))])
colors2 = plt.cm.Oranges([0.4 + 0.5*i/len(top_pc) for i in range(len(top_pc))])

axes[0].barh(top_total["country"], top_total["co2"], color=colors1)
axes[0].set_title("Top 10 by TOTAL CO\u2082\n(million tonnes, 2023)", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Million tonnes CO\u2082")
for s in ["top", "right"]:
    axes[0].spines[s].set_visible(False)

axes[1].barh(top_pc["country"], top_pc["co2_per_capita"], color=colors2)
axes[1].set_title("Top 10 by CO\u2082 PER PERSON\n(tonnes/capita, 2023)", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Tonnes CO\u2082 per capita")
for s in ["top", "right"]:
    axes[1].spines[s].set_visible(False)

# fig.suptitle("Two Different Rankings, Two Different Stories",
#               fontsize=15, fontweight="bold", y=1.03)

fig.suptitle("Top 10 Emitting Countries: Total CO\u2082 vs. CO\u2082 per Capita (2023)",
              fontsize=15, fontweight="bold", y=1.03)
# fig.text(0.5, -0.02,
#          "Source: Our World in Data \u2014 Global Carbon Project. Countries with population < 1M excluded.",
#          ha="center", fontsize=8, color="#888888", style="italic")

fig.tight_layout()
fig.savefig("output/02_top_emitters_total_vs_percapita.png", bbox_inches="tight")
print("saved 02_top_emitters_total_vs_percapita.png")
