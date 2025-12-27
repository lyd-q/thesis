#%%
import pandas as pd
import numpy as np
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent

# %%
census2000 = pd.read_csv(base_path / "Data/Census/census_2000/census2000_pop_educ_empl.csv")
county_cbsa_xwalk = pd.read_stata(base_path / "Data/Crosswalks/county_cbsa_xwalk.dta")

# %%
census2000["GEO_ID"] = census2000["GEO_ID"].astype(str).str.strip().str.zfill(5)
county_cbsa_xwalk["county_fips"] = county_cbsa_xwalk["county_fips"].astype(str).str.strip().str.zfill(5)
census2000.to_csv(base_path / "Data/Census/census_2000/census2000_check.csv", index=False)
county_cbsa_xwalk.to_csv(base_path / "Data/Census/census_2000/county_cbsa_xwalk_check.csv", index=False)

# %%
merged = census2000.merge(
    county_cbsa_xwalk,
    how="left",
    left_on="GEO_ID",
    right_on="county_fips",
    indicator=True
)
merged["_merge"].value_counts()

# %%
merged.to_csv(base_path / "Data/Census/census_2000/census2000_merged.csv", index=False)

#%%
percent_cols = [
    "pct_hs_grad",
    "pct_bachelors_degree",
    "pct_graduate_degree",
    "pct_hs_higher",
    "pct_bachelors_higher",
    "pct_employed"
]

absolute_cols = ["population", "median_household_income"]

merged_grouped = (
    merged.groupby(["CBSA_code", "CBSA_title"], as_index=False)
          .agg({col: "mean" for col in percent_cols} | {col: "sum" for col in absolute_cols})
          .round(2)
)
# %%
# percent_cols = ["pct_hs_grad", "pct_bachelors_degree", "pct_graduate_degree", "pct_hs_higher", "pct_bachelors_higher", "pct_employed"]
# merged = merged.groupby(['CBSA_code', 'CBSA_title'], as_index=False)[percent_cols].mean().round(2)
# merged.to_csv(base_path / "Data/Census/census_2000/census2000_cbsa.csv", index=False)
# %%
# now merge with NIH funding data on MSA level

nih_msa = pd.read_stata(base_path / "Data/nih_msa_collapsed_adjusted.dta")
merged_nih = nih_msa.merge(
    merged_grouped,
    how="left",
    left_on="CBSA_code",
    right_on="CBSA_code",
    indicator=True
)
merged_nih["_merge"].value_counts()
merged_nih = merged_nih.drop(columns="_merge")
(merged_nih["CBSA_title_x"] == merged_nih["CBSA_title_y"]).all()
merged_nih["CBSA_title"] = merged_nih["CBSA_title_x"]
merged_nih = merged_nih.drop(columns=["CBSA_title_x", "CBSA_title_y"])
merged_nih.to_csv(base_path / "Data/Cleaned/nih_census.csv", index=False)

# %%
########################################################
### Get per-capita funding too
nih_census2000 = pd.read_csv(base_path / "Data/Cleaned/nih_census.csv")

# Funding is in millions, change it to dollars
nih_census2000 = nih_census2000.rename(columns={"FUNDING": "funding_millions", "log_FUNDING": "log_funding_millions"})
nih_census2000["funding_dollars"] = nih_census2000["funding_millions"] * 1000000
nih_census2000["log_funding_dollars"] = np.log(nih_census2000["funding_dollars"])

# %%
# Take per-capita measures of funding dollars
nih_census2000['funding_percap'] = nih_census2000['funding_dollars']/nih_census2000['population']
#%%
nih_census2000['log_funding_percap'] = np.log(nih_census2000['funding_percap'] + 1)
nih_census2000.to_csv(base_path / "Data/Cleaned/nih_census.csv", index=False)
# %%
# Check average funding over years
nih_avg = nih_census2000.groupby(['CBSA_code', 'CBSA_title'], as_index=False).mean().round(2)
nih_avg.to_csv(base_path / "Data/Working/nih_avg.csv", index=False)
# %%
######################################
# Make descriptive plots on 1998 and 2003
