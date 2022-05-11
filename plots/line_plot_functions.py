import pandas as pd
import numpy as np
import seaborn as sns


def corr_across_stages(data, reference_stage="embryo", needs_log=True):
    if needs_log:
        data = np.log2(data)
    if reference_stage not in data.columns:
        raise ValueError("Reference stage not found in data")

    stage_corrs = data.corr(method="spearman")[reference_stage]
    return stage_corrs


def create_corr_df_across_stages(
    datasets,  # tuple of {'data': pandas DataFrame, 'species': species name}
    reference_stage="embryo",
):
    correlation_df = pd.DataFrame()
    for item in datasets:
        species = item["species"]
        df = item["data"]
        current_stage_corrs = corr_across_stages(df, reference_stage=reference_stage, needs_log=True)
        current_df = pd.DataFrame(
            {"stage": current_stage_corrs.index.tolist(), "corr_coef": current_stage_corrs.tolist()}
        )
        current_df["species"] = species
        correlation_df = pd.concat([correlation_df, current_df])
    return correlation_df


def pointplot(correlation_df, ax, ylim):
    species = list(set(correlation_df["species"]))
    cp = sns.pointplot(
        x="stage",
        y="corr_coef",
        hue="species",
        data=correlation_df,
        dodge=True,
        join=False,
        hue_order=species,
        ci="sd",
        errwidth=3,
        capsize=0.2,
        ax=ax,
    )
    cp.set_xticklabels(cp.get_xticklabels(), rotation=90)

    ax.set_ylim(ylim)
    ax.set_xlim(-1, correlation_df["stage"].shape[0])

    coloring_embryo_pupae = pd.Series(
        [
            1
            if name.startswith("embryo")
            else 0
            if name.startswith("larva")
            else 1
            if name.startswith("pupa")
            else 0
            for name in correlation_df["stage"].drop_duplicates()
        ]
    )
    cp.pcolorfast(
        cp.get_xlim(), cp.get_ylim(), coloring_embryo_pupae.values[np.newaxis], alpha=0.1, cmap="gray_r"
    )
