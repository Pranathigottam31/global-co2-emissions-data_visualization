"""
VIZ 5 — World map of CO2 emissions per capita (2023)
Built with geopandas + matplotlib (no headless-browser dependency).
Boundaries: johan/world.geo.json (GitHub), ISO3 feature ids.
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm

world = gpd.read_file("data/countries.geo.json")  # has 'id' = ISO3, properties.name
world = world[world["id"] != "ATA"]  # drop Antarctica (distorted polygon, no emissions data)

df = pd.read_csv("data/co2_countries_clean.csv")
d = df[df["year"] == 2023].dropna(subset=["iso_code", "co2_per_capita"])
d = d[d["iso_code"].str.len() == 3][["iso_code", "country", "co2_per_capita"]]

merged = world.merge(d, left_on="id", right_on="iso_code", how="left")

fig, ax = plt.subplots(figsize=(14, 7.5), dpi=200)
merged.boundary.plot(ax=ax, linewidth=0.3, color="#999999")
merged.plot(
    column="co2_per_capita", ax=ax, cmap="YlOrRd",
    linewidth=0.3, edgecolor="#999999",
    missing_kwds={"color": "#eeeeee", "label": "No data"},
    vmin=0, vmax=20, legend=False
)

ax.set_axis_off()
ax.set_title("CO2 Emissions per Capita Around the World (2023)",
             fontsize=18, fontweight="bold", pad=10)

sm = cm.ScalarMappable(cmap="YlOrRd", norm=Normalize(vmin=0, vmax=20))
cbar = fig.colorbar(sm, ax=ax, orientation="horizontal", fraction=0.04, pad=0.06, shrink=0.4)
cbar.set_label("Tonnes CO2 per capita (capped at 20)", fontsize=9)

# fig.text(0.5, -0.02, "Source: Our World in Data - Global Carbon Project. Gray = no data.",
#          ha="center", fontsize=9, color="#888888", style="italic")

fig.tight_layout()
fig.savefig("output/05_world_map_co2_percapita.png", bbox_inches="tight")
print("saved 05_world_map_co2_percapita.png")
