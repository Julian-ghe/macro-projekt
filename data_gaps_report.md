# Country_Data.xlsx – Data Gaps Report

Generated: 2026-05-01 15:22

## Remaining gaps after gap-filling from PWT 11.0 and WDI

Display: `non-null / total` per country × variable. Empty cells shown as `–`.

| Variable | IRN | QAT | USA | SAU | ARE | KWT | IRQ | DZA | VEN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Depreciation rate (Solow)** | 69/74 | 54/74 | OK (74) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **Real interest rate / Rental rate** | 69/74 | 54/74 | OK (74) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **Labor share (for α calibration)** | 69/74 | 54/74 | OK (74) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **Hours/worker (for N = emp×hours)** | 19/74 | 19/74 | OK (74) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **TFP (Constant)** | 65/74 | 50/74 | 70/74 | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **Capital Stock (K)** | 69/74 | 54/74 | OK (74) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **Capital Services** | 65/74 | 50/74 | 70/74 | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **Welfare** | 65/74 | 50/74 | 70/74 | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **Consumption share** | 69/74 | 54/74 | OK (74) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **Investment share** | 69/74 | 54/74 | OK (74) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **Population** | 69/74 | 54/74 | OK (74) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **Workforce (emp)** | 69/74 | 54/74 | OK (74) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |
| **Real GDP** | 69/74 | 54/74 | OK (74) | – (0) | – (0) | – (0) | – (0) | – (0) | – (0) |

## Data sources

- **Black values**: from PWT 11.0 (the original source of Country_Data)
- **<span style="color:red">Red values</span>**: added from World Development Indicators (Iran & Qatar)
  - Column `WDI: Inflation CPI (annual %)`
  - Column `WDI: Real interest rate (%)`

## Known unresolvable gaps

- `avg. annual hours per worker` for MENA countries: only available 2005–2023 (PWT's own limitation).
  Workaround: use N = Workforce without hours correction.
- `labsh`, `irr`, `TFP`, `Capital Service`, `Welfare` for **ARE** and **DZA**: not available in PWT 11.0.
  Workaround for Solow aggregation: exclude ARE/DZA from calculations that require these quantities, or
  assume α = 1/3 as a textbook value and compute TFP yourself.
- `TFP/Capital Service/Welfare` 2020–2023 for several countries: PWT 11.0 computes these with a lag.
- `csh_c` for Iraq only 12/54: 1990s sanctions period, acceptable gap (Iraq only used in OPEC aggregate).