# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
base_path = Path(__file__).resolve().parent.parent

# %%
nih = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")

# %% Percap growth
nih.loc[nih['year'] == 2003, 'percap_98_03'] = (nih['funding_dollars_percap'] - nih['funding_dollars_percap_5'])
nih['percap_98_03'] = nih.groupby('CBSA_code')['percap_98_03'].transform('first')
nih.to_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")

# Make Histogram
nih_plot = nih[nih['year'] == 1998]

# Create histogram
fig, ax = plt.subplots()
nih_plot['percap_98_03'].plot.hist(
    bins=30,
    ax=ax,
    color='steelblue',
    edgecolor='black'
)

# Title and labels
ax.set_title("Dollars per Capital Growth")
ax.set_xlabel("Change in Dollars per Capital")
ax.set_ylabel("Number of MSAs")

plt.show()
# %% Share industry
nih['share_health_indus'] = nih['indus_health_services'] / nih['total_pop']
nih['share_educ_indus'] = nih['indus_educ_services'] / nih['total_pop']
nih = nih.drop(columns=['indus_educ_services', 'indus_health_services'])
nih.to_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")


# %%
