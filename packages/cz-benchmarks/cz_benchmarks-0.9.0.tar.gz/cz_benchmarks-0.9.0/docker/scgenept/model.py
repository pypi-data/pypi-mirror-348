import argparse
import logging
import pathlib
from glob import glob
from typing import Set
import numpy as np
import pandas as pd
import torch
from gears import PertData
from omegaconf import OmegaConf

# utils.data_loading is a function in https://github.com/czi-ai/scGenePT/tree/main
from utils.data_loading import load_trained_scgenept_model

from czbenchmarks.datasets import (
    BaseDataset,
    DataType,
    PerturbationSingleCellDataset,
    Organism,
)
from czbenchmarks.models.implementations.base_model_implementation import (
    BaseModelImplementation,
)
from czbenchmarks.models.validators import BaseSingleCellValidator
from czbenchmarks.models.types import ModelType
from czbenchmarks.utils import download_file_from_remote, sync_s3_to_local

logger = logging.getLogger(__name__)


def load_dataloader(
    dataset_name, data_dir, batch_size, val_batch_size, split="simulation"
):
    pert_data = PertData(f"{data_dir}/")
    pert_data.load(data_name=dataset_name)
    pert_data.prepare_split(split=split, seed=1)
    pert_data.get_dataloader(batch_size=batch_size, test_batch_size=val_batch_size)
    return pert_data


class ScGenePTValidator(BaseSingleCellValidator):
    """Validation requirements for ScGenePT models.

    Validates datasets for use with Single-cell Gene Perturbation Transformer models.
    Requires gene symbols and currently only supports human data.
    Used for perturbation prediction tasks.
    """

    # Override dataset_type in BaseSingleCellValidator
    dataset_type = PerturbationSingleCellDataset
    available_organisms = [Organism.HUMAN]
    required_obs_keys = []
    required_var_keys = ["feature_name"]
    model_type = ModelType.SCGENEPT

    @property
    def inputs(self) -> Set[DataType]:
        """Required input data types.

        Returns:
            Set containing AnnData requirement
        """
        return {DataType.ANNDATA}

    @property
    def outputs(self) -> Set[DataType]:
        """Expected model output types.

        Returns:
            Set containing perturbation predictions and ground truth values for
            evaluating perturbation prediction performance
        """
        return {
            DataType.PERTURBATION_PRED,
            DataType.PERTURBATION_TRUTH,
        }


class ScGenePT(ScGenePTValidator, BaseModelImplementation):
    def create_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--model_variant", type=str, default="scgenept_go_c_gpt_concat"
        )
        parser.add_argument("--gene_pert", type=str, default="CEBPB+ctrl")
        parser.add_argument("--dataset_name", type=str, default="adamson")
        parser.add_argument("--chunk_size", type=int, default=512)
        return parser

    def get_model_weights_subdir(self, _dataset: BaseDataset) -> str:
        config = OmegaConf.load("/app/config.yaml")
        assert (
            f"{self.args.model_variant}__{self.args.dataset_name}" in config.models
        ), (
            f"Model {self.args.model_variant}__{self.args.dataset_name} not found in config"
        )
        return f"{self.args.model_variant}/{self.args.dataset_name}"

    def _download_model_weights(self, _dataset: BaseDataset):
        config = OmegaConf.load("/app/config.yaml")

        # Sync the finetuned model weights from S3 to the local model weights directory
        model_uri = config.models[
            f"{self.args.model_variant}__{self.args.dataset_name}"
        ]

        # Create all parent directories
        pathlib.Path(self.model_weights_dir).mkdir(parents=True, exist_ok=True)

        bucket = model_uri.split("/")[2]
        key = "/".join(model_uri.split("/")[3:])

        sync_s3_to_local(bucket, key, self.model_weights_dir)
        logger.info(
            f"Downloaded model weights from {model_uri} to {self.model_weights_dir}"
        )

        # Copy the vocab.json file from S3 to local model weights directory
        vocab_uri = config.models["vocab_uri"]

        vocab_dir = (
            pathlib.Path(self.model_weights_dir).parent.parent / "pretrained" / "scgpt"
        )
        vocab_dir.mkdir(parents=True, exist_ok=True)
        vocab_file = vocab_dir / "vocab.json"

        download_file_from_remote(vocab_uri, vocab_dir, "vocab.json")
        logger.info(f"Downloaded vocab.json from {vocab_uri} to {vocab_file}")

        # Copy the gene_embeddings directory from S3 to local model weights directory
        gene_embeddings_uri = config.models["gene_embeddings_uri"]
        gene_embeddings_key = "/".join(gene_embeddings_uri.split("/")[3:])
        gene_embeddings_dir = (
            pathlib.Path(self.model_weights_dir).parent.parent / "gene_embeddings"
        )
        gene_embeddings_dir.mkdir(parents=True, exist_ok=True)
        sync_s3_to_local(bucket, gene_embeddings_key, str(gene_embeddings_dir))
        logger.info(
            f"Downloaded gene_embeddings from {gene_embeddings_uri} "
            f"to {gene_embeddings_dir}"
        )

    def run_model(self, dataset: BaseDataset):
        adata = dataset.adata
        adata.var["gene_name"] = adata.var["feature_name"]

        dataset_name = self.args.dataset_name
        batch_size = 64
        eval_batch_size = 64

        pert_data_dir = (
            f"{str(pathlib.Path(self.model_weights_dir).parent.parent)}/data"
        )
        pathlib.Path(pert_data_dir).mkdir(parents=True, exist_ok=True)
        pert_data = load_dataloader(
            dataset_name,
            pert_data_dir,
            batch_size,
            eval_batch_size,
            split="simulation",
        )
        ref_adata = pert_data.adata

        adata = adata[
            :, [i for i in ref_adata.var_names if i in adata.var_names]
        ].copy()
        ref_adata = ref_adata[
            :, [i for i in ref_adata.var_names if i in adata.var_names]
        ].copy()

        model_filename = glob(f"{self.model_weights_dir}/*.pt")[0]
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model, gene_ids = load_trained_scgenept_model(
            ref_adata,
            self.args.model_variant,
            str(pathlib.Path(self.model_weights_dir).parent.parent) + "/",
            model_filename,
            device,
        )

        gene_names = adata.var["gene_name"].to_list()
        gene_pert = self.args.gene_pert
        chunk_size = self.args.chunk_size
        logger.info(f"Predicting perturbations for gene(s) {gene_pert}")
        all_preds = []

        num_chunks = (adata.shape[0] + chunk_size - 1) // chunk_size
        for i in range(num_chunks):
            logger.info(f"Predicting perturbations for chunk {i + 1} of {num_chunks}")
            chunk = adata[i * chunk_size : (i + 1) * chunk_size]
            preds = model.pred_perturb_from_ctrl(
                chunk,
                gene_pert,
                gene_names,
                device,
                gene_ids,
                pool_size=None,
                return_mean=False,
            ).squeeze()
            all_preds.append(preds)

        dataset.set_output(
            self.model_type,
            DataType.PERTURBATION_PRED,
            (
                gene_pert,
                pd.DataFrame(
                    data=np.concatenate(all_preds, axis=0),
                    index=adata.obs_names,
                    columns=adata.var_names.to_list(),
                ),
            ),
        )


if __name__ == "__main__":
    ScGenePT().run()
