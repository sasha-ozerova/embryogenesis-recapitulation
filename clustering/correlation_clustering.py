"""
Separates gene profiles into clusters using predefined default profiles as references.

Input file should contain expected profiles.
Output file consists of
gene name -> cluster ID -> correlation coefficint with the reference profile
Usage:
correlation_clustering.py /some/path/expression_matrix.csv /some/path/clusters.csv /output/path/clusters.csv
"""

import pandas as pd
import numpy as np
import sys


expression_filepath = sys.argv[1]
expected_clusters = sys.argv[2]
output_filepath = sys.argv[3]

clusters = pd.read_csv(expected_clusters)
df = np.log2(pd.read_csv(expression_filepath, index_col=0))
clusters_annotation = []
for name, row in df.iterrows():
    current_corrs = np.corrcoef(row, clusters)[0][1:]
    best_cluster = list(current_corrs).index(max(current_corrs))
    clusters_annotation.append([name, best_cluster, max(current_corrs)])

clustering_results = pd.DataFrame(clusters_annotation, columns=["gene", "cluster", "corrcoef"])
clustering_results.to_csv(output_filepath, index=False)
