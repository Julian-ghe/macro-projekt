"""
Macro – Task 2: Solow Model (Simulation)
========================================
Setup (corresponds to (a) in Task 1) loads Country_Data.xlsx and calibrates
the five model parameters for each subject country.

Tasks:
    (b) Calibration:        α, n, δ, g, s from data; A_0 = 1
    (c) Steady state:       k̃*, ỹ*, c̃*, k_t*, y_t*, c_t* analytically
    (d) Shock in period 20: permanently change one parameter
    (e) % change of steady-state values after shock
    (f) Simulation 100 periods: k̃, ỹ, c̃, A, k, y, c, ln(y), ln(c), g_y
    (g) Diagrams of the time evolution

Model equations (Cobb-Douglas, intensive form, with exogenous TFP A_t):
    ỹ_t = k̃_t^α
    k̃_{t+1} = (s·ỹ_t + (1-δ)·k̃_t) / ((1+n)(1+g))
    c̃_t = (1-s)·ỹ_t
    A_t = A_0·(1+g)^t
    k_t = k̃_t·A_t,  y_t = ỹ_t·A_t,  c_t = c̃_t·A_t

Steady state:
    k̃* = (s / (n+g+δ+ng))^(1/(1-α))
    ỹ* = (k̃*)^α
    c̃* = (1-s)·ỹ*

Shock motivation (see COUNTRY_SHOCKS below):
    Iran:  s drops 5 pp (oil price shock + sanctions reduce investment)
    Qatar: n drops from ~6 % to 2 % (normalization after LNG construction)

Assumptions from data consolidation (see macro_formeln.md):
    - N = Workforce without hours correction (avh only 2005+ for MENA).
    - α time-varying α_t = 1-labsh_t in the data; for calibration
      mean over the sample period.
    - g = mean of Δln(Y/N) over the sample (output-per-worker growth
      as approximation of the TFP trend).
    - s ≈ csh_i (investment share, standard Solow approximation).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Country_Data.xlsx"
OUT_DIR = BASE_DIR / "plots_task2"
OUT_DIR.mkdir(exist_ok=True)

COL_Y = "Real GDP  (Constant 2021 Prices$)"
COL_K = "Capital Stock (Constant 2021 Prices$)"
COL_POP = "Population"
COL_N = "Workforce"
COL_DELTA = "delta"
COL_LABSH = "labsh"
COL_CSH_I = "csh_i"

SUBJECTS = {"Iran": "IRN", "Qatar": "QAT"}
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
    "Iran":         "#1f77b4",
    "Qatar":        "#d62728",
    "USA":          "#2ca02c",
    "OPEC Core 6":  "#ff7f0e",
    "Middle East":  "#9467bd",
    "World":        "#7f7f7f",
}
LINESTYLES = {
    "Iran": "-", "Qatar": "-", "USA": "--",
    "OPEC Core 6": ":", "Middle East": "--", "World": ":",
}
LINEWIDTHS = {
    "Iran": 2.2, "Qatar": 2.2, "USA": 1.6,
    "OPEC Core 6": 1.8, "Middle East": 1.6, "World": 1.6,
}

# Shock definition per country
COUNTRY_SHOCKS = {
    "Iran": {
        "param": "s",
        "delta": -0.05,
        "motivation": (
            "Savings rate drops 5 pp (1986 oil price shock + tightened "
            "US sanctions reduce investment capacity; compare actual "
            "csh_i series for Iran in 1986-1990 and 2012+)."
        ),
    },
    "Qatar": {
        "param": "n",
        "delta": -0.04,
        "motivation": (
            "Population growth n drops from ~6 % to ~2 % (normalization "
            "after LNG construction phase, lower migration inflows). "
            "Empirically observable in PWT data for Qatar from 2016."
        ),
    },
    "USA": {
        "param": "g",
        "delta": -0.005,
        "motivation": (
            "TFP growth drops by 0.5 pp (Gordon's productivity-slowdown "
            "hypothesis: internet-boom effects fade, post-2000 stagnation "
            "of per-capita growth rates)."
        ),
    },
    "OPEC Core 6": {
        "param": "s",
        "delta": -0.05,
        "motivation": (
            "Savings rate drops 5 pp (oil price crash 2014/2020 reduces "
            "investment capacity of petrostates collectively)."
        ),
    },
}

# Simulation
T_TOTAL = 100
T_SHOCK = 20

# Backtest
T_FORECAST = 2023                      # End year (= last data year)
BACKTEST_HORIZONS = [40, 30, 20, 10]   # Years back from T_FORECAST

# Event-based backtest: calibrate up to the last "calm" year before
# an identifiable structural shock, then project from the shock onwards.
EVENTS = {
    "Iran":     {"t_cut": 1978, "name": "Islamic Revolution + Iran-Iraq War"},
    "Qatar":    {"t_cut": 1995, "name": "Start of LNG exports (Qatargas)"},
    "USA":      {"t_cut": 2007, "name": "Global Financial Crisis"},
    "OPEC Core 6": {"t_cut": 1985, "name": "Oil price crash 1986"},
}


# -----------------------------------------------------------------------------
# Data preparation & setup
# -----------------------------------------------------------------------------
def load_country(raw: pd.DataFrame, iso: str) -> pd.DataFrame:
    df = (
        raw.loc[raw["countrycode"] == iso]
        .sort_values("year")
        .set_index("year")
        .copy()
    )
    df["n_t"] = df[COL_POP].pct_change(fill_method=None)
    df["alpha_t"] = 1.0 - df[COL_LABSH]
    df["s_t"] = df[COL_CSH_I]
    df["delta_t"] = df[COL_DELTA]
    df["y_per_N"] = df[COL_Y] / df[COL_N]
    df["g_y_t"] = np.log(df["y_per_N"]).diff()
    return df


def load_data() -> dict[str, pd.DataFrame]:
    raw = pd.read_excel(DATA_FILE, sheet_name="Data")
    raw = raw.dropna(subset=["countrycode", "year"]).copy()
    raw["year"] = raw["year"].astype(int)
    out = {}
    for label, iso in SUBJECTS.items():
        out[label] = load_country(raw, iso)
    out[USA[0]] = load_country(raw, USA[1])
    # Regional benchmarks – precomputed aggregate rows in Country_Data
    for label, iso in PRECOMPUTED_BENCHMARKS.items():
        if (raw["countrycode"] == iso).any():
            out[label] = load_country(raw, iso)
    return out


# -----------------------------------------------------------------------------
# (b) Calibration
# -----------------------------------------------------------------------------
def calibrate(df: pd.DataFrame) -> dict:
    """Means of α, n, δ, g, s over the sample. A_0 = 1."""
    return {
        "alpha": float(df["alpha_t"].dropna().mean()),
        "n":     float(df["n_t"].dropna().mean()),
        "delta": float(df["delta_t"].dropna().mean()),
        "g":     float(df["g_y_t"].dropna().mean()),
        "s":     float(df["s_t"].dropna().mean()),
        "A0":    1.0,
    }


def task_b(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Calibration table and visualization of the underlying time series."""
    rows = []
    for label, df in data.items():
        p = calibrate(df)
        rows.append({"country": label, **p})
    table = pd.DataFrame(rows).set_index("country")

    # Plot of time series + calibration mean as horizontal line
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True)
    panels = [
        ("alpha_t", "α_t = 1 − labsh_t", "alpha"),
        ("n_t",     "n_t (population growth)", "n"),
        ("delta_t", "δ_t (depreciation)", "delta"),
        ("g_y_t",   "g_t = Δln(Y/N) (TFP trend proxy)", "g"),
        ("s_t",     "s_t = csh_i (investment share)", "s"),
    ]
    for ax, (col, title, key) in zip(axes.flat, panels):
        for label, df in data.items():
            ax.plot(df.index, df[col], label=label,
                    color=COLORS[label], linewidth=1.5)
            mean_val = table.loc[label, key]
            ax.axhline(mean_val, color=COLORS[label],
                       linestyle="--", linewidth=0.8, alpha=0.5)
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_title(title)
        ax.grid(alpha=0.3)
        ax.legend(loc="best", fontsize=8)
    axes[1, 2].set_visible(False)
    fig.suptitle("Task 2(b): Calibration – time series and means",
                 fontsize=14)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "2b_calibration.png", dpi=150)
    plt.close(fig)
    return table


# -----------------------------------------------------------------------------
# (c) Steady state (analytical)
# -----------------------------------------------------------------------------
def steady_state(p: dict) -> dict:
    """k̃*, ỹ*, c̃* with correct denominator (n+g+δ+ng)."""
    alpha, n, g, delta, s = p["alpha"], p["n"], p["g"], p["delta"], p["s"]
    denom = n + g + delta + n * g
    if denom <= 0 or alpha >= 1:
        return {"k_tilde": np.nan, "y_tilde": np.nan, "c_tilde": np.nan}
    k_tilde = (s / denom) ** (1 / (1 - alpha))
    y_tilde = k_tilde ** alpha
    c_tilde = (1 - s) * y_tilde
    return {"k_tilde": k_tilde, "y_tilde": y_tilde, "c_tilde": c_tilde}


def task_c(params: dict[str, dict]) -> pd.DataFrame:
    rows = []
    for label, p in params.items():
        ss = steady_state(p)
        rows.append({"country": label, **ss})
    table = pd.DataFrame(rows).set_index("country").round(4)
    return table


# -----------------------------------------------------------------------------
# (d) + (e) Shock and new steady state
# -----------------------------------------------------------------------------
def apply_shock(p: dict, shock: dict) -> dict:
    p_new = p.copy()
    p_new[shock["param"]] = p[shock["param"]] + shock["delta"]
    return p_new


def task_de(params: dict[str, dict]) -> pd.DataFrame:
    rows = []
    for label, p in params.items():
        if label not in COUNTRY_SHOCKS:
            continue
        shock = COUNTRY_SHOCKS[label]
        p_new = apply_shock(p, shock)
        ss_old = steady_state(p)
        ss_new = steady_state(p_new)
        for key in ["k_tilde", "y_tilde", "c_tilde"]:
            old, new = ss_old[key], ss_new[key]
            change_pct = (new / old - 1) * 100 if old else np.nan
            rows.append({
                "country": label,
                "shock_param": shock["param"],
                "shock_delta": shock["delta"],
                "variable": key,
                "ss_pre": old,
                "ss_post": new,
                "change_%": change_pct,
            })
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# (f) Simulation 100 periods with shock
# -----------------------------------------------------------------------------
def simulate(p_initial: dict, shock: dict | None = None,
             T: int = T_TOTAL, t_shock: int = T_SHOCK,
             k_tilde0: float | None = None,
             A0: float | None = None) -> pd.DataFrame:
    """
    Simulates the Solow trajectory.
    Default: start in pre-shock steady state, shock in t_shock.
    With k_tilde0/A0 override for backtest (start from observed data).
    """
    p_post = apply_shock(p_initial, shock) if shock is not None else p_initial

    if k_tilde0 is None:
        k_tilde0 = steady_state(p_initial)["k_tilde"]
    if A0 is None:
        A0 = p_initial["A0"]

    rows = []
    k_tilde = k_tilde0
    for t in range(T):
        p = p_post if (shock is not None and t >= t_shock) else p_initial
        alpha = p["alpha"]
        s, n, g, delta = p["s"], p["n"], p["g"], p["delta"]

        y_tilde = k_tilde ** alpha
        c_tilde = (1 - s) * y_tilde

        if t == 0:
            A = A0
        else:
            g_prev = (p_post["g"]
                      if (shock is not None and t-1 >= t_shock)
                      else p_initial["g"])
            A = rows[-1]["A"] * (1 + g_prev)

        k = k_tilde * A
        y = y_tilde * A
        c = c_tilde * A

        rows.append({
            "t": t,
            "k_tilde": k_tilde, "y_tilde": y_tilde, "c_tilde": c_tilde,
            "A": A, "k": k, "y": y, "c": c,
            "ln_y": np.log(y) if y > 0 else np.nan,
            "ln_c": np.log(c) if c > 0 else np.nan,
        })

        k_tilde = (s * y_tilde + (1 - delta) * k_tilde) / ((1 + n) * (1 + g))

    sim = pd.DataFrame(rows).set_index("t")
    sim["g_y"] = sim["ln_y"].diff()
    return sim


# -----------------------------------------------------------------------------
# (g) Diagrams
# -----------------------------------------------------------------------------
def task_fg(params: dict[str, dict], simulations: dict[str, pd.DataFrame]) -> None:
    """
    Per country: 2x3 subplots with the simulated series.
    Vertical line marks the shock period.
    """
    for label, sim in simulations.items():
        fig, axes = plt.subplots(2, 3, figsize=(16, 9))
        color = COLORS[label]
        shock = COUNTRY_SHOCKS[label]

        panels = [
            (axes[0, 0], ["k_tilde", "y_tilde", "c_tilde"],
             "Intensive form: k̃, ỹ, c̃ (per effective worker)"),
            (axes[0, 1], ["A"], "Technology A_t = (1+g)^t"),
            (axes[0, 2], ["k", "y", "c"],
             "Per worker: k, y, c (= intensive · A_t)"),
            (axes[1, 0], ["ln_y"], "ln(y_t) – output per worker (log)"),
            (axes[1, 1], ["ln_c"], "ln(c_t) – consumption per worker (log)"),
            (axes[1, 2], ["g_y"], "g_y_t = Δln(y_t) – growth rate"),
        ]
        line_styles = {"k_tilde": "-", "y_tilde": "--", "c_tilde": ":",
                       "k": "-", "y": "--", "c": ":",
                       "A": "-", "ln_y": "-", "ln_c": "-", "g_y": "-"}

        for ax, cols, title in panels:
            for col in cols:
                ax.plot(sim.index, sim[col], label=col,
                        color=color, linewidth=1.8,
                        linestyle=line_styles[col])
            ax.axvline(T_SHOCK, color="black", linestyle="--",
                       linewidth=0.8, alpha=0.7,
                       label=f"Shock (t={T_SHOCK})" if title.startswith("Intensive") else None)
            ax.set_title(title)
            ax.set_xlabel("Period t")
            ax.grid(alpha=0.3)
            ax.legend(loc="best", fontsize=8)
            if title.startswith("ln") or "log" in title:
                pass  # already log
            elif "growth" in title.lower() or "wachstum" in title.lower():
                ax.axhline(0, color="black", linewidth=0.6)

        # Header with shock info
        fig.suptitle(
            f"{label}: Solow simulation 100 periods (shock at t={T_SHOCK}: "
            f"{shock['param']} {shock['delta']:+.2f})",
            fontsize=14,
        )
        fig.tight_layout()
        fig.savefig(OUT_DIR / f"2fg_simulation_{label}.png", dpi=150)
        plt.close(fig)


# -----------------------------------------------------------------------------
# (h) Cross-country comparison of the simulations
# -----------------------------------------------------------------------------
def task_h_compare(simulations: dict[str, pd.DataFrame]) -> None:
    """Overlay all 4 country simulations in one plot."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    panels = [
        (axes[0, 0], "y_tilde", "ỹ_t (output per effective worker)"),
        (axes[0, 1], "k_tilde", "k̃_t (capital per effective worker)"),
        (axes[1, 0], "ln_y",    "ln(y_t) (output per worker, log)"),
        (axes[1, 1], "g_y",     "g_y_t = Δln(y_t) (growth rate)"),
    ]
    for ax, col, title in panels:
        for label, sim in simulations.items():
            ax.plot(sim.index, sim[col],
                    label=label,
                    color=COLORS[label],
                    linestyle=LINESTYLES[label],
                    linewidth=LINEWIDTHS[label])
        ax.axvline(T_SHOCK, color="black", linestyle="--",
                   linewidth=0.7, alpha=0.6)
        if "g_y" in col:
            ax.axhline(0, color="black", linewidth=0.5)
        ax.set_title(title)
        ax.set_xlabel("Period t")
        ax.grid(alpha=0.3)
        ax.legend(loc="best", fontsize=9)
    fig.suptitle(
        "Task 2(h): Comparison of the 4 Solow simulations "
        f"(shock at t={T_SHOCK}, country-specific)",
        fontsize=13,
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "2h_comparison.png", dpi=150)
    plt.close(fig)


# -----------------------------------------------------------------------------
# (i) Backtest: what would a 2013-calibrated model have predicted?
# -----------------------------------------------------------------------------
def backtest(label: str, df: pd.DataFrame,
             t_cut: int, t_end: int = T_FORECAST) -> dict:
    """
    Calibrate on data 1955-t_cut. Anchor the model at the observed
    values in t_cut. Simulate until t_end. Compare without shock
    against the actual data.
    """
    df_cal = df.loc[df.index <= t_cut].copy()
    p = calibrate(df_cal)

    # Anchor at the observed values in t_cut.
    # Harrod-neutral form:  y = k_tilde^α · A   with k_tilde = (K/N)/A
    # → y = (K/N)^α · A^(1-α)
    # → A^(1-α) = y / (K/N)^α  → A = (y / (K/N)^α)^(1/(1-α))
    Y0 = df.loc[t_cut, COL_Y]
    K0 = df.loc[t_cut, COL_K]
    N0 = df.loc[t_cut, COL_N]
    y0 = Y0 / N0
    k0 = K0 / N0
    alpha = p["alpha"]

    A0 = (y0 / (k0 ** alpha)) ** (1.0 / (1.0 - alpha))
    k_tilde0 = k0 / A0
    p["A0"] = A0

    horizon = t_end - t_cut + 1
    sim = simulate(p, shock=None, T=horizon,
                   k_tilde0=k_tilde0, A0=A0)
    sim.index = list(range(t_cut, t_cut + horizon))

    # Actual data over the forecast window
    actual = pd.DataFrame({
        "y_data":   df.loc[t_cut:t_end, COL_Y] / df.loc[t_cut:t_end, COL_N],
        "k_data":   df.loc[t_cut:t_end, COL_K] / df.loc[t_cut:t_end, COL_N],
    })
    return {
        "label": label,
        "params": p,
        "k_tilde0": k_tilde0,
        "A0": A0,
        "sim": sim,
        "actual": actual,
    }


def task_i_backtest(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    4 horizons (40/30/20/10 yrs) in a 2x2 grid. Per panel all 4 countries
    overlaid: solid = reality, dashed = Solow prediction.
    """
    backtest_targets = ["Iran", "Qatar", "USA",
                        "OPEC Core 6", "Middle East", "World"]
    fig, axes = plt.subplots(2, 2, figsize=(15, 11))
    summary = []

    for ax, h in zip(axes.flat, BACKTEST_HORIZONS):
        t_cut = T_FORECAST - h
        for label in backtest_targets:
            r = backtest(label, data[label], t_cut=t_cut)
            sim = r["sim"]
            actual = r["actual"]

            ax.plot(actual.index, actual["y_data"],
                    color=COLORS[label], linewidth=2.0,
                    marker="o", markersize=3, label=f"{label} (real)")
            ax.plot(sim.index, sim["y"],
                    color=COLORS[label], linestyle="--",
                    linewidth=1.4, alpha=0.85,
                    label=f"{label} (prediction)")

            join = sim[["y"]].join(actual["y_data"], how="inner").dropna()
            if len(join):
                err_pct = (join["y"] / join["y_data"] - 1) * 100
                summary.append({
                    "horizon_y": h,
                    "country": label,
                    "calib_period": f"1955-{t_cut}",
                    "forecast_period": f"{t_cut+1}-{T_FORECAST}",
                    "MAPE_%": round(err_pct.abs().mean(), 2),
                    "endpoint_error_%": round(err_pct.iloc[-1], 2),
                    "actual_y_endpoint": round(join["y_data"].iloc[-1], 0),
                    "predicted_y_endpoint": round(join["y"].iloc[-1], 0),
                })

        ax.axvline(t_cut, color="black", linestyle=":",
                   linewidth=0.8, alpha=0.7)
        ax.set_yscale("log")
        ax.set_title(
            f"Horizon {h} years: calibration 1955–{t_cut}, "
            f"forecast {t_cut+1}–{T_FORECAST}"
        )
        ax.set_ylabel("y = Y/N (USD per worker, log)")
        ax.set_xlabel("Year")
        ax.grid(alpha=0.3, which="both")
        # Compact legend: only one entry per country in the first panel
        if ax is axes[0, 0]:
            ax.legend(loc="lower right", fontsize=8, ncol=2)
        else:
            # Other panels: only countries (drop real/prediction suffix)
            handles, labels = ax.get_legend_handles_labels()
            uniq = {}
            for h_, l_ in zip(handles, labels):
                country = l_.split(" (")[0]
                if country not in uniq:
                    uniq[country] = h_
            ax.legend(uniq.values(), uniq.keys(),
                      loc="lower right", fontsize=8)

    fig.suptitle(
        "Task 2(i): Multi-horizon backtest – solid = reality, "
        "dashed = Solow prediction",
        fontsize=13,
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "2i_backtest.png", dpi=150)
    plt.close(fig)

    table = pd.DataFrame(summary).set_index(["horizon_y", "country"])
    return table


# -----------------------------------------------------------------------------
# Helper: Post-shock simulation for a single country × event
# -----------------------------------------------------------------------------
def post_shock_sim(df: pd.DataFrame, t_start: int,
                   t_end: int = T_FORECAST) -> pd.DataFrame | None:
    """
    Calibrates on post-shock data t_start..t_end and returns a join
    DataFrame with columns 'y_pred' and 'y_data'. Returns None if the
    data are insufficient.
    """
    if t_start not in df.index or len(df.loc[t_start:t_end]) < 5:
        return None
    df_post = df.loc[t_start:t_end].copy()
    p = calibrate(df_post)
    alpha = p["alpha"]
    if not np.isfinite(alpha) or alpha >= 1 or alpha <= 0:
        return None

    Y0 = df.loc[t_start, COL_Y]
    K0 = df.loc[t_start, COL_K]
    N0 = df.loc[t_start, COL_N]
    if pd.isna(Y0) or pd.isna(K0) or pd.isna(N0) or N0 == 0:
        return None
    y0 = Y0 / N0
    k0 = K0 / N0
    A0 = (y0 / (k0 ** alpha)) ** (1.0 / (1.0 - alpha))
    k_tilde0 = k0 / A0
    p["A0"] = A0

    horizon = t_end - t_start + 1
    sim = simulate(p, shock=None, T=horizon, k_tilde0=k_tilde0, A0=A0)
    sim.index = list(range(t_start, t_start + horizon))
    actual = df.loc[t_start:t_end, COL_Y] / df.loc[t_start:t_end, COL_N]
    join = sim[["y"]].rename(columns={"y": "y_pred"}).join(
        actual.rename("y_data"), how="inner"
    ).dropna()
    return join if len(join) else None


# -----------------------------------------------------------------------------
# (j) Post-shock backtest – calibrate from after the shock, all 4 countries
# -----------------------------------------------------------------------------
def task_j_post_shock_backtest(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    For each event: calibrate the parameters ONLY on post-shock data
    (T_event+1 to 2023). Anchor point is the first post-shock year.
    Simulation runs forward from there. For each event all 4 countries
    in one panel. This tests whether the post-shock path is a stable
    Solow trajectory (parameter-stable growth theory) or whether further
    structural breaks occur.
    """
    backtest_targets = ["Iran", "Qatar", "USA",
                        "OPEC Core 6", "Middle East", "World"]
    fig, axes = plt.subplots(2, 2, figsize=(15, 11))
    summary = []

    for ax, (event_country, ev) in zip(axes.flat, EVENTS.items()):
        t_start = ev["t_cut"] + 1   # first post-shock year
        t_end = T_FORECAST

        for label in backtest_targets:
            df = data[label]
            if t_start not in df.index or len(df.loc[t_start:t_end]) < 5:
                continue

            df_post = df.loc[t_start:t_end].copy()
            p = calibrate(df_post)
            alpha = p["alpha"]
            if not np.isfinite(alpha) or alpha >= 1 or alpha <= 0:
                continue

            # Anchor at the post-shock year
            Y0 = df.loc[t_start, COL_Y]
            K0 = df.loc[t_start, COL_K]
            N0 = df.loc[t_start, COL_N]
            if pd.isna(Y0) or pd.isna(K0) or pd.isna(N0) or N0 == 0:
                continue
            y0 = Y0 / N0
            k0 = K0 / N0
            A0 = (y0 / (k0 ** alpha)) ** (1.0 / (1.0 - alpha))
            k_tilde0 = k0 / A0
            p["A0"] = A0

            horizon = t_end - t_start + 1
            sim = simulate(p, shock=None, T=horizon,
                           k_tilde0=k_tilde0, A0=A0)
            sim.index = list(range(t_start, t_start + horizon))

            actual = df.loc[t_start:t_end, COL_Y] / df.loc[t_start:t_end, COL_N]

            ax.plot(actual.index, actual.values,
                    color=COLORS[label], linewidth=2.0,
                    marker="o", markersize=3,
                    label=f"{label} – real")
            ax.plot(sim.index, sim["y"],
                    color=COLORS[label], linestyle="--",
                    linewidth=1.4, alpha=0.85,
                    label=f"{label} – Solow (post-shock cal.)")

            join = sim[["y"]].join(actual.rename("y_data"), how="inner").dropna()
            if len(join):
                err_pct = (join["y"] / join["y_data"] - 1) * 100
                summary.append({
                    "event": f"{event_country} {ev['t_cut']}",
                    "event_name": ev["name"],
                    "t_start": t_start,
                    "country": label,
                    "horizon_y": t_end - t_start + 1,
                    "MAPE_%": round(err_pct.abs().mean(), 2),
                    "endpoint_error_%": round(err_pct.iloc[-1], 2),
                    "actual_y_endpoint": round(join["y_data"].iloc[-1], 0),
                    "predicted_y_endpoint": round(join["y"].iloc[-1], 0),
                })

        ax.axvline(t_start, color="black", linestyle=":",
                   linewidth=0.8, alpha=0.7)
        ax.set_yscale("log")
        ax.set_title(
            f"Post-shock: {event_country} {ev['t_cut']} – {ev['name']}\n"
            f"Calibration & simulation from {t_start}",
            fontsize=10,
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("y = Y/N (USD per worker, log)")
        ax.grid(alpha=0.3, which="both")

        # Legend: one line per country (real/Solow shown by line style)
        if ax is axes[0, 0]:
            ax.legend(loc="lower right", fontsize=7, ncol=2)
        else:
            handles, labels = ax.get_legend_handles_labels()
            uniq = {}
            for h_, l_ in zip(handles, labels):
                country = l_.split(" – ")[0]
                if country not in uniq:
                    uniq[country] = h_
            ax.legend(uniq.values(), uniq.keys(),
                      loc="lower right", fontsize=8)

    fig.suptitle(
        "Task 2(j): Post-shock backtest – Solow calibrated from post-shock, "
        "all 4 countries per event",
        fontsize=13,
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "2j_post_shock_backtest.png", dpi=150)
    plt.close(fig)

    return pd.DataFrame(summary).set_index(["event", "country"])


# -----------------------------------------------------------------------------
# (k) Rolling 5-yr MAPE – when does the prediction drift?
# -----------------------------------------------------------------------------
def task_k_rolling_error(data: dict[str, pd.DataFrame],
                         window: int = 5) -> None:
    """
    Per event, 4 countries: rolling 5-year MAPE of the post-shock
    prediction. Stable tracking phases are flat; an upward kink marks
    the timing of a follow-up shock at which the prediction loses
    track of reality.
    """
    backtest_targets = ["Iran", "Qatar", "USA",
                        "OPEC Core 6", "Middle East", "World"]
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    for ax, (event_country, ev) in zip(axes.flat, EVENTS.items()):
        t_start = ev["t_cut"] + 1

        for label in backtest_targets:
            join = post_shock_sim(data[label], t_start)
            if join is None:
                continue
            err = (join["y_pred"] / join["y_data"] - 1).abs() * 100
            roll = err.rolling(window, min_periods=3).mean()
            ax.plot(roll.index, roll.values,
                    color=COLORS[label],
                    linestyle=LINESTYLES[label],
                    linewidth=LINEWIDTHS[label],
                    label=label)

        # Reference lines
        ax.axhline(5, color="green", linestyle="--",
                   linewidth=0.7, alpha=0.5, label="5 % (good)")
        ax.axhline(20, color="orange", linestyle="--",
                   linewidth=0.7, alpha=0.5, label="20 % (critical)")
        ax.set_yscale("log")
        ax.set_ylim(0.5, 500)
        ax.set_title(
            f"Post-shock: {event_country} {ev['t_cut']} – {ev['name']}",
            fontsize=10,
        )
        ax.set_xlabel("Year")
        ax.set_ylabel(f"Rolling {window}-yr MAPE [%, log]")
        ax.grid(alpha=0.3, which="both")
        if ax is axes[0, 0]:
            ax.legend(loc="upper left", fontsize=7, ncol=2)

    fig.suptitle(
        "Task 2(k): Rolling 5-year MAPE – when does the prediction "
        "leave the real path?",
        fontsize=13,
    )
    fig.tight_layout()
    fig.savefig(OUT_DIR / "2k_rolling_error.png", dpi=150)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> None:
    data = load_data()

    # (b) Calibration
    print("="*80); print("(b) Calibration of model parameters (A_0 = 1)"); print("="*80)
    calib_table = task_b(data)
    print(calib_table.round(4).to_string())

    params = {label: calibrate(df) for label, df in data.items()}

    # (c) Steady state
    print("\n"+"="*80); print("(c) Steady-state values (analytical, balanced growth)"); print("="*80)
    ss_table = task_c(params)
    print(ss_table.to_string())

    print("\n--- Steady-state values per variable ---")
    for label, p in params.items():
        ss = steady_state(p)
        print(f"  {label}:")
        print(f"    - k̃* (capital per effective worker):   {ss['k_tilde']:.4f}")
        print(f"    - ỹ* (output per effective worker):    {ss['y_tilde']:.4f}")
        print(f"    - c̃* (consumption per effective worker): {ss['c_tilde']:.4f}")

    # (d) Shock motivation
    print("\n"+"="*80); print("(d) Shock motivation"); print("="*80)
    for label, shock in COUNTRY_SHOCKS.items():
        print(f"\n  {label}:")
        print(f"    - Parameter Choice: {shock['param']} (Δ = {shock['delta']:+.3f})")
        print(f"    - Motivation:       {shock['motivation']}")

    # (e) Steady-state change after shock
    print("\n"+"="*80); print("(e) Steady-state change after shock"); print("="*80)
    ss_change = task_de(params).round(3)
    print(ss_change.to_string(index=False))

    print("\n--- % Change of steady-state values per variable ---")
    for label, p in params.items():
        if label not in COUNTRY_SHOCKS:
            continue
        shock = COUNTRY_SHOCKS[label]
        ss_old = steady_state(p)
        ss_new = steady_state(apply_shock(p, shock))
        print(f"  {label}  (shock: {shock['param']} {shock['delta']:+.3f}):")
        for var, name in [("k_tilde", "k̃* (capital per effective worker)"),
                          ("y_tilde", "ỹ* (output per effective worker)"),
                          ("c_tilde", "c̃* (consumption per effective worker)")]:
            old, new = ss_old[var], ss_new[var]
            chg = (new / old - 1) * 100 if old else float("nan")
            print(f"    - {name:<42s}: {old:>10.4f} → {new:>10.4f}  ({chg:+.2f} %)")

    # (f)+(g) Simulation and plots
    print("\n"+"="*80); print("(f)+(g) Simulation 100 periods + plots"); print("="*80)
    sims = {}
    for label in COUNTRY_SHOCKS:
        sims[label] = simulate(params[label], COUNTRY_SHOCKS[label])
        head = sims[label].iloc[[0, T_SHOCK-1, T_SHOCK, T_SHOCK+1, -1]]
        print(f"\n--- {label} (excerpt) ---")
        print(head[["k_tilde", "y_tilde", "c_tilde", "A", "y", "g_y"]].round(4).to_string())
    # task_fg generates individual plots only for SUBJECTS – extend to USA
    # and OPEC manually if desired by extending the SUBJECTS loop in task_fg
    sims_subj = {l: sims[l] for l in SUBJECTS}
    task_fg(params, sims_subj)

    # (h) Comparison plot across all 4 countries
    print("\n"+"="*80); print("(h) Comparison plot across all 4 simulations"); print("="*80)
    task_h_compare(sims)

    # (i) Multi-horizon backtest
    print("\n"+"="*80)
    print("(i) Multi-horizon backtest – 40/30/20/10 years")
    print("="*80)
    print(task_i_backtest(data).to_string())

    # (j) Post-shock backtest – all 4 countries per event
    print("\n"+"="*80)
    print("(j) Post-shock backtest – calibrated on data AFTER the shock")
    print("="*80)
    print(task_j_post_shock_backtest(data).to_string())

    # (k) Rolling MAPE
    print("\n"+"="*80)
    print("(k) Rolling 5-yr MAPE – follow-up shock detection")
    print("="*80)
    task_k_rolling_error(data)
    print("Plot generated: 2k_rolling_error.png")

    print(f"\nDone. Plots in: {OUT_DIR}")


if __name__ == "__main__":
    main()
