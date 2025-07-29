import logging

import anndata as ad
import pandas as pd
from scipy import sparse

logger = logging.getLogger(__name__)


def filter_adata_by_hvg(adata: ad.AnnData, hvg_path: str) -> ad.AnnData:
    """Filter adata by HVGs."""
    # Create a full copy at the start to avoid view issues
    adata = adata.copy()

    hvg = pd.read_csv(hvg_path)
    adata.var_names = adata.var_names.astype(str)
    hvg["feature_id"] = hvg["feature_id"].astype(str)

    # Filter adata by only genes that are present in hvg.feature_id
    adata_filtered = adata[:, adata.var_names.isin(hvg.feature_id)].copy()

    # Check which features are missing from hvg.feature_id
    missing_features = set(hvg.feature_id) - set(adata.var_names)

    if missing_features:
        logger.info(
            f"WARNING:{len(missing_features)} HVGs are not present in the"
            " AnnData object"
        )
        # Create an empty adata with missing genes
        # as all zeros make array sparse
        missing_var = pd.DataFrame({"feature_id": list(missing_features)})
        missing_var["feature_name"] = missing_var["feature_id"]
        missing_var.set_index("feature_name", inplace=True)
        missing_X = sparse.csr_matrix((adata.n_obs, len(missing_features)))
        # Initialize AnnData with minimal metadata
        adata_missing = ad.AnnData(
            X=missing_X,
            var=missing_var,
            obs=adata_filtered.obs.copy(),  # Make sure to copy the obs
        )

        # Delete varm from adata_filtered to avoid AnnData bug
        # concat does not work with outer join for varm matrices.
        del adata_filtered.varm

        # Concatenate the filtered adata with the missing genes adata
        adata_concat = ad.concat(
            [adata_filtered, adata_missing],
            axis=1,
            join="outer",
            merge="first",
        )

    else:
        adata_concat = adata_filtered

    # Create a new AnnData object instead of a view
    assert hvg.feature_id.isin(adata_concat.var_names).all()
    adata_reordered = adata_concat[:, hvg.feature_id].copy()
    return adata_reordered
