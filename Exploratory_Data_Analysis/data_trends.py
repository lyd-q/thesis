# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent

nih_census = pd.read_csv(base_path / "Data/Cleaned/nih_census.csv")

# %%
# Plot annual averages over cbsa
nih_census_yr_avg = nih_census.groupby('year', as_index=False)[['funding_millions', 'log_funding_millions', 'funding_dollars', 'log_funding_dollars', 'funding_percap', 'log_funding_percap']].mean()

# %%
import seaborn as sns

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
