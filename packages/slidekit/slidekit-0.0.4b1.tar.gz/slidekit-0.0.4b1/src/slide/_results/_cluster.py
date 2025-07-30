"""
slide/_results/_cluster
~~~~~~~~~~~~~~~~~~~~~~~
"""

from typing import Literal, Union

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.ndimage import gaussian_filter1d
from scipy.spatial.distance import pdist
from sklearn.metrics import silhouette_score

from .._log import logger


def cluster_enrichment_profiles(
    enrichment_df: pd.DataFrame,
    method: str = "average",
    metric: str = "jaccard",
    threshold: Union[str, float] = "auto",
    criterion: Literal["distance", "maxclust"] = "distance",
) -> pd.Series:
    """
    Clusters rows (e.g., terms) in the enrichment matrix based on similarity.

    Args:
        enrichment_df (pd.DataFrame): A binary or continuous matrix (terms x windows), where values
            represent presence or strength of enrichment.
        method (str): Linkage method for hierarchical clustering. Default is 'average'.
        metric (str): Distance metric for pairwise comparisons. Default is 'jaccard'.
        threshold (Union[str, float]): Distance threshold or number of clusters.
            If "auto", threshold is set to 0.5 * max linkage distance.
        criterion (Literal["distance", "maxclust"]): Criterion for cluster assignment.

    Returns:
        pd.Series: A Series mapping index labels in `enrichment_df` to assigned cluster IDs.
            All-zero rows are dropped entirely.

    Raises:
        ValueError: If the input DataFrame has fewer than 2 rows, contains non-finite values,
            or if the threshold is invalid.
    """
    # Validate input DataFrame
    if enrichment_df.shape[0] < 2:
        raise ValueError("Clustering requires at least 2 rows.")

    # Fill NaNs and convert to a float array
    mat = enrichment_df.fillna(0).astype(float).to_numpy()
    if (mat == 0).all():
        raise ValueError("All-zero enrichment matrix. Cannot perform clustering.")

    # Drop rows that are entirely zero
    nonzero_mask = mat.any(axis=1)
    if not nonzero_mask.all():
        dropped = enrichment_df.index[~nonzero_mask]
        logger.warning(f"Dropping {len(dropped)} all-zero terms: {list(dropped)}")
        mat = mat[nonzero_mask]
    keep_index = enrichment_df.index[nonzero_mask]

    # Warn if clustering a very large number of rows
    if mat.shape[0] > 1000:
        logger.warning(
            f"Clustering being attempted on {mat.shape[0]} terms — "
            "this may take time. Consider pre-filtering."
        )
    # Ensure all values are finite
    if not np.isfinite(mat).all():
        raise ValueError(
            "Input matrix contains non-finite values (inf or nan), which are not supported."
        )

    # If using Jaccard but data isn't strictly binary, fall back to cosine
    if metric == "jaccard":
        is_binary = np.logical_or(mat == 0, mat == 1).all()
        if not is_binary:
            logger.warning(
                "Input matrix is not strictly 0/1. Switching metric from 'jaccard' to 'cosine'."
            )
            metric = "cosine"

    # If too few rows remain after dropping zeros, assign everyone to one cluster
    if mat.shape[0] < 2:
        return pd.Series(0, index=keep_index)

    # Compute hierarchical linkage
    condensed = pdist(mat, metric=metric)
    Z = linkage(condensed, method=method)

    # Resolve threshold value
    if isinstance(threshold, str) and threshold == "auto":
        if criterion != "distance":
            raise ValueError("Auto threshold only supported for 'distance' criterion.")
        threshold_value = _auto_silhouette_threshold(Z, mat, metric)
    elif isinstance(threshold, (int, float)):
        threshold_value = threshold
    else:
        raise ValueError(f"Invalid threshold value: {threshold}")

    # Assign flat clusters
    labels = fcluster(Z, t=threshold_value, criterion=criterion)

    # Return only for the non-zero rows
    return pd.Series(labels, index=keep_index)


def _auto_silhouette_threshold(
    Z: np.ndarray,
    matrix: np.ndarray,
    metric: str,
    frac_range: np.ndarray = np.linspace(0.2, 0.8, 7),
) -> float:
    """
    Find optimal silhouette threshold from a range of fractions of max linkage height.

    Args:
        Z (np.ndarray): Linkage matrix from hierarchical clustering.
        matrix (np.ndarray): Original data matrix.
        metric (str): Distance metric used for clustering.
        frac_range (np.ndarray): Range of fractions to test for thresholding.

    Returns:
        float: Optimal threshold for clustering.
    """
    best_score = -1
    best_threshold = None
    # Iterate over the fraction range
    for frac in frac_range:
        try:
            # Calculate the threshold based on the fraction of max linkage height
            t_val = frac * np.max(Z[:, 2])
            labels = fcluster(Z, t=t_val, criterion="distance")
            if len(np.unique(labels)) < 2:
                continue
            # Calculate silhouette score and check if it's the best
            score = silhouette_score(matrix, labels, metric=metric)
            if score > best_score:
                best_score = score
                best_threshold = t_val
        except Exception:
            continue

    if best_threshold is None:
        best_threshold = 0.5 * np.max(Z[:, 2])
        logger.warning("Silhouette optimization failed. Falling back to 0.5 * max linkage height.")

    return best_threshold if best_threshold is not None else 0.5 * np.max(Z[:, 2])
