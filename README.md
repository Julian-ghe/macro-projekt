# Macro Project — Iran & Qatar

Empirical macroeconomics project analysing **Iran** and **Qatar** from
the Penn World Table 11.0, with regional benchmarks (USA frontier,
OPEC Core 6, Middle East, World).

## Structure

| File | Purpose |
|---|---|
| `task1_analysis.py` | Task 1 (b)–(e): GDP per capita, unemployment proxy, inflation, stylized facts |
| `task2_solow.py` | Task 2 (b)–(k): Solow model — calibration, steady state, shock simulation, multi-horizon and post-shock backtests, rolling MAPE |
| `rebuild_country_data.py` | Builds `Country_Data.xlsx` from `pwt110.xlsx` (subjects + frontier benchmark only) |
| `fill_data_gaps.py` | Adds WDI columns (red, Iran/Qatar) and computes OPC/MEA/WLD aggregate rows |
| `macro_formulas&answers.md` | Reference: formulas and intended answers |

## Data sources

- **PWT 11.0** — `pwt110.xlsx` (Penn World Table)
- **WDI** — `Iran P_Data_Extract_…xlsx`, `Qatar P_Data_Extract_…xlsx` (World Bank)
- **Country_Data.xlsx** — derived working file with 3 base countries
  (IRN, QAT, USA) and 3 precomputed aggregate rows (OPC, MEA, WLD)

## Reproduce

```bash
python3 rebuild_country_data.py    # build Country_Data.xlsx from PWT 11.0
python3 fill_data_gaps.py          # add WDI cols + OPC/MEA/WLD aggregates
python3 task1_analysis.py          # Task 1 plots into plots_task1/
python3 task2_solow.py             # Task 2 plots into plots_task2/
```

Both task scripts print summary tables to stdout and save figures.

## Aggregates

`fill_data_gaps.py` computes three regional aggregates directly from
PWT 11.0 (independent of the working file's other rows):

| Code | Members | Method |
|---|---|---|
| `OPC` | SAU, ARE, KWT, IRQ, DZA, VEN | quantities summed; rates pop-weighted |
| `MEA` | BHR, IRQ, ISR, JOR, KWT, LBN, OMN, SAU, SYR, ARE, YEM, TUR, PSE | same |
| `WLD` | all PWT countries except IRN, QAT | same |

Iran and Qatar are deliberately excluded from every aggregate
(they are the subjects of the analysis).

## Outputs

- `plots_task1/` — Task 1 figures (1b real GDP p.c., 1c unemployment,
  1d inflation, 1e stylized facts)
- `plots_task2/` — Task 2 figures (calibration, simulation, comparison,
  multi-horizon/post-shock/rolling backtests)
- `data_gaps_report.md` — coverage of variables across countries
