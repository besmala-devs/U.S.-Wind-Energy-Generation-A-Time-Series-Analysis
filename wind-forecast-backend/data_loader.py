"""
Loads and cleans the EIA wind generation CSV, replicating the R preprocessing
steps from wind_energy_analysis.ipynb:
  - skip the 4 metadata header lines
  - drop blank/duplicate rows (EIA quirk: some months repeat with empty values)
  - reverse to chronological order (EIA stores newest first)
  - build a monthly series starting Dec 2000
  - split into train (Jan 2001 - Dec 2024) and test (Jan 2025 - Dec 2025)
"""
import pandas as pd

DATA_PATH = "..\Net_generation_wind_all_sectors_monthly.csv"


def load_wind_series(path: str = DATA_PATH) -> pd.Series:
    raw = pd.read_csv(path, skiprows=4)
    clean = raw[raw["United States thousand megawatthours"].notna()].copy()
    clean = clean.iloc[::-1].reset_index(drop=True)  # oldest -> newest

    y_values = clean["United States thousand megawatthours"].astype(float).values
    dates = pd.date_range(start="2000-12-01", periods=len(y_values), freq="MS")
    full_series = pd.Series(y_values, index=dates, name="wind_generation")

    # Jan 2001 onward, matching the R analysis window
    return full_series["2001-01-01":] 


def train_test_split(series: pd.Series):
    train = series[:"2024-12-01"]
    test = series["2025-01-01":]
    return train, test


if __name__ == "__main__":
    series = load_wind_series()
    train, test = train_test_split(series)
    print(f"Series length: {len(series)} (expected 300)")
    print(f"Train: {len(train)} obs | Test: {len(test)} obs")