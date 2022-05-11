from matplotlib.colors import LogNorm, PowerNorm
import numpy as np
import seaborn as sns
import random


def sampling_pvalues(data, target_row_names, species_name="", prefix=""):
    submatrix = data.loc[target_row_names]
    submatrix_corr = submatrix.corr(method="spearman")
    random_dfs_corr = []
    for _ in range(100):
        genes = random.sample(data.index.tolist(), submatrix.shape[0])
        random_df = data.loc[genes]
        random_df = random_df.corr(method="spearman")
        random_dfs_corr.append(random_df)
    result = []
    for stage1 in submatrix_corr.columns.tolist():
        current_row = []
        for stage2 in submatrix_corr.index.tolist():
            real_value = submatrix_corr.loc[stage2, stage1]
            random_values = [df.loc[stage2, stage1] for df in random_dfs_corr]
            p_value = len([value for value in random_values if value >= real_value]) / len(random_values)
            current_row.append(p_value)
        result.append(current_row)

    return np.array(result)


def correlation_map(
    data,  # correlation matrix
    ax=None,
    value_type="power",  # how to scale color bar
    max_value=1,
    min_value=0,
    cbar=True,  # display color bar or not
    cmap="coolwarm",  # color map
    center=0,  # value of the center of the color bar
):
    if value_type == "power":
        return sns.heatmap(
            data,
            norm=PowerNorm(2),
            vmin=0.01,
            vmax=1,
            center=center,
            cbar_kws=dict(ticks=[0, 0.5, 0.75, 1]),
            cmap=cmap,
            cbar=cbar,
            ax=ax,
        )
    elif value_type == "log":
        return sns.heatmap(
            data,
            norm=LogNorm(vmin=0.01, vmax=1),
            vmin=0.01,
            vmax=1,
            cbar_kws=dict(ticks=[0.01, 0.1, 1]),
            cmap=cmap,
            cbar=cbar,
            ax=ax,
            center=center,
        )
    elif value_type == "linear":
        return sns.heatmap(
            data,
            vmin=min_value,
            vmax=max_value,
            cmap=cmap,
            cbar=cbar,
            ax=ax,
            center=center,
        )
    else:
        raise ValueError("Unknown data type")
