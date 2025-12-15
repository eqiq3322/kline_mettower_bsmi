# BSMI Met Tower K-line Viewer

Interactive Plotly viewer for the BSMI met tower aggregated data.

## Files
- `bsmikline/index.html`: front-end viewer (works in browser via `python -m http.server`).
- `bsmikline/build_kline.py`: builds aggregated CSVs from raw `DATA/BSMIyyyymm.txt` files (1 Hz) into 10-min/hour/day/month means, plus gust factor, TI, and moving averages. Outputs to `DATA/bsmikline/agg/`.
- `DATA/bsmikline/agg/BSMIyyyymm.csv`: aggregated per-month data (10-min resolution). Columns: TIMESTAMP, WS_100, WS_69W, WS_38W, WD_97, WD_35, AT_95, RH_95, BP_93, GustFactor, TI_10min, MA_10min, MA_1h, MA_6h, MA_1mo.
- `DATA/bsmikline/agg/months.json`: list of available months.

## How to run the viewer locally
1. Install Python 3.
2. From repo root:
   ```
   python -m http.server 8000
   ```
3. Open in browser:
   `http://localhost:8000/bsmikline/index.html`
4. Use the controls to pick month, time averages, and series. Hover shows wind-speed box stats based on the selected time-average window.

## How to regenerate aggregated CSVs
1. Make sure raw files `DATA/BSMIyyyymm.txt` are present.
2. Run:
   ```
   python bsmikline/build_kline.py
   ```
3. Outputs land in `DATA/bsmikline/agg/` and update `months.json`.

## Notes
- Gust factor = 3-second maximum / 10-minute mean wind speed.
- Wind direction traces break across 0/360 to avoid wrapping lines.
- Default view loads 10-minute MA for WS_100 and WD_97; other series can be toggled on.
