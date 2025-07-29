from typing import Union
import numpy as np
import pandas as pd


def _safelog(a: np.ndarray) -> np.ndarray:
    """Compute safe log that handles zeros by returning 0.

    Args:
        a: Input array

    Returns:
        Array with log values, with 0s where input was 0
    """
    a = a.astype("float")
    return np.log(a, out=np.zeros_like(a), where=(a != 0))


def nearest_neighbors_hnsw(
    data: np.ndarray,
    expansion_factor: int = 200,
    max_links: int = 48,
    n_neighbors: int = 100,
) -> tuple[np.ndarray, np.ndarray]:
    """Find nearest neighbors using HNSW algorithm.

    Args:
        data: Input data matrix of shape (n_samples, n_features)
        expansion_factor: Size of dynamic candidate list for search
        max_links: Number of bi-directional links created for every new element
        n_neighbors: Number of nearest neighbors to find

    Returns:
        Tuple containing:
            - Indices array of shape (n_samples, n_neighbors)
            - Distances array of shape (n_samples, n_neighbors)
    """
    import hnswlib

    sample_indices = np.arange(data.shape[0])
    index = hnswlib.Index(space="l2", dim=data.shape[1])
    index.init_index(
        max_elements=data.shape[0],
        ef_construction=expansion_factor,
        M=max_links,
    )
    index.add_items(data, sample_indices)
    index.set_ef(expansion_factor)
    neighbor_indices, distances = index.knn_query(data, k=n_neighbors)
    return neighbor_indices, distances


def compute_entropy_per_cell(
    X: np.ndarray, labels: Union[pd.Categorical, pd.Series, np.ndarray]
) -> np.ndarray:
    """Compute entropy of batch labels in local neighborhoods.

    For each cell, finds nearest neighbors and computes entropy of
    batch label distribution in that neighborhood.

    Args:
        X: Cell embedding matrix of shape (n_cells, n_features)
        labels: Series containing batch labels for each cell

    Returns:
        Array of entropy values for each cell, normalized by log of number of batches
    """
    indices, _ = nearest_neighbors_hnsw(X, n_neighbors=200)
    labels = np.array(list(labels))
    unique_batch_labels = np.unique(labels)
    indices_batch = labels[indices]

    label_counts_per_cell = np.vstack(
        [(indices_batch == label).sum(1) for label in unique_batch_labels]
    ).T
    label_counts_per_cell_normed = (
        label_counts_per_cell / label_counts_per_cell.sum(1)[:, None]
    )
    return (
        (-label_counts_per_cell_normed * _safelog(label_counts_per_cell_normed)).sum(1)
        / _safelog(np.array([len(unique_batch_labels)]))
    ).mean()


def jaccard_score(y_true: set[str], y_pred: set[str]):
    """Compute Jaccard similarity between true and predicted values.

    Args:
        y_true: True values
        y_pred: Predicted values
    """
    return len(y_true.intersection(y_pred)) / len(y_true.union(y_pred))


def mean_fold_metric(results_df, metric="accuracy", classifier=None):
    """Compute mean of a metric across folds.

    Args:
        results_df: DataFrame containing cross-validation results. Must have columns:
            - "classifier": Name of the classifier (e.g., "lr", "knn")
            - One of the following metric columns:
                - "accuracy": For accuracy scores
                - "f1": For F1 scores
                - "precision": For precision scores
                - "recall": For recall scores
        metric: Name of metric column to average ("accuracy", "f1", etc.)
        classifier: Optional classifier name to filter results

    Returns:
        Mean value of the metric across folds

    Raises:
        KeyError: If the specified metric column is not present in results_df
    """
    if classifier:
        df = results_df[results_df["classifier"] == classifier]
    else:
        df = results_df
    return df[metric].mean()
