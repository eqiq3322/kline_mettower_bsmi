# BSMI Wind K-Line Viewer

This repository includes a local web viewer for exploring BSMI meteorological time-series data in a K-line style interface.

## Current Project Paths

- Viewer page: `topics/bsmikline/index.html`
- Aggregated monthly data: `topics/bsmikline/agg/`

## Quick Start

Run a local HTTP server from the repository root:

```powershell
cd C:\Users\Laura\NCKU\FSSL\data
python -m http.server 8000
```

Open this URL in your browser:

`http://localhost:8000/topics/bsmikline/index.html`

## Notes

- The viewer now reads data from the sibling `agg` folder under `topics/bsmikline`.
- If you use VS Code Live Server, open `topics/bsmikline/index.html` and use the generated local URL.
- Opening the HTML file directly with `file:///` may fail because the page loads `months.json` and monthly CSV files via `fetch()`.
