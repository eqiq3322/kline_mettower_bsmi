import pandas as pd
import numpy as np
from pathlib import Path
from math import atan2
import json

# Paths
BASE = Path(r"C:/Users/Laura/NCKU/FSSL/cupanemometer")
DATA_DIR = BASE / "DATA"
OUT_DIR = DATA_DIR / "bsmikline" / "agg"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Config
RESAMPLE = "1min"
ROLL_WINDOWS = {
    "MA_10min": "10min",
    "MA_1h": "1h",
    "MA_6h": "6h",
    "MA_1mo": "30d",  # approximate month
}
TI_WINDOW = "10min"
GUST_MEAN_WINDOW = "10min"  # denominator window

COLS = [
    "TIMESTAMP",
    "WS_100E",
    "WS_100W",
    "WS_69W",
    "WS_38W",
    "WD_97",
    "WD_35",
    "AT_95",
    "RH_95",
    "BP_93",
]


def vector_mean_deg(series):
    rad = np.deg2rad(series)
    sin_mean = np.nanmean(np.sin(rad))
    cos_mean = np.nanmean(np.cos(rad))
    if np.isnan(sin_mean) or np.isnan(cos_mean):
        return np.nan
    ang = atan2(sin_mean, cos_mean)
    deg = np.rad2deg(ang)
    if deg < 0:
        deg += 360
    return deg


def discover_months():
    months = []
    for p in DATA_DIR.glob("BSMI*.txt"):
        stem = p.stem  # e.g. BSMI201603
        ym = stem.replace("BSMI", "")
        if len(ym) == 6 and ym.isdigit() and "201603" <= ym <= "202503":
            months.append(ym)
    return sorted(set(months))


def process_month(ym: str):
    src = DATA_DIR / f"BSMI{ym}.txt"
    out_path = OUT_DIR / f"BSMI{ym}.csv"
    if out_path.exists():
        print(f"Skip {ym}: output exists")
        return
    if not src.exists():
        print(f"Skip {ym}: source not found")
        return

    try:
        df = pd.read_csv(src, usecols=COLS, parse_dates=["TIMESTAMP"], low_memory=False)
    except Exception as e:
        print(f"Skip {ym}: read_csv failed ({e})")
        return
    df["WS_100"] = (df["WS_100E"] + df["WS_100W"]) / 2
    df = df.set_index("TIMESTAMP").sort_index()
    df = df[~df.index.isna()]
    df = df[~df.index.duplicated(keep="first")]
    if df.empty:
        print(f"Skip {ym}: no data after cleaning")
        return

    # Gust factor: 3s max / 10min mean at native 1 Hz, then resample
    roll_max_3s = df["WS_100"].rolling("3s", min_periods=1).max()
    roll_mean_10m = df["WS_100"].rolling(GUST_MEAN_WINDOW, min_periods=1).mean()
    df["GustFactor"] = roll_max_3s / roll_mean_10m

    # Resample
    speed = df[["WS_100", "WS_69W", "WS_38W"]].resample(RESAMPLE).mean()
    wd97 = df["WD_97"].resample(RESAMPLE).apply(vector_mean_deg)
    wd35 = df["WD_35"].resample(RESAMPLE).apply(vector_mean_deg)
    scalars = df[["AT_95", "RH_95", "BP_93"]].resample(RESAMPLE).mean()
    gust = df["GustFactor"].resample(RESAMPLE).mean()

    res = pd.concat(
        [
            speed,
            wd97.rename("WD_97"),
            wd35.rename("WD_35"),
            scalars,
            gust.rename("GustFactor"),
        ],
        axis=1,
    )

    # TI
    res["TI_10min"] = res["WS_100"].rolling(TI_WINDOW, min_periods=1).apply(
        lambda x: np.nanstd(x) / np.nanmean(x) if np.nanmean(x) not in [0, np.nan] else np.nan
    )

    # Moving averages (WS_100)
    for col_name, window in ROLL_WINDOWS.items():
        res[col_name] = res["WS_100"].rolling(window, min_periods=1).mean()

    res = res.reset_index()
    res.to_csv(out_path, index=False, float_format="%.3f")
    print(f"Saved {out_path}")


def main():
    months = discover_months()
    print(f"Discovered {len(months)} months")
    for ym in months:
        try:
            process_month(ym)
        except Exception as e:
            print(f"Failed {ym}: {e}")

    existing = sorted([p.stem.replace("BSMI", "") for p in OUT_DIR.glob("BSMI*.csv") if p.stem.replace("BSMI", "").isdigit()])
    months_json = OUT_DIR / "months.json"
    months_json.write_text(json.dumps(existing), encoding="utf-8")
    print(f"Wrote {months_json}")


if __name__ == "__main__":
    main()
