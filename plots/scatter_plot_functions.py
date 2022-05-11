from scipy import stats
import pandas as pd
import numpy as np


LFC_label_ap = "log2 adult/pupae"
LFC_label_le = "log2 larvae/embryo"


def logFC(data, needs_log=True):
    if needs_log:
        data = np.log2(data)
    result = pd.DataFrame(
        {
            LFC_label_ap: data["adults"] - data["pupae"],
            LFC_label_le: data["larvae"] - data["embryo"],
        },
        index=data.index,
    )
    return result


def logFC_scatter_plot(data, ax=None, needs_log=True, log2_threshold=1.5):
    data = logFC(data, needs_log=needs_log)
    corr_coef = stats.spearmanr(data[LFC_label_ap], data[LFC_label_le]).correlation
    if ax:
        data["color"] = (abs(data[LFC_label_le]) > log2_threshold) & (
            abs(data[LFC_label_ap]) > log2_threshold
        )
        rho_label = r"$\rho$ = " + str(round(corr_coef, 2))

        ax.scatter(data[LFC_label_ap], data[LFC_label_le], c=data["color"], rasterized=True)
        ax.set_xlabel(LFC_label_ap, fontsize=15)
        ax.set_ylabel(LFC_label_le, fontsize=15)
        ax.text(0.02, 0.98, rho_label, ha="left", va="top", transform=ax.transAxes, fontsize=15)
        ax.axvline(x=0, color="black", alpha=0.5)
        ax.axhline(y=0, color="black", alpha=0.5)
        ax.set_facecolor("white")
