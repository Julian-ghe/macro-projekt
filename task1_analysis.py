"""
Macro – Task 1
==============
Reads Country_Data.xlsx and creates the plots for Task 1 (b)–(e)
according to macro_formeln.md.

Main countries:    Iran, Qatar
Benchmarks:        USA (frontier),
                   OPEC Core 6 (population-weighted, excluding Iran/Qatar):
                   SAU, ARE, KWT, IRQ, DZA, VEN

Mapping (see macro_formeln.md):
    Real GDP (Y)         = "Real GDP  (Constant 2021 Prices$)"
    Nominal GDP ($Y1)    = "Inside Real GDP (Current 2021 Prices$)"
    Population           = "Population"
    Workforce            = "Workforce"
    Consumption price    = "pl_con"
    Capital Stock (K)    = "Capital Stock (Constant 2021 Prices$)"

Formulas:
    (b) Real GDP per capita(t)   = Y(t) / Pop(t-1)
        g_y(t)                   = ln(y(t)) - ln(y(t-1))
        Avg. growth              = (ln(y_T) - ln(y_0)) / T
    (c) Unemployment-Rate(t)     = 1 - Workforce(t) / Pop(t)
    (d) GDP Deflator(t)          = $Y1(t) / Y(t)
        Inflation(t)             = Deflator(t)/Deflator(t-1) - 1
        Alt.: pl_con(t)/pl_con(t-1) - 1
    (e) Stylized facts: levels & growth comparison.

OPEC aggregation: variables are summed across countries (sum Y, sum Pop,
sum emp, sum nominal Y); the resulting ratios give the population-weighted
mean. Equivalent to treating OPEC as a single economy.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Country_Data.xlsx"
OUT_DIR = BASE_DIR / "plots_task1"
OUT_DIR.mkdir(exist_ok=True)

# -----------------------------------------------------------------------------
# Columns (long names as in Country_Data.xlsx)
# -----------------------------------------------------------------------------
COL_Y_REAL = "Real GDP  (Constant 2021 Prices$)"          # Real GDP (Y)
COL_Y_NOM = "Inside Real GDP (Current 2021 Prices$)"      # Nominal GDP ($Y1)
COL_POP = "Population"
COL_WORK = "Workforce"
COL_PL_CON = "pl_con"
COL_K = "Capital Stock (Constant 2021 Prices$)"
COL_LABSH = "labsh"                                       # labor compensation share

# -----------------------------------------------------------------------------
# Country configuration
# -----------------------------------------------------------------------------
SUBJECTS = {
    "Iran": "IRN",
    "Qatar": "QAT",
}

USA = ("USA", "USA")

# Regional benchmarks – precomputed aggregate rows in Country_Data
# (written by fill_data_gaps.py from PWT 11.0). Read directly as
# country rows.
PRECOMPUTED_BENCHMARKS = {
    "OPEC Core 6": "OPC",
    "Middle East": "MEA",
    "World":       "WLD",
}

COLORS = {
    "Iran":         "#1f77b4",  # blue
    "Qatar":        "#d62728",  # red
    "USA":          "#2ca02c",  # green
    "OPEC Core 6":  "#ff7f0e",  # orange
    "Middle East":  "#9467bd",  # purple
    "World":        "#7f7f7f",  # gray
}
LINESTYLES = {
    "Iran":         "-",
    "Qatar":        "-",
    "USA":          "--",
    "OPEC Core 6":  ":",
    "Middle East":  "--",
    "World":        ":",
}
LINEWIDTHS = {
    "Iran":         2.2,
    "Qatar":        2.2,
    "USA":          1.6,
    "OPEC Core 6":  1.8,
    "Middle East":  1.6,
    "World":        1.6,
}


# -----------------------------------------------------------------------------
# Data loading
# -----------------------------------------------------------------------------
def _series_for_country(raw: pd.DataFrame, iso: str) -> pd.DataFrame:
    df = (
        raw.loc[raw["countrycode"] == iso]
        .sort_values("year")
        .set_index("year")
        .copy()
    )
    return _add_metrics(df)


def _add_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df["GDP_pc"] = df[COL_Y_REAL] / df[COL_POP].shift(1)
    df["log_GDP_pc"] = np.log(df["GDP_pc"])
    df["growth_GDP_pc"] = df["log_GDP_pc"].diff()
    df["unemployment"] = 1.0 - df[COL_WORK] / df[COL_POP]
    df["GDP_deflator"] = df[COL_Y_NOM] / df[COL_Y_REAL]
    df["inflation_def"] = df["GDP_deflator"].pct_change(fill_method=None)
    if COL_PL_CON in df.columns:
        df["inflation_plcon"] = df[COL_PL_CON].pct_change(fill_method=None)
    else:
        df["inflation_plcon"] = np.nan
    return df


def load_data() -> dict[str, pd.DataFrame]:
    raw = pd.read_excel(DATA_FILE, sheet_name="Data")
    raw = raw.dropna(subset=["countrycode", "year"]).copy()
    raw["year"] = raw["year"].astype(int)

    out: dict[str, pd.DataFrame] = {}
    for label, iso in SUBJECTS.items():
        out[label] = _series_for_country(raw, iso)
    out[USA[0]] = _series_for_country(raw, USA[1])
    # Regional benchmarks – precomputed aggregate rows in Country_Data
    # (written by fill_data_gaps.py from PWT 11.0).
    for label, iso in PRECOMPUTED_BENCHMARKS.items():
        if (raw["countrycode"] == iso).any():
            out[label] = _series_for_country(raw, iso)
    return out


# -----------------------------------------------------------------------------
# Plot helper
# -----------------------------------------------------------------------------
def _plot_series(ax, label, series, **kwargs):
    s = series.dropna()
    ax.plot(
        s.index,
        s.values,
        label=label,
        color=COLORS[label],
        linestyle=LINESTYLES[label],
        linewidth=LINEWIDTHS[label],
        **kwargs,
    )


# -----------------------------------------------------------------------------
# Task (b): Real GDP per capita & growth rate
# -----------------------------------------------------------------------------
def task_b(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    fig, axes = plt.subplots(2, 1, figsize=(12, 9), sharex=True)

    summary_rows = []
    for label, df in data.items():
        s_level = df["GDP_pc"]
        s_growth = df["growth_GDP_pc"] * 100
        _plot_series(axes[0], label, s_level)
        _plot_series(axes[1], label, s_growth)

        log_y = df["log_GDP_pc"].dropna()
        if len(log_y) < 2:
            continue
        T = log_y.index[-1] - log_y.index[0]
        avg_g_endpoints = (log_y.iloc[-1] - log_y.iloc[0]) / T
        avg_g_mean = df["growth_GDP_pc"].dropna().mean()
        summary_rows.append({
            "country": label,
            "first_year": int(log_y.index[0]),
            "last_year": int(log_y.index[-1]),
            "GDP_pc_first": s_level.dropna().iloc[0],
            "GDP_pc_last": s_level.dropna().iloc[-1],
            "avg_growth_endpoints_%": avg_g_endpoints * 100,
            "avg_growth_mean_%": avg_g_mean * 100,
        })

    axes[0].set_yscale("log")
    axes[0].set_title("Task 1(b): Real GDP per capita (log scale)")
    axes[0].set_ylabel("Real GDP p.c. (Constant 2017 USD), log")
    axes[0].grid(alpha=0.3, which="both")
    axes[0].legend(loc="lower right", fontsize=9)

    axes[1].axhline(0, color="black", linewidth=0.7)
    axes[1].set_title("Growth rate of Real GDP per capita (log difference)")
    axes[1].set_ylabel("Growth [%]")
    axes[1].set_xlabel("Year")
    axes[1].grid(alpha=0.3)
    axes[1].legend(loc="lower right", fontsize=9)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "1b_real_gdp_per_capita.png", dpi=150)
    plt.close(fig)
    return pd.DataFrame(summary_rows).set_index("country")


# -----------------------------------------------------------------------------
# Task (c): Unemployment rate
# -----------------------------------------------------------------------------
def task_c(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    fig, ax = plt.subplots(figsize=(12, 6))
    summary_rows = []
    for label, df in data.items():
        s = df["unemployment"].dropna() * 100
        _plot_series(ax, label, s)
        if len(s) == 0:
            continue
        summary_rows.append({
            "country": label,
            "mean_%": s.mean(),
            "max_%": s.max(),
            "year_max": int(s.idxmax()),
            "min_%": s.min(),
            "year_min": int(s.idxmin()),
        })

    ax.set_title("Task 1(c): (1 - Workforce/Population) – non-employed share of population")
    ax.set_ylabel("Share [%]")
    ax.set_xlabel("Year")
    ax.grid(alpha=0.3)
    ax.legend(loc="best", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "1c_unemployment.png", dpi=150)
    plt.close(fig)
    return pd.DataFrame(summary_rows).set_index("country")


# -----------------------------------------------------------------------------
# Task (d): Inflation
# -----------------------------------------------------------------------------
def task_d(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    fig, axes = plt.subplots(2, 1, figsize=(12, 9), sharex=True)
    summary_rows = []
    for label, df in data.items():
        infl_def = df["inflation_def"] * 100
        infl_pl = df["inflation_plcon"] * 100
        _plot_series(axes[0], label, infl_def)
        _plot_series(axes[1], label, infl_pl)

        s = infl_def.dropna()
        if len(s) == 0:
            continue
        summary_rows.append({
            "country": label,
            "mean_infl_deflator_%": s.mean(),
            "max_infl_deflator_%": s.max(),
            "year_max_def": int(s.idxmax()),
            "min_infl_deflator_%": s.min(),
            "year_min_def": int(s.idxmin()),
            "mean_infl_plcon_%": infl_pl.dropna().mean(),
        })

    for ax, title in zip(
        axes,
        ["Task 1(d): Inflation from GDP deflator ($Y1 / Y)",
         "Inflation from pl_con (PPP consumption price level)"],
    ):
        ax.axhline(0, color="black", linewidth=0.7)
        ax.set_title(title)
        ax.set_ylabel("Inflation [%]")
        ax.grid(alpha=0.3)
        ax.legend(loc="best", fontsize=9)
    axes[1].set_xlabel("Year")

    # Synchronize y-axes – prevents hyperinflation spikes (e.g. Iraq 1991-95
    # under UN sanctions) from dominating the scale. Spikes that run off the
    # top are legitimate in the aggregation and are deliberately clipped.
    y_lim = (-50, 90)
    for ax in axes:
        ax.set_ylim(*y_lim)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "1d_inflation.png", dpi=150)
    plt.close(fig)

    # ----- Extra: method comparison per country (Iran & Qatar) -----
    _plot_inflation_methods_per_country(data, ["Iran", "Qatar"])
    return pd.DataFrame(summary_rows).set_index("country")


def _plot_inflation_methods_per_country(
    data: dict[str, pd.DataFrame], countries: list[str]
) -> None:
    """
    Direct comparison of the two inflation calculations
    (GDP deflator $Y1/Y vs. pl_con) per country in one subplot.
    """
    fig, axes = plt.subplots(len(countries), 1, figsize=(12, 4 * len(countries)),
                             sharex=True)
    if len(countries) == 1:
        axes = [axes]

    for ax, label in zip(axes, countries):
        df = data[label]
        infl_def = (df["inflation_def"] * 100).dropna()
        infl_pl = (df["inflation_plcon"] * 100).dropna()

        ax.plot(infl_def.index, infl_def.values,
                label="GDP deflator ($Y1 / Y)",
                color=COLORS[label], linestyle="-", linewidth=2)
        ax.plot(infl_pl.index, infl_pl.values,
                label="pl_con (PPP consumption)",
                color=COLORS[label], linestyle="--", linewidth=2, alpha=0.7)

        # Means as horizontal lines
        ax.axhline(infl_def.mean(), color=COLORS[label],
                   linewidth=0.6, alpha=0.4, linestyle="-")
        ax.axhline(infl_pl.mean(), color=COLORS[label],
                   linewidth=0.6, alpha=0.4, linestyle="--")
        ax.axhline(0, color="black", linewidth=0.7)

        ax.set_title(
            f"{label}: comparison of inflation methods "
            f"(mean Deflator = {infl_def.mean():.1f}%, "
            f"mean pl_con = {infl_pl.mean():.1f}%)"
        )
        ax.set_ylabel("Inflation [%]")
        ax.grid(alpha=0.3)
        ax.legend(loc="best", fontsize=9)

    axes[-1].set_xlabel("Year")
    fig.suptitle(
        "Task 1(d) – Method comparison GDP deflator vs. pl_con",
        fontsize=13,
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "1d_inflation_methods_per_country.png", dpi=150)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Task (e): Stylized Facts
# Layout follows Sorensen & Whitta-Jacobsen (2022) Lecture 3 examples:
#   Real GDP per capita & per worker (level + ln), labor share, capital share.
#
# Formulas used:
#   Real GDP per worker      = Y / Workforce
#   Logarithm GDP per worker = ln(Y / Workforce)
#   Real GDP per capita      = Y / Population
#   Logarithm GDP per capita = ln(Y / Population)
#   Labor share              = labsh   (= Real Wages · N / Y in the data)
#   Capital share            = 1 - Labor share
# -----------------------------------------------------------------------------
def task_e(data: dict[str, pd.DataFrame]) -> None:
    fig, axes = plt.subplots(4, 2, figsize=(14, 18))

    # Helper to compute all series per country
    def _series(df: pd.DataFrame) -> dict[str, pd.Series]:
        y_pc = (df[COL_Y_REAL] / df[COL_POP]).replace([np.inf, -np.inf], np.nan)
        y_pw = (df[COL_Y_REAL] / df[COL_WORK]).replace([np.inf, -np.inf], np.nan)
        labsh = df[COL_LABSH] if COL_LABSH in df.columns else pd.Series(dtype=float)
        return {
            "y_pc": y_pc,
            "ln_y_pc": np.log(y_pc),
            "y_pw": y_pw,
            "ln_y_pw": np.log(y_pw),
            # Growth rates as log differences (= year-on-year % growth in log form)
            "g_y_pc": np.log(y_pc).diff() * 100,
            "g_y_pw": np.log(y_pw).diff() * 100,
            "labor_share": labsh,
            "capital_share": (1.0 - labsh) if not labsh.empty else labsh,
        }

    panels = [
        (axes[0, 0], "y_pc",           "Real GDP per capita",
         "Y / Population (Constant 2021 USD)", False, False),
        (axes[0, 1], "ln_y_pc",        "Logarithm of Real GDP per capita",
         "ln(Y / Population)", False, False),
        (axes[1, 0], "y_pw",           "Real GDP per worker",
         "Y / Workforce (Constant 2021 USD)", False, False),
        (axes[1, 1], "ln_y_pw",        "Logarithm of Real GDP per worker",
         "ln(Y / Workforce)", False, False),
        (axes[2, 0], "g_y_pc",
         "Growth rate of Real GDP per capita  (Δln(Y/Pop))",
         "Growth", False, True),
        (axes[2, 1], "g_y_pw",
         "Growth rate of Real GDP per worker  (Δln(Y/N))",
         "Growth", False, True),
        (axes[3, 0], "labor_share",    "Labor share = labsh (= w·N / Y)",
         "Labor share", True, False),
        (axes[3, 1], "capital_share",  "Capital share = 1 − Labor share",
         "Capital share", True, False),
    ]

    for ax, key, title, ylabel, is_share, is_growth in panels:
        for label, df in data.items():
            series = _series(df)[key]
            if series.dropna().empty:
                continue
            plot_s = series * (100 if is_share else 1)
            _plot_series(ax, label, plot_s)
        ax.set_title(title)
        ax.set_ylabel(ylabel + (" [%]" if (is_share or is_growth) else ""))
        ax.grid(alpha=0.3)
        ax.legend(loc="best", fontsize=8)
        if is_share:
            ax.set_ylim(0, 100)
        if is_growth:
            ax.axhline(0, color="black", linewidth=0.7)

    for ax in axes[-1]:
        ax.set_xlabel("Year")

    fig.suptitle(
        "Task 1(e): Stylized Facts – Iran & Qatar vs. USA, "
        "OPEC Core 6, Middle East, World",
        fontsize=14,
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "1e_stylized_facts.png", dpi=150)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> None:
    data = load_data()

    print("=" * 80)
    print("Task 1(b): Real GDP per capita")
    print("=" * 80)
    table_b = task_b(data).round(2)
    print(table_b.to_string())

    # Explicit average growth rate (log-difference, whole sample) for subjects
    print("\n--- Average growth rate of Real GDP per capita (whole sample) ---")
    for c in ["Iran", "Qatar"]:
        if c in table_b.index:
            row = table_b.loc[c]
            print(
                f"  {c:<6}: {row['avg_growth_endpoints_%']:+.2f} %  "
                f"(endpoint method, {int(row['first_year'])}–{int(row['last_year'])}, "
                f"T = {int(row['last_year']) - int(row['first_year'])} years)"
            )

    print("\n" + "=" * 80)
    print("Task 1(c): (1 - Workforce/Population)")
    print("=" * 80)
    table_c = task_c(data).round(2)
    print(table_c.to_string())

    print("\n--- Unemployment Rate summary (Iran & Qatar) ---")
    for c in ["Iran", "Qatar"]:
        if c in table_c.index:
            row = table_c.loc[c]
            print(f"  {c}:")
            print(f"    - Smallest Value for Unemployment Rate: "
                  f"{row['min_%']:.2f} %  (in {int(row['year_min'])})")
            print(f"    - Average Unemployment Rate:            "
                  f"{row['mean_%']:.2f} %")
            print(f"    - Largest Value for Unemployment Rate:  "
                  f"{row['max_%']:.2f} %  (in {int(row['year_max'])})")

    print("\n" + "=" * 80)
    print("Task 1(d): Inflation")
    print("=" * 80)
    print(task_d(data).round(2).to_string())

    task_e(data)
    print("\nDone. Plots saved in:", OUT_DIR)


if __name__ == "__main__":
    main()
