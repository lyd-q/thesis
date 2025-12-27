# %%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent

# %%
bds = pd.read_csv(base_path / "Raw_data/BDS/bds2023_msa.csv")
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")

bds = bds.rename(columns={'msa': 'CBSA_code'})
nih_merge = nih.merge(
    bds,
    "left",
    on=['CBSA_code', 'year'],
    indicator=True
)
print(nih_merge['_merge'].value_counts())
nih_merge = nih_merge[nih_merge['_merge'] == 'both']
nih_merge.to_csv(base_path / "Data/Cleaned/full/nih_msa_bds.csv", index=False)

# %% ################## Levels and AVERAGES Version #############################
# Make new dataframe with 5-year buckets AVERAGES
nih_bds = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_bds.csv")
# nih_bds = nih_bds[(nih_bds['year'] > 1992) & (nih_bds['year'] < 2008)]
# 194 unique CBSA titles and codes
nih_buckets0 = (
    nih_bds[nih_bds['year'].between(1993, 1997)]
    .groupby(['CBSA_title', 'CBSA_code', 'CBSA_level', 'CBSA_title_abbrev', 'state'], as_index=False)
    .mean(numeric_only=True)
)
nih_buckets0['bucket'] = 0
# %% Treatment bucket
nih_bds = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_bds.csv")
nih_buckets1 = (
    nih_bds[nih_bds['year'].between(1998, 2003)]
    .groupby(['CBSA_title', 'CBSA_code', 'CBSA_level', 'CBSA_title_abbrev', 'state'], as_index=False)
    .mean(numeric_only=True)
)
nih_buckets1['bucket'] = 1
# %% Post bucket
nih_bds = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_bds.csv")
nih_buckets2 = (
    nih_bds[nih_bds['year'].between(2003, 2008)]
    .groupby(['CBSA_title', 'CBSA_code', 'CBSA_level', 'CBSA_title_abbrev', 'state'], as_index=False)
    .mean(numeric_only=True)
)
nih_buckets2['bucket'] = 2
# %% Append together
nih_buckets = pd.concat([nih_buckets0, nih_buckets1, nih_buckets2], ignore_index=True)
nih_buckets.to_csv(base_path / "Data/Cleaned/full/nih_buckets_levels.csv", index=False)

# %% Check histograms
fig, ax = plt.subplots()
nih_buckets2['estabs_entry_rate'].plot.hist(
    bins=30,
    ax=ax,
    color='steelblue',
    edgecolor='black'
)
# Title and labels
ax.set_title("Establishment entry rate, pre-treatment averages")
ax.set_xlabel("Establishment entry rate")
ax.set_ylabel("Number of MSAs")
plt.show()


# %% ################## Percap Changes Version #############################
nih_bds = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_bds.csv")
# nih_bds = nih_bds[(nih_bds['year'] > 1992) & (nih_bds['year'] < 2009)]
# 194 unique CBSA titles and codes

# Pre-treatment bucket
nih_buckets0 = nih_bds[nih_bds['year'].isin([1993, 1997])]
nih_buckets0_wide = (
    nih_buckets0
    .pivot(index='CBSA_code', columns='year', values='funding_dollars_percap')
)
nih_buckets0_wide['funding_change_0'] = nih_buckets0_wide[1997] - nih_buckets0_wide[1993]
nih_buckets0 = nih_buckets0_wide[['funding_change_0']].reset_index()

nih_buckets = nih_buckets.merge(nih_buckets0, on='CBSA_code', how='inner')

# %% Treatment bucket
nih_buckets1 = nih_bds[nih_bds['year'].isin([1998, 2003])]
nih_buckets1_wide = (
    nih_buckets1
    .pivot(index='CBSA_code', columns='year', values='funding_dollars_percap')
)
nih_buckets1_wide['funding_change_1'] = nih_buckets1_wide[2003] - nih_buckets1_wide[1998]
nih_buckets1 = nih_buckets1_wide[['funding_change_1']].reset_index()

nih_buckets = nih_buckets.merge(nih_buckets1, on='CBSA_code', how='inner')

# %% Post-treatment bucket
nih_buckets2 = nih_bds[nih_bds['year'].isin([2004, 2008])]
nih_buckets2_wide = (
    nih_buckets2
    .pivot(index='CBSA_code', columns='year', values='funding_dollars_percap')
)
nih_buckets2_wide['funding_change_2'] = nih_buckets2_wide[2008] - nih_buckets2_wide[2004]
nih_buckets2 = nih_buckets2_wide[['funding_change_2']].reset_index()

nih_buckets = nih_buckets.merge(nih_buckets2, on='CBSA_code', how='inner')

# %% Save
# nih_buckets = pd.concat([nih_buckets0, nih_buckets1, nih_buckets2], ignore_index=True)
nih_buckets = nih_buckets.dropna(subset=['funding_change_0','funding_change_1','funding_change_2'])
nih_buckets.to_csv(base_path / "Data/Cleaned/full/nih_buckets.csv", index=False)
# 158 CBSAs
# %% Check histograms
fig, ax = plt.subplots()
nih_buckets['funding_change_0'].plot.hist(
    bins=30,
    ax=ax,
    color='steelblue',
    edgecolor='black'
)
# Title and labels
ax.set_title("Establishment entry rate, pre-treatment averages")
ax.set_xlabel("Establishment entry rate")
ax.set_ylabel("Number of MSAs")
plt.show()

# %%
