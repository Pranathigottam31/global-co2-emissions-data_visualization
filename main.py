"""
main.py
========
Single entry point for the CO2 Emissions Data Visualization project.

Folder layout expected (all files sit in the SAME folder as main.py):

    project/
    ├── main.py                  <- you are here
    ├── requirements.txt
    ├── clean_data.py
    ├── viz1_trajectory.py
    ├── viz2_top_emitters.py
    ├── viz3_gdp_scatter.py
    ├── viz4_source_mix.py
    ├── viz5_world_map.py
    ├── viz6_correlation.py
    ├── viz7_network.py
    ├── data/                    <- input CSVs / GeoJSON live here
    │   ├── owid-co2-data.csv
    │   └── countries.geo.json
    └── output/                  <- generated PNGs land here (auto-created)

Run from VS Code (or terminal) with:

    python main.py

What it does:
  1. Makes sure data/ exists and output/ is created if missing.
  2. Runs clean_data.py to (re)generate the cleaned CSVs in data/.
  3. Runs each viz*.py script in order, each one reading from data/
     and writing its PNG into output/.
  4. Prints a clear pass/fail summary at the end.

Each script is run as its own subprocess (not imported) so that one
script's variables/state can never leak into another -- this keeps
every visualization fully independent and reproducible on its own.
"""
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"

# Order matters: clean_data.py must run first so the viz scripts have
# their input CSVs ready.
PIPELINE = [
    "clean_data.py",
    "viz1_trajectory.py",
    "viz2_top_emitters.py",
    "viz3_gdp_scatter.py",
    "viz4_source_mix.py",
    "viz5_world_map.py",
    "viz6_correlation.py",
    "viz7_network.py",
]


def check_setup():
    """Verify the data folder and required raw input exist before running."""
    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    required_raw_file = DATA_DIR / "owid-co2-data.csv"
    if not required_raw_file.exists():
        print(f"ERROR: missing required input file: {required_raw_file}")
        print("       Place 'owid-co2-data.csv' inside the data/ folder before running.")
        sys.exit(1)

    required_geojson = DATA_DIR / "countries.geo.json"
    if not required_geojson.exists():
        print(f"ERROR: missing required input file: {required_geojson}")
        print("       Place 'countries.geo.json' inside the data/ folder before running (needed for the choropleth map).")
        sys.exit(1)


def run_script(script_name: str) -> bool:
    """Run one pipeline script as a subprocess, from the project folder."""
    script_path = PROJECT_DIR / script_name
    if not script_path.exists():
        print(f"  [SKIPPED] {script_name} not found in project folder")
        return False

    print(f"\n--- Running {script_name} ---")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(PROJECT_DIR),   # so each script's relative "data/" and "output/" paths resolve correctly
        capture_output=True,
        text=True,
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print(f"  [FAILED] {script_name}")
        print(result.stderr.strip())
        return False
    return True


def main():
    # print("=" * 60)
    print("CO2 EMISSIONS DATA VISUALIZATION — PIPELINE START")
    # print("=" * 60)

    check_setup()

    results = {}
    for script in PIPELINE:
        results[script] = run_script(script)

    # print("\n" + "=" * 60)
    print("SUMMARY")
    # print("=" * 60)
    for script, ok in results.items():
        status = "OK" if ok else "FAILED"
        print(f"  [{status}] {script}")

    n_ok = sum(results.values())
    print(f"\n{n_ok}/{len(PIPELINE)} steps completed successfully.")
    if n_ok == len(PIPELINE):
        print(f"All visualizations saved to: {OUTPUT_DIR}")
    else:
        print("Some steps failed — see error output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
