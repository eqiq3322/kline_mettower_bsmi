# BSMI Wind K-Line Viewer

本專案包含 `bsmikline` 本地網頁介面，用來把風場觀測資料以類股市 K 線的互動圖方式檢視。

## 位置

- 介面檔案：`bsmikline/index.html`
- 資料目錄：`DATA/bsmikline/agg/`

## 快速啟動

在專案根目錄開本地伺服器，例如：

```powershell
python -m http.server 8000
```

瀏覽器開啟：

`http://localhost:8000/bsmikline/index.html`

## 目前介面重點

- 畫面高度為視窗 `2/3`，寬度滿版。
- 滑鼠在圖上會出現虛線十字準星。
- Hover 資訊固定在左下，分左右欄：
  - 左欄：時間與各參數值（含單位）
  - 右欄：`WS_100` 四分位數統計
- 風速主軸在左側；風向刻度顯示在同一條主軸線右側。
- 右側附加參數（BP/RH/AT/TI/GF）勾選時才顯示對應軸區間。
- 若 `Time averages` 全部未勾選，所有資料線都不顯示。

## 色彩規則（介面目前設定）

- Wind speed
  - `WS_100`: 深藍 `#1B4F9A`
  - `WS_69W`: 中藍 `#2E86DE`
  - `WS_38W`: 淺藍 `#85C1E9`
- Wind direction
  - `WD_97`: 深橘 `#D68910`
  - `WD_35`: 淺橘 `#F8C471`
- Temperature: `#E74C3C`
- Pressure: `#58D68D`
- Humidity: `#AF7AC5`
- TI: `#F1C40F`
- Gust factor: `#EC7063`

