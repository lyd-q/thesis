# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
base_path = Path(__file__).resolve().parent.parent

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
# %%
nih_counties = pd.read_stata(base_path / "Data/nih_counties.dta")
nih_counties = nih_counties.dropna(subset=['county'])
nih_counties['county'] = nih_counties['county'].astype('int').astype('string').str.strip().str.zfill(5)

# change Miami manually
nih_counties.loc[nih_counties['county_name'] == "Miami-Dade", 'county'] = '13083'
#%%
nih_counties['NIHDEPTCOMBININGNAME'].replace('', pd.NA)
nih_counties['NIHDEPTCOMBINNINGNAME'].replace('', pd.NA)
nih_counties['NIHDEPTCOMBININGNAME'] = nih_counties['NIHDEPTCOMBININGNAME'].fillna(nih_counties['NIHDEPTCOMBINNINGNAME'])

nih_counties.to_csv(base_path / "Data/Cleaned/nih_counties.csv", index=False)
#%%
############### Collapsing by counties ##############################
# Collapse NIH counties first, then merge in the census characteristics
# Counties
nih_counties = pd.read_csv(base_path / "Data/Cleaned/nih_counties.csv", low_memory=False)
nih_by_counties = nih_counties.groupby(['county', 'year'], as_index = False)['FUNDING'].agg('sum')
nih_by_counties.to_csv(base_path / "Data/Cleaned/nih_by_counties.csv", index=False)

all_counties = nih_by_counties['county'].unique()
all_years = nih_by_counties['year'].unique()

full_index = pd.MultiIndex.from_product(
    [all_counties, all_years],
    names=['county', 'year']
)
nih_by_counties_full = (
    nih_by_counties.set_index(['county', 'year'])
      .reindex(full_index)
      .reset_index()
)
nih_by_counties_full['FUNDING'] = nih_by_counties_full['FUNDING'].fillna(0)
nih_by_counties_full.to_csv(base_path / "Data/Cleaned/nih_by_counties.csv", index=False)


############### Following code is for "by counties" ##############################
#%%
nih_by_counties = pd.read_csv(base_path / "Data/Cleaned/nih_by_counties.csv")
nih_by_counties['county'] = nih_by_counties_full['county'].astype('string').str.strip().str.zfill(5)
nih_counties1990 = nih_by_counties.merge(
    census1990,
    "left",             
    left_on=['county'],
    right_on=['county'],
    indicator=True
)
nih_counties1990['_merge'].value_counts()
# state fips 66 and 72 are Guam and Puerto Rico
#%%
nih_counties1990.to_csv(base_path / "Data/Census/census_1990/nih_counties1990.csv", index=False)

#%%
################ Prepare census variables ############################
nih_counties1990 = nih_counties1990[nih_counties1990['_merge'] == 'both']
nih_counties1990 = nih_counties1990.rename(columns={'FUNDING': 'funding_dollars'})

# Census variables
# Share bachelors degree
# bachelors count is out of population 18 or older
nih_counties1990[['bachelors_deg', 'total_pop']] = nih_counties1990[['bachelors_deg', 'total_pop']].astype(int)
nih_counties1990['share_college'] = nih_counties1990['bachelors_deg'] / nih_counties1990['total_pop']
# Would be more accurate if I can divide this by total population over 18 years, but I think this is ok for now

nih_counties1990['log_pop'] = np.log(nih_counties1990['total_pop'])
nih_counties1990.to_csv(base_path / "Data/Census/census_1990/nih_counties1990.csv", index=False)

# %%
################ Merge county to CBSAs ############################
# using 2003 crosswalk
nih_counties1990 = pd.read_csv(base_path / "Data/Census/census_1990/nih_counties1990.csv")
county_cbsa = pd.read_csv(base_path / "Data/Crosswalks/county_cbsa_xwalk_2003.csv")
county_cbsa['county_fips'] = county_cbsa['county_fips'].astype('string').str.strip().str.zfill(5)
nih_counties1990['county'] = nih_counties1990['county'].astype('string').str.strip().str.zfill(5)
nih_msa = nih_counties1990.merge(
    county_cbsa,
    "left",
    left_on=['county'],
    right_on=['county_fips']
)
nih_msa['_merge'].value_counts()
#nih_msa.to_csv(base_path / "Data/Census/census_1990/nih_msa1990_justmerged.csv", index=False)

#%%
# Collapse by MSA
nih_msa = pd.read_csv(base_path / "Data/Census/census_1990/nih_msa1990_justmerged.csv")

# need to think a bit about the census vars
# income_per_cap
nih_msa['total_income_imputed'] = nih_msa['income_per_cap'] * nih_msa['total_pop']

nih_by_msa = nih_msa.groupby(['CBSA_code', 'year'], as_index = False).agg({
    'CBSA_level': 'first',
    'CBSA_title': 'first',
    'state': 'first',
    'funding_dollars': 'sum',
    'total_pop': 'sum',
    'total_income_imputed': 'sum',
    'bachelors_deg': 'sum',
    'graduate_deg': 'sum',
    'indus_health_services': 'sum',
    'indus_educ_services': 'sum',
})

# need to divide 'total_income_imputed' by 'total_pop' to get new MSA income_per_cap
nih_by_msa['income_per_cap'] = nih_by_msa['total_income_imputed'] / nih_by_msa['total_pop']
# share college
nih_by_msa['share_college'] = nih_by_msa['bachelors_deg'] / nih_by_msa['total_pop']
# share grad school
nih_by_msa['share_gradschool'] = nih_by_msa['graduate_deg'] / nih_by_msa['total_pop']

# NIH funding variables
nih_by_msa = nih_by_msa.dropna(subset=['funding_dollars']) 
# can drop these now that census values have been aggregated
nih_by_msa = nih_by_msa[nih_by_msa['funding_dollars'] != 0]
nih_by_msa['funding_dollars_percap'] = nih_by_msa['funding_dollars'] / nih_by_msa['total_pop'] 
nih_by_msa['funding_log_dollars'] = np.log(nih_by_msa['funding_dollars'])
nih_by_msa['funding_log_percap'] = np.log(nih_by_msa['funding_dollars_percap'])

nih_by_msa.to_csv(base_path / "Data/Census/census_1990/nih_msa1990.csv", index=False)
#%%
nih_by_msa = pd.read_csv(base_path / "Data/Census/census_1990/nih_msa1990.csv")

#%%
nih_by_msa = nih_by_msa[nih_by_msa['CBSA_level'] == 'Metropolitan Statistical Area'].reset_index(drop=True)
nih_by_msa['CBSA_code'].nunique()
# 322 MSAs

nih_by_msa = nih_by_msa.rename(columns={'funding_log_dollars': 'funding_log'})
# Create lags
for lag in range(1, 6):
    nih_by_msa['funding_dollars'+f"_{lag}"] = nih_by_msa.groupby('CBSA_code')['funding_dollars'].shift(lag)
    nih_by_msa['funding_dollars_percap'+f"_{lag}"] = nih_by_msa.groupby('CBSA_code')['funding_dollars_percap'].shift(lag)
    nih_by_msa['funding_log'+f"_{lag}"] = nih_by_msa.groupby('CBSA_code')['funding_log'].shift(lag)
    nih_by_msa['funding_log_percap'+f"_{lag}"] = nih_by_msa.groupby('CBSA_code')['funding_log_percap'].shift(lag)

nih_by_msa.to_csv(base_path / "Data/Census/census_1990/nih_msa_lags1990.csv", index=False)

#%%
# create log(f2003) - log(f1998) for LHS
nih_by_msa = pd.read_csv(base_path / "Data/Census/census_1990/nih_msa_lags1990.csv")
# Make sure that we have 1998 and 2003 observations
nih_by_msa = nih_by_msa[(nih_by_msa['year'] != 2003) | nih_by_msa['funding_dollars_5'].notna()]
# 204 observations for 2003

nih_by_msa.loc[nih_by_msa['year'] == 2003, 'log_98_03'] = (nih_by_msa['funding_log'] - nih_by_msa['funding_log_5'])
nih_by_msa.loc[nih_by_msa['year'] == 2003, 'log_percap_98_03'] = (nih_by_msa['funding_log_percap'] - nih_by_msa['funding_log_percap_5'])

nih_by_msa['log_98_03'] = nih_by_msa.groupby('CBSA_code')['log_98_03'].transform('first')
# check that percap growth rate is the same
nih_by_msa['log_percap_98_03'] = nih_by_msa.groupby('CBSA_code')['log_percap_98_03'].transform('first')
nih_by_msa.to_csv(base_path / "Data/Census/census_1990/nih_msa_regress.csv", index=False)
# yes, the ones that have growth rate observations are the same


#%%
############################## Collapsing by categories ###################################
##### NEED TO CLEAN MORE AND THINK
# Counties and departments
nih_by_dept = nih_counties.groupby(['county', 'year', 'NIHDEPTCOMBINNINGNAME'], as_index = False)['FUNDING'].agg('sum')
nih_by_dept.to_csv(base_path / "Data/Cleaned/nih_by_dept.csv", index=False)
nih_by_dept.head()

#%%
########### Counties and funding mechanism ##########
nih_counties = pd.read_csv(base_path / "Data/Cleaned/nih_counties.csv", low_memory=False)
nih_by_mech = nih_counties.groupby(['county', 'year', 'FUNDINGMECHANISM'], as_index = False)['FUNDING'].agg('sum')
nih_by_mech.to_csv(base_path / "Data/Cleaned/nih_by_mech.csv", index=False)
nih_by_mech.head()

all_counties = nih_by_mech['county'].unique()
all_years = nih_by_mech['year'].unique()
all_mech = nih_by_mech['FUNDINGMECHANISM'].unique()

full_index = pd.MultiIndex.from_product(
    [all_counties, all_years, all_mech],
    names=['county', 'year', 'FUNDINGMECHANISM']
)
nih_by_mech_full = (
    nih_by_mech.set_index(['county', 'year', 'FUNDINGMECHANISM'])
      .reindex(full_index)
      .reset_index()
)
nih_by_mech_full['FUNDING'] = nih_by_mech_full['FUNDING'].fillna(0)
nih_by_mech_full = nih_by_mech_full.rename(columns={'FUNDING': 'FUNDING_mech'})


# The different funding mechanisms:
# RPGs - SBIR/STTR
# R&D Contracts
# RPGs - Non SBIR/STTR
# Other Research-Related
# NULL
# Research Grants
# Training - Institutional
# Research Centers
# Construction
# Training - Individual
# Other

# For each county and year, calculate share of total funding that is in each
# Merge in county-year total funding
nih_by_counties = pd.read_csv(base_path / "Data/Cleaned/nih_by_counties.csv")
nih_by_mech_full = nih_by_mech_full.merge(
    nih_by_counties,
    "left",
    on=['county', 'year']
)
nih_by_mech_full.to_csv(base_path / "Data/Cleaned/funding_mech/nih_by_mech.csv", index=False)
nih_by_mech_full['FUNDING'] = nih_by_mech_full['FUNDING'].replace(0, 1)
nih_by_mech_full['share_mech'] = nih_by_mech_full['FUNDING_mech'] / nih_by_mech_full['FUNDING']

#%%
# append a full share sum
nih_mech_total = nih_by_mech_full.groupby(['county', 'year'])['share_mech'].sum().reset_index()

# pivot into each row is by county and year
nih_share_mech = nih_by_mech_full.pivot(index=['county', 'year'], columns='FUNDINGMECHANISM', values='share_mech').reset_index()
nih_share_mech['total_share_mech'] = nih_mech_total['share_mech']
nih_share_mech.columns.name = None
nih_share_mech.to_csv(base_path / "Data/Cleaned/funding_mech/nih_share_mech.csv", index=False)

# Append to county
nih_by_county = pd.read_csv(base_path / "Data/Census/census_1990/nih_counties1990.csv")
nih_by_county = nih_by_county.drop(columns=['_merge'])
nih_by_county['county'] = nih_by_county['county'].astype('string').str.strip().str.zfill(5)
nih_by_counties_merge = nih_by_county.merge(
    nih_share_mech,
    "left",
    on=['county', 'year'],
    indicator=True
)
print(nih_by_counties_merge['_merge'].value_counts())
nih_by_counties_merge = nih_by_counties_merge.drop(columns=['_merge'])
nih_by_counties_merge.to_csv(base_path / "Data/Cleaned/full/nih_county.csv", index=False)
# %%
############## Doing this by MSA requires summing funding across MSAs and then taking share
# FIX THE MSA collapse
county_cbsa = pd.read_csv(base_path / "Data/Crosswalks/county_cbsa_xwalk_2003.csv")
county_cbsa['county_fips'] = county_cbsa['county_fips'].astype('string').str.strip().str.zfill(5)
nih_by_mech_full['county'] = nih_by_mech_full['county'].astype('string').str.strip().str.zfill(5)
nih_mech_msa = nih_by_mech_full.merge(
    county_cbsa,
    "left",
    left_on=['county'],
    right_on=['county_fips'],
    indicator=True
)
print(nih_mech_msa['_merge'].value_counts())
nih_mech_msa = nih_mech_msa.drop(columns=['_merge'])
nih_mech_msa.to_csv(base_path / "Data/Cleaned/funding_mech/nih_mech_msa.csv", index=False)

nih_by_mech_full['FUNDING'] = nih_by_mech_full['FUNDING'].replace(0, 1)
nih_by_mech_full['share_mech'] = nih_by_mech_full['FUNDING_mech'] / nih_by_mech_full['FUNDING']

# append a full share sum
nih_mech_total = nih_by_mech_full.groupby(['county', 'year'])['share_mech'].sum().reset_index()

# %%
######### Now append to MSA and county files
# Append to MSA
nih_by_msa = pd.read_csv(base_path / "Data/Census/census_1990/nih_msa_regress.csv")
nih_mech_msa = nih_mech_msa.drop(columns=['_merge'])
nih_by_msa_merge = nih_by_msa.merge(
    nih_mech_msa,
    "left",
    on=['CBSA_code', 'year', 'CBSA_level', 'CBSA_title', 'state'],
    indicator=True
)
print(nih_by_msa_merge['_merge'].value_counts())
nih_by_msa_merge = nih_by_msa_merge.drop(columns=['_merge'])
nih_by_msa_merge.to_csv(base_path / "Data/Cleaned/full/nih_msa.csv", index=False)
# %%
####################################
# County drop duplicates
nih_fix = pd.read_csv(base_path / "Data/Cleaned/full/nih_msa_upload.csv")
#nih_fix = nih_fix.drop(columns=['county'])
#nih_fix = nih_fix.drop_duplicates()
nih_fix = nih_fix.drop(columns=['county_fips'])
nih_fix = nih_fix.sort_values(by=['log_98_03', 'year'], ascending=[False, True])
nih_fix.to_csv(base_path / "Data/Cleaned/full/nih_msa_upload.csv", index=False)
# %%
# %%
# Filter data for 1998
df_funding = nih_fix[nih_fix['year'] == 1998]

# Create histogram
fig, ax = plt.subplots()
df_funding['funding_log_percap'].plot.hist(
    bins=30,
    ax=ax,
    color='steelblue',
    edgecolor='black'
)

# Title and labels
ax.set_title("Log Per Capita NIH Funding in 1998")
ax.set_xlabel("Log Per Capita Funding")
ax.set_ylabel("Number of MSAs")

interval = 2 
ax.set_yticks(np.arange(0, ax.get_ylim()[1] + interval, interval))

plt.show()

# %%
# Filter data for 2003
df_funding = nih_fix[nih_fix['year'] == 2003]

# Create histogram
fig, ax = plt.subplots()
df_funding['funding_log_percap'].plot.hist(
    bins=30,
    ax=ax,
    color='steelblue',
    edgecolor='black'
)

# Title and labels
ax.set_title("Log Per Capita NIH Funding in 2003")
ax.set_xlabel("Log Per Capita Funding")
ax.set_ylabel("Number of MSAs")

interval = 2 
ax.set_yticks(np.arange(0, ax.get_ylim()[1] + interval, interval))

plt.show()
# %%
# %%
# Filter data for 2003
df_funding = nih_fix[nih_fix['year'] == 2003]

# Create histogram
fig, ax = plt.subplots()
df_funding['log_98_03'].plot.hist(
    bins=30,
    ax=ax,
    color='steelblue',
    edgecolor='black'
)

# Title and labels
ax.set_title("Log Growth Rate for 1998 - 2003")
ax.set_xlabel("Log Growth Rate")
ax.set_ylabel("Number of MSAs")

interval = 5
ax.set_yticks(np.arange(0, ax.get_ylim()[1] + interval, interval))

plt.show()
# %%
