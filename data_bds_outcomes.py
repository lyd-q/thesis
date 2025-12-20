# %%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent

# %%
bds = pd.read_csv(base_path / "Raw_data/BDS/bds2023_msa.csv")
nih_by_msa = pd.read_csv(base_path / "Data/Census/census_1990/nih_msa_regress.csv")

bds = bds.rename(columns={'msa': 'CBSA_code'})
nih_merge = nih_by_msa.merge(
    bds,
    "left",
    on=['CBSA_code', 'year'],
    indicator=True
)
print(nih_merge['_merge'].value_counts())

nih_merge.to_csv(base_path / "Data/Cleaned/full/nih_msa_bds.csv", index=False)

# %%
# Make 5-year buckets
