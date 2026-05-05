"""
Rebuild Country_Data.xlsx from scratch using PWT 11.0 as the authoritative
source. Only the 3 countries needed for the analysis are included as
country rows: the two subjects (IRN, QAT) and the frontier benchmark
(USA). All regional benchmarks (OPC, MEA, WLD) are added afterwards as
precomputed aggregate rows by fill_data_gaps.py.

Why a rebuild script:
- An earlier Country_Data.xlsx became corrupted during a long-running save
  (file shrunk from ~1MB to 4.8KB).
- It also had wrong Iraq values for `delta` and `csh_i` (~10× off vs.
  PWT 11.0). Rebuilding from PWT 11.0 fixes that bug automatically.
- The 6 individual OPEC member countries (SAU, ARE, KWT, IRQ, DZA, VEN)
  are no longer needed as separate rows since the OPC aggregate is
  computed directly from PWT 11.0 in fill_data_gaps.py.
"""

from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parent
PWT_FILE = BASE / "pwt110.xlsx"
CD_FILE = BASE / "Country_Data.xlsx"

# Base countries: subjects (Iran, Qatar) + frontier benchmark (USA).
# Regional aggregates (OPC / MEA / WLD) are added by fill_data_gaps.py.
BASE_ISOS = ["IRN", "QAT", "USA"]

# Column mapping: PWT short code -> Country_Data long header
# (matches the original Country_Data structure that user had)
PWT_TO_CD = [
    ("countrycode", "countrycode"),
    ("country", "country"),
    ("currency_unit", "currency_unit"),
    ("year", "year"),
    ("rgdpe",   "Inside Real GDP (Chained Prices$)"),
    ("rgdpo",   "Outside Real GDP (Chained Prices$)"),
    ("pop",     "Population"),
    ("emp",     "Workforce"),
    ("avh",     "avg. annual hours per worker"),
    ("hc",      "Human Capital Index"),
    ("ccon",    "Real Consuption (Current 2021 Prices$)"),
    ("cda",     "Domestic Absorbtion (Current 2021 Prices$)"),
    ("cgdpe",   "Inside Real GDP (Current 2021 Prices$)"),
    ("cgdpo",   "Outside Real GDP (Current 2021 Prices$)"),
    ("cn",      "Capital Stock (Current 2021 Prices$)"),
    ("ck",      "Capital Service level (Current 2021 Prices$)"),
    ("ctfp",    "TFP level (Current 2021 Prices$)"),
    ("cwtfp",   "Welfare level (Current 2021 Prices$)"),
    ("rgdpna",  "Real GDP  (Constant 2021 Prices$)"),
    ("rconna",  "Real Consuption (Constant 2021 Prices$)"),
    ("rdana",   "Domestic Absorbtion (Constant 2021 Prices$)"),
    ("rnna",    "Capital Stock (Constant 2021 Prices$)"),
    ("rkna",    "Capital Service level (Constant 2021 Prices$)"),
    ("rtfpna",  "TFP level (Constant 2021 Prices$)"),
    ("rwtfpna", "Welfare level (Constant 2021 Prices$)"),
    ("irr",     "(Real internal rate of return)"),
    ("delta",   "delta"),
    ("xr",      "Exchange rate to USD"),
    ("pl_con",  "pl_con"),
    ("pl_da",   "pl_da"),
    ("pl_gdpo", "pl_gdpo"),
    ("i_cig",   "i_cig"),
    ("i_xm",    "i_xm"),
    ("i_xr",    "i_xr"),
    ("i_outlier", "i_outlier"),
    ("i_irr",   "i_irr"),
    ("cor_exp", "cor_exp"),
    ("csh_c",   "csh_c"),
    ("csh_i",   "csh_i"),
    ("csh_g",   "csh_g"),
    ("csh_x",   "csh_x"),
    ("csh_m",   "csh_m"),
    ("csh_r",   "csh_r"),
    ("pl_c",    "pl_c"),
    ("pl_i",    "pl_i"),
    ("pl_g",    "pl_g"),
    ("pl_x",    "pl_x"),
    ("pl_m",    "pl_m"),
    ("pl_n",    "pl_n"),
    ("pl_k",    "pl_k"),
    ("labsh",   "labsh"),  # added column
]


def main() -> None:
    pwt = pd.read_excel(PWT_FILE, sheet_name="Data")
    sub = pwt[pwt["countrycode"].isin(BASE_ISOS)].copy()
    sub = sub.sort_values(["countrycode", "year"])

    # Keep only mapped columns and rename
    pwt_cols = [p for p, _ in PWT_TO_CD if p in sub.columns]
    cd_cols = [c for p, c in PWT_TO_CD if p in sub.columns]
    out = sub[pwt_cols].copy()
    out.columns = cd_cols
    out["year"] = out["year"].astype(int)

    # Two info sheets are nice-to-have but not strictly required
    info = pd.DataFrame({"Penn World Table, version 11.0": [
        "Rebuilt from pwt110.xlsx by rebuild_country_data.py",
        "9 base countries: IRN, QAT, USA, SAU, ARE, KWT, IRQ, DZA, VEN",
        "Run fill_data_gaps.py afterwards to add WDI cols + OPC/MEA/WLD aggregates.",
    ]})

    legend = pd.DataFrame({
        "Variable name": [c for _, c in PWT_TO_CD],
        "Variable definition": [p for p, _ in PWT_TO_CD],
    })

    with pd.ExcelWriter(CD_FILE, engine="openpyxl") as w:
        info.to_excel(w, sheet_name="Info", index=False)
        legend.to_excel(w, sheet_name="Legend", index=False)
        out.to_excel(w, sheet_name="Data", index=False)

    print(f"Rebuilt Country_Data.xlsx: {len(out)} rows, {len(out.columns)} cols")
    print(f"  Countries: {sorted(out['countrycode'].unique())}")
    print(f"  Years: {int(out['year'].min())}-{int(out['year'].max())}")


if __name__ == "__main__":
    main()
