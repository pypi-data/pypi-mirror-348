from dataclasses import dataclass
from enum import Enum
from typing import Type, Union, Dict
import numpy as np
import pandas as pd
import anndata as ad
from omegaconf import OmegaConf


class Organism(Enum):
    HUMAN = ("homo_sapiens", "ENSG")
    MOUSE = ("mus_musculus", "ENSMUSG")
    TROPICAL_CLAWED_FROG = ("xenopus_tropicalis", "ENSXETG")
    AFRICAN_CLAWED_FROG = ("xenopus_laevis", "ENSXLAG")
    ZEBRAFISH = ("danio_rerio", "ENSDARG")
    MOUSE_LEMUR = ("microcebus_murinus", "ENSMICG")
    WILD_BOAR = ("sus_scrofa", "ENSSSCG")
    CRAB_EATING_MACAQUE = ("macaca_fascicularis", "ENSMFAG")
    RHESUS_MACAQUE = ("macaca_mulatta", "ENSMMUG")
    PLATYPUS = ("ornithorhynchus_anatinus", "ENSOANG")
    OPOSSUM = ("monodelphis_domestica", "ENSMODG")
    GORILLA = ("gorilla_gorilla", "ENSGGOG")
    CHIMPANZEE = ("pan_troglodytes", "ENSPTRG")
    MARMOSET = ("callithrix_jacchus", "ENSCJAG")
    CHICKEN = ("gallus_gallus", "ENSGALG")
    RABBIT = ("oryctolagus_cuniculus", "ENSOCUG")
    FRUIT_FLY = ("drosophila_melanogaster", "FBgn")
    RAT = ("rattus_norvegicus", "ENSRNOG")
    NAKED_MOLE_RAT = ("heterocephalus_glaber", "ENSHGLG")
    CAENORHABDITIS_ELEGANS = ("caenorhabditis_elegans", "WBGene")
    YEAST = ("saccharomyces_cerevisiae", "")
    MALARIA_PARASITE = ("plasmodium_falciparum", "PF3D7")
    SEA_LAMPREY = ("petromyzon_marinus", "ENSPMAG")
    FRESHWATER_SPONGE = ("spongilla_lacustris", "ENSLPGG")
    CORAL = ("stylophora_pistillata", "LOC")
    SEA_URCHIN = ("lytechinus_variegatus", "")  # Mixed prefixes: LOC and GeneID

    # Todo: add other organisms
    def __init__(self, name: str, prefix: str):
        self._value_ = (name, prefix)  # This is handled automatically by Enum

    def __str__(self):
        return self.value[0]  # Access the name from the tuple

    def __repr__(self):
        return self.value[0]  # Access the name from the tuple

    @property
    def name(self):
        return self.value[0]

    @property
    def prefix(self):
        return self.value[1]


# Register Organism resolver
if not OmegaConf.has_resolver("organism"):  # Required for dataset test cases
    OmegaConf.register_new_resolver("organism", lambda name: getattr(Organism, name))


@dataclass(frozen=True)
class DataTypeSpec:
    """Specification for a data type in the system"""

    name: str
    dtype: Type
    description: str
    is_input: bool = True


class DataType(Enum):
    # Input types
    METADATA = DataTypeSpec(
        name="metadata", dtype=pd.DataFrame, description="Sample metadata"
    )
    ANNDATA = DataTypeSpec(
        name="anndata",
        dtype=ad.AnnData,
        description="AnnData object containing expression data",
    )

    ORGANISM = DataTypeSpec(
        name="organism",
        dtype=Organism,
        description="Organism type (e.g. human, mouse)",
    )

    # Output types
    EMBEDDING = DataTypeSpec(
        name="embedding",
        dtype=np.ndarray,
        description="Learned cell embeddings",
        is_input=False,
    )

    CONDITION_KEY = DataTypeSpec(
        name="condition_key",
        dtype=str,
        description="Condition key for perturbation data",
        is_input=True,
    )

    SPLIT_KEY = DataTypeSpec(
        name="split_key",
        dtype=str,
        description="Train, test, val, split key for perturbation data",
        is_input=True,
    )

    PERTURBATION_PRED = DataTypeSpec(
        name="perturbation",
        dtype=tuple[str, pd.DataFrame],
        description="Tuple of (condition_str, Predicted perturbation effects)",
        is_input=False,
    )
    PERTURBATION_TRUTH = DataTypeSpec(
        name="perturbation_truth",
        dtype=Dict[str, pd.DataFrame],
        description="Truth perturbation data",
        is_input=True,
    )

    @property
    def spec(self) -> DataTypeSpec:
        return self.value

    @property
    def dtype(self) -> Type:
        return self.value.dtype

    @property
    def description(self) -> str:
        return self.value.description

    @property
    def is_input(self) -> bool:
        return self.value.is_input

    @property
    def is_output(self) -> bool:
        return not self.value.is_input

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return super().__eq__(other)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


DataValue = Union[pd.DataFrame, ad.AnnData, np.ndarray, Organism]
