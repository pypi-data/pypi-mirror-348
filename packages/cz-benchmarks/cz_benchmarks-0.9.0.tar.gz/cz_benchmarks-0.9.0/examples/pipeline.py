"""
Benchmark Pipeline for Single-Cell Models

This script runs a comprehensive benchmarking pipeline for single-cell models
across multiple datasets. It evaluates model performance on three key tasks:
1. Cell clustering (comparing against cell_type labels)
2. Embedding quality assessment
3. Metadata label prediction (for cell_type and sex)

Results for all datasets and tasks are collected and saved to a .pkl file
for further analysis.

Usage:
    python pipeline.py
"""

import logging
import sys
from czbenchmarks.runner import run_inference
from czbenchmarks.tasks import (
    ClusteringTask,
    EmbeddingTask,
    MetadataLabelPredictionTask,
)
from czbenchmarks.datasets.utils import load_dataset, list_available_datasets
import pickle

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    all_datasets = list_available_datasets()

    all_results = {}

    for dataset_name in all_datasets:
        logger.info(dataset_name)
        if not dataset_name.startswith("tsv2_"):
            continue

        dataset = load_dataset(dataset_name)

        for model_name in ["SCVI", "SCGPT"]:
            dataset = run_inference(model_name, dataset)

        task = ClusteringTask(label_key="cell_type")
        task.set_baseline(dataset)
        clustering_results = task.run(dataset)

        task = EmbeddingTask(label_key="cell_type")
        task.set_baseline(dataset)
        embedding_results = task.run(dataset)

        task = MetadataLabelPredictionTask(label_key="cell_type")
        task.set_baseline(dataset)
        metadata_results_cell_type = task.run(dataset)

        task = MetadataLabelPredictionTask(label_key="sex")
        task.set_baseline(dataset)
        metadata_results_sex = task.run(dataset)

        all_results[dataset_name] = {
            "clustering_results": clustering_results,
            "embedding_results": embedding_results,
            "metadata_results_cell_type": metadata_results_cell_type,
            "metadata_results_sex": metadata_results_sex,
        }

        pickle.dump(all_results, open("all_results.pkl", "wb"))
