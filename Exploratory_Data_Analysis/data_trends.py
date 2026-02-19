# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import seaborn as sns


base_path = Path(__file__).resolve().parent.parent.parent

nih = pd.read_stata(base_path / "Data/NIH_v4/nih_funding_use.dta")
sns.scatterplot(
    data=nih.groupby('year', as_index=False)['funding_pc'].mean(),
    x='year',
    y='funding_pc'
)

#%%
nih_annual = (
    nih
    .groupby("year", as_index=False)["funding_pc"]
    .mean()
)

plt.figure(figsize=(8,5))
plt.plot(nih_annual["year"], nih_annual["funding_pc"])
plt.xlabel("Year")
plt.ylabel("Average Funding per Capita")
plt.title("Average NIH Funding per Capita Across MSAs")
plt.tight_layout()
plt.show()
#%%
# collapsed version - annual averages
nih_msa_avg = 
nih.hist(x='funding_pc')

#%% Cross section in growth

# %%
# Plot annual averages over cbsa
nih_census_yr_avg = nih_census.groupby('year', as_index=False)[['funding_millions', 'log_funding_millions', 'funding_dollars', 'log_funding_dollars', 'funding_percap', 'log_funding_percap']].mean()

# %%

# annual averages over MSAs
sns.lineplot(nih_census_yr_avg, x="year", y="funding_percap", marker="o")
plt.title("Average NIH Funding per Capita by Year")
plt.xlabel("Year")
plt.ylabel("Average Funding per Capita")
plt.savefig(base_path / "Outputs/Descriptive/avg_funding_percap.png")
plt.show()
# sns.histplot(nih_census_yr_avg["funding_percap"], 
#     bins=30, 
#     stat="count",
#     kde=False,
#     alpha=0.6,
#     element="step")
# plt.title("Average NIH Funding per Capita")
# plt.xlabel("Funding per Capita")
# plt.ylabel("Density")
# plt.show()


# %%
"`path'/Data/NIH_v3/nih_cbsa_msa_funding.dta"