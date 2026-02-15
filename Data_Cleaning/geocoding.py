# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
base_path = Path(__file__).resolve().parent.parent.parent
import pandas as pd
# from rapidfuzz import process, fuzz

########### Merging geocodes - Hospitals ######################################
# from scratch
# %%
nih_read = pd.read_stata("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_grants.dta")
nih_read.columns
nih_read.shape
# %%
nih = nih_read.copy()
# %% Old Hospital Datafile (was just addresses)
# cms = pd.read_csv("/Users/lydia/Desktop/Thesis/Raw_data/Geocoding/Hospital_General_Information.csv")
# cms.columns
# hospitals = cms.copy()[['Facility Name', 'Address', 'City/Town', 'State',
#        'ZIP Code', 'County/Parish']]
# hospitals.columns
# hospitals = hospitals.rename(columns={
#     "Facility Name":"organizationname_merged",
#     "Address":"address_merged",
#     "City/Town":"city_merged",
#     "State":"state_merged",
#     "ZIP Code":"zip_merged",
#     "County/Parish":"county_name_merged"
# })
# hospitals.shape
# hospitals = hospitals.drop_duplicates()
# hospitals.shape

# %% Updated Hospital Datafile with geocodes
us_hospital_locations = pd.read_csv("/Users/lydia/Desktop/Thesis/Raw_data/Geocoding/us_hospital_locations.csv")
us_hospital_locations.columns
hospitals = us_hospital_locations.copy()[['X', 'Y', 'NAME', 'ADDRESS', 'CITY', 'STATE', 'ZIP',
       'ZIP4', 'TYPE', 'STATUS', 'POPULATION', 'COUNTY',
       'COUNTYFIPS', 'LATITUDE', 'LONGITUDE', 'NAICS_CODE',
       'NAICS_DESC', 'STATE_ID', 'ALT_NAME', 'ST_FIPS', 'OWNER',
       'BEDS', 'TRAUMA', 'HELIPAD']]

# %% Make copies of variables before editing
nih[['organizationname', 'county_name']] = nih[['organizationname', 'county_name']].apply(lambda s: s.str.upper())
nih['name'] = nih['organizationname'].copy()

hospitals['name'] = hospitals['NAME'].copy()
hospitals['state'] = hospitals['STATE'].copy()

# %% I should use the alternate name too -- make another file with new observations with alt name as name and append.

# %%
##################
noise_and_abbrevs = {
    r"\bUNIV\b": "UNIVERSITY",
    r"\bSCH\b": "SCHOOL",
    r"\bCTR\b": "",
    r"\bCENTER\b": "",
    r"\bREGENTS\b": "",   
    r"\bOF\b": "",
    r"\bAND\b": "",
    r"\bST\.?\b": "SAINT",
    r"\bHOSP\b": "HOSPITAL",
    r"\bMED\.?\b": "MEDICAL",
    r"\b&\b": "AND",
}
def clean_org_column(df, col_name):
    # 1) Use pandas string dtype; keep missing as empty string (avoid "NAN")
    s = df[col_name].astype("string").fillna("").str.upper()

    # 2) Normalize punctuation/separators to spaces BEFORE word-level replacements
    s = (s.str.replace(r"[^A-Z0-9 ]", " ", regex=True)
           .str.replace(r"\s+", " ", regex=True)
           .str.strip())

    # 3) Expand/remove specific words with word boundaries
    for pattern, replacement in noise_and_abbrevs.items():
        s = s.str.replace(pattern, replacement, regex=True)

    # 4) Re-collapse whitespace after replacements
    s = (s.str.replace(r"\s+", " ", regex=True)
           .str.strip())

    # 5) Crush to alphanumeric-only (no spaces) for matching key
    s = s.str.replace(r"[^A-Z0-9]", "", regex=True)

    # Write back (overwriting col_name, since it's already your working copy)
    df[col_name] = s
    return df

# Apply in-place to your working columns
clean_org_column(nih, "name")
clean_org_column(nih, "state")

clean_org_column(hospitals, "name")
clean_org_column(hospitals, "state")

print("Shape before dropping name+state duplicates: ", hospitals.shape)
print("Hospital name duplicates: ", hospitals['name'].duplicated().sum())
print("Hospital name and state duplicates: ", hospitals[['name', 'state']].duplicated().sum())

# %% Dropping duplicates
hospitals[['name', 'state']].drop_duplicates()
print("Shape after dropping name+state duplicates: ", hospitals.shape)
print("NIH Shape: ", nih.shape)

####################
# %% Clean names
# hospitals['county'] = hospitals['county_name'].copy()
# nih['name'] = nih['name'] .str.replace(r"[^A-Z0-9]", "", regex=True)
# hospitals['name'] = hospitals['name'] .str.replace(r"[^A-Z0-9]", "", regex=True)

# nih['county'] = nih['county'] .str.replace(r"[^A-Z0-9]", "", regex=True)
# hospitals['county'] = hospitals['county'] .str.replace(r"[^A-Z0-9]", "", regex=True)

# %%
# matching on name ONLY
# nih_hospitals = nih.merge(hospitals, how='left', on=['name'], indicator=True)
# nih_hospitals['_merge'].value_counts()

# %%
# matching on name AND county
# should be a many to 1 merge
nih_hospitals_state = nih.merge(hospitals, how='left', on=['name', 'state'], indicator=True)
nih_hospitals_state['_merge'].value_counts()

#%% 
nih_hospitals_state.sort_values(by=['_merge'])
nih_hospitals_state.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_hospitals_exact.csv", index=False)
#%% 
# save matched
nih_hosp_matched = nih_hospitals_state[nih_hospitals_state['_merge'] == "both"]
nih_hosp_matched = nih_hosp_matched.drop(columns="_merge")
nih_hosp_matched.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_hosp_matched.csv", index=False)

# save unmatched
nih_hosp_unmatched = nih_hospitals_state[nih_hospitals_state['_merge'] == "left_only"]
nih_hosp_unmatched = nih_hosp_unmatched.drop(columns="_merge")
nih_hosp_unmatched.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_hosp_unmatched.csv", index=False)

###################
### most basic merge
# left_only     1556716
# both            93750

### after cleaning
# left_only     1544826
# both           105781

# name afer dropping name and county duplicates, on name only
# left_only     1544826
# both           105781

### name and county after dropping 
# left_only     1558102
# both            92210

### name and state
# left_only     1551729
# both            98603
#  %%
########### Merging addresses - Universities ######################################
ipeds = pd.read_csv("/Users/lydia/Desktop/Thesis/Raw_data/Geocoding/colleges_nhgis_geog_1990.csv")
ipeds.columns
# Data on unmatched, to be matched
nih_tomatch = pd.read_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_hosp_unmatched.csv")

#  %%
universities = ipeds.copy()
universities = universities.loc[(universities['year'] >= 1992) & (universities['year'] <= 2022)]
print(universities.shape)
universities = universities[['year', 'state_fips_geo', 'geo_longitude', 'geo_latitude', 'census_region', 'county_fips_geo', 'tract', 'block_group', 'msa_cmsa', 'inst_name', 'address', 'state_abbr', 'fips',
       'zip', 'county_name', 'county_fips']]
universities = universities.sort_values('year').drop_duplicates(['inst_name', 'state_abbr'], keep='first')
print(universities.shape)

# %% Now Merge
# Make university columns
nih_tomatch[['organizationname', 'state']] = nih_tomatch[['organizationname', 'state']].apply(lambda s: s.str.upper())
nih_tomatch['name'] = nih_tomatch['organizationname'].copy()
universities['name'] = universities['inst_name'].copy()
universities['state'] = universities['state_abbr'].copy()

# TO-DO: Delete everything in parenthesis? Harvard Univ (School of public health)
noise_and_abbrevs = {
    r"\bUNIV\b": "UNIVERSITY",
    r"\bSCH\b": "SCHOOL",
    r"\bCTR\b": "",
    r"\bCENTER\b": "",
    r"\bREGENTS\b": "",   
    r"\bOF\b": "",
    r"\bAND\b": "",
    r"\bST\.?\b": "SAINT",
    r"\bHOSP\b": "HOSPITAL",
    r"\bMED\.?\b": "MEDICAL",
    r"\b&\b": "AND",
}
def clean_org_column(df, col_name):
    # 1) Use pandas string dtype; keep missing as empty string (avoid "NAN")
    s = df[col_name].astype("string").fillna("").str.upper()

    # 2) Normalize punctuation/separators to spaces BEFORE word-level replacements
    s = (s.str.replace(r"[^A-Z0-9 ]", " ", regex=True)
           .str.replace(r"\s+", " ", regex=True)
           .str.strip())

    # 3) Expand/remove specific words with word boundaries
    for pattern, replacement in noise_and_abbrevs.items():
        s = s.str.replace(pattern, replacement, regex=True)

    # 4) Re-collapse whitespace after replacements
    s = (s.str.replace(r"\s+", " ", regex=True)
           .str.strip())

    # 5) Crush to alphanumeric-only (no spaces) for matching key
    s = s.str.replace(r"[^A-Z0-9]", "", regex=True)

    # Write back (overwriting col_name, since it's already your working copy)
    df[col_name] = s
    return df

# Apply in-place to your working columns
clean_org_column(nih, "name")
clean_org_column(nih, "state")

clean_org_column(hospitals, "name")
clean_org_column(hospitals, "state")

universities = universities.sort_values('year').drop_duplicates(['name', 'state'], keep='first')
print("Dropping after cleaning:", universities.shape)
# no additional drops
# %%
# matching on name AND state
# should be a many to 1 merge
nih_tomatch = nih_tomatch.drop(columns="_merge")
nih_univ_state = nih_tomatch.merge(universities, how='left', on=['name', 'state'], indicator=True)
nih_univ_state['_merge'].value_counts()

#%% 
nih_univ_state.sort_values(by=['_merge'])
nih_univ_state.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_univ_exact.csv", index=False)
#%% 
# save matched
nih_univ_matched = nih_univ_state[nih_univ_state['_merge'] == "both"]
nih_univ_matched = nih_univ_state.drop(columns="_merge")
nih_univ_matched.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_univ_matched.csv", index=False)

# save unmatched
nih_univ_unmatched = nih_univ_state[nih_univ_state['_merge'] == "left_only"]
nih_univ_unmatched = nih_univ_state.drop(columns="_merge")
nih_univ_unmatched.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_univ_unmatched.csv", index=False)


# %% The rest we try to clean, and then do with HHS
########## Getting addresses - HHS database #####################
# %%
nih_read = pd.read_stata("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_grants.dta")
nih_read.columns
nih_read.shape

# %%
nih = nih_read.copy()
# %%
taggs1 = pd.read_csv("/Users/lydia/Desktop/Thesis/Raw_data/Geocoding/HHS/TAGGS_97-06.csv")
taggs1.columns

taggs1 = taggs1.rename(columns={
    "Issue Date Fiscal Year":"year",
    "Legal Entity Name":"organizationname",
    "Legal Entity Address":"address",
    "Legal Entity City":"city",
    "Legal Entity State":"state",
    "Legal Entity ZIP Code":"zip",
    "Legal Entity County":"county_name",
    "Sum of Actions ":"funds"
})
taggs1 = taggs1.loc[taggs1.groupby(["organizationname", "county_name"])["funds"].idxmax()]
taggs1 = taggs1.drop(columns=["funds", "zip"])
taggs1 = taggs1.drop_duplicates()
print(taggs1.shape)
taggs2 = pd.read_csv("/Users/lydia/Desktop/Thesis/Raw_data/Geocoding/HHS/TAGGS_07-21.csv")
taggs2.columns
taggs2 = taggs2.rename(columns={
    "Issue Date Fiscal Year":"year",
    "Legal Entity Name":"organizationname",
    "Legal Entity Address":"address",
    "Legal Entity City":"city",
    "Legal Entity State":"state",
    "Legal Entity ZIP Code":"zip",
    "Legal Entity County":"county_name",
    "Sum of Actions ":"funds"
})
print(taggs2.shape)

taggs = pd.concat([taggs1, taggs2], axis=0)

# %%
# drop PO boxes
box = [r'POST OFFICE', r'\bP\.?O\.?\b', r'\bP\.?O\.?B\b', r'\bBOX\b']
pattern = "|".join(box)
taggs = taggs[
    ~taggs["address"]
     .str.upper()
     .str.contains(pattern, regex=True, na=False)
]
taggs["funds"] = pd.to_numeric(taggs["funds"], errors="coerce").fillna(0)
taggs = taggs.loc[taggs.groupby(["organizationname", "county_name"])["funds"].idxmax()]
taggs = taggs.drop(columns=["funds", "zip"])
taggs = taggs.drop_duplicates()

print(taggs.shape)


# %% Clean names
nih[['organizationname', 'county_name']] = nih[['organizationname', 'county_name']].apply(lambda s: s.str.upper())
taggs[['organizationname', 'county_name', 'address', 'city', 'state']] = taggs[['organizationname', 'county_name', 'address', 'city', 'state']].apply(lambda s : s.str.upper())
nih['name'] = nih['organizationname'].copy()
nih['county'] = nih['county_name'].copy()
taggs['name'] = taggs['organizationname'].copy()
taggs['county'] = taggs['county_name'].copy()

nih['name'] = nih['name'] .str.replace(r"[^A-Z0-9]", "", regex=True)
taggs['name'] = taggs['name'] .str.replace(r"[^A-Z0-9]", "", regex=True)

nih['county'] = nih['county'] .str.replace(r"[^A-Z0-9]", "", regex=True)
taggs['county'] = taggs['county'] .str.replace(r"[^A-Z0-9]", "", regex=True)

# do not match on county
nih_addresses_exact = nih.merge(taggs, how='left', on=['name'], indicator=True)
nih_addresses_exact['_merge'].value_counts()
#%% 
# exact match with PO boxes ignored
nih_addresses_exact.sort_values(by=['_merge'])
nih_addresses_exact.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses_exact.csv", index=False)


# %% Merge stats (OLD, from scratch)
# Normal merge
# both          1359919
# left_only      867299

# With punctuation removed
# both          1538412
# left_only      743149

# With spaces also removed
# both          1547172
# left_only      738752

# with PO removed
# both          1141715
# left_only      753004

# after regex and universities
# both          1677030
# left_only      729607

# With new regex
# both          984419
# left_only     876325

# # PO removed, regex, name only
# both          1654665
# left_only      541458
# = 75% match rate


########### Old version ######################################

nih = pd.read_stata("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_grants.dta")
nih.columns
nih.
# %%
taggs1 = pd.read_csv("/Users/lydia/Desktop/Thesis/Raw_data/Geocoding/HHS/TAGGS_97-06.csv")
taggs1.columns

taggs1 = taggs1.rename(columns={
    "Issue Date Fiscal Year":"year",
    "Legal Entity Name":"organizationname",
    "Legal Entity Address":"address",
    "Legal Entity City":"city",
    "Legal Entity State":"state",
    "Legal Entity ZIP Code":"zip",
    "Legal Entity County":"county_name",
    "Sum of Actions ":"funds"
})
taggs1 = taggs1.loc[taggs1.groupby(["organizationname", "county_name"])["funds"].idxmax()]
taggs1 = taggs1.drop(columns=["funds", "zip"])
taggs1 = taggs1.drop_duplicates()
print(taggs1.shape)
# %%
taggs2 = pd.read_csv("/Users/lydia/Desktop/Thesis/Raw_data/Geocoding/HHS/TAGGS_07-21.csv")
taggs2.columns
taggs2 = taggs2.rename(columns={
    "Issue Date Fiscal Year":"year",
    "Legal Entity Name":"organizationname",
    "Legal Entity Address":"address",
    "Legal Entity City":"city",
    "Legal Entity State":"state",
    "Legal Entity ZIP Code":"zip",
    "Legal Entity County":"county_name",
    "Sum of Actions ":"funds"
})
taggs2 = taggs2.loc[taggs2.groupby(["organizationname", "county_name"])["funds"].idxmax()]
taggs2 = taggs2.drop(columns=["funds", "zip"])
taggs2 = taggs2.drop_duplicates()
print(taggs2.shape)

taggs = pd.concat([taggs1, taggs2], axis=0)
taggs.shape

# %% Try merging
nih[['organizationname', 'county_name']] = nih[['organizationname', 'county_name']].apply(lambda s: s.str.upper())
taggs[['organizationname', 'county_name']] = taggs[['organizationname', 'county_name']].apply(lambda s : s.str.upper())
nih_addresses = nih.merge(taggs, how='left', on=['organizationname', 'county_name'], indicator=True)
# %% Try merging
nih[['organizationname', 'county_name']] = nih[['organizationname', 'county_name']].apply(lambda s: s.str.upper())
taggs[['organizationname', 'county_name']] = taggs[['organizationname', 'county_name']].apply(lambda s : s.str.upper())

nih['organizationname'] = nih['organizationname'] .str.replace(r"[.,]", "", regex=True)
taggs['organizationname'] = taggs['organizationname'] .str.replace(r"[.,]", "", regex=True)
nih['organizationname'] = nih['organizationname'] .str.replace(r"\s+", "", regex=True)
taggs['organizationname'] = taggs['organizationname'] .str.replace(r"\s+", "", regex=True)

nih_addresses = nih.merge(taggs, how='left', on=['organizationname', 'county_name'], indicator=True)
nih_addresses['_merge'].value_counts()
nih_addresses.sort_values(by=['_merge'])
# %%
nih_addresses_v2 = nih.merge(taggs, how='left', on=['organizationname'], indicator=True)
nih_addresses_v2['_merge'].value_counts()
nih_addresses_v2.sort_values(by=['_merge'])
nih_addresses_v2.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses_v2.csv", index=False)
# %%
nih_addresses.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses.csv", index=False)




# keep unmatched to do further clean/fuzzy matching
# %%
# Normalize common abbreviations / remove glue words (word-boundary safe)
noise_and_abbrevs = {
    r"\bUNIV\b": "UNIVERSITY",
    r"\bSCH\b": "SCHOOL",
    r"\bCTR\b": "CENTER",
    r"\bREGENTS\b": "",        # optional
    r"\bOF\b": "",
    r"\bAND\b": "",
    r"\bST\.?\b": "SAINT",     # matches ST and ST.
}

###
# other abbreviations: HOSP MED CTR
###

def clean_org_column(df, col_name):
    # 1) Use pandas string dtype; keep missing as empty string (avoid "NAN")
    s = df[col_name].astype("string").fillna("").str.upper()

    # 2) Normalize punctuation/separators to spaces BEFORE word-level replacements
    s = (s.str.replace(r"[^A-Z0-9 ]", " ", regex=True)
           .str.replace(r"\s+", " ", regex=True)
           .str.strip())

    # 3) Expand/remove specific words with word boundaries
    for pattern, replacement in noise_and_abbrevs.items():
        s = s.str.replace(pattern, replacement, regex=True)

    # 4) Re-collapse whitespace after replacements
    s = (s.str.replace(r"\s+", " ", regex=True)
           .str.strip())

    # 5) Crush to alphanumeric-only (no spaces) for matching key
    s = s.str.replace(r"[^A-Z0-9]", "", regex=True)

    # Write back (overwriting col_name, since it's already your working copy)
    df[col_name] = s
    return df

# Apply in-place to your working columns
clean_org_column(nih, "name")
clean_org_column(nih, "county")

clean_org_column(taggs, "name")
clean_org_column(taggs, "county")


# nih['county'] = nih['county'].str.replace(r"[^A-Z0-9]", "", regex=True)
# taggs['county'] = taggs['county'].str.replace(r"[^A-Z0-9]", "", regex=True)
# nih['county'] = nih['county'].str.replace(r"\bST\b", "", regex=True)
# taggs['county'] = taggs['county'].str.replace(r"\bST\b", "", regex=True)
# nih['county'] = nih['county'].str.replace(r"\s+", "", regex=True)
# taggs['county'] = taggs['county'].str.replace(r"\s+", "", regex=True)


# nih['name'] = nih['name'].str.replace(r"[^A-Z0-9]", "", regex=True)
# taggs['name'] = taggs['name'].str.replace(r"[^A-Z0-9]", "", regex=True)

# replace = {
#     r"\bUNIV\b": "UNIVERSITY",
#     r"\bSCH\b": "SCHOOL",
#     r"\bCTR\b": "CENTER",
# }
# for pattern, rep in replace.items():
#     nih['name'] = nih['name'].str.replace(pattern, rep, regex=True)
# nih['name'] = nih['name'].str.replace(r"\bREGENTS\b", "", regex=True)
# nih['name'] = nih['name'].str.replace(r"\bOF\b", "", regex=True)
# nih['name'] = nih['name'].str.replace(r"\s+", " ", regex=True).str.strip()

# for pattern, rep in replace.items():
#     taggs['name'] = taggs['name'].str.replace(pattern, rep, regex=True)
# taggs['name'] = taggs['name'].str.replace(r"\bREGENTS\b", "", regex=True)
# taggs['name'] = taggs['name'].str.replace(r"\bOF\b", "", regex=True)
# taggs['name'] = taggs['name'].str.replace(r"\s+", " ", regex=True).str.strip()

#%% Do exact match first
print(nih.shape)
print(taggs.shape)
nih_addresses = nih.merge(taggs, how='left', on=['organizationname', 'county'], indicator=True)
nih_addresses['_merge'].value_counts()
#%%
nih_addresses.sort_values(by=['_merge'])
nih_addresses.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses_keepPO.csv", index=False)


# %%
nih_addresses_v2 = nih.merge(taggs, how='left', on=['organizationname'], indicator=True)
nih_addresses_v2['_merge'].value_counts()
#%%
nih_addresses_v2.sort_values(by=['_merge'])
nih_addresses_v2.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses_v2.csv", index=False)
# %%
nih_unmatched_v2 = nih_addresses_v2[nih_addresses_v2['_merge'] == 'left_only']
print(nih_unmatched_v2['organizationname'].nunique())
nih_unmatched_v2.to_csv("/Users/lydia/Desktop/Thesis/Data/NIH_Indiv/nih_addresses.csv", index=False)