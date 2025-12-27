#%%
import pandas as pd
from pathlib import Path
base_path = Path(__file__).resolve().parent.parent   

### Education
################################################
census2000_educ_pop = pd.read_csv(base_path / "Raw_data/Census/census_2000/census2000_educ_pop/DECENNIALDPSF42000.DP2-Data.csv")

meta_census2000_educ_pop = pd.read_csv(base_path / "Raw_data/Census/census_2000/census2000_educ_pop/DECENNIALDPSF42000.DP2-Column-Metadata.csv")

# %%
keep = ["GEO_ID", "NAME", "POPGROUP", "POPGROUP_LABEL", "DP2_C13", "DP2_C19", "DP2_C25", "DP2_C27", "DP2_C28", "DP2_C29"]
census2000_educ_pop = census2000_educ_pop[keep]

rename_dict = {
    "DP2_C13": "pop_over25yrs",
    "DP2_C19": "pct_hs_grad",
    "DP2_C25": "pct_bachelors_degree",
    "DP2_C27": "pct_graduate_degree",
    "DP2_C28": "pct_hs_higher",
    "DP2_C29": "pct_bachelors_higher"
}

census2000_educ_pop = census2000_educ_pop.rename(columns=rename_dict)
# %%
census2000_educ_pop = census2000_educ_pop[census2000_educ_pop['POPGROUP_LABEL'] == 'Total population']
# %%
# remove race categories
census2000_educ_pop = census2000_educ_pop.drop(['POPGROUP', 'POPGROUP_LABEL'], axis=1)

# change percentages into floats
percent_cols = ["pct_hs_grad", "pct_bachelors_degree", "pct_graduate_degree", "pct_hs_higher", "pct_bachelors_higher"]
census2000_educ_pop[percent_cols] = census2000_educ_pop[percent_cols].astype(float)
census2000_educ_pop[percent_cols].dtypes

# %%
census2000_educ_pop["GEO_ID"] = census2000_educ_pop["GEO_ID"].astype(str).str.extract(r"US(\d+)")
#%%
census2000_educ_pop.to_csv(base_path / "Data/Census/census_2000/census2000_educ_pop.csv", index=False)
###########################

### Population and Employment Files
###########################
# Load data
census2000_pop = pd.read_csv(base_path / "Raw_data/Census/census_2000/census2000_pop/DECENNIALDPSF22000.DP1-Data.csv")
census2000_empl = pd.read_csv(base_path / "Raw_data/Census/census_2000/census2000_empl/DECENNIALDPSF42000.DP3-Data.csv")

# %%
keep = ["GEO_ID", "NAME", "POPGROUP", "POPGROUP_LABEL", "DP1_C0"]
census2000_pop = census2000_pop[keep]
census2000_pop = census2000_pop.rename(columns={"DP1_C0" : "population"})
census2000_pop = census2000_pop[census2000_pop['POPGROUP_LABEL'] == 'Total population']
census2000_pop["population"] = census2000_pop["population"].astype(float)
# %%
keep = ["GEO_ID", "NAME", "POPGROUP", "POPGROUP_LABEL", "DP3_C3", "DP3_C112"]

rename_dict = {
    "DP3_C3": "pct_employed",
    "DP3_C112": "median_household_income",
}
census2000_empl = census2000_empl[keep]
census2000_empl = census2000_empl.rename(columns=rename_dict)

# %%
census2000_empl = census2000_empl[census2000_empl['POPGROUP_LABEL'] == 'Total population']
census2000_empl[["pct_employed", "median_household_income"]] = census2000_empl[["pct_employed", "median_household_income"]].astype(float)
# %%
merged_census = census2000_pop.merge(
    census2000_empl,
    how="left",                 # keep all counties from master
    left_on=["GEO_ID", "NAME", "POPGROUP", "POPGROUP_LABEL"],
    right_on=["GEO_ID", "NAME", "POPGROUP", "POPGROUP_LABEL"]
)
# %%
merged_census = merged_census.drop(["POPGROUP", "POPGROUP_LABEL"], axis=1)
merged_census["GEO_ID"] = merged_census["GEO_ID"].astype(str).str.extract(r"US(\d+)")

# %%
merged_census["GEO_ID"] = merged_census["GEO_ID"].astype(int)
# %%
### Merge together
######################################################
census2000_educ_pop = pd.read_csv(base_path / "Data/Census/census_2000/census2000_educ_pop.csv")
census2000_educ_pop = census2000_educ_pop.drop(["pop_over25yrs"], axis=1)

merged_census_all = merged_census.merge(
    census2000_educ_pop,
    how="left",                 # keep all counties from master
    left_on=["GEO_ID", "NAME"],
    right_on=["GEO_ID", "NAME"]
)
merged_census_all.to_csv(base_path / "Data/Census/census_2000/census2000_pop_educ_empl.csv", index=False)

