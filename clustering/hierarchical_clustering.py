"""
Computes hierarchical clustering results based on Spearman correlation coefficient.

Input file is expected to contain expression matrix with genes as row names and samples as column names.

Output file format:
cluster ID (gene or the set of genes) -> other cluster ID (gene or the set of genes) -> distance

Usage:
hierarchical_clustering.py /some/path/expression_rpkm.csv /some/output/path/linkage_data.csv.gz
"""

import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as spc
import sys


expression_filepath = sys.argv[1]
output_filepath = sys.argv[2]

df = np.log2(pd.read_csv(expression_filepath, index_col=0))
df = df.transpose()
corr = df.corr(method="spearman")
pdist = spc.distance.pdist(corr)
linkage = spc.linkage(pdist, method="complete")
pd.DataFrame(linkage).to_csv(output_filepath, compression="gzip", index=False, header=False)
