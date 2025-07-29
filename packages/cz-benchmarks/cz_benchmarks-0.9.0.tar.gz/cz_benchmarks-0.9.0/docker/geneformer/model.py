import argparse
import shutil
import tempfile
import logging
from pathlib import Path

import numpy as np
import scipy.sparse
from geneformer import EmbExtractor, TranscriptomeTokenizer
from omegaconf import OmegaConf
from datasets import load_from_disk, Sequence, Value

from czbenchmarks.datasets import BaseDataset, DataType, Organism
from czbenchmarks.models.implementations.base_model_implementation import (
    BaseModelImplementation,
)
from czbenchmarks.models.validators import BaseSingleCellValidator
from czbenchmarks.models.types import ModelType
from typing import Set
from czbenchmarks.utils import sync_s3_to_local

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GeneformerValidator(BaseSingleCellValidator):
    """Validation requirements for Geneformer models.

    Validates datasets for use with Geneformer transformer models.
    Requires feature IDs and currently only supports human data.
    """

    available_organisms = [Organism.HUMAN]
    required_obs_keys = []
    required_var_keys = ["feature_id"]
    model_type = ModelType.GENEFORMER

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
            Set containing embedding output type
        """
        return {DataType.EMBEDDING}


class Geneformer(GeneformerValidator, BaseModelImplementation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = OmegaConf.load("/app/config.yaml")

        if self.args.model_variant not in self.config.models:
            logging.error(f"Model {self.args.model_variant} not found in config.")
            raise ValueError(f"Model {self.args.model_variant} not found in config.")

        self.selected_model = self.config.models[self.args.model_variant]
        self.token_config = self.selected_model.token_config

    def create_parser(self):
        parser = argparse.ArgumentParser(
            description="Run Geneformer model on input dataset."
        )
        parser.add_argument("--model-variant", type=str, default="gf_12L_30M")
        return parser

    def get_model_weights_subdir(self, _dataset: BaseDataset) -> str:
        """Get the model weights subdirectory for the selected model."""
        return self.args.model_variant

    def _download_model_weights(self, _dataset: BaseDataset):
        """Download model weights for the selected model."""
        model_uri = self.selected_model.model_uri
        Path(self.model_weights_dir).mkdir(parents=True, exist_ok=True)

        bucket, key = model_uri.split("/")[2], "/".join(model_uri.split("/")[3:])
        sync_s3_to_local(bucket, key, self.model_weights_dir)

        model_weights_dir_parent = Path(self.model_weights_dir).parent

        vocabs_bucket = self.config.geneformer_vocabs_uri.split("/")[2]
        prefix = "/".join(self.config.geneformer_vocabs_uri.split("/")[3:])
        sync_s3_to_local(
            vocabs_bucket, prefix, f"{model_weights_dir_parent}/gene_dictionaries/"
        )

        logging.info(
            f"Downloaded model weights from {model_uri} to {self.model_weights_dir}"
        )

    def _validate_input_data(self, dataset: BaseDataset):
        """Check for NaN values in input data."""
        X = dataset.adata.X
        if scipy.sparse.issparse(X):
            logging.info(
                "Input is a sparse matrix; checking non-zero elements for NaN..."
            )
            if np.isnan(X.data).any():
                logging.warning(
                    f"Input data contains {np.isnan(X.data).sum()} "
                    "NaN values in non-zero elements."
                )
        else:
            if np.isnan(X).any():
                logging.warning("Input data contains NaN values.")
                logging.info(f"NaN locations: {np.where(np.isnan(X))}")

    def _prepare_metadata(self, dataset: BaseDataset):
        """Ensure metadata columns are present and properly formatted."""
        dataset.adata.obs["cell_idx"] = np.arange(len(dataset.adata.obs))

        if "n_counts" not in dataset.adata.obs.columns:
            dataset.adata.obs["n_counts"] = np.asarray(
                dataset.adata.X.sum(axis=1)
            ).flatten()
            if np.isnan(dataset.adata.obs["n_counts"]).any():
                logging.warning("NaN values detected in 'n_counts' calculation.")

        # Remove version numbers from ensembl_id column
        dataset.adata.var["ensembl_id"] = (
            dataset.adata.var["ensembl_id"].str.split(".").str[0]
        )

    def _save_dataset_temp(self, dataset: BaseDataset) -> Path:
        """Save dataset to a temporary file."""
        temp_dir = tempfile.TemporaryDirectory()
        temp_dir = Path(temp_dir.name) / "h5ad_data"
        temp_dir.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            suffix=".h5ad", dir=temp_dir, delete=False
        ) as tmp_file:
            temp_path = Path(tmp_file.name)
            dataset.adata.write_h5ad(temp_path)
        return temp_path

    def _tokenize_dataset(self, temp_path: Path) -> Path:
        """Tokenize dataset and return the tokenized dataset path."""
        dataset_dir = temp_path.parent.parent / "dataset"
        dataset_dir.mkdir(parents=True, exist_ok=True)
        model_weights_dir_parent = Path(self.model_weights_dir).parent
        tk = TranscriptomeTokenizer(
            custom_attr_name_dict={"cell_idx": "cell_idx"},
            nproc=4,
            gene_median_file=str(
                Path(f"{model_weights_dir_parent}/{self.token_config.gene_median_file}")
            ),
            token_dictionary_file=str(
                Path(
                    f"{model_weights_dir_parent}/"
                    f"{self.token_config.token_dictionary_file}"
                )
            ),
            gene_mapping_file=str(
                Path(
                    f"{model_weights_dir_parent}/"
                    f"{self.token_config.ensembl_mapping_file}"
                )
            ),
            special_token=(self.token_config.input_size != 2048),
            model_input_size=self.token_config.input_size,
        )

        tk.tokenize_data(
            str(temp_path.parent),
            str(dataset_dir),
            "tokenized_dataset",
            file_format="h5ad",
        )
        return dataset_dir / "tokenized_dataset.dataset"

    def _load_tokenized_dataset(self, tokenized_dataset_path: Path):
        """Load tokenized dataset from disk."""
        return load_from_disk(str(tokenized_dataset_path))

    def _validate_tokenized_data(self, tokenized_dataset):
        """Ensure tokenized data has expected properties."""
        input_ids = np.array(tokenized_dataset[0]["input_ids"])
        if input_ids.ndim != 1:
            logging.warning(f"Unexpected input_ids shape: {input_ids.shape}")
        logging.info(f"Actual sequence length: {input_ids.shape}")

        # Validate sequence length
        # minimum length of 2 to catch empty or single-token sequences
        if len(input_ids) < 2:
            logging.error(
                f"Tokenized sequences are too short (length={len(input_ids)})."
            )
            raise ValueError(
                f"Tokenized sequences are too short (length={len(input_ids)})."
            )

    def _ensure_correct_dtype(self, tokenized_dataset, tokenized_dataset_path: Path):
        """Ensure tokenized dataset has the correct dtype for `input_ids`."""
        input_ids_dtype = np.array(tokenized_dataset["input_ids"][0]).dtype
        if np.issubdtype(input_ids_dtype, np.floating):
            logging.warning("Detected floating-point input_ids. Converting to int64...")
            new_features = tokenized_dataset.features.copy()
            new_features["input_ids"] = Sequence(Value("int64"))
            tokenized_dataset = tokenized_dataset.cast(new_features)
            tokenized_dataset.save_to_disk(str(tokenized_dataset_path))
            logging.info("Successfully converted input_ids to int64.")

    def _extract_embeddings(self, tokenized_dataset_path: Path, dataset: BaseDataset):
        """Extract embeddings from tokenized dataset."""
        model_weights_dir_parent = Path(self.model_weights_dir).parent
        embex = EmbExtractor(
            model_type="Pretrained",
            emb_layer=-1,
            emb_mode="cell",
            forward_batch_size=32,
            nproc=4,
            token_dictionary_file=str(
                Path(
                    f"{model_weights_dir_parent}/"
                    f"{self.token_config.token_dictionary_file}"
                )
            ),
            max_ncells=None,
            emb_label=["cell_idx"],
        )

        embs = embex.extract_embs(
            model_directory=self.model_weights_dir,
            input_data_file=str(tokenized_dataset_path),
            output_directory=".",
            output_prefix="geneformer",
            cell_state=None,
            output_torch_embs=False,
        )

        # Clean embeddings
        embs = embs.sort_values("cell_idx").drop(columns=["cell_idx"])
        emb_array = embs.to_numpy()
        if np.isnan(emb_array).any():
            logging.warning("Found NaN values in embeddings. Replacing with 0.0")
            emb_array = np.nan_to_num(emb_array, nan=0.0)

        dataset.set_output(self.model_type, DataType.EMBEDDING, emb_array)

    def _cleanup_temp_files(self, temp_path: Path):
        """Remove temporary files and directories."""
        try:
            shutil.rmtree(temp_path.parent.parent, ignore_errors=True)
        finally:
            logging.info("Run complete. Temporary files cleaned up.")

    def run_model(self, dataset: BaseDataset):
        """Run the full Geneformer model pipeline."""
        self._validate_input_data(dataset)
        self._prepare_metadata(dataset)

        temp_path = self._save_dataset_temp(dataset)
        tokenized_dataset_path = self._tokenize_dataset(temp_path)
        tokenized_dataset = self._load_tokenized_dataset(tokenized_dataset_path)

        self._validate_tokenized_data(tokenized_dataset)
        self._ensure_correct_dtype(tokenized_dataset, tokenized_dataset_path)
        self._extract_embeddings(tokenized_dataset_path, dataset)

        self._cleanup_temp_files(temp_path)


if __name__ == "__main__":
    Geneformer().run()
