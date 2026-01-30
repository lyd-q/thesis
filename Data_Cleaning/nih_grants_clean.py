
#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
base_path = Path(__file__).resolve().parent.parent.parent

########### Get NIH complete grants from Stata #############
#%%
base_path = "/Users/lydia/Desktop/Thesis"
nih = pd.read_stata(f"{base_path}/Data/NIH_v3/nih_cbsa_msa.dta")
nih.head()

# %%
# Keep relevant info
nih.columns
nih = nih.rename(columns={"funding_adj": "funding", "funding_real": "funding_nominal"}) # correcting naming mistake
nih["CBSA_code"] = nih["CBSA_code"].astype(str)
nih = nih[['ORGANIZATIONNAME', 'PROJECTNUMBER', 'FUNDINGMECHANISM', 'PINAME',
           'PROJECTTITLE', 'CONGRESSIONALDISTRICT', 'ZIPCODE', 'INSTITUTIONTYPE',
           'funding_nominal', 'funding',
           'year', 'city', 'state', 'county_fips', 'county_name',
           'CBSA_code', 'CBSA_title', 'CSA_code', 'CSA_title',
           'msan', 'pmsan', 'msa', 'pmsa',
           'org_dept', 'org_duns']]

# %%
base_path = Path(__file__).resolve().parent.parent.parent
nih.to_csv(base_path / "Data/NIH_v3/nih_grants_complete.csv", index=False)
# This is one file to upload to RDC
# Other file will be collapsed with BDS outcomes and census info (which I can always merge back to individual level)
# And need to bring in CBSA crosswalk I have been using

########### Collapse and make funding metrics ###############
# %%
nih_funding = nih.groupby(['CBSA_code', 'CBSA_title', 'year'], as_index = False)[['funding_nominal', 'funding']].agg('sum')
nih_funding['log_funding'] = np.log(nih_funding['funding'])
nih_funding.to_csv(base_path / "Data/NIH_v3/nih_funding.csv", index=False)

# %%
########### Share of Field by MSAs ###############

nih_dept = nih.groupby(["CBSA_code", "year", "org_dept"], as_index=False)["funding"].sum()

# Fix inconsistent field labels (VALUES in org_dept, not columns)
var_map = {
    "BIOSTATISTICS &OTHER MATH SCI": "BIOSTATISTICS & OTHER MATH SCI",
    "PUBLIC HEALTH &PREV MEDICINE": "PUBLIC HEALTH & PREV MEDICINE",
    "OBSTETRICS &GYNECOLOGY": "OBSTETRICS & GYNECOLOGY",
    "PHYSICAL MEDICINE &REHAB": "PHYSICAL MEDICINE & REHAB",
}
nih_dept["org_dept"] = nih_dept["org_dept"].replace(var_map)

# Aggregate
nih_dept = nih_dept.groupby(["CBSA_code", "year", "org_dept"], as_index=False)["funding"].sum()
nih_dept["CBSA_code"] = nih_dept["CBSA_code"].astype(str)

all_msa = nih_dept['CBSA_code'].unique()
all_year = nih_dept['year'].unique()
all_dept = nih_dept['org_dept'].unique()

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

# Keep only science fields
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
nih_by_field_wide["total_share_field"] = nih_by_field_wide[dept_cols].sum(axis=1)
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
# ['Other', 'RPGs - SBIR/STTR', 'Other Research-Related',
#        'RPGs - Non SBIR/STTR', 'NULL', 'Training - Individual',
#        'R&D Contracts', 'Training - Institutional', 'Research Centers',
#        'Research Grants', 'Construction']

# Keep only science fields
excluded = ["", "NULL", "Other"]
# Drop excluded rows completely
nih_mech_coded = nih_mech_full.loc[
    ~nih_mech_full["FUNDINGMECHANISM"].isin(excluded)
].copy()

# Denominator: total funding across coded fields only (per CBSA-year)
coded_totals = (
    nih_mech_coded
    .groupby(["CBSA_code", "year"], as_index=False)["funding_mech"]
    .sum()
    .rename(columns={"funding_mech": "funding_mech_total"})
)
nih_mech_coded = nih_mech_coded.merge(
    coded_totals,
    on=["CBSA_code", "year"],
    how="left"
)

nih_mech_coded["funding_mech_total"] = nih_mech_coded["funding_mech_total"].replace(0, 1)

# Share among coded fields only
nih_mech_coded["share_mech_coded"] = (nih_mech_coded["funding_mech"] / nih_mech_coded["funding_mech_total"])

# save wide format
nih_by_mech_wide = (
    nih_mech_coded.pivot_table(
        index=["CBSA_code", "year"],
        columns="FUNDINGMECHANISM",
        values="share_mech_coded",
        fill_value=0
    )
    .reset_index()
)
nih_by_mech_wide.columns.name = None

# add total share
mech_cols = [
    c for c in nih_by_mech_wide.columns
    if c not in ["CBSA_code", "year"]
]
nih_by_mech_wide["total_share_mech"] = nih_by_mech_wide[mech_cols].sum(axis=1)
# %%
# Append to CBSA_code
nih_msa = pd.read_csv(base_path / "Data/NIH_v3/nih_funding.csv")
nih_msa["CBSA_code"] = nih_msa["CBSA_code"].astype(str)
nih_by_mech_wide["CBSA_code"] = nih_by_mech_wide["CBSA_code"].astype(str)
nih_msa_mech = nih_msa.merge(
    nih_by_mech_wide,
    "left",
    on=['CBSA_code', 'year'],
    indicator=True
)
print(nih_msa_mech['_merge'].value_counts())
nih_msa_mech = nih_msa_mech.drop(columns=['_merge'])
nih_msa_mech.to_csv(base_path / "Data/NIH_v3/nih_funding_mech.csv", index=False)


#%%
########### Merge Census (so have population for percap) ###############
nih_msa = pd.read_csv(base_path / "Data/NIH_v3/nih_working.csv")
census = pd.read_csv(base_path / "Data/NIH_v3/census1990_msa.csv")
nih_msa = nih_msa.merge(
    census,
    "left",
    on=['CBSA_code', 'CBSA_title'],
    indicator=True
)
print(nih_msa['_merge'].value_counts())
# the unmatched ones are Puerto Rico
nih_msa = nih_msa[nih_msa['_merge'] == "both"]
nih_msa = nih_msa.drop(columns=['_merge'])
nih_msa.to_csv(base_path / "Data/NIH_v3/nih_working.csv", index='False')

#%%
########### Making funding variables ###############
nih_msa = nih_msa[nih_msa['funding'] != 0]
nih_msa['funding_pc'] = nih_msa['funding'] / nih_msa['total_pop'] 
nih_msa['log_funding_pc'] = np.log(nih_msa['funding_pc'])
nih_msa.to_csv(base_path / "Data/NIH_v3/nih_working.csv", index='False')

#%%
########### Merge in share of mech and funding ###############
nih_working = pd.read_csv(base_path / "Data/NIH_v3/nih_working.csv")
nih_field = pd.read_csv(base_path / "Data/NIH_v3/nih_funding_field.csv")
nih_field = nih_field.drop(columns=['funding_nominal', 'funding', 'log_funding'])
nih_mech = pd.read_csv(base_path / "Data/NIH_v3/nih_funding_mech.csv")
nih_mech = nih_mech.drop(columns=['funding_nominal', 'funding', 'log_funding'])

nih_all = nih_working.merge(
    nih_field,
    "inner",
    on=['CBSA_code', 'CBSA_title', 'year'],
    indicator=True
)
print(nih_all['_merge'].value_counts())
nih_all = nih_all.drop(columns='_merge')

nih_all = nih_all.merge(
    nih_mech,
    "inner",
    on=['CBSA_code', 'CBSA_title', 'year'],
    indicator=True
)
print(nih_all['_merge'].value_counts())
nih_all = nih_all.drop(columns='_merge')
nih_all.to_csv(base_path / "Data/NIH_v3/nih_all.csv", index=False)

# Drop if no 98-03 observation
nih_all = nih_all[nih_all['log_98_03'].notna()]
nih_all = nih_all[nih_all['percap_98_03'].notna()]
nih_all.to_csv(base_path / "Data/NIH_v3/nih_all.csv", index=False)

# 204 MSAs

#%% ########### Re-do Funding Lags and Growth, Making a separate dataframe and merging in ###############
nih_all = pd.read_csv(base_path / "Data/NIH_v3/nih_all.csv")
nih_funding = nih_all.drop(columns=['funding_pc_1', 'log_funding_1', 'log_funding_pc_1', 'log_98_03', 'percap_98_03'])
nih_funding = nih_funding[nih_funding["year"].isin([1997, 1998, 2003])]
vars = [
    "funding",
    "funding_pc",
    "log_funding",
    "log_funding_pc",
]
nih_wide = nih_funding.pivot_table(index="CBSA_code", columns="year", values=vars)

# Flatten MultiIndex columns
nih_wide.columns = [f"{v}_{int(y)}" for v, y in nih_wide.columns]
nih_wide = nih_wide.reset_index()
nih_wide.to_csv(base_path / "Data/NIH_v3/nih_funding_working.csv", index=False)

#%%
nih_funding = nih_wide[nih_wide['funding_1998'].notna()].copy()
nih_funding['log_98_03'] = nih_funding['log_funding_2003'] - nih_funding['log_funding_1998']
nih_funding['percap_98_03'] = nih_funding['funding_pc_2003'] - nih_funding['funding_pc_1998']
nih_funding.to_csv(base_path / "Data/NIH_v3/nih_funding_working.csv", index=False)
nih_funding['log_98_03'].describe()
nih_funding['percap_98_03'].describe()

#%%
# Now merge these funding values into the overall dataset
nih_all = pd.read_csv(base_path / "Data/NIH_v3/nih_all_old.csv")
nih_all = nih_all.drop(columns=['log_98_03', 'percap_98_03','funding_pc_1', 'log_funding_1', 'log_funding_pc_1'])
nih_merge = nih_all.merge(
    nih_funding,
    "left",
    on='CBSA_code',
    indicator=True
)
print(nih_merge['_merge'].value_counts())
nih_merge = nih_merge[nih_merge['_merge'] == "both"] #193 unique CBSAs as expected
nih_merge = nih_merge.drop(columns=['_merge'])
nih_merge.to_csv(base_path / "Data/NIH_v3/nih_all.csv", index=False)

#%%
########### Add abbreviated CBSA to prepare for graphing ########
base_path = Path(__file__).resolve().parent.parent.parent
def shorten_cbsa_name(name):
    city_part, state_part = name.split(", ")
    first_city = city_part.split("-")[0]
    return f"{first_city}, {state_part}"
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_all.csv")
nih["CBSA_title_abbrev"] = nih["CBSA_title"].apply(shorten_cbsa_name)
nih.to_csv(base_path / "Data/NIH_v3/nih_all.csv", index=False)

#%%
########### Further edits ########
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_all.csv")
nih = nih.drop(columns=['total_income_imputed'])
nih.to_csv(base_path / "Data/NIH_v3/nih_all.csv", index=False)

#%% 
########### Fields and mechanisms ########
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
################### Aggregate science fields into bins ###################
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_all.csv")

for bin_name, cols in field_bins.items():
    nih[f"field_{bin_name}"] = nih[cols].sum(axis=1)
nih.head()
nih.columns

nih.to_csv(base_path / "Data/NIH_v3/nih_all.csv", index=False)


#%%
################### Aggregate science fields into bins ###################
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_all.csv")

for bin_name, cols in mech_bins.items():
    nih[f"mech_{bin_name}"] = nih[cols].sum(axis=1)
nih.head()
nih.columns
nih.to_csv(base_path / "Data/NIH_v3/nih_all.csv", index=False)

#%%
### Add relative (percent) change ###
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_all.csv")
nih['rel_98_03'] = nih['percap_98_03'] / nih['funding_pc_1998']
nih.head()
nih.to_csv(base_path / "Data/NIH_v3/nih_all.csv", index=False)
#%%
################### Make version that only keeps aggregated bins ###################

field_cols = [c for cols in field_bins.values() for c in cols]
mech_cols = [c for cols in mech_bins.values() for c in cols]
nih_abbrev = nih.drop(columns=field_cols+mech_cols)
nih_abbrev.to_csv(base_path / "Data/NIH_v3/nih_use.csv", index=False)

# %%
###### Merge BDS Economics Outcomes #######
bds = pd.read_csv(base_path / "Raw_data/BDS/bds2023_msa.csv", low_memory=False)
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_use.csv")
nih = nih[nih['year'] != 2024] # BDS goes up to 2023
bds = bds.rename(columns={'msa': 'CBSA_code'})
nih_merge = nih.merge(
    bds,
    "left",
    on=['CBSA_code', 'year'],
    indicator=True
)
print(nih_merge['_merge'].value_counts())
nih_merge = nih_merge[nih_merge['_merge'] == "both"] #193 unique CBSAs as expected
nih_merge = nih_merge.drop(columns=['_merge'])
nih_merge.to_csv(base_path / "Data/NIH_v3/nih_use_outcomes.csv", index=False)

# unmatched are some MSAs: 
# Anderson, SC; Bloomington-Normal, IL; Cleveland-Elyria-Mentor, OH; Dayton, OH; Honolulu, HI; Lafayette, IN
# Los Angeles, CA; Poughkeepsie-Newburgh-Middletown, NY; Santa Barbara-Santa Maria-Goleta, CA; 

# %% MORE GRANULAR BDS OUTCOME VARIABLES
# BDS Sectors of interest: 
# 54 - Professional, Scientific, and Technical Services
# 61 - Educational Services
# 62 - Health Care and Social Assistance

bds_detailed = pd.read_csv(base_path / "Raw_data/BDS/bds2023_msa_sec_fzc.csv")
bds_detailed = bds_detailed[bds_detailed["sector"].isin(["54", "61", "62"])]
bds_detailed = bds_detailed[bds_detailed["year"] >= 1992]
bds_detailed.to_csv(base_path / "Data/Outcomes/bds_sector_firmsize.csv", index=False)

bds = pd.read_csv(base_path / "Data/Outcomes/bds_sector_firmsize.csv")
# make bds_science, bds_educ, bds_health
outcomes = ['firms', 'estabs', 'emp',
       'denom', 'estabs_entry', 'estabs_entry_rate', 'estabs_exit',
       'estabs_exit_rate', 'job_creation', 'job_creation_births',
       'job_creation_continuers', 'job_creation_rate_births',
       'job_creation_rate', 'job_destruction', 'job_destruction_deaths',
       'job_destruction_continuers', 'job_destruction_rate_deaths',
       'job_destruction_rate', 'net_job_creation', 'net_job_creation_rate',
       'reallocation_rate', 'firmdeath_firms', 'firmdeath_estabs',
       'firmdeath_emp']

# (for now) Set "D" to 0 -- too small for disclosure
bds = bds.replace("D", 0)
bds = bds.replace("N", 0)
bds['firmsize'] = ''

# make wide with firm size
# SCIENCE
bds_science = bds[bds['sector'] == 54]
bds_science.loc[bds_science['fsizecoarse'] == 'a) 1 to 19', 'firmsize'] = "small"
bds_science.loc[bds_science['fsizecoarse'] == 'b) 20 to 499', 'firmsize'] = "medium"
bds_science.loc[bds_science['fsizecoarse'] == 'c) 500+', 'firmsize'] = 'large'
bds_science = bds_science.drop(columns="fsizecoarse")
bds_science[outcomes] = bds_science[outcomes].apply(pd.to_numeric)
wide = bds_science.set_index(['year','msa','sector','firmsize'])[outcomes].unstack('firmsize')
wide.columns = [f"{m}_{s}" for (m, s) in wide.columns]   # this WILL be tuples here
bds_science_wide = wide.reset_index()
bds_science_wide.to_csv(base_path / "Data/Outcomes/bds_science.csv", index=False)

# EDUCATION
bds_educ = bds[bds['sector'] == 61]
bds_educ.loc[bds_educ['fsizecoarse'] == 'a) 1 to 19', 'firmsize'] = "small"
bds_educ.loc[bds_educ['fsizecoarse'] == 'b) 20 to 499', 'firmsize'] = "medium"
bds_educ.loc[bds_educ['fsizecoarse'] == 'c) 500+', 'firmsize'] = 'large'
bds_educ = bds_educ.drop(columns="fsizecoarse")
bds_educ[outcomes] = bds_educ[outcomes].apply(pd.to_numeric)
wide = bds_educ.set_index(['year','msa','sector','firmsize'])[outcomes].unstack('firmsize')
wide.columns = [f"{m}_{s}" for (m, s) in wide.columns]   # this WILL be tuples here
bds_educ_wide = wide.reset_index()
bds_educ_wide.to_csv(base_path / "Data/Outcomes/bds_educ.csv", index=False)

# HEALTH
bds_health = bds[bds['sector'] == 62]
bds_health.loc[bds_health['fsizecoarse'] == 'a) 1 to 19', 'firmsize'] = "small"
bds_health.loc[bds_health['fsizecoarse'] == 'b) 20 to 499', 'firmsize'] = "medium"
bds_health.loc[bds_health['fsizecoarse'] == 'c) 500+', 'firmsize'] = 'large'
bds_health = bds_health.drop(columns="fsizecoarse")
bds_health[outcomes] = bds_health[outcomes].apply(pd.to_numeric)
wide = bds_health.set_index(['year','msa','sector','firmsize'])[outcomes].unstack('firmsize')
wide.columns = [f"{m}_{s}" for (m, s) in wide.columns]   # this WILL be tuples here
bds_health_wide = wide.reset_index()
bds_health_wide.to_csv(base_path / "Data/Outcomes/bds_health.csv", index=False)

# %% MORE GRANULAR BDS OUTCOME VARIABLES
# Merge with NIH and demographics data

bds_science = pd.read_csv(base_path / "Data/Outcomes/bds_science.csv")
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_use.csv")
nih = nih[nih['year'] != 2024] # BDS goes up to 2023
bds_science = bds_science.rename(columns={'msa': 'CBSA_code'})
nih_merge = nih.merge(
    bds_science,
    "left",
    on=['CBSA_code', 'year'],
    indicator=True
)
print(nih_merge['_merge'].value_counts())

nih_missing = nih_merge[nih_merge['_merge'] == 'left_only']
nih_missing['CBSA_title'].unique()
# unmatched: ['Anderson, SC', 'Bloomington-Normal, IL',
    #    'Cleveland-Elyria-Mentor, OH', 'Dayton, OH', 'Honolulu, HI',
    #    'Lafayette, IN', 'Los Angeles-Long Beach-Santa Ana, CA',
    #    'Poughkeepsie-Newburgh-Middletown, NY',
    #    'Santa Barbara-Santa Maria-Goleta, CA']
nih_merge = nih_merge[nih_merge['_merge'] == "both"]
nih_merge = nih_merge.drop(columns=['_merge'])
nih_merge.to_csv(base_path / "Data/NIH_Outcomes/nih_outcomes_science.csv", index=False)

bds_educ = pd.read_csv(base_path / "Data/Outcomes/bds_educ.csv")
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_use.csv")
nih = nih[nih['year'] != 2024] # BDS goes up to 2023
bds_educ = bds_educ.rename(columns={'msa': 'CBSA_code'})
nih_merge = nih.merge(
    bds_educ,
    "left",
    on=['CBSA_code', 'year'],
    indicator=True
)
print(nih_merge['_merge'].value_counts())
nih_merge = nih_merge[nih_merge['_merge'] == "both"]
nih_merge = nih_merge.drop(columns=['_merge'])
nih_merge.to_csv(base_path / "Data/NIH_Outcomes/nih_outcomes_educ.csv", index=False)

bds_health = pd.read_csv(base_path / "Data/Outcomes/bds_health.csv")
nih = pd.read_csv(base_path / "Data/NIH_v3/nih_use.csv")
nih = nih[nih['year'] != 2024] # BDS goes up to 2023
bds_health = bds_health.rename(columns={'msa': 'CBSA_code'})
nih_merge = nih.merge(
    bds_health,
    "left",
    on=['CBSA_code', 'year'],
    indicator=True
)
print(nih_merge['_merge'].value_counts())
nih_merge = nih_merge[nih_merge['_merge'] == "both"]
nih_merge = nih_merge.drop(columns=['_merge'])
nih_merge.to_csv(base_path / "Data/NIH_Outcomes/nih_outcomes_health.csv", index=False)
