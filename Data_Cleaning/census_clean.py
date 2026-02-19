# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
base_path = Path(__file__).resolve().parent.parent.parent

# %% ######################## 1990 Census #######################
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
# census1990['state_code'] = census1990['state_code'].astype('string').str.strip().str.zfill(2)
# census1990['county_code'] = census1990['county_code'].astype('string').str.strip().str.zfill(3)
census1990['county'] = census1990['state_code'] + census1990['county_code']
census1990['county'] = census1990['county'].astype('string').str.strip().str.zfill(5)
census1990.head()
# census1990.to_csv(base_path / "Data/Census/census_1990_v2/census1990.csv")


# Merge with MSAs
county_cbsa = pd.read_csv(base_path / "Data/Crosswalks/Used/county_cbsa_xwalk_2009.csv")
county_cbsa['county_fips'] = county_cbsa['county_fips'].astype('string').str.strip().str.zfill(5)
census1990['county'] = census1990['county'].astype('string').str.strip().str.zfill(5)
census_msa = census1990.merge(
    county_cbsa,
    "left",
    left_on=['county'],
    right_on=['county_fips'],
    indicator=True
)
print(census_msa['_merge'].value_counts()) # this is fine! because all the cbsas are merged in
census_msa = census_msa[census_msa['_merge'] == 'both']
# census_msa.to_csv(base_path / "Data/Census/census_1990_v2/census1990_county_msa.csv", index=False)

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
# census_msa = census_msa[['CBSA_code', 'CBSA_title', 'total_pop',
#        'total_income_imputed', 'income_per_cap',
#        'share_college', 'share_gradschool', 'share_health_indus',
#        'share_educ_indus', 'log_pop']]
census_msa.to_csv(base_path / "Data/Census/census_1990_v2/census1990_msa.csv", index=False)
# census_msa.to_csv(base_path / "Data/NIH_v3/census1990_msa.csv", index=False)

# now this is 1990 census info ready to merge with NIH data



# %% Annual Census Counts -- moved to Stata
infile = base_path / "Raw_data/99c8_00.txt"

colspecs = [
    (0, 1),      # summary level
    (2, 9),      # county fips
    (10, 23),    # 1999
    (24, 37),    # 1998
    (38, 51),    # 1997
    (52, 65),    # 1996
    (66, 79),    # 1995
    (80, 93),    # 1994
    (94, 107),   # 1993
    (108, 121),  # 1992
    (122, 135),  # 1991
    (136, 149),  # 1990
    (150, 163),  # April 1, 1990
    (164, 199),  # area name
]

names = [
    "level", "cty_fips",
    "pop1999","pop1998","pop1997","pop1996","pop1995",
    "pop1994","pop1993","pop1992","pop1991","pop1990",
    "base1990","cty_name"
]

df = pd.read_fwf(infile, colspecs=colspecs, names=names, dtype=str)

# Clean numbers
for c in names[1:-1]:
    df[c] = (
        df[c]
        .str.replace(",", "", regex=False)
        .astype(float)
        .astype("Int64")
    )

df["level"] = df["level"].astype(int)
df["areaname"] = df["areaname"].str.strip()

df.to_csv(base_path / "Data/census/pop_1990_1999.csv", index=False)

#%% ################ 2000 Census: Here we go again ####################

# This is total population so I don't even necessarily want it
census2000 = pd.read_csv('/Users/lydia/Desktop/Thesis/Raw_data/Census/census_2000/nhgis0006_csv/nhgis0006_ts_nominal_county.csv')

census2000 = census2000.rename(columns={
    'STATEFP' : 'state_code',
    'COUNTYFP' : 'county_code',
    'COUNTY' : 'county_name',
    "B69AC2000" : "college",
    "B84AA2000" : "employed",
    "BD5AA2000" : "income_per_cap",
})

census2000 = census2000[['state_code', 'county_code', 'county_name', 'college', 'employed', 'income_per_cap']]

census2000[['county_code', 'state_code']] = census2000[['county_code', 'state_code']].astype(str)
census2000.head()
# %%
# make combined county code
census2000['state_code'] = census2000['state_code'].astype('string').str.strip().str.zfill(2)
census2000['county_code'] = census2000['county_code'].astype('string').str.strip().str.zfill(3)
census2000['county'] = census2000['state_code'] + census2000['county_code']
census2000['county'] = census2000['county'].astype('string').str.strip().str.zfill(5)

census2000.to_csv(base_path / "Data/Census/census_2000_v2/census2000_county.csv", index=False)

#%% add population
pop2000 = pd.read_csv('/Users/lydia/Desktop/Thesis/Raw_data/Census/census_2000/nhgis0007_csv/nhgis0007_ts_nominal_county.csv')
pop2000 = pop2000.rename(columns={
    'STATEFP' : 'state_code',
    'COUNTYFP' : 'county_code',
    'COUNTY' : 'county_name',
    "AV0AA2000" : 'pop'
})

pop2000 = pop2000[['state_code', 'county_code', 'pop']]
pop2000['state_code'] = pop2000['state_code'].astype('string').str.strip().str.zfill(2)
pop2000['county_code'] = pop2000['county_code'].astype('string').str.strip().str.zfill(3)
pop2000['county'] = pop2000['state_code'] + pop2000['county_code']
pop2000['county'] = pop2000['county'].astype('string').str.strip().str.zfill(5)
pop2000 = pop2000.drop(columns=['county_code', 'state_code'])
# %%
census2000_merged = census2000.merge(pop2000, on=['county'], indicator=True)
print(census2000_merged['_merge'].value_counts())
census2000_merged = census2000_merged.drop(columns=['_merge'])
# %% Merge to MSAs
county_cbsa = pd.read_csv(base_path / "Data/Crosswalks/Used/county_cbsa_xwalk_2009.csv")
county_cbsa['county_fips'] = county_cbsa['county_fips'].astype('string').str.strip().str.zfill(5)
census2000_merged['county'] = census2000_merged['county'].astype('string').str.strip().str.zfill(5)
census_msa = census2000_merged.merge(
    county_cbsa,
    "inner",
    left_on=['county'],
    right_on=['county_fips'],
    indicator=True
)
print(census_msa['_merge'].value_counts()) # this is fine! because all the cbsas are merged in
census_msa = census_msa[census_msa['_merge'] == 'both']
census_msa.to_csv(base_path / "Data/Census/census_2000_v2/census2000_county_msa.csv", index=False)

# %% Now to collapse
# Need to go from county income_per_cap to MSA income_per_cap
census_msa['total_income_imputed'] = census_msa['income_per_cap'] * census_msa['pop']

# collapse
census_msa = census_msa.groupby(['CBSA_code'], as_index = False).agg({
    'CBSA_level': 'first',
    'CBSA_title': 'first',
    'state': 'first',
    'pop': 'sum',
    'total_income_imputed': 'sum',
    'college': 'sum',
})


# Divide 'total_income_imputed' by 'total_pop' to get new MSA income_per_cap
census_msa['income_per_cap'] = census_msa['total_income_imputed'] / census_msa['pop']

# share college
census_msa['share_college'] = census_msa['college'] / census_msa['pop']
census_msa.to_csv(base_path / "Data/Census/census_2000_v2/census2000_msa.csv", index=False)

#%% ################ 2010 Census: Here we go again v2 ####################

census2010 = pd.read_csv("/Users/lydia/Desktop/Thesis/Data/Census/census_2010/nhgis0009_csv/nhgis0009_ds175_2010_county.csv")
census2010 = census2010.rename(columns={
    'STATEA' : 'state_code',
    'COUNTYA' : 'county_code',
    'COUNTY' : 'county_name',
    "IXMM022" : "college",
    "I9CE001" : "employed",
    "I6IM001" : "income_per_cap",
})

census2010 = census2010[['state_code', 'county_code', 'county_name', 'college', 'employed', 'income_per_cap']]