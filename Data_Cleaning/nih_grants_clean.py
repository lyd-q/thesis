
#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

########### Get NIH complete grants from Stata #############
#%%
base_path = "/Users/lydia/Desktop/Thesis"
nih = pd.read_stata(f"{base_path}/Data/NIH_v3/nih_cbsa_msa.dta")
nih.head()

# %%
# Keep relevant info
nih.columns
nih = nih.rename(columns={"funding_adj": "funding"})
nih["CBSA_code"] = nih["CBSA_code"].astype(str)
nih = nih[['ORGANIZATIONNAME', 'PROJECTNUMBER', 'FUNDINGMECHANISM', 'PINAME',
           'PROJECTTITLE', 'CONGRESSIONALDISTRICT', 'ZIPCODE', 'INSTITUTIONTYPE',
           'funding_real', 'funding',
           'year', 'city', 'state', 'county_fips', 'county_name',
           'CBSA_code', 'CBSA_title', 'CSA_code', 'CSA_title',
           'msan', 'pmsan', 'msa', 'pmsa',
           'org_dept', 'org_duns']]

# %%
base_path = Path(__file__).resolve().parent.parent.parent
nih.to_csv(base_path / "Data/NIH_v3/nih_grants_complete.csv", index=False)
# This is one file to upload to RDC
# Other file will be collapsed with BDS outcomes and census info (which I can always merge back to individual level)

########### Collapse and make funding metrics ###############
# %%
nih_funding = nih.groupby(['CBSA_code', 'CBSA_title', 'year'], as_index = False)[['funding_real', 'funding']].agg('sum')
nih_funding['log_funding'] = np.log(nih_funding['funding'])
nih_funding.to_csv(base_path / "Data/NIH_v3/nih_funding.csv", index=False)

# %%
########### Share of Field by MSAs ###############
nih_dept = nih.groupby(['CBSA_code', 'year', 'org_dept'], as_index = False)['funding'].agg('sum')
nih_dept["CBSA_code"] = nih_dept["CBSA_code"].astype(str)
all_msa = nih_dept['CBSA_code'].unique()
all_year = nih_dept['year'].unique()
all_dept = nih_dept['org_dept'].unique()
# There are 21 different fields: ['', 'BIOLOGY', 'BIOMEDICAL ENGINEERING', 'CHEMISTRY',
    #    'MICROBIOLOGY/IMMUN/VIROLOGY', 'NONE', 'OTHER BASIC SCIENCES',
    #    'PHYSIOLOGY', 'PSYCHOLOGY', 'SOCIAL SCIENCES',
    #    'ANATOMY/CELL BIOLOGY', 'BIOCHEMISTRY',
    #    'BIOSTATISTICS &OTHER MATH SCI', 'INTERNAL MEDICINE/MEDICINE',
    #    'PHARMACOLOGY', 'OTHER HEALTH PROFESSIONS', 'MISCELLANEOUS',
    #    'PHYSICS', 'BIOSTATISTICS & OTHER MATH SCI',
    #    'ENGINEERING (ALL TYPES)', 'PEDIATRICS', 'SURGERY', 'PATHOLOGY',
    #    'RADIATION-DIAGNOSTIC/ONCOLOGY', 'NEUROLOGY', 'OPHTHALMOLOGY',
    #    'PUBLIC HEALTH &PREV MEDICINE', 'PSYCHIATRY', 'GENETICS',
    #    'PUBLIC HEALTH & PREV MEDICINE', 'NEUROSCIENCES', 'ADMINISTRATION',
    #    'FAMILY MEDICINE', 'OBSTETRICS &GYNECOLOGY', 'EMERGENCY MEDICINE',
    #    'VETERINARY SCIENCES', 'OBSTETRICS & GYNECOLOGY', 'ORTHOPEDICS',
    #    'NEUROSURGERY', 'ANESTHESIOLOGY', 'NUTRITION', 'ZOOLOGY',
    #    'DENTISTRY', 'DERMATOLOGY', 'OTOLARYNGOLOGY',
    #    'PHYSICAL MEDICINE &REHAB', 'UROLOGY', 'PHYSICAL MEDICINE & REHAB',
    #    'BIOPHYSICS', 'OTHER CLINICAL SCIENCES', 'NO CODE ASSIGNED',
    #    'PLASTIC SURGERY']

full_index = pd.MultiIndex.from_product(
    [all_msa, all_year, all_dept],
    names=['CBSA_code', 'year', 'org_dept']
)
nih_dept_full = (
    nih_dept.set_index(['CBSA_code', 'year', 'org_dept'])
      .reindex(full_index)
      .reset_index()
)
nih_dept_full['funding'] = nih_dept_full['funding'].fillna(0)
nih_dept_full = nih_dept_full.rename(columns={'funding': 'funding_field'})
nih_dept_full["CBSA_code"] = nih_dept_full["CBSA_code"].astype(str)

# For each CBSA_code and year, calculate share of total funding that is in each
# Merge in CBSA_code-year total funding
nih_funding = pd.read_csv(base_path / "Data/NIH_v3/nih_funding.csv")
nih_funding["CBSA_code"] = nih_funding["CBSA_code"].astype(str)
# nih_dept_full = nih_dept_full.merge(
#     nih_funding,
#     "left",
#     on=['CBSA_code', 'year']
# )
# nih_dept_full.to_csv(base_path / "Data/Cleaned/funding_mech/nih_by_field.csv", index=False)
# nih_dept_full['funding'] = nih_dept_full['funding'].replace(0, 1)
# nih_dept_full['share_field'] = nih_dept_full['funding_field'] / nih_dept_full['funding']

# keep only science fields
excluded = ["", "NONE", "NO CODE ASSIGNED", "MISCELLANEOUS"]

# Drop excluded rows completely
nih_dept_coded = nih_dept_full.loc[
    ~nih_dept_full["org_dept"].isin(excluded)
].copy()

# Denominator: total funding across coded fields only (per CBSA-year)
coded_totals = (
    nih_dept_coded
    .groupby(["CBSA_code", "year"], as_index=False)["funding_field"]
    .sum()
    .rename(columns={"funding_field": "funding_fields_total"})
)

nih_dept_coded = nih_dept_coded.merge(
    coded_totals,
    on=["CBSA_code", "year"],
    how="left"
)

nih_dept_coded["funding_fields_total"] = nih_dept_coded["funding_fields_total"].replace(0, 1)

# Share among coded fields only
nih_dept_coded["share_field_coded"] = (nih_dept_coded["funding_field"] / nih_dept_coded["funding_fields_total"])

# save wide format
nih_by_field_wide = (
    nih_dept_coded.pivot_table(
        index=["CBSA_code", "year"],
        columns="org_dept",
        values="share_field_coded",
        fill_value=0
    )
    .reset_index()
)
nih_by_field_wide.columns.name = None

# add total share
dept_cols = [
    c for c in nih_by_field_wide.columns
    if c not in ["CBSA_code", "year"]
]
nih_by_field_wide["total_share_field_coded"] = nih_by_field_wide[dept_cols].sum(axis=1)
# %%
# Append to CBSA_code
nih_msa = pd.read_csv(base_path / "Data/NIH_v3/nih_funding.csv")
nih_msa["CBSA_code"] = nih_msa["CBSA_code"].astype(str)
nih_by_field_wide["CBSA_code"] = nih_by_field_wide["CBSA_code"].astype(str)
nih_msa_dept = nih_msa.merge(
    nih_by_field_wide,
    "left",
    on=['CBSA_code', 'year'],
    indicator=True
)
print(nih_msa_dept['_merge'].value_counts())
nih_msa_dept = nih_msa_dept.drop(columns=['_merge'])
nih_msa_dept.to_csv(base_path / "Data/NIH_v3/nih_funding_field.csv", index=False)



# %%
########### Share of Mech by MSAs ###############
nih_mech = nih.groupby(['CBSA_code', 'year', 'FUNDINGMECHANISM'], as_index = False)['funding'].agg('sum')
nih_mech["CBSA_code"] = nih_mech["CBSA_code"].astype(str)
all_msa = nih_mech['CBSA_code'].unique()
all_year = nih_mech['year'].unique()
all_mech = nih_mech['FUNDINGMECHANISM'].unique()

full_index = pd.MultiIndex.from_product(
    [all_msa, all_year, all_mech],
    names=['CBSA_code', 'year', 'FUNDINGMECHANISM']
)
nih_mech_full = (
    nih_mech.set_index(['CBSA_code', 'year', 'FUNDINGMECHANISM'])
      .reindex(full_index)
      .reset_index()
)
nih_mech_full['funding'] = nih_mech_full['funding'].fillna(0)
nih_mech_full = nih_mech_full.rename(columns={'funding': 'funding_mech'})
nih_mech_full["CBSA_code"] = nih_mech_full["CBSA_code"].astype(str)

# The different funding mechanisms:
# RPGs - SBIR/STTR
# R&D Contracts
# RPGs - Non SBIR/STTR --> this is R01s, and majority, and most interesting
# Other Research-Related
# NULL
# Research Grants
# Training - Institutional
# Research Centers
# Construction
# Training - Individual
# Other

# For each CBSA_code and year, calculate share of total funding that is in each
# Merge in CBSA_code-year total funding
nih_funding = pd.read_csv(base_path / "Data/NIH_v3/nih_funding.csv")
nih_funding["CBSA_code"] = nih_funding["CBSA_code"].astype(str)
nih_mech_full = nih_mech_full.merge(
    nih_funding,
    "left",
    on=['CBSA_code', 'year']
)
nih_mech_full.to_csv(base_path / "Data/Cleaned/funding_mech/nih_by_mech.csv", index=False)
nih_mech_full['funding'] = nih_mech_full['funding'].replace(0, 1)
nih_mech_full['share_mech'] = nih_mech_full['funding_mech'] / nih_mech_full['funding']


#%%
# append a full share sum
nih_mech_total = nih_mech_full.groupby(['CBSA_code', 'year'])['share_mech'].sum().reset_index()

# pivot into each row is by CBSA_code and year
nih_share_mech = nih_mech_full.pivot(index=['CBSA_code', 'year'], columns='FUNDINGMECHANISM', values='share_mech').reset_index()
nih_share_mech['total_share_mech'] = nih_mech_total['share_mech']
nih_share_mech.columns.name = None
nih_share_mech.to_csv(base_path / "Data/NIH_v3/nih_funding_mech.csv", index=False)

# Append to CBSA_code
nih_msa = pd.read_csv(base_path / "Data/NIH_v3/nih_funding.csv")
nih_msa["CBSA_code"] = nih_msa["CBSA_code"].astype(str)
nih_msa_mech = nih_msa.merge(
    nih_share_mech,
    "left",
    on=['CBSA_code', 'year'],
    indicator=True
)
print(nih_msa_mech['_merge'].value_counts())
nih_msa_mech = nih_msa_mech.drop(columns=['_merge'])
nih_msa_mech.to_csv(base_path / "Data/NIH_v3/nih_funding_mech.csv", index=False)


#%%
########### Merge share of mech and funding together (?) ###############


#%%
########### Making funding variables ###############
nih_by_msa = nih_by_msa[nih_by_msa['funding_dollars'] != 0]
nih_by_msa['funding_dollars_percap'] = nih_by_msa['funding_dollars'] / nih_by_msa['total_pop'] 
nih_by_msa['funding_log_dollars'] = np.log(nih_by_msa['funding_dollars'])
nih_by_msa['funding_log_percap'] = np.log(nih_by_msa['funding_dollars_percap'])


#%%
########### Funding Lags ###############

for lag in range(1, 6):
    nih['funding_dollars'+f"_{lag}"] = nih.groupby('CBSA_code')['funding_dollars'].shift(lag)
    nih['funding_dollars_percap'+f"_{lag}"] = nih.groupby('CBSA_code')['funding_dollars_percap'].shift(lag)
    nih['funding_log'+f"_{lag}"] = nih.groupby('CBSA_code')['funding_log'].shift(lag)


# create log(f2003) - log(f1998) for LHS
nih = pd.read_csv(base_path / "Data/Census/census_1990/nih_msa_lags1990.csv")
# Make sure that we have 1998 and 2003 observations
nih = nih[(nih['year'] != 2003) | nih['funding_dollars_5'].notna()]
# 204 observations for 2003

nih.loc[nih['year'] == 2003, 'log_98_03'] = (nih['funding_log'] - nih['funding_log_5'])

nih.loc[nih['year'] == 2003, 'percap_98_03'] = (nih['funding_dollars_percap'] - nih['funding_dollars_percap_5'])
nih['percap_98_03'] = nih.groupby('CBSA_code')['percap_98_03'].transform('first')
nih.to_csv(base_path / "Data/Cleaned/full/nih_msa_updated.csv")


