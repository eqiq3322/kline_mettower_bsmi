# BSMI Wind K-Line Viewer

This repository includes a local web interface (`bsmikline`) for exploring meteorological time-series data in a K-line style workflow.

## Project Paths

- Viewer page: `bsmikline/index.html`
- Aggregated monthly data: `DATA/bsmikline/agg/`

## Quick Start

From the repository root, start a local HTTP server:

```powershell
python -m http.server 8000
```

Open this URL in your browser:

`http://localhost:8000/bsmikline/index.html`

## Current UI Behavior

- The app occupies full browser width and `2/3` of the viewport height.
- A dashed crosshair follows the cursor inside the plotting area.
- Hover information is shown in a fixed panel at the lower-left corner.
  - Left column: timestamp + variable values (with units)
  - Right column: `WS_100` statistical summary (`MA`, `min`, `q1`, `med`, `q3`, `max`)
- Left side axis:
  - Wind speed main axis
  - Wind direction ticks displayed on the right side of the same left boundary line
- Right side axes (`BP`, `RH`, `AT`, `TI`, `Gust`) appear only when the corresponding series is checked.
- If all `Time averages` checkboxes are unchecked, all plotted series are hidden (regardless of `Series` checkboxes).

## Color Mapping

- Wind speed
  - `WS_100`: `#1B4F9A` (dark blue)
  - `WS_69W`: `#2E86DE` (medium blue)
  - `WS_38W`: `#85C1E9` (light blue)
- Wind direction
  - `WD_97`: `#D68910` (dark orange)
  - `WD_35`: `#F8C471` (light orange)
- Temperature (`AT_95`): `#E74C3C`
- Pressure (`BP_93`): `#58D68D`
- Humidity (`RH_95`): `#AF7AC5`
- Turbulence intensity (`TI_10min`): `#F1C40F`
- Gust factor: `#EC7063`

## Line-Style Rules

- Main series: line width `2`
- Secondary series: line width `1`
- Background series: line width `0.8` with alpha `0.5`

