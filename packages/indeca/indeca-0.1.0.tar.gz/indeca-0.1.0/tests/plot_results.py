# %% imports and definition
from ast import literal_eval
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from testing_utils.misc import load_agg_result
from testing_utils.plotting import plot_agg_boxswarm, plot_pipeline_iter

IN_RES_PATH = Path(__file__).parent / "output" / "data" / "agg"
FIG_PATH = Path(__file__).parent / "output" / "figs" / "agg"


# %% plot pipeline realds results
fig_path = FIG_PATH / "pipeline_realds"
fig_path.mkdir(parents=True, exist_ok=True)
res_bin = load_agg_result(IN_RES_PATH / "test_demo_pipeline_realds")
res_cnmf = load_agg_result(IN_RES_PATH / "test_demo_pipeline_realds_cnmf")
if res_bin is not None or res_cnmf is not None:
    result = pd.concat([res_bin, res_cnmf], ignore_index=True)
    result = result.drop_duplicates().fillna("None")
    id_vars = [
        "dsname",
        "ncell",
        "method",
        "use_all",
        "tau_init",
        "unit_id",
        "iter",
        "qthres",
        "test_id",
        "upsamp",
    ]
    val_vals = ["f1", "dhm0", "dhm1"]
    resdf = pd.melt(
        result,
        id_vars=id_vars,
        value_vars=val_vals,
        var_name="metric",
        value_name="value",
    ).drop_duplicates()
    for (ds, ncell), res_sub in resdf.groupby(["dsname", "ncell"]):
        res_sub = res_sub[res_sub["method"] != "gt"].copy()
        res_sub["row_lab"] = res_sub["metric"]
        res_sub["col_lab"] = (
            res_sub["method"]
            + "|"
            + res_sub["use_all"].map(lambda u: "all" if u else "individual")
            + "|"
            + res_sub["tau_init"].map(lambda t: "no_init" if t == "None" else "init")
        )
        col_ord = sorted(res_sub["col_lab"].unique().tolist())
        g = sns.FacetGrid(
            res_sub,
            height=2.5,
            aspect=2,
            row="row_lab",
            col="col_lab",
            sharey="row",
            sharex="col",
            hue="col_lab",
            col_order=col_ord,
            hue_order=col_ord,
            margin_titles=True,
        )
        g.map_dataframe(plot_pipeline_iter, aggregate=False)
        g.add_legend()
        g.figure.savefig(fig_path / "{}-{}.svg".format(ds, ncell))
        plt.close(g.figure)


# %% plot pipeline results
fig_path = FIG_PATH / "pipeline"
fig_path.mkdir(parents=True, exist_ok=True)
result = load_agg_result(IN_RES_PATH / "test_pipeline")
if result is not None:
    result = result.drop_duplicates().rename(columns={"ar_use_all": "use_all"})
    id_vars = [
        "method",
        "use_all",
        "err_weighting",
        "unit_id",
        "iter",
        "qthres",
        "test_id",
        "upsamp",
        "ns_lev",
        "taus",
    ]
    val_vals = ["f1", "dhm0", "dhm1"]
    resdf = pd.melt(
        result,
        id_vars=id_vars,
        value_vars=val_vals,
        var_name="metric",
        value_name="value",
    ).drop_duplicates()
    for (ns_lev, tau, upsamp), res_sub in resdf.groupby(["ns_lev", "taus", "upsamp"]):
        res_gt = res_sub[res_sub["method"] == "gt"].copy()
        dhm0 = res_gt.query("metric == 'dhm0'")["value"].unique().item()
        dhm1 = res_gt.query("metric == 'dhm1'")["value"].unique().item()
        res_sub = res_sub[res_sub["method"] != "gt"].copy()
        res_sub["row_lab"] = res_sub["metric"]
        res_sub["col_lab"] = (
            res_sub["method"]
            + "|"
            + res_sub["err_weighting"].fillna("None")
            + "|"
            + res_sub["use_all"].map(lambda u: "all" if u else "individual")
        )
        col_ord = sorted(res_sub["col_lab"].unique().tolist())
        g = sns.FacetGrid(
            res_sub,
            height=2.5,
            aspect=1.4,
            row="row_lab",
            col="col_lab",
            sharey="row",
            sharex="col",
            hue="col_lab",
            col_order=col_ord,
            hue_order=col_ord,
            margin_titles=True,
        )
        g.map_dataframe(plot_pipeline_iter, dhm0=dhm0, dhm1=dhm1)
        g.add_legend()
        g.figure.savefig(fig_path / "{}-{}-{}.svg".format(ns_lev, tau, upsamp))
        plt.close(g.figure)


# %% plot AR results
def AR_scatter(data, color, x, y, palette, zorder, **kwargs):
    ax = plt.gca()
    data = data.copy()
    res_gt = data[data["method"] == "truth"]
    x_gt = res_gt[x].unique().item()
    y_gt = res_gt[y].unique().item()
    ax.axhline(y_gt, c="gray", ls=":", zorder=0)
    ax.axvline(x_gt, c="gray", ls=":", zorder=0)
    data["method"] = data["method"] + data["unit"].map(
        lambda u: "-all" if u == "all" else ""
    )
    for (mthd, isreal), subdf in data[data["method"] != "truth-all"].groupby(
        ["method", "isreal"], observed=True
    ):
        mk_kws = (
            {"ec": None, "fc": palette[mthd]}
            if isreal
            else {"ec": palette[mthd], "fc": "none"}
        )
        ax.scatter(subdf[x], subdf[y], label=mthd, **mk_kws, **kwargs)


fig_path = FIG_PATH / "demo_solve_fit_h"
fig_path.mkdir(parents=True, exist_ok=True)
result = load_agg_result(IN_RES_PATH / "test_demo_solve_fit_h_num")
if result is not None:
    result = result.rename(columns=lambda c: c.removesuffix("_param"))
    result["taus"] = result["taus"].map(literal_eval)
    cmap = plt.get_cmap("tab10").colors
    palette = {
        "cnmf_smth": cmap[0],
        "cnmf_raw": cmap[1],
        "solve_fit": cmap[2],
        "solve_fit-all": cmap[3],
    }
    for (td, tr), res_sub in result.groupby("taus"):
        g = sns.FacetGrid(res_sub, row="upsamp", col="ns_lev", margin_titles=True)
        g.map_dataframe(
            AR_scatter,
            x="dhm0",
            y="dhm1",
            zorder={"cnmf_smth": 1, "cnmf_raw": 1, "solve_fit": 2, "solve_fit-all": 3},
            palette=palette,
            lw=0.6,
            s=6,
        )
        g.add_legend()
        g.figure.savefig(
            fig_path / "tau({},{}).svg".format(td, tr), bbox_inches="tight"
        )
        plt.close(g.figure)


# %% plot penalty results
def sel_thres(resdf, th_idx, label, met_cols):
    res = resdf.iloc[th_idx, :]
    return pd.DataFrame([{"label": label} | res[met_cols].to_dict()])


def agg_result(
    resdf,
    samp_thres=[0.25, 0.5, 0.75],
    met_cols=["mdist", "f1", "prec", "recall", "scals", "objs"],
):
    res_agg = []
    res_raw = resdf[resdf["group"] == "CNMF"]
    res_nopn = resdf[resdf["group"] == "No Penalty"]
    res_pn = resdf[resdf["group"] == "Penalty"]
    # raw threshold results
    for th in samp_thres:
        th_idx = np.argmin((res_raw["thres"] - th).abs())
        res_agg.append(sel_thres(res_raw, th_idx, "thres{:.2f}".format(th), met_cols))
    # opt threshold with scaling
    opt_idx_scl = res_nopn["opt_idx"].unique().item()
    res_agg.append(sel_thres(res_nopn, opt_idx_scl, "optimal thres", met_cols))
    # opt penalty
    opt_idx_pn = res_pn["opt_idx"].unique().item()
    res_agg.append(
        sel_thres(res_pn, opt_idx_pn, "optimal thres\n /w penalty", met_cols)
    )
    res_agg = pd.concat(res_agg, ignore_index=True)
    return res_agg.set_index("label")


fig_path = FIG_PATH / "demo_solve_penal"
fig_path.mkdir(parents=True, exist_ok=True)
result = load_agg_result(IN_RES_PATH / "test_demo_solve_penal")
if result is not None:
    result = result[~result["y_scaling"]].drop_duplicates()
    grp_dim = ["tau_d", "tau_r", "ns_lev", "upsamp", "rand_seed"]
    res_agg = result.groupby(grp_dim).apply(agg_result).reset_index().drop_duplicates()
    for (td, tr), res_sub in res_agg.groupby(["tau_d", "tau_r"]):
        for met in ["mdist", "f1", "prec", "recall"]:
            g = plot_agg_boxswarm(
                res_sub,
                row="upsamp",
                col="ns_lev",
                x="label",
                y=met,
                facet_kws={"height": 3.5},
            )
            g.tick_params(rotation=45)
            g.figure.savefig(
                fig_path / "tau({},{})-{}.svg".format(td, tr, met), bbox_inches="tight"
            )
            plt.close(g.figure)


# %% plot thresholds
fig_path = FIG_PATH / "solve_thres"
fig_path.mkdir(parents=True, exist_ok=True)
result = load_agg_result(IN_RES_PATH / "test_solve_thres").drop_duplicates()
if result is not None:
    for (td, tr), res_sub in result.groupby(["tau_d", "tau_r"]):
        for met in ["mdist", "f1", "precs", "recall"]:
            g = plot_agg_boxswarm(
                res_sub,
                row="upsamp",
                col="upsamp_y",
                x="ns_lev",
                y=met,
                facet_kws={"margin_titles": True},
            )
            g.figure.savefig(
                fig_path / "tau({},{})-{}.svg".format(td, tr, met), bbox_inches="tight"
            )
            plt.close(g.figure)
