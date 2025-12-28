# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
base_path = Path(__file__).resolve().parent.parent.parent

# %%
census1990 = pd.read_csv(base_path / "Raw_data/Census/census_1990/census1990.csv")

keep = ["STUSAB", "COUNTY", "COUNTYA", "STATE", "STATEA", "ET1001", "E37006", "E37007", "E4P014", "E4P015", "E4U001", "E01001"]
census1990 = census1990[keep]

# %%
rename_dict = {
    "STUSAB": "state_abbrev",
    "COUNTY": "county_name",
    "COUNTYA": "county_code",
    "STATE": "state_name",
    "STATEA": "state_code",
    "ET1001": "total_pop",
    "E37006": "bachelors_deg",
    "E37007": "graduate_deg",
    "E4P014": "indus_health_services",
    "E4P015": "indus_educ_services",
    "E4U001": "income_household_median",
    "E01001": "income_per_cap"
}
census1990 = census1990.rename(columns=rename_dict)
census1990.head()

#%%
census1990 = census1990.iloc[1:]
census1990[['county_code', 'state_code']] = census1990[['county_code', 'state_code']].astype(str)
census1990.head()
# %%
# make combined county code
census1990['county'] = census1990['state_code'] + census1990['county_code']
census1990['county'] = census1990['county'].astype('string').str.strip().str.zfill(5)
census1990.head()
census1990.to_csv(base_path / "Data/Census/census_1990_v2/census1990.csv")


# Merge with MSAs
county_cbsa = pd.read_csv(base_path / "Data/Crosswalks/county_cbsa_xwalk_2009.csv")
county_cbsa['county_fips'] = county_cbsa['county_fips'].astype('string').str.strip().str.zfill(5)
census1990['county'] = census1990['county'].astype('string').str.strip().str.zfill(5)
census_msa = census1990.merge(
    county_cbsa,
    "left",
    left_on=['county'],
    right_on=['county_fips'],
    indicator=True
)
census_msa['_merge'].value_counts() # this is fine! because all the cbsas are merged in
census_msa = census_msa[census_msa['_merge'] == 'both']
census_msa.to_csv(base_path / "Data/Census/census_1990_v2/census1990_county_msa.csv", index=False)

# %% Now to collapse
census_msa = pd.read_csv(base_path / "Data/Census/census_1990_v2/census1990_county_msa.csv")

# Need to go from county income_per_cap to MSA income_per_cap
census_msa['total_income_imputed'] = census_msa['income_per_cap'] * census_msa['total_pop']

# collapse
census_msa = census_msa.groupby(['CBSA_code'], as_index = False).agg({
    'CBSA_level': 'first',
    'CBSA_title': 'first',
    'state': 'first',
    'total_pop': 'sum',
    'total_income_imputed': 'sum',
    'bachelors_deg': 'sum',
    'graduate_deg': 'sum',
    'indus_health_services': 'sum',
    'indus_educ_services': 'sum',
})


# Divide 'total_income_imputed' by 'total_pop' to get new MSA income_per_cap
census_msa['income_per_cap'] = census_msa['total_income_imputed'] / census_msa['total_pop']

# share college
census_msa['share_college'] = census_msa['bachelors_deg'] / census_msa['total_pop']
# share grad school
census_msa['share_gradschool'] = census_msa['graduate_deg'] / census_msa['total_pop']

census_msa['share_health_indus'] = census_msa['indus_health_services'] / census_msa['total_pop']
census_msa['share_educ_indus'] = census_msa['indus_educ_services'] / census_msa['total_pop']

# log population
census_msa['log_pop'] = np.log(census_msa['total_pop'])

# %%
# keep relevant columns only
census_msa = census_msa[['CBSA_code', 'CBSA_title', 'total_pop',
       'total_income_imputed', 'income_per_cap',
       'share_college', 'share_gradschool', 'share_health_indus',
       'share_educ_indus', 'log_pop']]
census_msa.to_csv(base_path / "Data/Census/census_1990_v2/census1990_msa.csv", index=False)
census_msa.to_csv(base_path / "Data/NIH_v3/census1990_msa.csv", index=False)

# now this is 1990 census info ready to merge with NIH data


