# 2/18/2026: Combining NIH, mech/funding, census, and outcomes at MSA level

# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
base_path = Path(__file__).resolve().parent.parent.parent

#%% Read in files
# NIH funding
nih = pd.read_stata(base_path / "Data/NIH_v4/nih_funding_use.dta")

# NIH mechanism
nih_field = pd.read_csv(base_path / "Data/NIH_v3/Working/nih_funding_field.csv")
nih_mech = pd.read_csv(base_path / "Data/NIH_v3/Working/nih_funding_mech.csv")

# Census
# Notes: share_emp for 1990 and 2000 seems off. share_college for 2010 seems off.
census1990 = pd.read_csv(base_path / "Data/Census/census_1990_v2/census1990_msa.csv")
census2000 = pd.read_csv(base_path / "Data/Census/census_2000_v2/census2000_msa.csv")
census2010 = pd.read_csv(base_path / "Data/Census/census_2010/census2010_msa.csv")

# Outcomes
bds_educ = pd.read_stata(base_path / "Data/Outcomes/sector/bds_educ.dta")
bds_science = pd.read_stata(base_path / "Data/Outcomes/sector/bds_science.dta")
bds_health = pd.read_stata(base_path / "Data/Outcomes/sector/bds_health.dta")

# %%
################# Fields and mechanisms ####################
# Standardize CBSA code as a 5-char string
nih_field['CBSA_code'] = nih_field['CBSA_code'].astype(str)
nih_field = nih_field.drop(columns=['funding_nominal', 'funding',
       'log_funding'])

nih_mech['CBSA_code'] = nih_mech['CBSA_code'].astype(str)
nih_mech = nih_mech.drop(columns=['funding_nominal', 'funding',
       'log_funding'])

# %%
field_bins = {
    "admin": ["ADMINISTRATION"],
    "basic_science": [
        "ANATOMY/CELL BIOLOGY", "BIOCHEMISTRY", "BIOLOGY", "BIOPHYSICS", "GENETICS",
        "MICROBIOLOGY/IMMUN/VIROLOGY", "PHYSIOLOGY", "ZOOLOGY", "CHEMISTRY", "PHYSICS",
        "PHARMACOLOGY", "NEUROSCIENCES", "OTHER BASIC SCIENCES"
    ],
    "engineering": ["BIOMEDICAL ENGINEERING", "ENGINEERING (ALL TYPES)"],
    "medicine": [
        "ANESTHESIOLOGY", "DERMATOLOGY", "EMERGENCY MEDICINE", "FAMILY MEDICINE",
        "INTERNAL MEDICINE/MEDICINE", "PEDIATRICS", "OBSTETRICS & GYNECOLOGY",
        "OPHTHALMOLOGY", "OTOLARYNGOLOGY", "PATHOLOGY", "PHYSICAL MEDICINE & REHAB",
        "RADIATION-DIAGNOSTIC/ONCOLOGY", "SURGERY", "NEUROSURGERY", "ORTHOPEDICS", 
        "PLASTIC SURGERY", "UROLOGY", "DENTISTRY", "NEUROLOGY", "PSYCHIATRY",
        "OTHER CLINICAL SCIENCES"
    ],
    "pop_behave_science": [
        "PUBLIC HEALTH & PREV MEDICINE", "BIOSTATISTICS & OTHER MATH SCI",
        "SOCIAL SCIENCES", "PSYCHOLOGY", "NUTRITION", 
        "OTHER HEALTH PROFESSIONS", "VETERINARY SCIENCES"
    ]
}
mech_bins = {
    "research": ["Research Grants", "RPGs - Non SBIR/STTR", "RPGs - SBIR/STTR"],
    "infrastructure": ["Research Centers", "Construction"],
    "training": ["Training - Individual", "Training - Institutional"],
    "contracts": ["R&D Contracts"],
    "other": ["Other Research-Related"],
}
#%%
### Aggregate science fields into bins 
for bin_name, cols in field_bins.items():
    nih_field[f"field_{bin_name}"] = nih_field[cols].sum(axis=1)

nih_field = nih_field[['CBSA_code', 'CBSA_title', 'year', 'total_share_field', 'field_admin', 'field_basic_science',
       'field_engineering', 'field_medicine', 'field_pop_behave_science']]
nih_field.to_csv(base_path / "Data/NIH_v4/Working/nih_field_bins.csv", index=False)

#%%
### Aggregate mech fields into bins 
for bin_name, cols in mech_bins.items():
    nih_mech[f"mech_{bin_name}"] = nih_mech[cols].sum(axis=1)

nih_mech = nih_mech[['CBSA_code', 'CBSA_title', 'year', 'total_share_mech',
       'mech_research', 'mech_infrastructure', 'mech_training',
       'mech_contracts', 'mech_other']]
nih_mech.to_csv(base_path / "Data/NIH_v4/Working/nih_mech_bins.csv", index=False)


# %%
# Merge field
combined = nih.merge(nih_field, on=['CBSA_title', 'CBSA_code', 'year'], how='left', indicator=True)
print(combined['_merge'].value_counts())
combined = combined.drop(columns='_merge')
combined = combined.fillna(0)

# Merge mech
combined = combined.merge(nih_mech, on=['CBSA_title', 'CBSA_code', 'year'], how='left', indicator=True)
print(combined['_merge'].value_counts())
combined = combined.drop(columns='_merge')
combined = combined.fillna(0)

move_cols = ["total_share_field", "total_share_mech"]
other_cols = [c for c in combined.columns if c not in move_cols]
combined = combined[other_cols + move_cols]

combined.to_csv(base_path / "Data/NIH_v4/Working/nih_field_mech_merge.csv", index=False)


# %%
################# Census ####################
combined = pd.read_csv(base_path / "Data/NIH_v4/Working/nih_field_mech_merge.csv")

# Split by year
nih1990 = combined[combined['year'] < 2000]
nih2000 = combined[(combined['year'] >= 2000) & (combined['year'] < 2010)]
nih2010 = combined[(combined['year'] >= 2010) & (combined['year'] <= 2020)] # exclude

# Drop population in census before merging because it is in NIH file already
census1990 = census1990.drop(columns='pop')
census2000 = census2000.drop(columns='pop')
census2010 = census2010.drop(columns='pop')

# Examining census
combined_1990 = nih1990.merge(census1990, on=['CBSA_title', 'CBSA_code'], how='left', indicator=True)
print(combined_1990['_merge'].value_counts())
combined_1990 = combined_1990.drop(columns='_merge')
print(combined_1990['CBSA_title'].value_counts())

combined_2000 = nih2000.merge(census2000, on=['CBSA_title', 'CBSA_code'], how='left', indicator=True)
print(combined_2000['_merge'].value_counts())
combined_2000 = combined_2000.drop(columns='_merge')
print(combined_2000['CBSA_title'].value_counts())

combined = pd.concat([combined_1990, combined_2000], axis=0)
combined = combined.sort_values(by=['CBSA_code', 'year'])

# Rename log to ln
combined = combined.rename(columns = {'log_funding' : 'ln_funding', 'log_funding_pc' : 'ln_funding_pc'})
combined['ln_pop'] = np.log(combined['pop'])
combined.to_csv(base_path / "Data/NIH_v4/Working/nih_fieldmech_census_merge.csv", index=False)

# %%
################# BDS - EDUCATION ####################
combined = pd.read_csv(base_path / "Data/NIH_v4/Working/nih_fieldmech_census_merge.csv")
bds_educ = bds_educ.rename(columns={'cbsa_code' : 'CBSA_code'})
combined_educ = combined.merge(bds_educ, on=['year', 'CBSA_code'], how='left')
combined_educ.to_csv(base_path / "Data/NIH_v4/Use/nih_educ.csv", index=False)

# %%
################# BDS - SCIENCE ####################
combined = pd.read_csv(base_path / "Data/NIH_v4/Working/nih_fieldmech_census_merge.csv")
bds_science = bds_science.rename(columns={'cbsa_code' : 'CBSA_code'})
combined_science = combined.merge(bds_science, on=['year', 'CBSA_code'], how='left')
combined_science.to_csv(base_path / "Data/NIH_v4/Use/nih_science.csv", index=False)

# %%
################# BDS - HEALTH ####################
combined = pd.read_csv(base_path / "Data/NIH_v4/Working/nih_fieldmech_census_merge.csv")
bds_health = bds_health.rename(columns={'cbsa_code' : 'CBSA_code'})
combined_health = combined.merge(bds_health, on=['year', 'CBSA_code'], how='left')
combined_health.to_csv(base_path / "Data/NIH_v4/Use/nih_health.csv", index=False)

# %% ### Side note: what MSAs are missing in the BDS files?
county_cbsa = pd.read_csv(base_path / "Data/Crosswalks/Used/county_cbsa_xwalk_2009.csv")
county_cbsa = county_cbsa[county_cbsa['CBSA_level_id'] == 1]
county_cbsa = county_cbsa[['CBSA_code', 'CBSA_title']].drop_duplicates()
bds_educ = bds_educ.rename(columns={'cbsa_code' : 'CBSA_code'})
bds_educ = bds_educ.loc[(bds_educ['year'] >= 1992) & (bds_educ['year'] <= 2008)]
bds_health_check = bds_educ.merge(county_cbsa, on=['CBSA_code'], how='outer', indicator=True)
print(bds_health_check['_merge'].value_counts())
bds_health_check = bds_health_check[bds_health_check['_merge'] == 'right_only']
print(bds_health_check['CBSA_title'].value_counts())
# %%
bds_health_check.to_csv(base_path / "Data/NIH_v4/Use/nih_health_check.csv", index=False)
### 343 MSAs for later regressions. The unmatched are mostly PR and some other MSAs with code issues. Will not address rn.
