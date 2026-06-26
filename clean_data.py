"""
Data cleaning / preparation
Project: Who's Driving Climate Change? A Global CO2 Emissions Story
Source: Our World in Data CO2 & Greenhouse Gas Emissions Dataset
        https://github.com/owid/co2-data  (CC-BY 4.0)
"""
import pandas as pd
import numpy as np

RAW = "data/owid-co2-data.csv"
df = pd.read_csv(RAW)

# Keep only real countries (drop aggregates like "World", "Asia", income groups, etc.)
AGGREGATES = [
    "World", "Asia", "Africa", "Europe", "North America", "South America",
    "Oceania", "European Union (27)", "European Union (28)",
    "High-income countries", "Low-income countries", "Lower-middle-income countries",
    "Upper-middle-income countries", "International transport", "Antarctica",
    "Asia (excl. China and India)", "North America (excl. USA)",
    "Europe (excl. EU-27)", "Europe (excl. EU-28)"
]

countries_df = df[~df["country"].isin(AGGREGATES)].copy()
world_df = df[df["country"] == "World"].copy()

# Core columns used across the project
KEEP_COLS = [
    "country", "year", "iso_code", "population", "gdp",
    "co2", "co2_per_capita", "co2_growth_prct", "cumulative_co2",
    "coal_co2", "oil_co2", "gas_co2", "cement_co2",
    "share_global_co2", "share_global_cumulative_co2",
    "primary_energy_consumption", "energy_per_capita",
    "methane", "nitrous_oxide", "total_ghg",
    "temperature_change_from_ghg"
]
core = countries_df[KEEP_COLS].copy()

# Drop rows with no CO2 figure at all (can't analyze what isn't measured)
core = core.dropna(subset=["co2"])

core.to_csv("data/co2_countries_clean.csv", index=False)
world_df.to_csv("data/co2_world_clean.csv", index=False)

print("Countries (cleaned):", core.shape)
print("Year range:", core["year"].min(), "-", core["year"].max())
print("Countries:", core["country"].nunique())
print("World rows:", world_df.shape)
